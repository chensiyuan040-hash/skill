# 七步工作流(引擎中立)

一条代码视频的质量,通常不是败在"不会写代码",而是败在三件事:**没有风格基准、没有质量门槛、没人敢说不好看**。本流程把三件事钉死:先选风格,再拉满标准,最后独立 critic 打分。

## 工作区

默认 `~/code/video/`(可用 `--workspace` 改):`assets/` 跨项目素材、`projects/` 工程、`samples/` 样片与 contact sheet、`_archive/` 旧工程。

## 0. 起项目

```bash
python ~/.claude/skills/video-studio/scripts/new_project.py <name> \
  --style 01-black-hud-meta --aspect 16:9 --duration 45
```

生成 docs/(BRIEF/STYLE/STORYBOARD/SCORECARD/REFERENCES)、CHECKLIST.md、可跑的 `src/film.html`(seek(t) 模板)。

## 1. Brief 一句话

先拿到**主题/文案、画幅、时长**三要素;素材没有就 TTS + 代码合成。写成一句话后自查:陌生人只看这句能懂吗。不懂不往下走。

## 2. 选风格

读 [style-library.md](style-library.md),按**表达目的**选 1 主 + 最多 1 辅(讲产品→product-ui/3d-showcase;讲观点→black-hud-meta/kinetic-type;讲原理→paper-ink/isometric-clean…)。写 brief 前读 [cases/index.md](cases/index.md) 选 0-2 张案例卡,借用与偏离记进 `docs/REFERENCES.md`。风格名 + 一句话理由写进 STYLE.md。

## 3. 质量门槛

生成代码的提示词开头原样放(实测有效,见 [prompts.md](prompts.md)):

> You are the director, motion designer, engineer and sound designer of ONE film. The goal is the most classic yet most stunning form of this style — award-shortlist / high-end commercial quality. **A clean, template-looking result is a fail.**

中文补充:不用 UI 套壳、不用默认缓动、不堆无意义粒子,每个元素为文案服务。

## 4. 先出 4 张关键帧,过了再动整片

首帧/主视觉/转折/片尾,**不许直接渲染整片**。检查四项:文字溢出/遮挡、主体够大、颜色统一、无模板感。多模态模型用 Read 看图;无视觉模型走盲审管线——`frame_audit.py` 质心审计 + OCR 提字 + DOM 几何报告(叠字/溢出靠 bbox 判,比像素准)。

4 张都愿意署名 → 渲 **10 秒样片**。

## 5. 独立 critic 五陪审

作者不自评。Agent 工具新开 subagent(general-purpose,不用你自己),给 brief、风格名、4 帧、样片、[critic.md](critic.md),要严格 JSON 输出。**通过线:总分 ≥ 8 且无单项 < 7**;不过按 top3_fixes 改,最多 4 轮,还上不去就换风格或砍需求。评分进 SCORECARD.md。

## 6. 全量渲染

渲染前:总帧数=时长×fps、音频峰值/响度合理、首帧非黑白、片尾有落版。渲染后:

1. `teardown_reference.py` 对自家成片跑一份,和参考片数据对照(切镜率/运动能量)
2. 抽 8-12 帧 contact sheet,critic 复审(盲审走 frame_audit + 定点抽帧 OCR)
3. 转场中点、结论/数字出现点定点抽帧检查

## 7. 交付四样 + 硬验收

```bash
python scripts/verify_delivery.py out/final.mp4 --expected 1920x1080 --fps 30 \
  --duration 45 --require-audio --report docs/delivery-report.md
```

PASS 才交付:**成片 mp4 / 可编辑工程 / contact sheet / SCORECARD.md(含 delivery-report 摘录)**。WARNING(如响度 -16 LUFS 边缘)不自动重编码,报告说明原因;FAIL 一律返工。**质检对象是编码后的最终 MP4,预览帧不算数。**

## 模式

- **A 原创**:七步直走
- **B 参考片复刻**:`teardown_reference.py` 拆参考片 → 写/选案例卡 → 3 个 3 秒样片给用户选 → 10 秒样片 → critic → 全量 → 验收
- **C 口播二创**:`transcribe_words.py` 词级时间轴 → 场景映射(每句/每拍一画面)→ 4 帧 → 样片 → critic → 全量 → 验收

## 弱模型三原则(DeepSeek 等无多模态)

1. **填表优先**:结构化产物(storyboard/字幕表/风格卡)比自由代码稳,能填表不写码——竖版宣传直接用本地 brewreel
2. **确定性脚本扛质检**:lint/check、frame_audit、verify_delivery、teardown_reference 四层,能算的不靠看
3. **文字层替代视觉层**:OCR 提帧上文字、DOM bbox 判重叠、"美不美"才主观且标注 [subjective]
