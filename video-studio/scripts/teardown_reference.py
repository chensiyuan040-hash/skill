#!/usr/bin/env python3
"""Quantitative teardown of a reference video: cut rate + motion energy.

Automates the manual methodology in references/hyperframes-pitfalls.md
("参考视频定量拆解"): scene-cut times, shot count / median / <2s share,
per-second motion energy, longest static stretch — the numbers you need to
answer "为什么这条片灵动".

Examples:
  python teardown_reference.py ref.mp4
  python teardown_reference.py ref.mp4 --scene-th 0.3 --report teardown.md
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

W, H = 160, 90  # motion-probe frame size


def run(cmd: list[str], binary: bool = False):
    p = subprocess.run(cmd, capture_output=True)
    return p.stdout if binary else (p.stderr + p.stdout).decode("utf-8", "replace")


def duration(path: Path) -> float:
    out = run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(path)])
    return float(out.strip().splitlines()[0])


def scene_cuts(path: Path, th: float) -> list[float]:
    out = run(["ffprobe", "-v", "quiet", "-f", "lavfi",
               f"movie={path},select=gt(scene\\,{th})",
               "-show_entries", "frame=pts_time", "-of", "csv=p=0"])
    return [float(x) for x in out.split() if x.replace(".", "").replace("-", "").isdigit()]


def motion_series(path: Path) -> list[float]:
    """Mean abs diff between consecutive 1fps grayscale thumbnails."""
    raw = run(["ffmpeg", "-v", "quiet", "-i", str(path), "-vf",
               f"fps=1,scale={W}:{H},format=gray", "-f", "rawvideo", "-"],
              binary=True)
    n = len(raw) // (W * H)
    frames = [raw[i * W * H:(i + 1) * W * H] for i in range(n)]
    return [sum(abs(a - b) for a, b in zip(f1, f2)) / (W * H)
            for f1, f2 in zip(frames, frames[1:])]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--scene-th", type=float, default=0.25,
                    help="scene-change score threshold (default 0.25)")
    ap.add_argument("--motion-th", type=float, default=2.0,
                    help="mean-abs-diff above this counts as visible motion")
    ap.add_argument("--report", type=Path, default=None, help="also write markdown report")
    ap.add_argument("--json", type=Path, default=None, help="also write JSON")
    args = ap.parse_args()

    if not args.video.is_file():
        raise SystemExit(f"not found: {args.video}")
    dur = duration(args.video)
    cuts = scene_cuts(args.video, args.scene_th)

    bounds = [0.0] + cuts + [dur]
    shots = [b - a for a, b in zip(bounds, bounds[1:]) if b - a > 0.2]
    med = statistics.median(shots) if shots else dur
    under2 = sum(1 for s in shots if s < 2) / len(shots) if shots else 0.0

    series = motion_series(args.video)
    moving = [d >= args.motion_th for d in series]
    pct_moving = sum(moving) / len(moving) * 100 if moving else 0.0
    longest_static = run_len = 0
    for m in moving + [True]:  # sentinel flushes the last run
        run_len = 0 if m else run_len + 1
        longest_static = max(longest_static, run_len)

    verdict_dynamic = pct_moving >= 70 and longest_static <= 3
    result = {
        "video": str(args.video), "duration_s": round(dur, 2),
        "scene_threshold": args.scene_th,
        "cuts": [round(c, 2) for c in cuts],
        "shot_count": len(shots),
        "median_shot_s": round(med, 2),
        "under_2s_share": round(under2, 2),
        "motion_threshold": args.motion_th,
        "seconds_with_motion_pct": round(pct_moving, 1),
        "longest_static_s": longest_static,
        "verdict_dynamic": verdict_dynamic,
    }

    if args.json:
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    if args.report:
        lines = [f"# Teardown · {args.video.name}", "",
                 f"- 时长 {dur:.1f}s · {len(shots)} 个镜头 · 中位镜头 {med:.2f}s · <2s 占 {under2:.0%}",
                 f"- 运动能量:{pct_moving:.0f}% 的秒有可见运动 · 最长静止 {longest_static}s",
                 f"- 灵动判定(≥70% 秒在动且最长静止≤3s):{'✅' if verdict_dynamic else '❌'}",
                 "", "## 切镜时间点", ""]
        lines += [f"- {c:.2f}s" for c in cuts] or ["- (无检测到切镜)"]
        args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
