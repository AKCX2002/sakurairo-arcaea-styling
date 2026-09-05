# Prism Previewers Arcaea Glass Layer (v1.0.9+)

## 概述

将 Prism 官方 Previewers 插件的 5 个悬浮预览组件（Color · Gradient · Angle · Time · Easing）从「开发工具小浮窗」改造为 Arcaea 风格的玻璃拟态交互组件。

## 文件结构

```
assets/prism/
├── prism-previewers.js            # 官方 Previewers JS (从 jsDelivr 下载)
├── prism-previewers.css           # 官方 Previewers CSS (从 jsDelivr 下载)
└── prism-previewers-arcaea.css    # Arcaea 玻璃层覆盖 (版本控制)
```

## 加载顺序 (PHP enqueue)

```
Core → Toolbar → Show Language → Line Numbers → Line Highlight →
Match Braces → Normalize Whitespace → Command Line → Treeview →
  Previewers ← 插入点
Copy → Autoloader (LAST)
```

## 设计原则

### 基础原则

| 官方默认 | Arcaea 覆盖 |
|---------|------------|
| 小方块，边框重 | 42px 圆角玻璃球 |
| 无 blur | `backdrop-filter: blur(20px) saturate(140%)` |
| 白色实线边框 | `rgba(255,255,255,0.08)` 细边框 |
| 硬阴影 | `0 8px 32px rgba(0,0,0,0.40) + 0 0 24px rgba(130,170,255,0.18)` 霓虹辉光 |
| 浏览器默认 transition | `opacity 0.25s ease + transform 0.25s ease` |

### 各 Previewer 差异

#### Color - 悬浮辉光彩球

- 14px 圆角
- `background-clip: padding-box` + 内边框包裹色块
- Hover 放大 `scale(1.08)` + 辉光增强
- 透明白/灰格底纸替换 checkerboard

#### Gradient - 宽卡片渐变预览

- 72px 宽 (vs 官方 64px)
- 双层 border: 外部 `rgba(255,255,255,0.08)` 细边 + 内部 `rgba(255,255,255,0.12)` 渐变锚定
- `box-shadow: 0 0 30px rgba(180,220,255,0.12)`

#### Angle - 深色罗盘

- 圆形深灰 `rgba(15,18,22,0.92)` 底 + blur
- 方向线 `stroke: #82aaff` + `drop-shadow(0 0 4px rgba(130,170,255,0.40))`
- 圆圈弧线 `rgba(130,170,255,0.20)` 弱显

#### Time - 动画计时环

- 同 Angle 圆形深底
- 弧线 `animation: prism-previewer-time 3s linear infinite`
- 弧线 `stroke: rgba(130,170,255,0.15)` + 动画段 `stroke-dasharray`

#### Easing - 缓动曲线预览

- 68px 宽暗玻璃卡 (vs 官方 60px)
- 曲线 `#82aaff` 蓝色 + `drop-shadow(0 0 6px rgba(130,170,255,0.35))` 发光
- 控制点 `rgba(15,18,22,0.95)` 深色
- 网格线 `rgba(255,255,255,0.15)` 弱显
- 暗/亮模式适配

## 移动端

- `@media (pointer: coarse)`: 禁用 hover，tap 显示
- `max-width: 80vw` 防溢出

## z-index 限制

```css
.prism-previewer { z-index: 9999 !important; }
```

防止被 Sakurairo 主题的 LightGallery (z-index 9997)、APlayer、Live2D 遮挡。

## 设置页

后台 → 设置 → Arcaea Code → Previewers 复选框（默认开启）

## CI 自动下载

在 `release.yml` 的 Prism 下载步骤中:

```yaml
curl -sL "$B/plugins/previewers/prism-previewers.min.js" -o assets/prism/prism-previewers.js
curl -sL "$B/plugins/previewers/prism-previewers.min.css" -o assets/prism/prism-previewers.css
```

`prism-previewers-arcaea.css` 在仓库版本控制中，不下载。
