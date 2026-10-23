#!/usr/bin/env python3
"""逐句字幕批量注入器:把句子列表写进场景文件的字幕条(HTML)+CSS+JS 动画一次到位。

用法:
  python3 inject_subtitles.py <scene.html> <prefix> <composition-id> \
      --sentences "0.8,6.0|句子一;6.3,12.0|句子二;..."

注意:场景文件需已有 <div class="<prefix>-subtitle-bar">(可含旧文本,会被替换)。
"""
import argparse, re, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file"); ap.add_argument("prefix"); ap.add_argument("comp_id")
    ap.add_argument("--sentences", required=True, help="in,out|text;in,out|text;...")
    a = ap.parse_args()

    items = []
    for chunk in a.sentences.split(";"):
        times, _, text = chunk.partition("|")
        i, _, o = times.partition(",")
        items.append((float(i), float(o), text.strip()))

    s = open(a.file).read()
    # 1) replace subtitle bar content with sentence spans (tolerate data-hf-id attrs)
    bar = re.search(r'(<div[^>]*class="' + a.prefix + r'-subtitle-bar">)(.*?)(</div>)', s, re.S)
    if not bar:
        sys.exit("subtitle bar not found")
    spans = "".join(f'\n          <span class="{a.prefix}-sub">{t}</span>' for _, _, t in items)
    s = s[:bar.start(2)] + spans + "\n        " + s[bar.end(2):]

    # 2) append CSS before </style> if .sub rule missing
    if f".{a.prefix}-sub {{" not in s:
        s = s.replace("      </style>", (
            f"        .{a.prefix}-sub {{\n"
            "          position: absolute; left: 0; bottom: 0; width: 1920px; height: 120px;\n"
            "          display: flex; align-items: center; justify-content: center;\n"
            "          padding: 0 140px; box-sizing: border-box; opacity: 0;\n"
            "          font-size: 32px; font-weight: 500; line-height: 1.45; text-align: center; color: #d5cfc0;\n"
            "        }\n"
            f"        .{a.prefix}-subtitle-bar {{ height: 120px; }}\n"
            "      </style>"), 1)

    # 3) insert animation before timeline registration
    reg = f'window.__timelines["{a.comp_id}"] = tl;'
    if reg not in s:
        sys.exit("timeline registration not found")
    times = str([[i, o] for i, o, _ in items])
    js = (
        f"        const subs = document.querySelectorAll(\".{a.prefix}-sub\");\n"
        f"        const subTimes = {times};\n"
        "        for (let i = 0; i < subs.length; i++) {\n"
        "          if (i === 0) tl.fromTo(subs[i], { opacity: 0 }, { opacity: 1, duration: 0.4, overwrite: \"auto\" }, subTimes[i][0]);\n"
        "          else tl.fromTo(subs[i], { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false, overwrite: \"auto\" }, subTimes[i][0]);\n"
        "          tl.to(subs[i], { opacity: 0, duration: 0.3, overwrite: \"auto\" }, subTimes[i][1]);\n"
        "        }\n"
    )
    s = s.replace("        " + reg, js + "        " + reg, 1)
    open(a.file, "w").write(s)
    print(f"injected {len(items)} sentences into {a.file}")

if __name__ == "__main__":
    main()
