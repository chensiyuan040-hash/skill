#!/usr/bin/env python3
"""Deterministic delivery QA for a rendered video. Produces PASS/WARNING/FAIL.

Checks (engine-agnostic, only needs ffprobe/ffmpeg):
  FAIL    resolution / fps / frame-count / duration mismatch vs expected
  FAIL    true peak > -1 dBTP, required audio missing
  FAIL    first or last frame is pure black/white
  WARNING loudness below -16 LUFS, silence or frozen segments, no audio
          while project didn't require it

Examples:
  python verify_delivery.py out/final.mp4 --expected 1080x1920 --fps 30 \
      --duration 45 --require-audio --report delivery-report.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stderr + p.stdout


def probe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_streams", "-show_format", str(path)])
    return json.loads(out)


def audio_checks(path: Path) -> tuple[str, float, float, list[str]]:
    """Return (loudness_lufs, true_peak_dbtp, silence_intervals)."""
    out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
               "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", out, re.S)
    lufs = tp = float("nan")
    if m:
        try:
            j = json.loads(m.group(0))
            lufs = float(j["input_i"])
            tp = float(j["input_tp"])
        except (ValueError, KeyError):
            pass
    sil = re.findall(r"silence_(?:start|end): ([-\d.]+)", out)
    return lufs, tp, sil


def detect(path: Path, vf: str) -> str:
    return run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
                "-vf", vf, "-an", "-f", "null", "-"])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--expected", default="", help="WxH, e.g. 1080x1920")
    ap.add_argument("--fps", type=float)
    ap.add_argument("--duration", type=float, help="expected seconds")
    ap.add_argument("--frames", type=int, help="expected total frames")
    ap.add_argument("--require-audio", action="store_true")
    ap.add_argument("--report", type=Path, default=None)
    args = ap.parse_args()

    v = args.video
    if not v.is_file():
        raise SystemExit(f"not found: {v}")
    lines: list[str] = [f"# Delivery Report · {v.name}", ""]
    fails: list[str] = []
    warns: list[str] = []
    oks: list[str] = []

    def check(ok: bool, label: str, detail: str, fail=True, warn=False):
        if ok:
            oks.append(f"{label}: ok")
        elif warn:
            warns.append(f"{label}: {detail}")
        elif fail:
            fails.append(f"{label}: {detail}")

    info = probe(v)
    streams = info.get("streams", [])
    vs = next((s for s in streams if s.get("codec_type") == "video"), None)
    has_audio = any(s.get("codec_type") == "audio" for s in streams)
    if not vs:
        raise SystemExit("no video stream")
    w, h = int(vs["width"]), int(vs["height"])
    rate = vs.get("avg_frame_rate") or vs.get("r_frame_rate", "0/1")
    fps = eval(rate) if "/" in rate else float(rate)  # noqa: S307 trusted ffprobe
    dur = float(vs.get("duration") or info.get("format", {}).get("duration", 0))
    nb = int(vs.get("nb_frames") or 0)

    oks.append(f"stream: {w}x{h} {fps:.3f}fps {dur:.2f}s"
          + (f" {nb}f" if nb else "") + (" +audio" if has_audio else " no-audio"))

    if args.expected:
        ew, eh = (int(x) for x in args.expected.lower().split("x"))
        check((w, h) == (ew, eh), "resolution", f"{w}x{h} vs expected {args.expected}")
    if args.fps:
        check(abs(fps - args.fps) < 0.05, "fps", f"{fps:.3f} vs expected {args.fps:g}")
    if args.duration:
        drift = abs(dur - args.duration)
        check(drift <= max(0.5, args.duration * 0.02),
              "duration", f"{dur:.2f}s vs expected {args.duration:g}s (drift {drift:.2f}s)")
    if args.frames and nb:
        check(abs(nb - args.frames) <= 2, "frames", f"{nb} vs expected {args.frames}")

    check(has_audio or not args.require_audio, "audio-required",
          "missing but required" if (args.require_audio and not has_audio) else "present/ok")

    if has_audio:
        lufs, tp, _ = audio_checks(v)
        if not (lufs != lufs):  # not NaN
            check(lufs >= -16, "loudness", f"{lufs:.1f} LUFS (< -16)", fail=False, warn=True)
            check(tp <= -1.0, "true-peak", f"{tp:.2f} dBTP (> -1)")
        sil_out = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(v),
                       "-af", "silencedetect=d=1.5", "-f", "null", "-"])
        sil = re.findall(r"silence_start: ([-\d.]+)", sil_out)
        check(not sil, "silence", f"{len(sil)} silent segment(s) ≥1.5s", fail=False, warn=True)
    else:
        warns.append("audio: none (project did not require it)")

    def edge_black(vf: str) -> tuple[bool, bool]:
        """(starts_pure, ends_pure) for a blackdetect chain."""
        out = detect(v, vf)
        starts = bool(re.search(r"black_start: 0\.0*\b", out))
        ends_at = re.findall(r"black_end: (\d+\.?\d*)", out)
        ends = bool(ends_at) and float(ends_at[-1]) >= dur - 0.6
        return starts, ends

    b0, b1 = edge_black("blackdetect=d=0.5:pic_th=0.98")
    check(not b0, "first-frame", "pure black at t=0")
    check(not b1, "last-frame", f"pure black at tail (t≈{dur:.1f}s)")
    w0, w1 = edge_black("negate,blackdetect=d=0.5:pic_th=0.98")
    check(not w0, "first-frame-white", "pure white at t=0")
    check(not w1, "last-frame-white", "pure white at tail")

    freeze = re.findall(r"freeze_start: ([-\d.]+)", detect(v, "freezedetect=n=-60dB:d=3"))
    check(not freeze, "frozen", f"{len(freeze)} frozen segment(s) ≥3s", fail=False, warn=True)

    sha = hashlib.sha256(v.read_bytes()).hexdigest()[:16]
    verdict = "FAIL" if fails else ("WARNING" if warns else "PASS")

    lines += [f"- file: `{v}` ({v.stat().st_size / 1e6:.1f} MB, sha256 {sha}…)",
              f"- verdict: **{verdict}**", ""]
    for sec, items in (("FAIL", fails), ("WARNING", warns), ("PASS", oks)):
        if items:
            lines.append(f"## {sec}")
            lines += [f"- {i}" for i in items]
            lines.append("")
    report = "\n".join(lines)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
        print(f"{verdict} -> {args.report}")
    else:
        print(report)
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
