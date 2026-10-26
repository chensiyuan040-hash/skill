# edge-tts 中文配音管线

## 生成(自动适配场景时长)

`scripts/gen_voice.py`:每段文案 + 目标场景时长 → 默认语速出样 → ffprobe 实测 → 若超时则按比例加 rate 重生成(rate 超过 +12% 建议改拉长场景,语速自然度优先)。

运行(系统 Python 是 PEP668,走 uv):
```
uv run --with edge-tts python scripts/gen_voice.py --project <hyperframes项目目录> --voice zh-CN-YunxiNeural
```
- 推荐音色:zh-CN-YunxiNeural(年轻沉稳男)/ zh-CN-YunyangNeural(新闻播报)
- 中文语速实测 ~5.1 字/s(Yunxi 默认);先按 5.1 字/s 估时长规划文案

## 集成(关键坑见 pitfalls#6)

1. 音频 mp3 放 `assets/voice/scene-NN.mp3`(文件名保持稳定,重配音只换文件)
2. **主 index.html 的 root div 内部**挂:`<audio id="vN" src="assets/voice/scene-NN.mp3" data-start="<场景起点+0.3>" data-duration="<实测时长>" data-volume="1.0" data-track-index="2"></audio>`
3. 验证:`npx hyperframes timeline` 输出应出现 `audio (N)` 段;渲染摘要行 `audio` 不再是 0.0s
4. ffmpeg 抽无声底版(给剪映等二次配音):`ffmpeg -i voiced.mp4 -c:v copy -an silent.mp4`

## 时间轴适配原则

叙事时间轴(字幕句时间戳)一旦定稿就锁死;配音按场景生成,场景时长 = max(画面需求, 音频+1.2s);配音与字幕文字同源(narration.md 是唯一真源),字幕句是精简版、配音是完整版——两版并存即可,不必逐字一致。

## 吸收的音频原则(hbg-douyin 竞品,2026-10-26)

- **TTS 按"完整说话人轮次"生成,不按视觉场景切**——说话人切换才是音频的硬边界,视觉场景不是;逐场景配会切断语气连贯
- **Whisper 只负责时间轴,显示文本一律用校正稿**——规避 ASR 同音错字(的/地/得、专有名词)进字幕
- **语速加速只做一次**(TTS 阶段定 rate),不要 TTS 加一遍、后期又加一遍,叠加速出机械感
- **BGM 全片稳定增益 + 交叉循环,不逐句抽吸**;只在明显遮人声的段落做 ducking
