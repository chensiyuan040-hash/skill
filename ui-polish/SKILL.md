---
name: ui-polish
description: 前端 UI 质感与交互细节的工程参数规范(色阶分层、字重补偿、流式打字、弹簧动效、组件选型边界)。当用户要求写或改前端界面、做页面/组件/样式/动效、优化界面"质感/精致感/廉价感"、为弹层或反馈场景选组件时使用,适用于 React+AntD、Vite、HTML/CSS 等任意前端栈。Engineering-grade UI polish rules: color-tier layering, font-weight compensation, streaming text, spring motion parameters, and component selection boundaries.
---

# UI 质感规范

界面的"高级感"来自可量化的细节参数。按本规范写样式与动效;与项目既有 design token / AntD 主题冲突时,以项目为准。双主题一律用 `html[data-theme]` 作用域的 CSS 变量实现,不要用 `light-dark()`(旧内核兼容坑)。

## 一、质感铁律

1. **分层不画边框**:层级用 1%–3% 明度差的背景色阶表达,禁纯黑 `#000`。
   - 浅色:页面底 `#f5f5f3` / 卡片 `#fcfcfb`;暗色:`#0b0b0a` / `#151515` / `#1a1a19` / `#20201e`(由深到浅的层级阶梯)
   - AntD 项目对齐 token(colorBgLayout/colorBgContainer),不要逐处写死色值
2. **聚焦用阴影不用 outline**:输入框/卡片聚焦时用双环 `box-shadow`(内环实色描边 + 外环低透明度主色光晕)造"咬合感";去掉默认 outline,但 `:focus-visible` 必须保留可见焦点
3. **暗色字重补偿**:暗色模式下字重降一档(400→300,可变字体可精确 360),抵消白字发胖的光晕效应;随主题用 CSS 变量切换
4. **流式打字水墨晕染**:单字 90ms,从 `blur(6px)` + 半透明过渡到清晰,缓动 `cubic-bezier(.215,.61,.355,1)`,相邻字错开 30ms 晕开;禁止逐字硬蹦,也禁止整段闪现
5. **行内图标对齐**:`vertical-align: -0.125em`,或用 flex + `align-items: center` 包裹
6. **数字防抖**:统计数字/时间/价格一律 `font-variant-numeric: tabular-nums`,刷新或变动时宽度不跳
7. **丝滑折叠**:高度动画不 JS 算高,用 `display: grid` + `grid-template-rows: 0fr → 1fr` 过渡(内层 `overflow: hidden`)
8. **防孤字**:正文 `text-wrap: pretty`,标题 `text-wrap: balance`
9. **动效分性格**:
   - 拖拽/吸附/定位:过阻尼弹簧(stiffness 1200 / damping 80)或 `cubic-bezier(.2,0,0,1)`,零回弹,一次咬死
   - 点赞/对勾/成功反馈:欠阻尼(380 / 18),一次小回弹,Q 弹
   - 进场 150–250ms,退场 100–150ms,快而克制
10. **反馈自熄**:复制/保存等临时反馈展示 2–2.5s 后自动淡出恢复原状,不要等用户手动关

## 二、廉价感反向清单(自查)

出现任一项即返工:
- 用 1px 边框划分所有区域;大面积纯黑/纯白底
- 聚焦时浏览器默认蓝 outline
- 暗色界面沿用浅色模式的字重(白字发胖)
- 流式输出逐字硬蹦或整段闪现
- 数字变化时跳动;所有动效共用同一个 ease,没有快慢性格
- 临时反馈永不消失,需要手动关闭
- 无信息量的装饰堆砌:ALL-CAPS 眉标、中点分隔字符串、按钮后缀 `→`、到处渐变光晕

## 三、组件选型边界(弹层与反馈)

| 场景 | 用 | 要点 |
|------|----|------|
| 底部半屏内容浏览,可拖拽调高(移动端) | Bottom Sheet(AntD `Drawer placement="bottom"`) | 阻尼手势、分档吸附,高度三档 peek/half/full ≈ 25/50/90% |
| 少数互斥动作选择(移动端) | Action Sheet | 扁平按钮、独立取消项、危险动作标红且与取消隔开 |
| 操作后轻提示、可撤销 | Snackbar(AntD `message` + 撤销按钮) | 底部浮条、带时限自动消失、撤销要能真实逆转操作 |
| 高危/阻断确认 | AlertDialog(AntD `Modal`) | 锁死背景遮罩;不可逆操作才禁 Esc,其余保留 |
| 新功能/新手指引 | Tour(AntD `Tour`) | 高亮定位 + 步骤漫游,可跳过 |
| 图片/媒体放大 | Lightbox(`antd-image` 或自绘) | 滚轮缩放、Esc 关闭 |
| 表单字段校验 | Inline Alert(AntD Form 校验) | 输入框下红字、即时校验、改正即消失;不要用全局 message 报字段错 |

阻断性从低到高:Snackbar < Inline Alert < Sheet < Action Sheet < Dialog。桌面端优先 Modal/message,移动端优先 Sheet 家族;拿不准就选阻断性更低的。

## 四、动效性格库(按需取用,别全堆)

- **完成反馈按钮**:点击后收缩成圆形 → 对勾 stroke 画出 → 粒子迸发,300–400ms
- **勾选联动**:勾选 → 进度环增长 + 数字滚动 + 顶部背景随进度变化
- **叠卡展开**:卡片组依次展开(每张 stagger 50ms),再点收起叠回
- **吸附卡 + 画线**:横向滑动松手后吸附最近卡位(弹簧 1200/80);切换时时间线用 `stroke-dashoffset` 逐段绘制
- **惯性滚轮**:picker 惯性旋转 → 减速 → 吸附刻度;滑过头回弹(欠阻尼 380/18)
- **圆形扩散转场**:从手指/光标按下位置 `clip-path: circle()` 扩散铺满,400–500ms

实现优先 CSS transition/animation 与 Web Animations;弹簧参数按 framer-motion 语义(stiffness/damping);所有动效必须有 `prefers-reduced-motion` 降级(直接切换/淡入即可)。

## 五、交付自检

- [ ] 分层靠色阶,无纯黑/纯白大底,无全边框划分
- [ ] 键盘 focus 可见(双环阴影),触摸目标 ≥ 44px
- [ ] 暗色模式字重已补偿
- [ ] 数字 `tabular-nums`;正文 `text-wrap: pretty`
- [ ] 动效两档性格,时长在规定区间;`prefers-reduced-motion` 有降级
- [ ] 临时反馈 2–2.5s 自动消失;表单错误走行内提示

## 来源

参数提炼自三个抖音视频(2026-10):Ludi《扒大厂AI客户端源码,质感全靠这5招》《6个隐藏王牌组件》、西瓜同学《第14集:让AI做的App更精致的6个交互》。
