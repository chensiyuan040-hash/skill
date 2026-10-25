#!/usr/bin/env python3
"""Scaffold a code-video project from the workspace template.

Examples:
  python new_project.py my-film
  python new_project.py my-film --style 01-black-hud-meta --aspect 9:16 --duration 30
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

WORKSPACE = Path.home() / "code" / "video"
TEMPLATE = WORKSPACE / "projects" / "_template"
ASPECTS = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
    "4:3": (1440, 1080),
}


def slugify(name: str) -> str:
    slug = name.strip().replace(" ", "-")
    slug = re.sub(r"[^0-9A-Za-z一-鿿_-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "untitled"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--style", default="01-black-hud-meta")
    ap.add_argument("--aspect", default="16:9", choices=sorted(ASPECTS))
    ap.add_argument("--duration", type=float, default=10.0)
    args = ap.parse_args()

    if not TEMPLATE.is_dir():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    slug = slugify(args.name)
    target = WORKSPACE / "projects" / slug
    if target.exists():
        raise SystemExit(f"Project already exists: {target}")

    shutil.copytree(TEMPLATE, target)
    for sub in ("assets", "out", "stills"):
        (target / sub).mkdir(exist_ok=True)

    width, height = ASPECTS[args.aspect]
    scale = width / 1920
    replacements = {
        "{{NAME}}": args.name,
        "{{STYLE}}": args.style,
        "{{ASPECT}}": args.aspect,
        "{{DURATION}}": f"{args.duration:g}",
    }

    for path in target.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".html", ".css", ".js"}:
            continue
        text = path.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        if path.suffix.lower() == ".html":
            text = text.replace("const DURATION = 10;", f"const DURATION = {args.duration:g};")
            text = text.replace("width: 1920px; height: 1080px;",
                                f"width: {width}px; height: {height}px;")
            text = text.replace("walk * 1400", f"walk * {width - 380}")
            text = text.replace("font-size: 112px", f"font-size: {round(112 * scale)}px")
            text = text.replace("font-size: 34px", f"font-size: {round(34 * scale)}px")
            text = text.replace("font-size: 22px", f"font-size: {round(22 * scale)}px")
            text = text.replace("font-size: 26px", f"font-size: {round(26 * scale)}px")
            text = text.replace("width: 120px; height: 120px;",
                                f"width: {round(120 * scale)}px; height: {round(120 * scale)}px;")
        path.write_text(text, encoding="utf-8")

    print(f"Created {target}")
    print("Next:")
    print(f"  1. Fill {target / 'docs/BRIEF.md'} (see CHECKLIST.md)")
    print(f"  2. Preview: ~/.venvs/video/bin/python "
          f"~/.claude/skills/video-director/scripts/render_seek.py "
          f"{target / 'src/film.html'} --preview 0,3,6,9 --out {target / 'stills'}")
    print(f"  3. Draft:   ~/.venvs/video/bin/python "
          f"~/.claude/skills/video-director/scripts/render_seek.py "
          f"{target / 'src/film.html'} --duration {args.duration:g} --fps 30 "
          f"--out {target / 'out/draft.mp4'}")


if __name__ == "__main__":
    main()
