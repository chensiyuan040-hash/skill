# HyperFrames 本机踩坑手册(2026-10 实战验证)

按症状查。每条都是真踩过、修过的。

## 环境

1. **渲染报 Chrome not found / 自动下载 chrome-headless-shell 失败**:引擎下载走网络会被代理掐。
   修:`HYPERFRAMES_BROWSER_PATH=/usr/bin/google-chrome npx hyperframes render`。本机无 NVIDIA GPU,走 screenshot 捕获 + software GPU,365s@1080p30 约 9-10 分钟(5 worker 并行),可接受。
2. **改场景文件后内容"没变化"/替换静默失败**:Studio(preview)会给元素插入 `data-hf-id="hf-xxx"` 属性,`<div class="s1-sub">` 之类的精确字符串匹配会悄悄失配。
   修:改前先 grep 实际 HTML;python 替换用宽松正则(`<div[^>]*class="..."`);替换后必须断言命中(`assert old in s`)。
3. **本机浏览器能直连 cia.gov 等外网**:Playwright chromium 走系统代理(clash),采集真实网页截图直接 `browser_navigate` + `browser_take_screenshot`;但 curl 直连不通,curl 走 clash 端口也常失败——抓 CDN 资源时 curl 要带 `-H 'Referer: https://www.douyin.com/'` 和浏览器 UA。

## 编写契约

4. **sub-comp 场景结构**:`<template>` 内必须有 `<style>`+`<div id="root" data-composition-id>`+`<script>`(head 里的 style/script 会被装配器丢弃);host 的 `data-composition-id` 必须 = 场景内部 id = `window.__timelines["id"]` 三处一致;场景 root 用 `inset: 0` 不要写死 1920px。
5. **lint 首过必挂清单**(写代码时直接避开):
   - CSS transform 初始值 + GSAP 同属性 tween → `gsap_css_transform_conflict`(初始态全放 fromTo 的 from 里)
   - 循环里对同 class 多元素 fromTo → 加 `immediateRender: false`(除最早那个);间隔必须 > duration(否则 overlapping 警告),或加 `overwrite: "auto"`
   - JS 变量名:场景 script 里 `const nodes/items/rows/stats/pits` 等通用名极易与注入代码撞名 → `invalid_inline_script_syntax`,新注入代码用 `fXxx`/`tlXxx` 前缀
   - ghost 大字(装饰性低对比)过不了 WCAG 3:1:透明度方案无效(非线性),直接用实色中灰 `#6a6b64`;故意出画的大字加 `data-layout-allow-overflow`
   - 中文引号 “” 在 heredoc/python 字符串里会被转义出错 → 用「」
6. **音频挂载位置(大坑)**:`<audio>` 放 sub-comp 的 template 里**不生效**(timeline 不识别、渲染无声也不报错);放主 index 的 composition root **外面**也不生效(`closest([data-composition-id])` 解析不到宿主被静默忽略)。**唯一可靠位置:主 index.html 的 root div 内部**,每个 audio 必须有 id。挂载后用 `npx hyperframes timeline` 验证出现 `audio (N)` 段。
7. **布局审计(content_overlap)三层修法**:①元素真重叠 → 改几何;②有意压盖(图章/大字盖内容)→ 给元素加 `data-layout-allow-overlap`;③跨场景残留(上一场景 host 已隐藏但 DOM 几何还在,和常驻元素如右上角徽标几何重叠)→ 同样加标记。文字对比度不够时审计会给建议色,直接抄。

## 引擎已知 bug(未解,勿踩)

8. **大画布相机方案不可用**:用"内容铺在 2-3 倍宽画布 + 对 world 容器做连续 x/y/scale transform 链(镜头巡航)"——GSAP 独立验证(顺序/跳跃 seek)全部正确,但引擎渲染管线内镜头系统性错位/丢失(to/fromTo/补 duration 均无解,最小复现项目证实)。**动画只做元素级 fromTo**(入场/高亮/缩放/旋转单个元素是可靠的)。等上游修复后再试相机。

## 工作流坑

9. **Studio preview 与文件编辑竞态**:preview 进程存活时会回写文件(data-hf-id);批量改文件前 `npx hyperframes preview --stop`,改完再 `--background` 拉起(自动热重载)。
10. **改时间轴后必跑 lint**:场景时长/host data-start 改动后 `clip_ends_past_root_duration` 会提示 root duration 与最后一个 host 结束时间不一致,同步改 index 的 `data-duration`。
11. **snapshot 可用于渲染帧质心审计**(画面偏移/空白排查):帧 PNG + python 算非背景像素质心,正常应接近 (960, 500±150);偏到角落或亮像素 <0.5% 就是布局/动画 bug——配合本 skill 的 `scripts/frame_audit.py`。

## 参考视频定量拆解方法论

拆一支视频"为什么灵动":三步拿数据——
1. **下载**:playwright 打开视频页(抖音需登录态,等 5s 懒加载)→ `browser_network_requests` 过滤 `douyinvod.*media-video` → curl 带 Referer+UA 下载
2. **切镜率**:`ffprobe -f lavfi "movie=v.mp4,select=gt(scene\,0.25)" -show_entries frame=pts_time` → 统计镜头数/中位时长/<2s 占比
3. **运动能量**:ffmpeg 每秒 1 帧 160x90 灰度 → 相邻帧平均像素差 → "X% 的秒有可见运动、最长静止 N 秒"

实测基准(2026-10):
- 快切 MV 型(《别发给 Dario》149s):46 切、中位镜头 1.47s、82% 秒在动、最长静止 3s
- 讲解长镜头型(同作者流程自述 83.5s):仅 2 次大切换、前 46s 单构图,但 77% 秒在动、最长静止 2s
- **结论:讲解型视频不必追快切;"每 1-2 秒都有元素在动 + 最长静止不超过 2-3 秒"就是灵动的充分条件**——元素级动画完全做得到
