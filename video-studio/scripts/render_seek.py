#!/usr/bin/env python3
"""Render a seek(t) HTML film: Playwright screenshots -> ffmpeg MP4.

The page must expose `window.seek(t)` and ideally `window.ready`.
Every frame is a pure function of time; the renderer never relies on CSS
transitions, timers, or wall-clock state.

Examples:
  python render_seek.py film.html --preview 0,3,6,9 --out out/preview
  python render_seek.py film.html --duration 10 --fps 30 --out out/draft.mp4
  python render_seek.py film.html --duration 45 --fps 30 --out out/final.mp4 \
      --audio assets/music.mp3
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def find_chrome(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    cache = Path.home() / ".cache/ms-playwright"
    if cache.exists():
        candidates = []
        for path in cache.glob("chromium-*/chrome-linux*/chrome"):
            try:
                build = int(path.parent.parent.name.split("-")[1])
            except (IndexError, ValueError):
                build = 0
            candidates.append((build, path))
        for _, path in sorted(candidates, reverse=True):
            if path.exists():
                return str(path)
    for path in (
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ):
        if Path(path).exists():
            return path
    raise SystemExit("Chrome not found: pass --chrome or set CHROME_PATH")


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def open_page(pw, args, url: str):
    chrome_args = [
        "--no-sandbox",
        "--allow-file-access-from-files",
        "--force-color-profile=srgb",
        "--ignore-gpu-blocklist",
    ]
    if args.soft_gl:
        chrome_args += ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
    browser = pw.chromium.launch(executable_path=find_chrome(args.chrome), args=chrome_args)
    viewport = {"width": args.width or 1920, "height": args.height or 1080}
    page = browser.new_page(viewport=viewport, device_scale_factor=1)
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_function("typeof window.seek === 'function'", timeout=120000)
    try:
        page.wait_for_function("window.ready === undefined || window.ready === true", timeout=120000)
    except Exception:
        pass
    return browser, page


def seek(page, t: float) -> None:
    page.evaluate(f"window.seek({t})")
    # Two rAFs let layout/paint settle without introducing wall-clock state.
    page.evaluate(
        "() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))"
    )


def contact_sheet(files: list[Path], out: Path, width: int = 480) -> None:
    if not files:
        return
    cols = 2 if len(files) <= 4 else 3
    rows = (len(files) + cols - 1) // cols
    tmp = out.with_suffix("")
    tmp.mkdir(parents=True, exist_ok=True)
    pattern = tmp / "p_%02d.png"
    for i, file in enumerate(files):
        shutil.copyfile(file, tmp / f"p_{i:02d}.png")
    run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", "1",
        "-i", str(pattern), "-vf",
        f"scale={width}:-1,tile={cols}x{rows}:padding=6:color=white",
        "-frames:v", "1", str(out),
    ])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, default=10.0)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--format", choices=["png", "jpg"], default="png",
                    help="frame format; jpg is faster for drafts")
    ap.add_argument("--crf", type=int, default=18,
                    help="x264 quality; 16 for a delivery master, 18 for drafts")
    ap.add_argument("--range", default=None, help="start:end seconds")
    ap.add_argument("--selector", default="#stage")
    ap.add_argument("--preview", default=None, help="comma-separated times")
    ap.add_argument("--audio", default=None)
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--soft-gl", action="store_true")
    ap.add_argument("--url", default=None, help="serve over http instead of file://")
    ap.add_argument("--width", type=int, default=None)
    ap.add_argument("--height", type=int, default=None)
    args = ap.parse_args()

    html = Path(args.html).resolve()
    if not html.exists():
        raise SystemExit(f"HTML not found: {html}")
    url = args.url or html.as_uri()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser, page = open_page(pw, args, url)
        try:
            if args.preview:
                times = [float(x) for x in args.preview.split(",")]
                preview_dir = out if out.suffix == "" else out.with_suffix("")
                preview_dir.mkdir(parents=True, exist_ok=True)
                files = []
                for i, t in enumerate(times):
                    seek(page, t)
                    path = preview_dir / f"frame_{i:02d}_{t:g}s.png"
                    page.locator(args.selector).screenshot(path=str(path))
                    files.append(path)
                    print(f"preview {t:g}s -> {path}")
                sheet = preview_dir / "sheet.png"
                contact_sheet(files, sheet)
                print(f"sheet -> {sheet}")
                return

            if args.range:
                start, end = (float(x) for x in args.range.split(":"))
            else:
                start, end = 0.0, args.duration
            n = max(1, round((end - start) * args.fps))
            frames = out.with_suffix("") / "frames"
            if frames.exists():
                shutil.rmtree(frames)
            frames.mkdir(parents=True)
            suffix = ".jpg" if args.format == "jpg" else ".png"
            for i in range(n):
                t = start + i / args.fps
                seek(page, t)
                shot = frames / f"f{i:05d}{suffix}"
                if args.format == "jpg":
                    page.locator(args.selector).screenshot(
                        path=str(shot), type="jpeg", quality=90
                    )
                else:
                    page.locator(args.selector).screenshot(path=str(shot))
                if i % 30 == 0:
                    print(f"frame {i}/{n}", flush=True)
        finally:
            browser.close()

    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-stats",
        "-framerate", str(args.fps), "-i", str(frames / f"f%05d{suffix}"),
    ]
    audio = None
    if args.audio:
        audio = Path(args.audio).resolve()
        if not audio.exists():
            raise SystemExit(f"Audio not found: {audio}")
        cmd += ["-i", str(audio)]
    cmd += [
        "-vf", "scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p",
        "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709", "-color_range", "tv",
        "-c:v", "libx264", "-crf", str(args.crf), "-preset", "slow",
        "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    ]
    if audio:
        cmd += ["-map", "0:v", "-map", "1:a",
                "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd.append(str(out))
    run(cmd)
    print(f"video -> {out}")


if __name__ == "__main__":
    main()
