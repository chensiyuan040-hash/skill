# 社区项目决策表

> 扫描日期：2026-10-25。来源：`awesome-claude-video-skills`、`awesome-video-skills`、`agentskillshub`、`skillleaderboard`。
>
> 星数是扫描时的快照，会随时间漂移；许可以及仓库状态也会变化。安装、试装或商用前，重新核对 LICENSE、README 与脚本。

这张表回答一个问题：社区里的视频 skill / 项目，哪些值得吸收，哪些只该读，哪些直接跳过。分层按“是否值得动代码”划分：

- **Tier S**：吸收方法，或在隔离环境试装做 A/B。
- **Tier A**：只读参考，把方法转写进本 skill，不装代码。
- **Tier B**：条件使用，只有明确需求出现时才评估。
- **Tier C**：跳过，不安装、不引用、不纳入路由。

## 同仓库的 skill

同仓库（当前未配置远程，发布时再定）里还有两个兄弟 skill。它们不是社区项目，选型时先分清边界：

| skill | 定位 | 怎么配合 |
|---|---|---|
| `hyperframes-video` | HyperFrames 中文讲解实战：本机安装、渲染流程与踩坑 | 互补。用到 HyperFrames 时先读它的 `SKILL.md` 与 `references/pitfalls.md`；它讲工具与本机坑，本 skill 讲导演、评审与交付 |
| `ui-polish` | 前端 UI 质感规范 | 与视频流程无直接重叠；只有做封面页、发布页或网页包装时才参考 |

本表不修改、也不依赖这两个 skill。

## Tier S：吸收方法或试装

| 项目 | 数据 | 许可 | 拿什么 | 结论 |
|---|---|---|---|---|
| `remotion-dev/skills` | 官方 12 件套（1 个路由 + 11 个子技能），约 5.1k★；本机已装 4.0.538 | 随 Remotion 生态分发；Remotion 本体为公司许可，个人免费，>3 人商用需授权 | 全部子技能与路由说明：create、markup、render、captions、studio、docs、multimedia、maps、interactivity、saas、upgrade | 已装，不重复安装；只补路由说明和项目适配 |
| `haidrrrry/claude-remotion-skill` | 621★；10 条动效铁律；render→inspect→fix 闭环 | MIT | 动效铁律与“渲染-检查-修复”闭环，整理进 `references/remotion-craft.md` | 吸收方法，不安装仓库 |
| `Vincentwei1021/anything2explainer` | 2.7k★；201 个文件；随仓库附一条 5 分钟、44 镜头的参考片 | PolyForm 非商业许可 | 中文字幕预算（每块约 16 字、44px 描边）、章节卡、`frame_metrics.py` QC、多 agent 并行构建 | 只吸收方法；不装代码，商用需取得授权或重写实现 |
| `Vincentwei1021/video-shotcraft` | 13.5k★；124–152 张 shot cards（数量随版本漂移），25 个 typography 镜头 | Apache-2.0 | 镜头词汇、typography 镜头、caption 与剪映导出思路 | 可试装或吸收；不整体替换现有引擎，无像素类内容 |
| `awesomezun/awesome-showreels` | MIT；88 个示例；6 种 pixel 风格 | MIT | beat grid、`verify_sync`、15/30/60s 多版本结构 | 试装做 A/B；作为 showreel 辅卡，不作主引擎 |
| `Agentchengfeng/chengfeng-video-styles` | Apache-2.0；16 种风格；17 个 3 秒样片 | Apache-2.0 | 皮影、像素典故、白板、漫画分格、时间线等风格卡与样片选型流程 | 吸收风格卡与选型流程；不整体替换现有风格库 |
| `bobobo2026/explainer-video` | 词级强制对齐；9 项 rubric（单项低于 2/5 不出片）；-14 LUFS；平台文案 | MIT | 词级对齐、rubric 门槛、响度与平台文案方法 | 方法吸收；画面模板不采用 |
| `lemomo-ai/lemo-opuscar` | 6.7k★；59 种片风分类法 | MIT | 片风分类法与角色驱动动画参考 | 吸收片风分类法，不安装仓库 |

## Tier A：只作参考

| 项目 | 数据 | 许可 | 拿什么 | 结论 |
|---|---|---|---|---|
| `nateherkai/hyperframes-student-kit` | 2.1k★；15 个 skills；12 个教学项目；406 张动效卡 | 分层许可：主体 MIT（Copyright 2026 Nate Herk，2026-04-18）+ `licenses/PIPELINE-USE-PERMISSION.txt`；HyperFrames 组件 Apache-2.0；AIS 品牌素材不随 MIT 授权 | `cut-silences`、`cut-mistakes`、EDL 审核、preflight、动效卡用法 | 只吸收方法。扫描时观察（2026-10-25）：仓库已更名为 `herk-edit-kit`，旧名 `hyperframes-student-kit` 仍可访问（GitHub 重定向）；发布前复核仓库名与许可，商用前逐层复核品牌素材 |
| `geekjourneyx/hyperframes-motion-director` | 467★；场景/矢量/动效 JSON 合同；QA 阶梯 | AGPL-3.0 | 场景、矢量、动效的 JSON 合同与 QA 阶梯概念 | 只吸收概念；AGPL 不装代码、不 vendor |
| `iart-ai/motion-skills` | 993★ | MIT | deliver-and-verify：冻帧、contact sheet、ffprobe 验收 | 只读；方法可写进交付验收脚本 |
| `iart-ai/javascript-animation-skills` | 33★ | MIT | JS 动画技法与可运行示例 | 只读参考，按需摘手法 |
| `gongnyang/awesome-ai-motion` | 637 种技法；128 条参考片；11 个 recipe | MIT | 技法索引与 recipe 分类 | 只读查询，当作选型索引 |
| `joeseesun/opus-video-prompts` | 734★；54 个案例；9 条技术路线 | 无明确许可（默认保留所有权利） | 案例结构与技术路线分类 | 只读参考；不复制提示词原文与素材 |
| `Barty-Bart/motion-graphics` | 832★ | MIT | 动效设计与排版参考 | 只读参考，按需借视觉语法 |

## Tier B：条件使用

| 项目 | 数据 | 许可 | 拿什么 | 结论 |
|---|---|---|---|---|
| `0xsline/OpenChatCut` | 2.5k★ | AGPL-3.0 | 真实素材剪辑、多轨时间线 | 条件使用：需要剪真实素材/多轨时间线时再评估；不装代码 |
| `ymybxx/SoloMCN` | 71★；pre-1.0 | MIT | 多平台发布适配器 | 只拆发布适配器；不整套安装，版本不稳 |
| `skulitom/pixelbolt-plugin` | JSON recipe 驱动的精灵动画 | MIT | JSON recipe 精灵动画 | 需要精灵动画时试装 |
| `NousResearch` pixel-art | 像素角色与表情资产 | 许可待查 | 色盘与背景特效 | 许可未知不装；不依赖多表情生成 |
| `0x0funky/agent-sprite-forge` | 游戏精灵资产管线 | MIT | 精灵与游戏资产管线 | 本项目暂不需要 |
| `diffusionstudio/lottie` | 5.6k★ | MIT | Lottie 播放/导出、AE 交接 | 需要 Lottie/AE 交接时使用 |
| `HyperFrames` | 43.8k★；seek(t) 架构 | Apache-2.0 | 整条 HyperFrames 流水线 | 替换不划算：与现有 seek(t) 同架构，无像素/CJK 代差；需要 HyperFrames 时走同仓库 `hyperframes-video` |
| `dashi-animationstyle` | 动画风格参考；工具链限 macOS | MIT | 风格与质感参考 | 条件使用；注意 macOS 平台限制 |
| `shreefentsar/remotion-video-toolkit` | Lambda 渲染、3D、charts | 许可未核实 | 无（未独立验证） | 未独立验证；需要时先审查再试装 |
| `jammaru/launch-video-craft` | 产品发布视频流程 | 许可未核实 | 无（未独立验证） | 未独立验证；需要时先审查再试装 |

## Tier C：跳过

| 项目 | 数据 | 许可 | 拿什么 | 结论 |
|---|---|---|---|---|
| `imMamdouhaboammar/motion-graphics-skills` | 动效技能合集 | Proprietary（all rights reserved） | 无 | 跳过；只看公开说明，不装代码 |
| `calesthio/OpenMontage` | AGPLv3；12 条流水线 | AGPL-3.0 | 无 | 跳过；过度工程，维护成本高于收益 |
| `nolangz/pixel2motion` | 实际是 logo 矢量化 | 许可未核实 | 无 | 跳过；会磨平像素，方向不符 |
| `SeeCut` | 未找到可靠仓库索引 | 未知 | 无 | 跳过；暂不纳入 |
| `ghost-editor` | 未找到可靠仓库索引 | 未知 | 无 | 跳过；暂不纳入 |
| `heygen-com/skills` | 以数字人 avatar 为主 | 许可未核实 | 无 | 跳过；avatar only，不产出代码画面 |
| `story-to-handdrawn-video` | 只有无声画面轨 | 许可未核实 | 无 | 跳过；缺音频/解说轨，不适合本流程 |

## 采用规则

1. **Tier S**：可吸收方法或试装。试装只在隔离目录做 A/B，通过后把结论写回本表；不把第三方仓库作为默认依赖。
2. **Tier A**：只读。方法转写进本 skill 的 `references/`，不克隆、不安装、不复制提示词原文与素材。
3. **Tier B**：条件使用。只有明确需求（真实素材剪辑、Lottie 交接、精灵管线等）出现时才评估，先隔离审查。
4. **Tier C**：跳过。不安装、不引用、不纳入任何路由。

安全与许可红线：

- Proprietary / 非商业 / AGPL 项目一律只吸收方法，不安装代码、不 vendor、不二次分发。
- 只有 MIT / Apache-2.0 才考虑试装；试装前把仓库克隆到隔离目录，先读 `install` / `postinstall`、网络请求、文件写入和权限声明，依赖安装使用 `--ignore-scripts`。
- 任何社区 skill 不得读取 `~/code/docs/api.md` 或其它含真实 API Key 的文件；不要把 Key 写进提示词、配置或日志。
- Remotion 本体是公司许可：个人使用免费，>3 人商用需授权；安装技能包不等于获得商业授权。
- 星数与许可均为 2026-10-25 快照；新增项目或准备商用前重新核对，发现变化就更新本表。
