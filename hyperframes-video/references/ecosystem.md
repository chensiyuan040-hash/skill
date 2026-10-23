# 开源生态与外部工具清单

2026-10 调研沉淀。总入口:[awesome-video-agent-skills](https://github.com/tentenco/awesome-video-agent-skills)(Tenten AI,"能直接交给 coding agent 跑产片"才收录,含完整产线架构图)。

## HyperFrames 官方隐藏能力(本机 CLI 已验证存在)

- `hyperframes capture --video` —— 官方 "Recreate any video 1:1":把成片视频逆向成可编辑组件(video-manifest.json 模式)。学参考视频动效的杀器,不用手动逐帧拆
- `hyperframes snapshot` —— 关键帧 PNG 出图。两个用途:①渲染后视觉自检;②**封面图直接用它出**,不用另开设计工具
- [官方 Examples 页](https://hyperframes.heygen.com/examples) —— 成片分类看(产品片/kinetic type/beat-synced cuts/VFX/music-to-video),配 hyperframes.dev 社区的 publish/remix
- Registry blocks(~400 个):现成动效块先搜再手写,`hyperframes catalog` 查

## 同赛道开源 skill(直接对比学习配方)

- **hyperframes-motion-director**(geekjourneyx)—— 中文优先 HyperFrames 导演 skill,文章/官网/README→动效片,与本项目同定位
- **hyperframes-student-kit** —— 12 个完整 HyperFrames+GSAP 教学工程,解决"画面 PPT 感/不够灵动"最直接的路:抄现成动效写法
- **claude-video** `/watch`(bradautomates) —— 自动下载→抽帧→转写→拆解 Hook/视觉节奏/字幕排版→成片 QC;手动 ffprobe 场景切分的全自动化版
- **video-shotcraft**(~5.6k★) —— 152 张镜头配方卡 + 209 段 motion 预览 + 2.5D 运镜,可导剪映草稿

## 交付打通

- **pyJianYingDraft** —— Python 生成剪映原生草稿工程(轨道/特效/关键帧/贴纸)。用户用剪映精修配音时,agent 可直接产出剪映工程,打通最后一公里
- **VideoCaptioner** —— 中文字幕产线常用件

## 配音升级(edge-tts 之外)

- **Index-TTS**(B 站开源)—— 零样本音色克隆 + **拼音纠音**(专治 AI 读错中文名/专有名词),8G 显卡可跑,有整合包;中文旁白的开源首选
- **GPT-SoVITS** —— 老牌开源 TTS,少样本微调音色

## Prompt 素材库

- **lanshu-awesome-ai-video-kit** —— 500+ 实测 prompt,跨 15 模型,每周 CI 校验
- **AI_Animation**(Unclecheng-li)—— AI 生成炫酷 HTML 动画的 prompt 合集,持续更新

## 方法论(产线共识)

- **视觉自检迭代闭环**:生成 HTML → 渲染 → 抽帧视觉分析 → 提改进 → 再渲染。agent 做视频的标配循环,frame_audit.py + snapshot 是本机版
- **按"职位"分工**:拆解编剧 → 生成运镜 → 确定性成片 → 配音字幕,不同阶段不同 skill,而非一个大 prompt 全包
- **先锁叙事再调画面**:参考作者们(含抖音范本)的流程一致——写完代码才第一次看成片,人只当第一个观众

## 框架选型(为什么留 HyperFrames)

| 框架 | 定位 | 备注 |
|------|------|------|
| Remotion(~25k★) | React,数据驱动批量产片 | source-available,**公司用需商业授权** |
| Motion Canvas | TS,手作精排动画 | 全开源 |
| Revideo | MC 的开源分支 | 程序化渲染取向 |
| Manim | Python 数学动画 | 科普向,3Blue1Brown 同款 |
| HyperFrames | agent 原生,HTML 零失真 | 无扩散失真、skill 生态最全,**本项目所用** |
