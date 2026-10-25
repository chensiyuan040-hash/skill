---
name: video-director-custom
description: Chen 定制版代码视频导演工作流（优先使用本 skill）。在 video-director 基础上加入 13 张案例卡、21 风格库、参考片复刻/口播二创模式、独立 critic 专项与交付验收脚本。当用户要做代码生成的视频、复刻某种视频风格、做口播二创/像素二创，或说“做一条视频/宣传片/MV/科普片/动效片/showreel”时使用。上游 video-director 仅作参考。
metadata:
  version: "1.1.0"
  upstream: "video-director 1.0.0 @ 2026-10-25"
---

# Video Director（Chen 定制版）

> 本 skill 是 `video-director` 的独立定制分支。若同时加载了上游 `video-director`，以本 skill 为准。

一条代码视频的质量，通常不是败在“不会写代码”，而是败在三件事：**没有风格基准、没有质量门槛、没人敢说不好看**。这个 skill 把这三件事固定成流程：先选风格模板，再把质量标准写到最高，最后让一个**独立的 critic subagent** 打分，作者本人不给自己打分。

## 何时使用

用户说“做一条视频”“复刻这个风格”“把这段文案做成视频”“优化这条片子”“做一个宣传片 / MV / 科普片 / showreel / 口播片”，或给了一个参考视频链接时，先用本 skill 定流程，再调用具体引擎。

## 工作区

素材、工程、成品统一放在 `/home/chen/code/video/`：

```
assets/     跨项目素材（清单 assets/MANIFEST.md）
projects/   可编辑工程（文档在 docs/，模板 projects/_template/）
examples/   校准示例
samples/    样片、关键帧、contact sheet
scripts/    开发脚本
_archive/   旧工程与草稿
```

## 案例库

`references/cases/index.md` 是选卡入口。写 brief 前先读它，按“表达目的”选 0–2 张案例卡；在项目 `docs/REFERENCES.md` 记录借用的元素和偏离。

- 选卡表：`references/cases/index.md`
- 社区项目决策表：`references/community-landscape.md`
- Remotion 专项规则：`references/remotion-craft.md`

## 七步流程

### 0. 起项目

```bash
python ~/.claude/skills/video-director-custom/scripts/new_project.py <name> \
  --style 01-black-hud-meta --aspect 16:9 --duration 45
```

生成 `docs/BRIEF.md`、`docs/STYLE.md`、`docs/STORYBOARD.md`、`docs/SCORECARD.md`、`CHECKLIST.md`、`src/film.html`（可直接跑的 `seek(t)` 模板）以及 `assets/`、`out/`、`stills/`。

### 1. Brief（一句话）

先拿到三样：**主题/文案、画幅（横屏 16:9 / 竖屏 9:16）、时长**。素材有则更好（口播、图片、音乐、Logo），没有就用 TTS + 代码合成。

把 brief 写成一句话，例如：

> 用 45 秒、竖屏 9:16，讲清楚“我如何用一句话做出一条视频”。

不要急着写代码。先确认这句话能不能让一个陌生人看懂。

### 2. 选风格

读 [references/style-library.md](references/style-library.md)，从 21 个风格里选 1 个主风格 + 最多 1 个辅助风格。选择依据是**表达目的**，不是“哪个看起来酷”：

- 讲产品 → `product-ui` / `3d-showcase`
- 讲观点/知识 → `black-hud-meta` / `kinetic-type` / `swiss-minimal`
- 讲故事/情绪 → `hand-painted` / `comic-pop`
- 讲数学/原理 → `paper-ink` / `isometric-clean`
- 音乐/歌词 → `lyric-karaoke` / `p5r-mad`
- 技术/工具 → `dark-tech-console` / `crt-shader`

选完把风格名和一句话理由写进 `projects/<name>/docs/STYLE.md`。

### 3. 质量门槛

在给模型的提示词开头，原样放入这段英文（来自参考教程，实测有效）：

```text
You are the director, motion designer, engineer and sound designer
of ONE 10-second motion-design film.
The goal is the most classic yet most stunning form of this style —
award-shortlist / high-end commercial quality.
A clean, template-looking result is a fail.
```

中文补充：

> 目标是获奖短片/高端商业定制的完成度；一个“干净的模板感”结果视为失败。不要用现成 UI 套壳，不要用默认缓动，不要用无意义的粒子堆砌。

### 4. 先出 4 张关键帧

不要一上来渲染整片。先做 4 张不同时间点的静帧（首帧、主视觉、转折、片尾），用 Read 工具亲自看：

- 文字有没有溢出/遮挡
- 主体是否足够大
- 颜色是否统一
- 有没有“模板感”

不满意就改，直到 4 张都愿意署名。然后再渲染 **10 秒样片**。

### 5. 独立 critic 打分

**作者不给自己打分。** 用 Agent 工具新开一个 subagent（`subagent_type: "general-purpose"` 或 `"fork"`，但不要用你自己），把 brief、风格名、4 张关键帧、10 秒样片、以及 [references/critic.md](references/critic.md) 一起给它，让它按 1–10 分打分并给出具体修改项。

评分锚点：

| 分数 | 含义 |
|---|---|
| 5 | 合格的学生作业 |
| 6 | 模板 / 剪映水平 |
| 7 | 扎实的专业水准 |
| 8 | 获奖短片 / 高端商业定制 |
| 9 | 例外级，值得主动传播 |
| 10 | 大师级，风格定义者 |

**通过线：总分 ≥ 8，且没有任何单项 < 7。** 不通过就按 critic 的 top 3 fixes 改，再跑一轮。最多 4 轮；如果 4 轮还上不去，换风格或砍需求，不要硬堆效果。

### 6. 全量渲染

通过后再渲染完整时长。渲染前检查：

- 总帧数 = 时长 × fps
- 音频有峰值、不削波、响度合理
- 首帧不是黑屏/白屏
- 片尾有明确的落版（logo / 标题 / CTA）

渲染后抽 8–12 帧做 contact sheet，再让 critic 看一次完整片（至少看 contact sheet + 关键转场帧）。

### 7. 交付

交付四样：

1. `projects/<name>/out/<name>.mp4` — 成片
2. `projects/<name>/` — 可编辑工程（`docs/` + `src/` + `assets/`）
3. `samples/final/<name>-contact-sheet.jpg` — 审片用关键帧
4. `projects/<name>/docs/SCORECARD.md` — critic 的评分、证据、修改记录

## 工作流模式

### 模式 A：原创

七步流程：brief → 风格 → 4 关键帧 → 10 秒样片 → critic → 全量 → 交付。

### 模式 B：参考片复刻

```text
参考片 → teardown_reference.py 抽帧/场景切点 → 写/选案例卡
→ 3 个 3 秒样片（不同风格或节奏）→ 用户选型
→ 10 秒样片 → 独立 critic → 全量 → 交付验收
```

### 模式 C：口播二创

```text
原声/口播 → transcribe_words.py 词级时间轴
→ 场景映射（每句/每拍对应画面）
→ 4 张关键帧 → 10 秒样片 → 独立 critic → 全量 → 交付验收
```

## 交付验收

全量渲染后跑 `verify_delivery.py`，把 `delivery-report.md` 和 contact sheet 写入 `docs/SCORECARD.md`。

- PASS：所有硬性检查通过。
- WARNING：响度低于 -16 LUFS、检测到静音/静止段、无音频但项目未要求音频。
- FAIL：分辨率/fps/帧数/时长不符、true peak 超限、要求音频但缺失、首尾帧纯黑/纯白。

响度 WARNING 不自动重编码；保留原声的项目在报告中说明原因。

## 引擎路由

| 需求 | 引擎 | 入口 |
|---|---|---|
| HTML/CSS/SVG + 逐帧截图 | motion-design | `~/.claude/skills/motion-design/scripts/render_template.py` |
| Canvas/Three.js + 字效 | kinetic-reel | `~/.claude/skills/kinetic-reel/template/render.mjs` |
| p5.js 水彩手绘 | painted-animation | `~/.claude/skills/painted-animation/template/render.mjs` |
| Manim 数学动画 + 中文 TTS | math-concept-film | `~/.claude/skills/math-concept-film/SKILL.md` |
| React 组件视频 | remotion-best-practices | `npx remotion render` |
| 口播模板 / .motion | adu-motion-video | `~/.claude/skills/adu-motion-video/scripts/pipeline.py` |

> HyperFrames：若同一仓库有 `hyperframes-video/`，先读它的 `SKILL.md` 和 `references/pitfalls.md`；它讲 HyperFrames 本机坑，本 skill 讲导演/评审。

如果工程是我们自己的 `seek(t)` HTML（推荐，最可控），用 [scripts/render_seek.py](scripts/render_seek.py)：

```bash
# 4 张关键帧
~/.venvs/video/bin/python scripts/render_seek.py film.html --preview 0,3,6,9 --out out/preview

# 10 秒样片
~/.venvs/video/bin/python scripts/render_seek.py film.html --duration 10 --fps 30 --out out/draft.mp4

# 全量
~/.venvs/video/bin/python scripts/render_seek.py film.html --duration 45 --fps 30 --out out/final.mp4 --audio assets/music.mp3
```

无 GPU 时，painted-animation / kinetic-reel 的 `render.mjs` 必须加 `--soft-gl`；自己的 `seek(t)` 页面如果用了 WebGL，也给 `render_seek.py` 加 `--soft-gl`。

性能提示：全屏 CSS `mask-image` / 重 `filter` 会让逐帧截图慢 5–10 倍。草稿用 `--format jpg --crf 18`（约 10 帧/秒），正式片用 `--format png --crf 16`。实测去掉一个全屏 mask 后，300 帧从 ~10 分钟降到 ~30 秒。

## 参考文件

- [references/style-library.md](references/style-library.md) — 21 个风格模板、配色、动效词汇、失败模式
- [references/critic.md](references/critic.md) — 1–10 评分卡、评审流程、输出格式
- [references/prompts.md](references/prompts.md) — 高质量 brief、风格适配、迭代提示词
- [references/community-landscape.md](references/community-landscape.md) — 社区项目分档与选型
- [references/remotion-craft.md](references/remotion-craft.md) — Remotion 10 条铁律与官方技能路由
- [references/cases/index.md](references/cases/index.md) — 13 张案例卡索引
