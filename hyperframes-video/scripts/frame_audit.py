#!/usr/bin/env python3
"""渲染帧质心审计:对 hyperframes snapshot 输出的帧 PNG 算内容质心,自动标出偏移/空白帧。

用法:
  1) npx hyperframes snapshot --at t1,t2,...(在项目目录)
  2) uv run --with pillow --with numpy python frame_audit.py <snapshot目录>

判定:质心 x 不在 [700,1220] 或 y 不在 [380,700] → OFF;亮像素 <0.5% → SPARSE。
"""
import sys, glob, os
import numpy as np
from PIL import Image

def main(d):
    files = sorted(glob.glob(os.path.join(d, "frame-*.png")))
    if not files:
        sys.exit("no frames found")
    bad = 0
    for f in files:
        im = np.asarray(Image.open(f).convert("RGB"), dtype=np.float32)
        lum = im.mean(axis=2)
        m = lum > 45
        ys, xs = np.nonzero(m)
        name = os.path.basename(f)
        if len(xs) < 5000:
            print(f"{name}: SPARSE ({len(xs)} px)"); bad += 1; continue
        cx, cy = xs.mean(), ys.mean()
        flags = []
        if cx < 700 or cx > 1220: flags.append("X-OFF")
        if cy < 380 or cy > 700: flags.append("Y-OFF")
        if m.mean() < 0.005: flags.append("SPARSE")
        if flags: bad += 1
        print(f"{name}: centroid ({cx:.0f},{cy:.0f}) bright {m.mean()*100:.2f}% {' '.join(flags)}")
    print(f"\nflagged {bad}/{len(files)}")

if __name__ == "__main__":
    main(sys.argv[1])
