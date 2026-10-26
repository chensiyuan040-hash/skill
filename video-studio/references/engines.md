# 引擎路由(只列两边机器都实际可用的)

按片选引擎,不逮着任何一个不放。选型第一问:**这条片要什么,哪个引擎最短路径给到**。

## 路由表

| 场景 | 引擎 | 入口 | 何时不用 |
|------|------|------|----------|
| 通用动效/自渲染 HTML(默认推荐) | 自家 `seek(t)` | `scripts/render_seek.py` | 要 HyperFrames 字幕系统时 |
| 中文讲解片(确定性、逐句字幕、场景 sub-comp) | HyperFrames | `npx hyperframes`,坑见 [hyperframes-pitfalls.md](hyperframes-pitfalls.md) | 追求渲染速度时(同题实测最慢) |
| React 组件复用/数据驱动批量 | Remotion | `npx remotion render`,规则见 [remotion-craft.md](remotion-craft.md) | 公司项目(需商业授权) |
| 数学/公式动画 | Manim | `pip/uv run manim` | 非数学题材 |
| 竖版宣传/填表快出 | brewreel(本地已装) | 填 `storyboard.json`,一条命令出片 | 要自由设计时(只填表不写码) |
| 最快试验片 | explainroo(~/code/explainroo) | 进目录让 agent 读 AGENTS.md | 要精细控制画面时 |
| DeepSeek 级模型做 Remotion 动效 | motion-design-prompt-generator(本地已装) | 按其 SKILL.md 走五陪审 | 已有本 skill 流程时重叠 |

## 自渲染 seek(t) 契约(skill 自带,零外部依赖)

页面是时间的纯函数:`window.seek(t)` 由 `render_seek.py` 逐帧调用,不用 CSS transition/定时器/墙钟。依赖 Playwright + ffmpeg(`uv run --with playwright`)。

```bash
# 4 张关键帧(零步渲染,秒出)
python scripts/render_seek.py src/film.html --preview 0,3,6,9 --out stills
# 10 秒样片 / 全量 / 带配乐
python scripts/render_seek.py src/film.html --duration 10 --fps 30 --out out/draft.mp4
python scripts/render_seek.py src/film.html --duration 45 --fps 30 --out out/final.mp4 --audio assets/music.mp3
```

无 GPU 时 WebGL 页面加 `--soft-gl`;草稿 `--format jpg --crf 18`(约 10 帧/s),正式 `--format png --crf 16`。全屏 CSS mask/重 filter 拖慢截图 5-10 倍,能免则免。

## HyperFrames 要点(详见 hyperframes-pitfalls.md)

讲解片的成熟路:场景 sub-comp + 逐句字幕(`scene-recipe.md`)+ edge-tts 配音(`voice-pipeline.md`)+ lint/check 全绿再渲。三大坑先记:Chrome 要 `HYPERFRAMES_BROWSER_PATH`、audio 只能挂主 index root 内、相机 transform 链 bug 别碰(只做元素级动画)。

## 配音(引擎无关)

edge-tts 起手(`gen_voice.py`);要音色克隆/中文纠音上 Index-TTS;词级时间轴用 `transcribe_words.py`(Whisper)。音频原则(说话人轮次是硬边界、语速只加速一次、BGM 稳定不逐句抽吸)见 [voice-pipeline.md](voice-pipeline.md)。
