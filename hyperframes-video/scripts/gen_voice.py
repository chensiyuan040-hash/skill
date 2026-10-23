#!/usr/bin/env python3
"""edge-tts 批量配音生成器:按场景生成 mp3 并自动适配目标时长(超时自动加语速)。

用法(uv 隔离依赖):
  uv run --with edge-tts python gen_voice.py --project /path/to/hyperframes-project \
      --voice zh-CN-YunxiNeural --segments-json '[{"id":"scene-01","sceneLen":20,"text":"..."},...]'
输出 <project>/assets/voice/<id>.mp3 + segments-meta.json(实测时长/语速)。
"""
import argparse, asyncio, json, math, subprocess, os

def dur(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode().strip())

async def gen(text, out, voice, rate):
    import edge_tts
    await edge_tts.Communicate(text, voice, rate=rate).save(out)

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--voice", default="zh-CN-YunxiNeural")
    ap.add_argument("--segments-json", required=True)
    ap.add_argument("--max-rate", type=int, default=12, help="语速上限%%,超过则报错提示拉长场景")
    a = ap.parse_args()

    outdir = os.path.join(a.project, "assets", "voice")
    os.makedirs(outdir, exist_ok=True)
    meta = {}
    for seg in json.loads(a.segments_json):
        sid, scene_len, text = seg["id"], seg["sceneLen"], seg["text"]
        out = os.path.join(outdir, f"{sid}.mp3")
        rate = "+0%"
        await gen(text, out, a.voice, rate)
        d = dur(out)
        budget = scene_len - 1.2
        if d > budget:
            pct = int((d / budget - 1) * 100) + 3
            if pct > a.max_rate:
                print(f"!! {sid}: 需 +{pct}% 语速超上限,建议把场景从 {scene_len}s 拉长到 {math.ceil(d)+2}s 或删文案")
                continue
            rate = f"+{pct}%"
            await gen(text, out, a.voice, rate)
            d = dur(out)
        meta[sid] = {"dur": round(d, 2), "scene": scene_len, "rate": rate}
        print(f"{sid}: {d:.1f}s / {scene_len}s rate={rate}")
    json.dump(meta, open(os.path.join(a.project, "scripts", "voice", "segments-meta.json"), "w"),
              ensure_ascii=False, indent=1) if os.path.isdir(os.path.join(a.project, "scripts", "voice")) else \
        json.dump(meta, open(os.path.join(a.project, "voice-meta.json"), "w"), ensure_ascii=False, indent=1)

asyncio.run(main())
