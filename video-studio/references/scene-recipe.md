# 场景配方(实证过的中文讲解视频场景结构)

## 单屏场景骨架(推荐,相机方案已证实不可用)

每个场景 = 一个 1920x1080 sub-comp 文件 `compositions/frames/scene-NN.html`:

```
<template>
  <style>   #root{position:absolute;inset:0;...} 场景内全部 CSS(含字幕条/字幕句)  </style>
  <div id="root" data-composition-id="scene-NN" data-width="1920" data-height="1080">
    <div class="sN-grid"></div>            背景网格(120px 格,琥珀 4% 透明)
    ... 场景内容(卡片/表格/图,初始 opacity:0 由动画入场) ...
    <div class="sN-subtitle-bar">           底部字幕条(高 120px)
      <span class="sN-sub">句子1</span> ...  每句旁白一个 span,叠放
    </div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    ... 内容入场(fromTo)...
    ... 逐句字幕循环 ...
    ... 节奏高亮 ...
    window.__timelines["scene-NN"] = tl;
  </script>
</template>
```

## 逐句字幕系统(核心:讲解视频的"节奏骨架")

字幕句 = 旁白按句切分,时间戳即节拍网格(无音乐时的节奏来源)。CSS:

```css
.sN-sub { position:absolute; left:0; bottom:0; width:1920px; height:120px;
  display:flex; align-items:center; justify-content:center; padding:0 140px;
  box-sizing:border-box; opacity:0; font-size:32px; font-weight:500;
  line-height:1.45; text-align:center; color:#d5cfc0; }
```

JS(整段照抄,只改 subTimes):

```js
const subs = document.querySelectorAll(".sN-sub");
const subTimes = [[t1_in,t1_out],[t2_in,t2_out],...];
for (let i = 0; i < subs.length; i++) {
  if (i === 0) tl.fromTo(subs[i], { opacity: 0 }, { opacity: 1, duration: 0.4, overwrite: "auto" }, subTimes[i][0]);
  else tl.fromTo(subs[i], { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false, overwrite: "auto" }, subTimes[i][0]);
  tl.to(subs[i], { opacity: 0, duration: 0.3, overwrite: "auto" }, subTimes[i][1]);
}
```

批量注入用 `scripts/inject_subtitles.py`(免手写)。

## 节奏高亮(消灭"入场后定帧")

字幕讲到哪,画面元素高亮到哪:表格行扫色、时间轴条目点亮、卡片边框闪。模式:

```js
// 讲到某行时(时间=对应字幕句内):
tl.to(rows[n], { backgroundColor: "rgba(217,164,65,0.14)", duration: 0.4, ease: "power1.out" }, t);
// 强调色语义:A 级结论绿 rgba(107,143,94,*)、警示红 rgba(224,112,95,*)、中性琥珀 rgba(217,164,65,*)
```

## 标注动画(讲重点时"打在内容上",不挡内容)

- 手绘圈:SVG ellipse,`strokeDasharray/dashoffset` 从周长→0(0.8s,power2.inOut)
- 下划线:div 高 9px,`scaleX 0→1`(transform-origin left)
- 图章(✗/✓):`fromTo {opacity:0,scale:3.2,rotation:r±20} → {1,1,r}`(0.3s,**power4.in** 急落)+ 落地 `scale 1→1.18 yoyo` 震颤;坐标对准目标块中心,元素加 `data-layout-allow-overlap`
- 箭头:SVG path 描边生长 + 箭头头 0.15s 淡入
- 星标:小 ✦ back.out(3) 弹入 + yoyo 漂浮

## 常用入场编排

- 卡片:`back.out(1.4-1.6)` + 方向轮换(x -80/+80/y 70),错开 0.4-0.7s
- 表格:逐行 0.42s 间隔 x -36 滑入
- 列表项:0.28-0.5s 间隔
- 背景 idle:主块 ±5-6px 上下漂浮(2.6-3.1s yoyo),**起始时间错开入场结束**
- ghost 大字(装饰):入场后 ±26px 缓慢漂移

## 设计系统(可直接抄)

深色档案风:bg `#10130e` / 面板 `#1a1f17` / 文字 `#ece7d9` / 副文字 `#d5cfc0` / accent 琥珀 `#d9a441` 与亮体 `#f0d9a8` / 正确绿 `#a5c99a`(底 `rgba(107,143,94,*)`)/ 警示红 `#e0705f`(底 `rgba(192,57,43,*)`)/ ghost `#6a6b64`。
视频字号:标题 44-58、卡片题 26-36、正文 22-30、字幕 32;边框 2-4px;标签/徽章用圆角胶囊。**font-family 只写 sans-serif/monospace**(命名字体需本地 @font-face,lint 会拦)。

## 真实截图接入

`<img>` 本地路径(assets/screenshots/),容器 `object-fit:cover; object-position:top` + 固定高;图上可叠半透明标注浮层(背景 rgba(16,19,14,0.9))。采集方法见 hyperframes-pitfalls#3。

## 成片包装

封面:渲染后用 `hyperframes snapshot --at <代表帧时间>` 出 1920x1080 PNG 即是封面图。常驻元素(免责徽标)放主 index 的 root 内、场景 host 之外,全程可见;它有呼吸动画要挂主 timeline(`window.__timelines["主id"]`)。
