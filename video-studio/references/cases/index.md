# 案例卡索引

选 0–2 张：1 张主卡定结构，1 张辅卡定一个可迁移手法。写进项目 `docs/REFERENCES.md`。

| 卡片 | 来源 | 什么时候用 | 风格映射 | 层级 |
|---|---|---|---|---|
| case-opus-meta | 黑底 HUD 元叙事 | 讲创作过程/方法/幕后 | 01-black-hud-meta | S |
| case-ultraman-pixel | 像素二创 | 像素角色 + 字幕驱动搞笑 | 08-pixel-arcade、16-pixel-jrpg | S |
| case-ag-pokemon | AG v5 | 原声驱动 + 像素二创 | 08-pixel-arcade、12-comic-pop | S |
| case-xuanjian-tutorial | 悬剑教程 | 需要评分标准和评审闭环 | 通用 | S |
| case-leaderai-tutorial | LeaderAI 教程 | 需要完整技术栈/成本参考 | 通用 | A |
| case-chengfeng-styles | 成峰 16 风格 | 需要中文风格选型 | 16–21 | S |
| case-opus-prompts | 54 案例 | 需要找技术路线/案例 | 通用 | A |
| case-awesome-showreels | 像素 showreel | 需要 beat sync/多版本 | 08/16/17/18 | S |
| case-bobobo-explainer | 中文科普 | 需要词级对齐/rubric | 20-whiteboard-handdrawn | S |
| case-anything2explainer | 中文讲解 | 需要中文字幕预算/QC | 01/20 | S |
| case-video-shotcraft | 产品镜头卡 | 需要镜头/typography 词汇 | 01/05/13 | A |
| case-hyperframes-student-kit | 口播剪辑 | 需要 transcript cuts/EDL | 通用 | A |
| case-remotion-official | Remotion 12 件套 | 需要 React 视频 | 通用 | S |

## 使用规则

- 主卡只借结构和节奏；辅卡只借 1–2 个手法。
- 不逐句复制案例文案；不把专有/非商业项目的提示词原文搬进来。
- 借用的元素和偏离原因必须写进 `docs/REFERENCES.md`。
- 案例卡里的时间轴是近似值；制作前用 `teardown_reference.py` 复核。
- 本地案例卡的媒体路径只作核对用；渲染时不要直接引用他人素材，除非项目已确认授权。
