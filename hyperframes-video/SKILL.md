---
name: hyperframes-video
description: 用 HyperFrames(HTML→MP4 逐帧渲染)制作中文讲解/科普视频的实战工作流与本机踩坑手册。当用户要"做视频/讲解视频/科普视频/动画演示视频"、"用 HyperFrames/hyperframes 做视频"、给已有 hyperframes 项目"加字幕/加配音/改场景/排查渲染问题"时使用。覆盖:项目初始化、场景 sub-composition 编写、逐句字幕系统、edge-tts 中文配音管线、lint/check 修复套路、真实网页截图采集、参考视频定量拆解。官方 12 个 hyperframes skill 讲通用规范,本 skill 讲本机实证过的坑与中文视频实战配方。
---

# HyperFrames 中文视频实战

在 HTML 里写视频,引擎逐帧渲染成 MP4。本 skill 是 2026-10 一次完整 6.5 分钟中文科普视频(含真实数据、配音、截图)的实战沉淀,重点是官方文档没写、踩过才知的坑。

## 全流程(五步)

1. **初始化**:`npx hyperframes init <dir>` → Node22+、FFmpeg 前置;本机需 `HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome`(引擎自动下载 chrome-headless-shell 会因网络失败,见 pitfalls#1)
2. **结构与内容**:主 `index.html` 串联场景 sub-comp;内容素材(真实数据/截图)先归档 `scripts/sources.md` 再上画面——**信息密度是讲解视频的第一生命**
3. **动画**:每场景一个 paused GSAP timeline;逐句字幕系统 + 节奏高亮(配方见 `references/scene-recipe.md`)
4. **校验**:`npx hyperframes check` 全绿是渲染前提;修复套路见 `references/pitfalls.md`(90% 的错误都在手册里有现成解法)
5. **配音**(可选):edge-tts 生成 → 按实测时长适配语速 → **音频必须挂主 index 的 root 内**(sub-comp 里不生效,见 pitfalls#6)→ 重渲
6. **质检与交付**:渲染后 `npx hyperframes snapshot` 抽关键帧逐张看(视觉自检闭环:渲染→看帧→改进→再渲);**封面图直接用 snapshot 出**,不另开工具

关键命令:preview 用 `--background`(可热重载);渲染 365s@1080p 约 9-10 分钟(5 worker 截图模式,本机无 GPU)。

## 何时读哪个参考

- 任何报错/渲染异常 → **先查 `references/pitfalls.md`**(按症状查,含相机 transform 链这个未解引擎 bug 的结论)
- 写新场景 → `references/scene-recipe.md`(含逐句字幕 JS 模板、标注动画模式)
- 加配音 → `references/voice-pipeline.md`
- 分析参考视频(抖音等)→ pitfalls.md 末节"参考视频定量拆解"
- 找现成动效块/同赛道 skill/配音升级/剪映打通等外部工具 → `references/ecosystem.md`(开源生态清单,含官方 capture --video 1:1 复刻)

## 自带脚本

- `scripts/inject_subtitles.py` —— 逐句字幕批量注入(HTML/CSS/JS 一次到位,防手写错)
- `scripts/gen_voice.py` —— edge-tts 批量生成 + 自动语速适配场景时长(uv run 执行)
- `scripts/frame_audit.py` —— 渲染帧质心审计(画面偏移/空白自动检出,排镜头问题必备)

## 三条铁律

1. **改任何场景文件前先 grep**:Studio 会给元素插 `data-hf-id`,字符串替换会静默失败(pitfalls#2)
2. **不碰大画布相机方案**:引擎渲染管线对连续 transform 链驱动错位,已多方案验证无解(pitfalls#8),动画只做元素级
3. **叙事时间轴先行**:字幕句时间 + 配音时长决定一切动画节奏;先锁时间轴再做动画,返工成本最低
