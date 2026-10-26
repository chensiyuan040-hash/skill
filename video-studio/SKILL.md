---
name: video-studio
description: 代码视频统一工作台(引擎中立):导演流程 + 风格库 + 独立评审 + 确定性交付验收。当用户要"做视频/讲解视频/科普视频/宣传片/MV/动效片/showreel"、复刻某种视频风格、口播二创/像素二创、给已有项目加字幕/配音/改场景/排查渲染问题时使用。前身 hyperframes-video + video-director-custom 已合并进来:HyperFrames 中文讲解实战坑、21 风格库、13 案例卡、五陪审 critic、弱模型(DeepSeek 等无多模态)适配。
metadata:
  version: "2.0.0"
  lineage: "hyperframes-video 1.2 + video-director-custom 1.1 → 2026-10-26 合并重构"
---

# Video Studio

代码视频统一入口:先定流程,再选引擎,质量靠独立评审和确定性脚本兜底,不靠运气。

## 一分钟上手

1. **起项目**:`python scripts/new_project.py <name> --style <编号> --aspect 16:9|9:16 --duration <秒>`
2. **Brief 一句话** → **选风格**(21 库,按表达目的)→ **质量门槛提示词**(prompts.md)
3. **4 张关键帧**(首帧/主视觉/转折/片尾)过了文字层检查 → **10 秒样片**
4. **独立 critic 五陪审**打分,总分 ≥8 且无单项 <7 才继续
5. **全量渲染** → `verify_delivery.py` 硬验收 PASS → 交付四样(成片/工程/contact sheet/SCORECARD)

详细每步:**references/workflow.md**。模式 B 参考片复刻、模式 C 口播二创也在里面。

## 引擎路由(不逮着 HyperFrames 放)

| 场景 | 引擎 |
|---|---|
| 通用动效(默认推荐) | 自渲染 seek(t) + `render_seek.py` |
| 中文讲解片(逐句字幕/确定性) | HyperFrames(坑手册:hyperframes-pitfalls.md) |
| React 复用/批量 | Remotion(remotion-craft.md;商用授权注意) |
| 数学公式 | Manim |
| 竖版宣传快出 | 本地 brewreel(填表不写码) |
| 最快试验 | ~/code/explainroo |

选型与命令:**references/engines.md**

## 弱模型适配(DeepSeek 等无多模态)

填表优先、确定性脚本扛质检(lint/check → frame_audit → verify_delivery → teardown_reference 四层)、文字层(OCR/DOM bbox)替代视觉层;critic 陪审照打,证据换脚本输出,主观项标 [subjective]。详见 workflow.md 末节与 critic.md"盲审适配"。

## 何时读哪个参考

- 走流程/评审/交付 → **workflow.md** + **critic.md**
- 选风格 → **style-library.md**;选案例卡 → **cases/index.md**
- 引擎怎么选、渲染命令 → **engines.md**
- HyperFrames 报错/渲染异常 → **hyperframes-pitfalls.md**(按症状查)
- 写讲解场景/逐句字幕 → **scene-recipe.md**;配音 → **voice-pipeline.md**
- 参考片怎么拆 → **teardown_reference.py** + hyperframes-pitfalls.md 末节方法论
- 社区生态/该吸收什么 → **ecosystem.md** + **community-landscape.md**
- Remotion → **remotion-craft.md**;提示词模板 → **prompts.md**

## 自带脚本

- `new_project.py` —— 起项目(内置模板,跨机器可用)
- `render_seek.py` —— seek(t) HTML → 关键帧/样片/成片(Playwright+ffmpeg)
- `verify_delivery.py` —— 交付硬验收(PASS/WARNING/FAIL + markdown 报告)
- `teardown_reference.py` —— 参考片定量拆解(切镜率+运动能量)
- `transcribe_words.py` —— 词级时间轴(Whisper)
- `gen_voice.py` / `inject_subtitles.py` —— edge-tts 配音 / 字幕批量注入(HyperFrames 管线)
- `frame_audit.py` —— 帧质心审计(偏移/空白自动检出,盲审第一层)

## 三条铁律

1. **作者不自评**:critic 独立 subagent,五陪审 JSON 打分,不过线不渲染全量
2. **最终 MP4 才算交付物**:质检从编码后成片取证据,预览帧不算数
3. **叙事时间轴先行**:字幕句时间 + 配音时长决定一切动画节奏,先锁时间轴再动画
