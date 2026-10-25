# Remotion 工艺卡

> 用途：确定什么时候该用 Remotion、动效按什么标准做、遇到具体问题查哪个官方子技能。
>
> 来源：10 条铁律整理自 `haidrrrry/claude-remotion-skill`（MIT，扫描快照 2026-10-25）；官方技能路由对应本机已装的 `remotion-best-practices` 4.0.538（1 个路由 + 11 个子技能，共 12 件套）。本文是项目内的工艺约束，API 细节仍以官方子技能为准。

## 1. 何时用 Remotion，何时用 seek(t)

两种引擎都能出 MP4，区别在“画面由谁决定”：

| 维度 | Remotion | seek(t)（本项目 HTML/Canvas 引擎） |
|---|---|---|
| 画面构成 | React 组件、DOM、CSS、SVG | Canvas / WebGL / p5.js / 手写 DOM |
| 最适合 | UI 演示、产品界面、数据面板、地图、复杂字幕、组件复用 | 像素画、粒子、着色器、手绘、逐帧确定性强的视觉 |
| 时间模型 | 帧驱动，`useCurrentFrame()` + `fps` | 纯函数 `seek(t)`，任意时刻可重放 |
| 迭代方式 | `remotion studio` 实时预览、拖动时间轴 | 改 HTML 后重新截帧 |
| 依赖 | Node + React + Remotion 工程 | 一个 HTML 文件 + Playwright/FFmpeg |
| 风险 | 依赖体积、许可、字体加载 | 复杂 UI 布局和字幕排版要自己写 |

选择规则：

- 需要 **React 组件生态、UI 级排版、地图、词级字幕**，或团队本来就写 React/TypeScript → 用 Remotion。
- 需要 **像素级确定性、Canvas/WebGL/p5.js、单文件交付、已有 seek(t) 工程** → 继续用 seek(t)，不要为了统一技术栈重写。
- 同一支片可以混用：Remotion 渲染透明背景的 UI 段落，再交给 FFmpeg 与 seek(t) 段落合成。合成前统一分辨率、fps、色彩空间与 alpha 处理方式。
- 只做静态封面、纯文字卡、简单转场时，两者都过度；先用模板或 FFmpeg 解决。

进入 Remotion 路线后，先读官方路由 `remotion-best-practices`，只加载当前任务需要的子技能，不要一次读完 11 个。

## 2. 十条动效铁律

这 10 条是出片质量底线。critic 评审时逐条对照；违反 3 条以上直接退回。

### 2.1 用 spring / bezier，不用线性插值

线性 `interpolate(frame, [0, 20], [0, 1])` 会让画面像机器在推。入场优先 `spring()`，需要精确曲线时用 `Easing.bezier()`；所有会影响透明度、位置、裁切的插值都要 `clamp`，避免 spring 过冲把元素顶出画外或产生负透明度。

```tsx
const progress = spring({
  frame: frame - delay,
  fps,
  config: { damping: 18, stiffness: 120, mass: 0.8 },
});
const opacity = interpolate(progress, [0, 1], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

### 2.2 入场同时动 2–3 个属性

单个 opacity 淡入像 PPT。一次入场至少组合 2–3 个属性：透明度 + 位移 + 缩放，或透明度 + 模糊 + 旋转。不要超过 3 个，属性越多越像廉价模板；主次仍要有一个主导属性。

### 2.3 入场 stagger

多个元素不要同一帧全部出现。按索引错开，间隔从 `fps` 推导（例如 2–4 帧或 0.06–0.12 秒），让视线有落点。stagger 只用于同一组元素；跨场景的节奏由分镜决定。

```tsx
const delay = index * Math.round(0.08 * fps);
```

### 2.4 必须有 exit，exit 比 enter 快

只进不出会让画面“堵住”，剪辑点也只能硬切。每个入场元素都要有对应的出场：enter 用 12–20 帧，exit 用 6–10 帧；exit 通常只做透明度 + 轻微位移/缩放，不要完整倒放入场。用 `Sequence` 控制 `durationInFrames`，或用带 `clamp` 的插值收尾。

### 2.5 五层合成

一张有质感的画面至少叠五层，从下到上：

1. **渐变背景**：不是纯色，用径向/网格渐变或缓慢流动的色场。
2. **素材层**：图片、视频、3D 渲染或截图。
3. **图形层**：文字、线条、形状、HUD、标注。
4. **调色层**：统一色温、对比、饱和度，可用 CSS filter 或混合模式。
5. **颗粒/暗角层**：轻噪点 + 暗角，把各层“粘”成同一张画面。

五层缺一，画面就会像素材拼贴。颗粒和暗角宁轻勿重，透明度通常 3%–10%。

### 2.6 每个静图加 Ken Burns；视频组件按版本选

静态图片必须做缓慢的推拉摇移（Ken Burns）：6–10 秒内缩放 1.00→1.06–1.10，配合 1%–3% 平移，用 bezier 或 spring 缓动。

视频素材按 Remotion 版本选组件：

- **4.0.538（本机官方技能）**：用 `@remotion/media` 的 `<Video>`。官方 `remotion-markup` 的 embedding-videos 指南只给出这个入口，未提及旧版 `remotion` 包里的 `<Video>`。
- **沿用旧版 `remotion` 的 `<Video>`**：渲染时换成 `<OffthreadVideo>`。旧版 `<Video>` 依赖浏览器播放时钟，逐帧渲染容易丢帧或音画不同步；`<OffthreadVideo>` 在渲染时逐帧精确取帧。

两条路都要保证画面与音频逐帧对齐，动画时间仍从 `fps` 推导。

### 2.7 idle 元素加正弦微动

画面里长时间不动的元素（Logo、角标、背景图形、待机角色）加正弦微动：`Math.sin((frame / fps) * 2 * Math.PI * 0.3)`，幅度控制在 1–2% 或 1–3px。目的是“活着”，不是“跳舞”；频率过高会变成抖动。

```tsx
const idleY = Math.sin((frame / fps) * Math.PI * 2 * 0.3) * 2;
```

### 2.8 时间从 fps 推导，不写死帧号

所有时长写“秒”，再乘 `fps` 得到帧数：

```tsx
const fps = 30;
const durationInFrames = Math.round(9 * fps);
const enterFrames = Math.round(0.6 * fps);
```

不要出现 `frame > 137` 这类魔法数。交付前至少用 30fps 和 60fps 各检查一次关键时间点；换 fps 后节奏应保持一致。

### 2.9 颜色/缓动集中到 theme.ts

颜色、圆角、字体、缓动曲线、动效时长统一放在 `theme.ts`，组件里不写 inline 十六进制色值和散落的 bezier：

```ts
export const theme = {
  colors: { bg: "#0B0B0F", ink: "#F5F2EA", accent: "#C6FF4A" },
  easing: { enter: [0.22, 1, 0.36, 1], exit: [0.4, 0, 1, 1] },
  motion: { enterFrames: 18, exitFrames: 8, staggerFrames: 3 },
} as const;
```

改一处全片生效，也方便和 `references/style-library.md` 的风格卡对齐。

### 2.10 渲染 → 抽帧 → 肉眼检查 → 修 → 再渲染

不验帧不算交付。每次 `render` 后抽 8–12 帧（覆盖开头、结尾、字幕最密处、转场点），逐张看：文字有没有溢出、字体有没有变豆腐块、层级有没有盖错、对比度够不够、有没有跳帧。发现问题改代码再渲染，直到抽帧全部通过。

## 3. 官方 12 件套路由

本机安装位置：`~/.claude/skills/remotion-best-practices`，版本 4.0.538。总入口是路由 skill，不要绕过它直接猜。

| # | 技能 | 解决什么 | 什么时候加载 |
|---|---|---|---|
| 1 | `remotion-best-practices` | 总入口 / 路由，按任务分发到子技能 | 每次进入 Remotion 任务先读 |
| 2 | `remotion-create` | 新建 Remotion 工程与 composition | 没有工程，或要加新 composition |
| 3 | `remotion-markup` | React markup、动画与特效最佳实践 | 写场景、调动画、改样式 |
| 4 | `remotion-studio` | Preview / Studio 启动与调试 | 迭代阶段实时预览 |
| 5 | `remotion-render` | 导出与高级渲染选项 | 出片、调 codec/并发/图片格式 |
| 6 | `remotion-maps` | 静态地图、路线动画、Mapbox/MapLibre/GeoJSON、3D 飞行 | 地理类镜头 |
| 7 | `remotion-captions` | 转写、显示、动画字幕（Caption JSON） | 口播、歌词、词级字幕 |
| 8 | `remotion-saas` | `<Player>`、Lambda/Vercel/Cloudflare/Express、客户端渲染 | 做工具、批量渲染、云端出片 |
| 9 | `remotion-interactivity` | 让 Studio 时间轴可选中、可拖动、可回写 | 需要交付可编辑工程时 |
| 10 | `remotion-docs` | 用 Algolia 查最新官方文档 | API 不确定、版本有疑问 |
| 11 | `remotion-upgrade` | 升级 Remotion 及相关包与技能 | 升级工程或技能版本 |
| 12 | `remotion-multimedia` | Mediabunny：浏览器内裁剪、裁切、取元数据 | 处理音视频素材的时长/元数据 |

使用纪律：

- 路由 skill 已经写明分发逻辑，按需加载一个子技能即可；不要把 12 份文档一次性塞进上下文。
- 迭代阶段用 `remotion studio` 预览，不要每改一版就全量 `npx remotion render`；全量渲染留到交付。
- 官方子技能讲 API 与工程做法，本卡讲动效与验收标准；冲突时 API 以官方为准，质量标准以本卡为准。

## 4. CJK 字幕与字体

官方 4.0.538 没有中文专项指南：`remotion-captions` 只解决 Caption JSON 的结构与动画机制，中文排版、断行和字体回退要自己负责。

- **字号**：以 1080×1920 竖屏为基准，字幕 44px；横屏 1920×1080 用 36–40px 是版式选择（横屏信息密度更高），不是等比缩放的结果。两种画幅都必须重新抽帧确认可读性，不能靠“看起来差不多”。
- **描边**：深色描边或阴影保证压在亮背景上也清楚。描边 4–6px，或 2–4px 阴影加 60%–80% 不透明度的暗底条；不要只靠纯白字。
- **每块约 16 字**：中文信息密度高，单块控制在 16 字左右、最多两行；按标点断句，不把词拆开，避免最后一行只剩 1–2 个字。
- **先测换行**：正式渲染前用最长的一句、含中英混排和数字的句子做一张测试帧，确认断行位置、标点避头尾和行高（1.4–1.6）。不同字体宽度不同，换字体必须重测。
- **先测字体 fallback**：无头 Chrome / Linux 环境常常没有中文字体，默认 `sans-serif` 可能直接出豆腐块。显式写字体栈，并把字体文件随工程打包或通过 `@remotion/google-fonts` 加载：

  ```css
  font-family: "Noto Sans SC", "Source Han Sans SC", "Microsoft YaHei", sans-serif;
  ```

  加载完成前不要开始渲染（用 `delayRender` / `continueRender` 或字体加载 API），否则首帧可能用回退字体。
- **不要用默认无衬线而不检查**：默认字体在不同机器上宽度和字形都不同，会改变断行和字幕块时长。字体是交付物的一部分。
- **分词**：中文没有空格，词级字幕不能靠空格切分；Caption JSON 需要按字/词显式给时间戳，或按语义短语分块。字幕安全区留在画面底部 12%–18% 以上。

## 5. 交付检查

Remotion 只负责出画面，交付前仍走本 skill 的统一验收：

1. **抽帧**：`render` 后用 `verify_delivery.py` 抽 12 帧。手动用 ffmpeg 时按片长均匀取帧，再单独补首帧、尾帧和每个转场点：

   ```bash
   # 12 帧均匀分布，45 换成实际片长（秒）
   ffmpeg -i out/final.mp4 -vf "fps=12/45" out/stills/frame-%03d.png

   # 首帧与尾帧单独补
   ffmpeg -ss 0 -i out/final.mp4 -frames:v 1 out/stills/first.png
   ffmpeg -sseof -0.1 -i out/final.mp4 -frames:v 1 out/stills/last.png
   ```

   均匀帧负责整体检查，首帧/尾帧和转场帧负责抓边界问题，两者都要看。

2. **技术参数**：用 `ffprobe` 核对分辨率、fps、帧数、时长、音频轨：

   ```bash
   ffprobe -v error -select_streams v:0 \
     -show_entries stream=width,height,r_frame_rate,nb_frames,duration \
     -of default=noprint_wrappers=1 out/final.mp4
   ```

3. **响度**：按 `verify_delivery.py` 的阈值执行（低于 -16 LUFS 记 WARNING，true peak 超限记 FAIL）；短视频平台投放目标可参考案例卡的 -14 LUFS / -1.5 dBTP。
4. **肉眼检查**：抽帧逐张看文字、字体、层级、对比度、转场；首尾帧不得纯黑/纯白（除非分镜要求）。
5. **记录**：把抽帧、`delivery-report.md` 和结论写进项目 `docs/SCORECARD.md`。

## 6. 许可

Remotion 本体是**公司许可（company license）**，不是 MIT：

- 公司员工不超过 3 人可免费商用（个人使用免费）。
- **公司员工超过 3 人的商业使用需要向 Remotion 购买授权**。
- 安装官方 skill 包、复制本卡的方法，都不改变 Remotion 本体的许可；技能包免费不等于商业授权。
- `haidrrrry/claude-remotion-skill` 的 10 条铁律为 MIT，可吸收改写；引用时保留来源说明。
- 商用前复核 Remotion 官网最新许可条款；许可会随版本变化。

## 7. 与本 skill 流程的接法

- 引擎路由命中“React 组件视频”时，入口是 `remotion-best-practices`，再按第 3 节加载子技能。
- 风格仍从 `references/style-library.md` 选；Remotion 只是实现手段，不改变风格卡里的配色、动效词汇和失败模式。
- critic 评审使用 `references/critic.md` 的评分卡，同时逐条对照第 2 节的 10 条铁律；铁律违反项写进扣分理由。
- 交付验收按第 5 节执行，和 seek(t) 工程同一套硬性检查。
