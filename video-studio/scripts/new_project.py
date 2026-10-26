#!/usr/bin/env python3
"""Scaffold a code-video project from the skill-bundled template.

Examples:
  python new_project.py my-film
  python new_project.py my-film --style 01-black-hud-meta --aspect 9:16 --duration 30
  python new_project.py my-film --workspace ~/code/video
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "template"
DEFAULT_WORKSPACE = Path.home() / "code" / "video"
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
    ap.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE,
                    help=f"video workspace root (default {DEFAULT_WORKSPACE})")
    args = ap.parse_args()

    if not TEMPLATE.is_dir():
        raise SystemExit(f"Template not found: {TEMPLATE}")

    slug = slugify(args.name)
    target = args.workspace / "projects" / slug
    if target.exists():
        raise SystemExit(f"Project already exists: {target}")

    shutil.copytree(TEMPLATE, target)

    width, height = ASPECTS[args.aspect]
    scale = width / 1920
    replacements = {
        "{{NAME}}": args.name,
        "{{STYLE}}": args.style,
        "{{ASPECT}}": args.aspect,
        "{{DURATION}}": f"{args.duration:g}",
        "{{WIDTH}}": str(width),
        "{{HEIGHT}}": str(height),
        "{{FONT_XL}}": str(round(112 * scale)),
        "{{FONT_L}}": str(round(34 * scale)),
        "{{FONT_S}}": str(round(22 * scale)),
        "{{TITLE_LINE_1}}": args.name,
        "{{TITLE_LINE_2}}": "一句话主题",
    }

    for path in target.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".html", ".css", ".js"}:
            continue
        text = path.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        path.write_text(text, encoding="utf-8")

    py = sys.executable or "python3"
    render = Path(__file__).resolve().parent / "render_seek.py"
    print(f"Created {target}")
    print("Next:")
    print(f"  1. Fill {target / 'docs/BRIEF.md'} (see CHECKLIST.md)")
    print(f"  2. Preview: {py} {render} {target / 'src/film.html'} "
          f"--preview 0,3,6,9 --out {target / 'stills'}")
    print(f"  3. Draft:   {py} {render} {target / 'src/film.html'} "
          f"--duration {args.duration:g} --fps 30 --out {target / 'out/draft.mp4'}")


if __name__ == "__main__":
    main()
