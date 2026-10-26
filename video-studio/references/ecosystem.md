# 开源生态与外部工具清单

2026-10-26 更新(并入 10-23 版;新增 347 仓全景、16-skill 同题实测、弱模型配方区)。两个总入口:

- [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills)(zhuyansen,347 仓、按类型分、安全分级 SAFE/CAUTION、在线筛选页,10-25 生成,**当前最全**)
- [awesome-video-agent-skills](https://github.com/tentenco/awesome-video-agent-skills)(Tenten AI,"能直接交给 coding agent 跑产片"才收录,含完整产线架构图)

## 16-skill 同题实测(2026-10-11,awesome list 作者)

同一 15s brief、同机跑 16 个 skill 的硬数据:

| skill | 结果 | 耗时 |
|-------|------|------|
| explainroo | 🥇 成片带声音 | 2.0 min |
| Remotion 官方 skill | 🥉 稳定可靠 | 4.5 min |
| onetake | 连续无切换叙事 | 8.5 min |
| **hyperframes** | 能出但**最慢** | **23.5 min** |
| 裸 agent 不装 skill | 4/4 检查全过 | 4.4 min |

- 结论引用:**"skill 的价值在于风格、流程和可剪素材,而不是能不能出片"**——本仓两个 skill(video-director-custom 管流程纪律、hyperframes-video 管引擎坑)恰好落在价值层
- HyperFrames 慢是已知代价(本机 365s@1080p 约 9-10 分钟),质量优先才值得;快糙活考虑 html-video/Remotion 路线

## 同赛道中文讲解视频 skill

- **hbg-douyin-code-explainer-video**(Mr-funny)—— 同 HyperFrames 底座、中文 9:16、确定性流水线,与本仓定位最接近的竞品;其音频原则与最终 MP4 质检法已吸收进本 skill(voice-pipeline.md 末节、hyperframes-pitfalls#12-13)
- **dashi-animationstyle**(chuspeeism)—— 中文知识口播 → 7 种画风讲解动画,HTML/Canvas 逐帧
- **ai-self-media-video-packaging-skill** —— Remotion 口播包装 + 线稿插画 + seek-safe 动效
- **docvideoer** —— 文档 URL/MD → 中文旁白 Remotion 讲解片
- **hand-drawn-explainer-video-nikola**(428★)—— 中文手绘知识讲解
- **hyperframes-motion-director**(geekjourneyx)—— 中文优先 HyperFrames 导演 skill,文章/官网/README→动效片
- **hyperframes-student-kit** —— 12 个完整 HyperFrames+GSAP 教学工程,解决"画面 PPT 感"最直接的路:抄现成动效写法
- **claude-video** `/watch`(bradautomates)—— 自动下载→抽帧→转写→拆解 Hook/视觉节奏/字幕排版→成片 QC
- **video-shotcraft**(~5.6k★)—— 152 张镜头配方卡 + 209 段 motion 预览 + 2.5D 运镜,可导剪映草稿
- **MathLens** —— Manim 数学题讲解

## 弱模型配方区(DeepSeek 等非旗舰/无多模态)

- **deepseek-opus-motion-skill**(8533502-dev)—— 目标就是"让 DeepSeek 用 Opus 级提示词做出接近的 Remotion 动效"
- **promo-video-skill / BrewReel**(Finderchangchang)—— 明确"让便宜模型也能做好看的竖版宣传片"
- **video-shotcraft-dsh**(kingselyjoe)—— 镜头配方卡的 DeepSeek Harness 版
- **cheap-claude-video**(JuneYaooo)—— Claude 出片一次 → 蒸馏成视频配方 → 其他模型按配方复刻(**配方蒸馏方法论**)
- **xiaoma-studio** —— 30 条高赞视频拆解出的工作流,模型无关
- 实践共识:弱模型出片靠 ①确定性脚本扛质检(verify_delivery/frame_audit 这层)②配方卡+风格库收敛生成空间(video-director-custom 的 21 风格库同理)③文字层检查替代视觉判断

## HyperFrames 官方隐藏能力(本机 CLI 已验证存在)

- `hyperframes capture --video` —— 官方 "Recreate any video 1:1":把成片视频逆向成可编辑组件(video-manifest.json 模式)。学参考视频动效的杀器,不用手动逐帧拆
- `hyperframes snapshot` —— 关键帧 PNG 出图。两个用途:①渲染后视觉自检;②**封面图直接用它出**,不用另开设计工具
- [官方 Examples 页](https://hyperframes.heygen.com/examples) —— 成片分类看(产品片/kinetic type/beat-synced cuts/VFX/music-to-video),配 hyperframes.dev 社区的 publish/remix
- Registry blocks(~400 个):现成动效块先搜再手写,`hyperframes catalog` 查

## 交付打通与剪辑生态

- **pyJianYingDraft** —— Python 生成剪映原生草稿工程(轨道/特效/关键帧/贴纸),剪映精修最后一公里
- **VideoCaptioner** —— 中文字幕产线常用件
- 剪辑向新势力:FireRed-OpenStoryline(3.6k★,长视频剪辑决策)、chengfeng-videocut-skills(3.1k★)、OpenChatCut(2.7k★)、Premiere Pro MCP(755★)——素材粗剪/长视频剪辑方向,与讲解视频产线互补

## 配音升级(edge-tts 之外)

- **Index-TTS**(B 站开源)—— 零样本音色克隆 + **拼音纠音**(专治 AI 读错中文名/专有名词),8G 显卡可跑;中文旁白的开源首选
- **GPT-SoVITS** —— 老牌开源 TTS,少样本微调音色
- **Kokoro**(explainroo 采用)—— 本地轻量语音 + Whisper 词级时间轴;video-director-custom 的 transcribe_words.py 同思路

## 大产能产线(批量化参考)

- **OpenMontage**(71.8k★)—— agentic 视频产线:12 条 pipeline、100+ 工具、700+ skill 文件
- **hypit**(25.5k★)—— 爆款视频复刻
- **lottie-mcp / diffusionstudio 系**(5.6k★)—— After Effects/Lottie 路线

## Prompt 素材库

- **lanshu-awesome-ai-video-kit** —— 500+ 实测 prompt,跨 15 模型,每周 CI 校验
- **AI_Animation**(Unclecheng-li)—— AI 生成炫酷 HTML 动画的 prompt 合集,持续更新

## 方法论(产线共识)

- **视觉自检迭代闭环**:生成 HTML → 渲染 → 抽帧视觉分析 → 提改进 → 再渲染。agent 做视频的标配循环,frame_audit.py + snapshot 是本机版
- **最终 MP4 才算交付物**:质检从编码后的 MP4 抽帧,浏览器源帧/预览不算数(hbg 教训,见 hyperframes-pitfalls#13)
- **按"职位"分工**:拆解编剧 → 生成运镜 → 确定性成片 → 配音字幕,不同阶段不同 skill,而非一个大 prompt 全包
- **先锁叙事再调画面**:参考作者们(含抖音范本)的流程一致——写完代码才第一次看成片,人只当第一个观众

## 框架选型(HyperFrames 为默认,不锁死)

| 框架 | 定位 | 备注 |
|------|------|------|
| HyperFrames(71.8k★) | agent 原生,HTML 零失真 | 无扩散失真、skill 生态最全,**本项目所用**;同题实测最慢 |
| [nexu-io/html-video](https://github.com/nexu-io/html-video)(4.7k★) | HTML→MP4 | 可插拔渲染引擎 + 21 模板,轻量备选 |
| Remotion(~25k★) | React,数据驱动批量产片 | 官方 skill 5.7k★(2026-01 起);source-available,**公司用需商业授权** |
| OpenMontage(71.8k★) | agentic 产线系统 | 见"大产能产线" |
| Motion Canvas | TS,手作精排动画 | 全开源 |
| Revideo | MC 的开源分支 | 程序化渲染取向 |
| Manim | Python 数学动画 | 科普向,3Blue1Brown 同款 |

## 安全分级提醒

Agent Skills Hub 对社区 skill 的 README/安装步骤做 SAFE/CAUTION 分级,装前看一眼;部分含系统改动的 skill(如 hermes-video-editing)被标 CAUTION。
