# 风格模板库（21 种）

选择依据是**表达目的**，不是“哪个看起来酷”。每个风格都给出参考帧/参考案例卡、引擎、视觉要素、动效词汇和失败模式。

---

## 01 · black-hud-meta · 黑底 HUD 元叙事

- **氛围**：近黑底、橙色发光画框、常驻时间码/帧号 HUD，像“制作过程本身被拍成了片子”。
- **适合**：讲创作过程、工具、方法、幕后；也可承载产品故事。
- **画幅**：16:9 优先，竖屏需重排 HUD。
- **引擎**：motion-design / Remotion。
- **参考帧**：`/home/chen/code/video/samples/references/opus-ref-85s.jpg`
- **本地示例**：`/home/chen/code/video/examples/starter-demo/src/film.html`（10 秒校准片，已过 critic 评审）
- **视觉要素**：`#0b0b0c` 底、`#ff6a2a` 橙、白色大字、等宽字体 HUD、圆角发光框、代码绘制的插画场景、小方块角色。
- **动效**：字符逐个出现、光标闪烁、画框内缓慢推拉、场景之间的硬切/闪白、帧号连续跳动。
- **失败模式**：HUD 抢戏、插画太满、橙色用成大面积底色、每个场景都加粒子。
- **提示词开头**：`黑底 #0b0b0c，橙色 #ff6a2a 强调。常驻左上作者、顶部中间一句问题、右上“第 N 帧 / 共 M 帧”。插画必须由 SVG/Canvas 代码绘制，不要用位图素材。`

---

## 02 · isometric-clean · 等距 3D 数据城市

- **氛围**：干净的等距视角，数据/流程变成可漫步的城市、格子、管道。
- **适合**：系统原理、工作流、产品架构、增长数据。
- **画幅**：16:9 / 1:1。
- **引擎**：kinetic-reel（Three.js）或 CSS 3D。
- **参考**：教程 `prompts/03-isometric.md` 的 10 秒短片。
- **视觉要素**：30° 等距网格、低饱和底色、单一高饱和强调色、柔和长阴影、细线标注。
- **动效**：镜头沿网格平移、模块从地面“长”出来、数据沿管道流动、焦点模块轻微抬起。
- **失败模式**：等距角度不统一、阴影方向混乱、颜色超过 3 种、模块像乐高堆叠。
- **提示词开头**：`isometric 3D diagram, 30-degree axonometric grid, muted base with one accent color, soft long shadows, clean thin annotations, no perspective distortion.`

---

## 03 · p5r-mad · 高饱和漫画 MAD

- **氛围**：Persona 5 Royal 式的红黑碰撞、漫画分镜、贴纸、速度线、卡点狂潮。
- **适合**：音乐、游戏、态度表达、二创 MAD。
- **画幅**：16:9 / 9:16。
- **引擎**：kinetic-reel / p5.js。
- **视觉要素**：红 `#e60012`、黑、白、荧光黄；粗描边；网点；斜切构图；角色剪影。
- **动效**：每拍一次硬切、贴纸弹入、速度线扫过、文字错位抖动、镜头急推。
- **失败模式**：所有元素一起动、没有节拍层级、红色铺满、贴纸挡住主体。
- **提示词开头**：`Persona 5 Royal-inspired MAD, high-contrast red/black/white, comic panels, halftone dots, speed lines, sticker cutouts, every cut lands on the beat.`

---

## 04 · paper-ink · 纸墨手账

- **氛围**：纸张纹理、墨线、手写标注、老师傅在笔记本上推演。
- **适合**：数学、物理、历史、方法论、慢节奏解释。
- **画幅**：16:9 / 4:3。
- **引擎**：math-concept-film（Manim）或 motion-design。
- **视觉要素**：米白纸底、墨黑、朱红批注、手绘箭头、纸张边缘阴影。
- **动效**：线条逐笔画出、公式逐项展开、镜头推近局部、批注盖章。
- **失败模式**：字体太现代、线条太直、页面太满、没有留白。
- **提示词开头**：`paper-and-ink explainer, warm off-white paper, hand-drawn ink lines, vermilion annotations, slow push-ins, generous margins.`

---

## 05 · kinetic-type · 大字排版

- **氛围**：瑞士/编辑设计式的强烈字阶，黑白或荧光色，HUD 微字。
- **适合**：观点、金句、产品卖点、showreel 片头。
- **画幅**：16:9 / 9:16。
- **引擎**：kinetic-reel。
- **参考帧**：`/home/chen/code/video/samples/final/kinetic-reel-sheet.jpg`
- **视觉要素**：超粗无衬线、紧凑字距、网格线、编号、微小的等宽注释。
- **动效**：整词位移、遮罩上升、字重/字宽变化、硬切、数字滚动。
- **失败模式**：字不够大、行距太松、每个词都做弹簧、颜色太多。
- **提示词开头**：`editorial kinetic typography, oversized condensed sans, tight tracking, grid lines, monospace micro-labels, hard cuts on the beat.`

---

## 06 · product-ui · 产品落地页

- **氛围**：干净的 SaaS 落地页，卡片、光标、弹簧、玻璃拟态。
- **适合**：软件产品、功能发布、工具演示。
- **画幅**：16:9 / 4:5 / 9:16。
- **引擎**：motion-design。
- **参考帧**：`/home/chen/code/video/samples/final/motion-design-sheet.png`
- **视觉要素**：暖白底、深墨字、单一品牌色、圆角卡片、真实 UI 组件、macOS 光标。
- **动效**：卡片依次浮入、光标点击、开关切换、内容 morph、页面滚动。
- **失败模式**：假 UI、占位方块、太多阴影、光标乱飞。
- **提示词开头**：`premium SaaS product film, warm off-white, real UI components, macOS cursor, spring-based micro-interactions, no fake placeholder blocks.`

---

## 07 · hand-painted · 水彩手绘

- **氛围**：水彩晕染、墨线“沸腾”、手绘角色，像一本会动的绘本。
- **适合**：故事、情绪、儿童、歌词、品牌温度。
- **画幅**：16:9 / 9:16。
- **引擎**：painted-animation。
- **参考帧**：`/home/chen/code/video/samples/final/painted-animation-sheet.jpg`
- **视觉要素**：水彩纸纹理、有限色盘、墨线抖动、角色大而简单、留白。
- **动效**：逐帧手绘（boiling lines）、角色表演、镜头缓慢横移、场景淡入。
- **失败模式**：线条太干净、颜色太 digital、角色太小、背景比角色抢。
- **提示词开头**：`hand-painted watercolor and ink, paper texture, boiling lines, limited palette, big simple character, generous negative space.`

---

## 08 · pixel-arcade · 像素街机

- **氛围**：低分辨率画布、整数倍放大、关掉平滑，8-bit/16-bit 游戏感。
- **适合**：游戏、怀旧、技术梗、轻量科普。
- **画幅**：16:9 / 1:1。
- **引擎**：motion-design（Canvas，`image-rendering: pixelated`）。
- **视觉要素**：320×180 或 480×270 逻辑画布、16 色盘、像素字体、硬边。
- **动效**：逐帧精灵动画、镜头按整像素移动、调色板闪烁、扫描线。
- **失败模式**：非整数缩放导致糊、抗锯齿、超过 16 色、字体不是像素字。
- **提示词开头**：`pixel art, 320x180 logical canvas, integer scaling, image-rendering: pixelated, 16-color palette, no antialiasing.`

---

## 09 · crt-shader · 老电视 / CRT

- **氛围**：扫描线、色差、噪点、弯曲屏幕，像从旧电视里播出来。
- **适合**：怀旧、恐怖、赛博、音乐视觉。
- **画幅**：16:9 / 4:3。
- **引擎**：motion-design（WebGL/GLSL）。
- **视觉要素**：扫描线、RGB 分离、暗角、噪点、屏幕曲率、色温偏绿/偏蓝。
- **动效**：信号切换、雪花、画面滚动、突然故障（glitch）。
- **失败模式**：shader 太重导致文字不可读、每帧都 glitch、色差过度。
- **提示词开头**：`CRT television shader: scanlines, RGB split, vignette, grain, slight screen curvature, occasional signal glitch. Keep text readable.`

---

## 10 · dark-tech-console · 深色科技控制台

- **氛围**：粒子仪器台、玻璃面板、数据流、深色 HUD。
- **适合**：技术讲解、自动化流程、工具实测、AI 产品。
- **画幅**：16:9 / 9:16。
- **引擎**：kinetic-reel / adu-motion-video。
- **参考帧**：`/home/chen/code/video/samples/final/adu-demo-frame.jpg`
- **视觉要素**：`#0a0e14` 底、青色/蓝色发光、玻璃卡片、细网格、等宽数字。
- **动效**：数据流滚动、面板展开、连接线激活、扫描高亮。
- **失败模式**：发光过曝、面板太多、数据是假的却不标注。
- **提示词开头**：`dark tech console, near-black base, cyan accents, glass panels, thin grid, monospace data, restrained glow.`

---

## 11 · vox-collage · 纸片拼贴解释

- **氛围**：Vox 风格的纸片、地图、箭头、档案照片拼贴。
- **适合**：新闻解释、历史、社会议题、复杂背景。
- **画幅**：16:9。
- **引擎**：motion-design（HTML/CSS/SVG）。
- **视觉要素**：米色纸底、剪贴照片、粗箭头、手写标注、地图。
- **动效**：纸片滑入、镜头推近地图、箭头逐段画出、档案照片盖章。
- **失败模式**：照片版权、纸片太多、箭头指错、信息密度过高。
- **提示词开头**：`Vox-style paper collage explainer, cream paper, cut-out photos, thick arrows, hand-drawn annotations, map push-ins.`

---

## 12 · comic-pop · 美漫波普

- **氛围**：粗描边、网点、拟声词、贴纸、波普色块。
- **适合**：年轻向、娱乐、态度表达、教程。
- **画幅**：16:9 / 9:16。
- **引擎**：p5.js / motion-design。
- **视觉要素**：黑粗边、红黄蓝、网点、爆炸形、拟声词。
- **动效**：贴纸弹入、拟声词放大、分格切换、速度线。
- **失败模式**：颜色过饱和、网点太密、拟声词乱入。
- **提示词开头**：`American comic pop art, thick black outlines, halftone dots, primary colors, onomatopoeia, sticker cutouts.`

---

## 13 · swiss-minimal · 瑞士网格

- **氛围**：严格网格、无衬线、红黑白、精确到像素的排版。
- **适合**：设计、建筑、品牌、高端观点。
- **画幅**：16:9 / 1:1。
- **引擎**：motion-design。
- **视觉要素**：12 栏网格、Helvetica/Inter、红 `#e30613`、黑、白、大量留白。
- **动效**：元素按网格对齐、数字/日期滚动、极简淡入、硬切。
- **失败模式**：网格不严格、字体不统一、加了多余装饰。
- **提示词开头**：`Swiss International Style, strict 12-column grid, Helvetica-like sans, red/black/white, precise alignment, generous whitespace.`

---

## 14 · 3d-showcase · 多屏 3D 展陈

- **氛围**：暗色舞台、立体窗口、多屏比较、镜头推进。
- **适合**：产品演示、作品集、软件评测、成果比较。
- **画幅**：16:9 / 9:16。
- **引擎**：kinetic-reel（Three.js）。
- **视觉要素**：暗色环境、发光边框、3D 屏幕、反射地面、景深。
- **动效**：镜头推进、屏幕旋转、多个窗口并排、重点放大。
- **失败模式**：模型太糙、光照不一致、反射过强、镜头晕。
- **提示词开头**：`dark 3D showcase, multiple floating screens, soft reflections, cinematic dolly-in, shallow depth of field, restrained rim light.`

---

## 15 · lyric-karaoke · 歌词卡拉 OK

- **氛围**：歌词逐字高亮、卡点、手绘或霓虹，情绪优先。
- **适合**：音乐 MV、歌词视频、品牌情绪片。
- **画幅**：16:9 / 9:16。
- **引擎**：painted-animation / kinetic-reel。
- **视觉要素**：大字歌词、逐字高亮、节拍脉冲、角色/场景随歌词变化。
- **动效**：逐字 karaoke、镜头随鼓点、场景切换卡拍、尾音拖长。
- **失败模式**：字太小、高亮不准、每句都换场景、音乐被音效盖住。
- **提示词开头**：`karaoke lyric video, one line at a time, word-by-word highlight locked to the vocal, scene changes on bar lines, restrained SFX.`

---

## 快速选择表

| 你要讲什么 | 首选 | 备选 |
|---|---|---|
| 创作过程 / 工具 / 方法 | 01 black-hud-meta | 05 kinetic-type |
| 系统 / 流程 / 架构 | 02 isometric-clean | 10 dark-tech-console |
| 音乐 / 游戏 / 态度 | 03 p5r-mad | 15 lyric-karaoke |
| 数学 / 原理 / 历史 | 04 paper-ink | 11 vox-collage |
| 观点 / 金句 / 卖点 | 05 kinetic-type | 13 swiss-minimal |
| 软件产品 / 功能 | 06 product-ui | 14 3d-showcase |
| 故事 / 情绪 / 儿童 | 07 hand-painted | 12 comic-pop |
| 怀旧 / 赛博 / 故障 | 09 crt-shader | 08 pixel-arcade |
| 新闻 / 社会 / 复杂背景 | 11 vox-collage | 04 paper-ink |
| 高端 / 设计 / 品牌 | 13 swiss-minimal | 14 3d-showcase |
| 角色对话 / 吐槽 / 游戏梗 | 16 pixel-jrpg | 08 pixel-arcade |
| 动作 / 闯关 / 成长进度 | 17 pixel-platformer | 08 pixel-arcade |
| 流程 / 系统 / 生活流 | 18 pixel-isometric | 02 isometric-clean |
| 故事 / 民俗 / 品牌温度 | 19 paper-puppet | 07 hand-painted |
| 知识讲解 / 口播 / 教程 | 20 whiteboard-handdrawn | 04 paper-ink |
| 吐槽 / 对比 / 梗图 | 21 comic-panel | 12 comic-pop |

---

## 16 · pixel-jrpg · 16-bit JRPG

- **氛围**：16-bit JRPG 对话框、头像、遇敌闪白、格子地图，像从 GBA 卡带里截出来。
- **适合**：角色对话、吐槽、游戏梗、轻剧情。
- **画幅**：16:9 / 9:16。
- **引擎**：motion-design（seek(t)）。
- **参考案例卡**：`references/cases/case-ultraman-pixel.md`。
- **视觉要素**：16–24 色、3px 描边、像素字、对话框占下 1/3、头像 32×32。
- **动效**：文字逐字、头像眨眼、遇敌闪白 2 帧、角色 2 帧 idle。
- **失败模式**：精灵比例不一致、现代字体混入、对话框遮住关键动作、颜色超限。
- **提示词开头**：`16-bit JRPG, 384x216 logical canvas, integer scaling, limited 24-color palette, 3px outlines, pixel font, bottom dialogue box, no antialiasing.`

---

## 17 · pixel-platformer · 横版平台

- **氛围**：横版卷轴、视差背景、跳跃/落地 squash、金币/分数，像街机平台游戏。
- **适合**：动作、闯关、进度/成长叙事、轻科普。
- **画幅**：16:9 / 9:16。
- **引擎**：motion-design（seek(t)）。
- **参考案例卡**：`references/cases/case-awesome-showreels.md`。
- **视觉要素**：16 色、2–3 层视差、32×32 tile、硬边、像素字 HUD。
- **动效**：跳跃 squash/stretch、落地尘土、金币旋转、镜头按整像素滚动。
- **失败模式**：非整数滚动、运动模糊、跳跃没有重量、背景比前景抢眼。
- **提示词开头**：`16-bit side-scrolling platformer, 2-3 parallax layers, 32x32 tiles, integer camera scroll, squash-and-stretch jump, limited palette, no blur.`

---

## 18 · pixel-isometric · 等距像素

- **氛围**：2:1 等距像素小店/流程/城市，暖色、低饱和、可漫步。
- **适合**：流程、系统、产品结构、生活流。
- **画幅**：16:9 / 1:1。
- **引擎**：kinetic-reel（seek(t)）。
- **参考案例卡**：`references/cases/case-awesome-showreels.md`。
- **视觉要素**：2:1 等距网格、32×16 tile、低饱和底 + 单一强调色、细描边。
- **动效**：镜头沿网格平移、模块从地面长出、角色沿路径走、环境 1px idle。
- **失败模式**：等距角度错误、颜色超限、模块像贴纸、阴影方向混乱。
- **提示词开头**：`isometric pixel art, 2:1 grid, 32x16 tiles, muted palette with one accent, clean outlines, ambient idle, no perspective distortion.`

---

## 19 · paper-puppet · 皮影/纸偶

- **氛围**：关节纸偶、暖光幕布、投影、手工纸材质，像皮影戏或纸偶动画。
- **适合**：故事、民俗、观点表达、品牌温度片。
- **画幅**：16:9 / 9:16。
- **引擎**：motion-design / Remotion。
- **参考案例卡**：`references/cases/case-chengfeng-styles.md`。
- **视觉要素**：纸质纹理、关节分层、暖黄背光、幕布暗角、投影偏移。
- **动效**：关节摆动、纸片轻微抖动、光源缓慢移动、转场用“换幕”。
- **失败模式**：关节僵硬、没有投影、材质过平、光太冷。
- **提示词开头**：`paper puppet theatre, jointed cutout limbs, warm backlight, soft shadow, paper texture, slight hand-made jitter, stage vignette.`

---

## 20 · whiteboard-handdrawn · 白板手绘

- **氛围**：白板/纸张、马克笔逐笔、口播讲解、草图感。
- **适合**：知识讲解、口播、教程、观点拆解。
- **画幅**：16:9 / 9:16。
- **引擎**：motion-design / painted-animation。
- **参考案例卡**：`references/cases/case-bobobo-explainer.md`、`references/cases/case-anything2explainer.md`。
- **视觉要素**：暖白纸、深蓝/黑色笔、橙色强调、手写字体、留白。
- **动效**：逐笔绘制、笔尖跟随、擦除、圈重点、箭头。
- **失败模式**：画得太快、文字不可读、线条抖动过头、画面太满。
- **提示词开头**：`whiteboard hand-drawn explainer, warm white paper, dark blue marker, orange accent, stroke-by-stroke drawing, generous whitespace, legible handwriting.`

---

## 21 · comic-panel · 漫画分格

- **氛围**：漫画分格、速度线、拟声词、定格大字、波普色。
- **适合**：吐槽、对比、冲突、梗图、二创。
- **画幅**：16:9 / 9:16。
- **引擎**：motion-design / kinetic-reel。
- **参考案例卡**：`references/cases/case-ultraman-pixel.md`、`references/cases/case-chengfeng-styles.md`。
- **视觉要素**：2–6 格、粗黑边框、速度线、拟声词、半调网点、高饱和强调色。
- **动效**：分格进入、定格大字、速度线扫过、拟声词弹入、画面抖动。
- **失败模式**：分格过满、线宽不统一、拟声词抢戏、颜色超过 3 种主色。
- **提示词开头**：`comic panel layout, 2-6 panels, bold black borders, speed lines, onomatopoeia, halftone dots, one high-saturation accent, freeze-frame impact.`
