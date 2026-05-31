#!/usr/bin/env python3
"""Extract keyframes from video — smart mode only.

Strategy:
  1. Scene-change detection via ffmpeg (captures PPT flips, code switches, etc.)
  2. Max-gap fallback: force-capture a frame every N seconds when scene is static
  3. Merge, deduplicate close frames (< min_gap seconds apart), cap at max_frames
  4. Output keyframes.json with trigger + scene_score metadata

Replaces the old interval/scene/both modes with a single unified smart mode.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Sequence


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Keyframe:
    file: str
    timestamp_seconds: float
    timestamp_label: str
    trigger: str          # "scene" | "gap" (max-gap fallback)
    scene_score: float    # 0.0 for gap frames; >0 for scene-detected


@dataclass(frozen=True)
class ExtractResult:
    video_path: str
    output_dir: str
    max_frames: int
    keyframes: list[Keyframe]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def env_or_default(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None:
        return default
    cleaned = value.strip()
    return cleaned if cleaned else default


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract keyframes from a video using smart scene + gap mode.",
    )
    parser.add_argument("--video", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--output-dir", required=True,
        help="Directory where keyframe images and index JSON are written.",
    )
    parser.add_argument(
        "--timestamps",
        default=None,
        help=(
            "Path to a JSON file containing subtitle-guided recommended timestamps. "
            "Format: [{\"ts\": 90.0, \"reason\": \"code demo\"}, ...]. "
            "These timestamps take priority over scene detection."
        ),
    )
    parser.add_argument(
        "--max-frames", type=int,
        default=int(env_or_default("KF_MAX_FRAMES", "40") or "40"),
        help="Maximum number of keyframes to extract. Default: KF_MAX_FRAMES env or 40.",
    )
    parser.add_argument(
        "--scene-threshold", type=float,
        default=float(env_or_default("KF_SCENE_THRESHOLD", "0.25") or "0.25"),
        help="Scene-change sensitivity (lower = more sensitive). Default: 0.25.",
    )
    parser.add_argument(
        "--max-gap", type=int,
        default=int(env_or_default("KF_MAX_GAP", "120") or "120"),
        help=(
            "Maximum seconds between consecutive keyframes. "
            "When the scene is static for longer than this, force-capture a frame. "
            "Default: KF_MAX_GAP env or 120."
        ),
    )
    parser.add_argument(
        "--min-gap", type=int,
        default=int(env_or_default("KF_MIN_GAP", "3") or "3"),
        help=(
            "Minimum seconds between consecutive keyframes. "
            "Frames closer than this are deduplicated (keep higher score). "
            "Default: KF_MIN_GAP env or 3."
        ),
    )
    return parser.parse_args(argv)


def find_ffmpeg() -> str:
    """Locate ffmpeg executable."""
    import shutil
    path = shutil.which("ffmpeg")
    if path:
        return path
    winget_base = Path(
        os.environ.get("LOCALAPPDATA", "")
    ) / "Microsoft" / "WinGet" / "Packages"
    if winget_base.exists():
        for pkg in winget_base.iterdir():
            if "ffmpeg" in pkg.name.lower():
                bin_dir = pkg / "bin"
                ffmpeg = shutil.which("ffmpeg", path=str(bin_dir))
                if ffmpeg:
                    return ffmpeg
                for child in pkg.rglob("ffmpeg.exe"):
                    return str(child)
    raise RuntimeError(
        "ffmpeg not found. Install with: winget install Gyan.FFmpeg  "
        "(Windows) / brew install ffmpeg (macOS) / sudo apt install ffmpeg (Linux)"
    )


def find_ffprobe(ffmpeg_bin: str) -> str | None:
    """Locate ffprobe executable, falling back to same dir as ffmpeg."""
    import shutil
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        return ffprobe
    candidate = str(Path(ffmpeg_bin).parent / "ffprobe")
    return candidate if Path(candidate).exists() else None


# ---------------------------------------------------------------------------
# Timestamp formatting
# ---------------------------------------------------------------------------

def fmt_timestamp(seconds: float) -> str:
    """Format seconds into HHhMMmSSs or MMmSSs label."""
    total = int(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02d}h{minutes:02d}m{secs:02d}s"
    return f"{minutes:02d}m{secs:02d}s"


def fmt_filename(index: int, seconds: float) -> str:
    """Generate filename like frame_0001_01m30s.png."""
    return f"frame_{index:04d}_{fmt_timestamp(seconds)}.png"


# ---------------------------------------------------------------------------
# Scene-change extraction (with precise timestamps via ffmpeg showinfo)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Subtitle-guided timestamp extraction
# ---------------------------------------------------------------------------

def extract_guided_frames(
    video_path: str,
    output_dir: Path,
    timestamps_path: str,
    ffmpeg_bin: str,
) -> list[Keyframe]:
    """Extract frames at subtitle-guided timestamps.

    Reads a JSON file with recommended timestamps and reasons,
    extracts one frame per timestamp using ffmpeg -ss seeking.
    """
    ts_file = Path(timestamps_path)
    if not ts_file.exists():
        return []

    try:
        raw = json.loads(ts_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    # Accept both [{ts, reason}, ...] and [ts, ...] formats
    entries: list[dict] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, (int, float)):
                entries.append({"ts": float(item), "reason": ""})
            elif isinstance(item, dict) and "ts" in item:
                entries.append({"ts": float(item["ts"]), "reason": str(item.get("reason", ""))})

    if not entries:
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    keyframes: list[Keyframe] = []

    for i, entry in enumerate(entries):
        ts = entry["ts"]
        out_name = f"_guided_{i:04d}.png"
        out_path = output_dir / out_name

        cmd = [
            ffmpeg_bin,
            "-ss", f"{ts:.3f}",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            "-y",
            str(out_path),
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=10)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            out_path.unlink(missing_ok=True)
            continue

        if not out_path.exists():
            continue

        final_name = fmt_filename(i + 1, ts)
        final_path = output_dir / final_name
        out_path.rename(final_path)

        keyframes.append(Keyframe(
            file=final_name,
            timestamp_seconds=ts,
            timestamp_label=fmt_timestamp(ts),
            trigger="guided",
            scene_score=1.0,  # guided frames have "AI-confirmed" value
        ))

    return keyframes

def extract_scene_frames(
    video_path: str,
    output_dir: Path,
    max_frames: int,
    ffmpeg_bin: str,
    threshold: float = 0.25,
) -> list[Keyframe]:
    """Extract frames at scene changes with precise timestamps.

    Uses ffmpeg's showinfo filter to get exact PTS for each detected scene
    change frame, then renames the output files to include timestamps.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Phase 1: extract scene-change frames with sequential naming
    tmp_pattern = str(output_dir / "_scene_%04d.png")
    filter_v = f"select=gt(scene\\,{threshold}),showinfo"

    cmd = [
        ffmpeg_bin,
        "-i", str(video_path),
        "-vf", filter_v,
        "-vsync", "vfr",
        "-frames:v", str(max_frames),
        "-q:v", "2",
        "-y",
        tmp_pattern,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    # showinfo output goes to stderr
    showinfo_output = result.stderr

    # Phase 2: parse precise timestamps from showinfo output
    # Format: "[Parsed_showinfo_1 @ ...] n:0 pts:12345 pts_time:12.345 ..."
    ts_map: dict[int, float] = {}
    for line in showinfo_output.splitlines():
        m = re.search(r"n:(\d+)\s+pts:\d+\s+pts_time:([\d.]+)", line)
        if m:
            idx = int(m.group(1))
            ts = float(m.group(2))
            ts_map[idx] = ts

    # Phase 3: collect and rename files
    keyframes: list[Keyframe] = []
    scene_files = sorted(output_dir.glob("_scene_*.png"))

    for i, png in enumerate(scene_files):
        ts = ts_map.get(i, None)
        if ts is None:
            # Fallback: try to parse from filename or skip
            # Could not determine timestamp — remove the file
            png.unlink(missing_ok=True)
            continue

        new_name = fmt_filename(i + 1, ts)
        new_path = png.parent / new_name
        png.rename(new_path)

        keyframes.append(Keyframe(
            file=new_name,
            timestamp_seconds=ts,
            timestamp_label=fmt_timestamp(ts),
            trigger="scene",
            scene_score=threshold,  # base score = the threshold that triggered it
        ))

    return keyframes


# ---------------------------------------------------------------------------
# Max-gap fallback extraction
# ---------------------------------------------------------------------------

def extract_gap_frames(
    video_path: str,
    output_dir: Path,
    max_gap: int,
    max_frames: int,
    ffmpeg_bin: str,
    existing_timestamps: list[float],
) -> list[Keyframe]:
    """Force-capture frames at regular intervals to fill gaps.

    Only adds frames where the gap between consecutive existing keyframes
    exceeds max_gap seconds.
    """
    if not existing_timestamps:
        # No scene frames at all — use interval extraction as fallback
        return _extract_interval_fallback(video_path, output_dir, max_gap, max_frames, ffmpeg_bin)

    # Determine where to insert gap frames
    gap_timestamps: list[float] = []
    video_duration = _get_video_duration(video_path, ffmpeg_bin)

    # Build full timeline including 0 and end
    boundaries = [0.0] + sorted(existing_timestamps)
    if video_duration:
        boundaries.append(video_duration)

    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        gap = end - start

        if gap > max_gap:
            # Insert frames at max_gap intervals within this gap
            t = start + max_gap
            while t < end - (max_gap * 0.5):  # don't place too close to next scene frame
                gap_timestamps.append(t)
                t += max_gap

    if not gap_timestamps:
        return []

    # Extract specific timestamps using ffmpeg's -ss seeking
    output_dir.mkdir(parents=True, exist_ok=True)
    keyframes: list[Keyframe] = []

    # Use a single ffmpeg pass with the select filter for precise timestamps
    ts_list = ",".join(f"{t:.3f}" for t in gap_timestamps)
    # Build a filter that captures at specific timestamps
    # Using fps + trim approach: extract at calculated fps, then filter
    # Simpler: extract one frame per gap timestamp
    for idx, ts in enumerate(gap_timestamps):
        out_name = f"_gap_{idx:04d}.png"
        out_path = output_dir / out_name

        cmd = [
            ffmpeg_bin,
            "-ss", f"{ts:.3f}",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            "-y",
            str(out_path),
        ]
        try:
            subprocess.run(cmd, capture_output=True, check=True, timeout=10)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            out_path.unlink(missing_ok=True)
            continue

        if not out_path.exists():
            continue

        final_name = fmt_filename(len(existing_timestamps) + idx + 1, ts)
        final_path = output_dir / final_name
        out_path.rename(final_path)

        keyframes.append(Keyframe(
            file=final_name,
            timestamp_seconds=ts,
            timestamp_label=fmt_timestamp(ts),
            trigger="gap",
            scene_score=0.0,
        ))

    return keyframes


def _extract_interval_fallback(
    video_path: str,
    output_dir: Path,
    interval: int,
    max_frames: int,
    ffmpeg_bin: str,
) -> list[Keyframe]:
    """Pure interval fallback when scene detection finds nothing."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fps = 1.0 / interval
    pattern = str(output_dir / "_fallback_%04d.png")

    cmd = [
        ffmpeg_bin,
        "-i", str(video_path),
        "-vf", f"fps={fps:.6f}",
        "-frames:v", str(max_frames),
        "-q:v", "2",
        "-y",
        pattern,
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    keyframes: list[Keyframe] = []
    for i, png in enumerate(sorted(output_dir.glob("_fallback_*.png"))):
        ts = i * interval
        new_name = fmt_filename(i + 1, ts)
        new_path = png.parent / new_name
        png.rename(new_path)
        keyframes.append(Keyframe(
            file=new_name,
            timestamp_seconds=float(ts),
            timestamp_label=fmt_timestamp(ts),
            trigger="gap",
            scene_score=0.0,
        ))

    return keyframes


def _get_video_duration(video_path: str, ffmpeg_bin: str) -> float | None:
    """Get video duration via ffprobe."""
    ffprobe = find_ffprobe(ffmpeg_bin)
    if not ffprobe:
        return None
    try:
        result = subprocess.run(
            [ffprobe, "-v", "quiet", "-print_format", "json",
             "-show_format", str(video_path)],
            capture_output=True, text=True, check=True,
        )
        info = json.loads(result.stdout)
        return float(info.get("format", {}).get("duration", 0))
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Merge + deduplicate
# ---------------------------------------------------------------------------

def merge_and_dedup(
    guided_frames: list[Keyframe],
    scene_frames: list[Keyframe],
    gap_frames: list[Keyframe],
    min_gap: int,
    max_frames: int,
) -> list[Keyframe]:
    """Merge guided, scene, and gap frames; deduplicate; cap at max_frames.

    Priority for dedup: guided (score 1.0) > scene (score >0) > gap (score 0.0).
    When two frames are within min_gap seconds, keep the higher-scored one.
    """
    all_frames = sorted(
        guided_frames + scene_frames + gap_frames,
        key=lambda k: k.timestamp_seconds,
    )

    if not all_frames:
        return []

    deduped: list[Keyframe] = [all_frames[0]]

    for frame in all_frames[1:]:
        prev = deduped[-1]
        gap = frame.timestamp_seconds - prev.timestamp_seconds

        if gap < min_gap:
            # Too close — keep the higher-scoring one
            if frame.scene_score > prev.scene_score:
                deduped[-1] = frame
            # else keep prev
        else:
            deduped.append(frame)

    return deduped[:max_frames]


# ---------------------------------------------------------------------------
# Main extraction
# ---------------------------------------------------------------------------

def extract_keyframes(
    video_path: str,
    output_dir: Path,
    max_frames: int,
    scene_threshold: float,
    max_gap: int,
    min_gap: int,
    timestamps_path: str | None = None,
) -> ExtractResult:
    """Smart extraction: subtitle-guided + scene detection + max-gap fallback."""
    ffmpeg_bin = find_ffmpeg()

    if not Path(video_path).exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    frames_dir = output_dir / "frames"

    # Step 1: Subtitle-guided timestamps (highest priority)
    guided_frames: list[Keyframe] = []
    if timestamps_path:
        guided_frames = extract_guided_frames(
            video_path, frames_dir, timestamps_path, ffmpeg_bin,
        )

    # Step 2: Scene-change detection (fills gaps guided timestamps missed)
    scene_frames = extract_scene_frames(
        video_path, frames_dir, max_frames, ffmpeg_bin, scene_threshold,
    )

    # Step 3: Fill remaining gaps with fallback frames
    existing_ts = [kf.timestamp_seconds for kf in guided_frames + scene_frames]
    gap_frames = extract_gap_frames(
        video_path, frames_dir, max_gap,
        max_frames - len(guided_frames) - len(scene_frames),
        ffmpeg_bin, existing_ts,
    )

    # Step 4: Merge + deduplicate (guided > scene > gap priority)
    final_frames = merge_and_dedup(
        guided_frames, scene_frames, gap_frames, min_gap, max_frames,
    )

    # Step 4: Re-number filenames sequentially
    for i, kf in enumerate(final_frames):
        old_path = frames_dir / kf.file
        if old_path.exists():
            new_name = fmt_filename(i + 1, kf.timestamp_seconds)
            new_path = frames_dir / new_name
            if old_path.name != new_name:
                old_path.rename(new_path)
            # Update the keyframe's filename (create new frozen dataclass)
            final_frames[i] = Keyframe(
                file=new_name,
                timestamp_seconds=kf.timestamp_seconds,
                timestamp_label=kf.timestamp_label,
                trigger=kf.trigger,
                scene_score=kf.scene_score,
            )

    # Step 5: Clean up any leftover temp files
    for f in frames_dir.iterdir():
        if f.name.startswith("_"):
            f.unlink(missing_ok=True)

    # Step 6: Write index JSON
    frames_dir.mkdir(parents=True, exist_ok=True)
    index_path = frames_dir / "keyframes.json"
    index_data = [asdict(kf) for kf in final_frames]
    index_path.write_text(
        json.dumps(index_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return ExtractResult(
        video_path=str(video_path),
        output_dir=str(output_dir),
        max_frames=max_frames,
        keyframes=final_frames,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    video_path = Path(args.video).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    if not video_path.exists():
        print(f"ERROR: Video file not found: {video_path}", file=sys.stderr)
        return 1

    try:
        result = extract_keyframes(
            video_path=str(video_path),
            output_dir=output_dir,
            max_frames=args.max_frames,
            scene_threshold=args.scene_threshold,
            max_gap=args.max_gap,
            min_gap=args.min_gap,
            timestamps_path=args.timestamps,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    # Summary output
    guided_count = sum(1 for kf in result.keyframes if kf.trigger == "guided")
    scene_count = sum(1 for kf in result.keyframes if kf.trigger == "scene")
    gap_count = sum(1 for kf in result.keyframes if kf.trigger == "gap")
    parts = []
    if guided_count:
        parts.append(f"guided: {guided_count}")
    parts.append(f"scene: {scene_count}")
    parts.append(f"gap: {gap_count}")
    print(
        f"OK: {len(result.keyframes)} keyframes extracted ({', '.join(parts)})",
        file=sys.stderr,
    )

    payload = {"result": asdict(result)}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
