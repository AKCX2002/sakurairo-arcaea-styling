# Mermaid subgraph viewBox 膨胀：完整根因分析与修复记录

> 涵盖 2026-06-01 至 2026-06-02 在 babel36acl.xyz 上 Babel Arcaea Code 插件的一轮完整排查。

## 现象

部分 Mermaid 流程图在 Sakurairo + Arcaea 主题下渲染异常：

- 节点正常生成、连线存在
- 但节点被分散到画布四个角落
- SVG `viewBox` 被异常放大（典型值 5000~8000px）
- 浏览器将超宽 SVG 缩放到容器内后，节点变得极小

不是所有图都触发：直线流程图（7 节点、0 subgraph）正常，带多层 subgraph 的架构图（27 节点、8 subgraph）才出问题。

2026-06-02 追加确认：同一类长流程/超宽图还会出现另一种相反问题：

- 第一个超长超宽 Mermaid 图显示不全，但容器没有横向滚动条
- 全屏预览也显示不全，打开后仍沿用被裁坏的 SVG 视口
- `.arcaea-mermaid-box` 和 `pre.mermaid` 都是 `overflow: auto`，多个图形成嵌套滚动区，页面滚动手感异常且容易卡顿
- Chrome 控制台未发现 `error/warn`，问题主要来自布局策略和 viewBox 误裁剪，不是运行时报错
- 线上资源版本检查到 `mermaid.css?ver=1.6.26`、`mermaid-init.js?ver=1.6.26`、`mermaid-enhance.*?ver=1.6.26`

---

## 根因链

```
Sakurairo 全局 CSS (* { transition: all 0.4s }; body { text-shadow: ... })
      │
      ▼
穿透 .arcaea-mermaid-box 容器继承链
      │
      ├──→ 污染 foreignObject 文字排版
      │         │
      │         ▼
      │    dagre 布局引擎计算节点尺寸偏大
      │         │
      │         ▼
      │    subgraph 边界逐层放大（子图→父图→同级间距推开）
      │         │
      │         ▼
      │    Mermaid 输出 viewBox="0 0 8000 5000"
      │
      └──→ 每个 SVG rect/path/text 挂 400ms transition
                │
                ▼
           浏览器 Forced reflow 爆炸
```

### 第二轮根因：长图被误裁剪

第一轮修复加入了“渲染后从 `.node/.cluster/.statediagram-*` 的 `getBBox()` 重算紧凑 viewBox”的裁剪逻辑。该逻辑对极端膨胀的 viewBox 有用，但对正常的长流程/超宽图存在风险：

1. Mermaid 11 的节点通常包在 `<g class="node" transform="translate(...)">` 中。
2. `getBBox()` 返回的是该元素自身坐标系内的局部 bbox，不等同于根 SVG viewBox 坐标。
3. 如果直接把多个局部 bbox 求并集，会把本来分布在不同 `translate(...)` 位置的节点误当作聚集在局部原点附近。
4. 裁剪后 viewBox 会被错误压缩，例如线上第一个超宽图被裁成约 `789 x 550`，但右侧和下方内容实际仍存在于 SVG 内部。
5. 因为 viewBox 已经被裁坏，容器 `scrollWidth == clientWidth`，所以不会出现横向滚动条；全屏克隆这个 SVG 时也只会显示被裁后的区域。

结论：viewBox 裁剪只能作为“极端异常 viewBox”的兜底，不应无条件应用到普通长图/宽图。

### 第三轮根因：嵌套滚动导致页面卡顿

早期 Mermaid 响应式策略是：

- 外层 `.arcaea-mermaid-box`：`overflow-x: auto; overflow-y: auto; max-height: min(90vh, 960px)`
- 内层 `pre.mermaid`：继承主题 `pre` 的 `overflow: auto`
- 超宽图：JS 进入 `scroll` 模式，给 SVG 设置大于容器的宽度

这会造成两个问题：

- 鼠标滚轮落在图表区域时，浏览器优先滚动 Mermaid 容器或内层 `pre`，而不是滚动整页。
- 多个长图同时存在时，嵌套滚动区和 SVG 重排叠加，页面表现为卡顿、滚动断续。

最终策略改为：常态下不滚动 Mermaid 容器，正文图表按容器自动缩放完整显示；需要查看细节时点击进入全屏预览。

### 三层污染源

| 泄漏源 | 规则 | 影响 |
|--------|------|------|
| `*` | `transition: all 0.4s cubic-bezier(...)` | SVG 内部所有元素挂 400ms 过渡 |
| `body` | `text-shadow: 0 0 1px rgba(0,0,0,.1)` | 透过继承进入容器 |
| Sakurairo 全局样式 | `font-family`, `line-height`, `font-size`, `zoom`, `transform` | 穿透到 foreignObject，dagre 尺寸计算偏大 |

### 为什么 `htmlLabels: false` 没拦住

Mermaid 11.15+ 的 flowchart 图**不管 `htmlLabels` 设什么值都输出 `<foreignObject>`**。该选项对 diagram type `flowchart-v2` 的实际渲染引擎不生效。证据是线上 SVG 源码中每个节点都是：

```html
<foreignObject width="127" height="90">
  <div style="display: table-cell; ...">
    <span class="nodeLabel"><p>节点文字</p></span>
  </div>
</foreignObject>
```

### 为什么只有 subgraph 图触发

直线流程图（无 subgraph）的 dagre 布局只做一次局部计算，即使 foreignObject 尺寸略偏大，最终 viewBox 也在 200~600px 正常范围。

带 subgraph 的图：dagre 先计算子图内节点布局 → 再计算子图边界框 → 再放置跨子图连线。**任何子图边界偏大会逐层放大**：子图 rect 被撑大 → 同级子图间距被推开 → 整个画布膨胀数千像素。

---

## 防御体系

按加载顺序排列：

| 层 | 位置 | 规则 | 目标 |
|----|------|------|------|
| 1 | `mermaid.css` `.arcaea-mermaid-box` | `font-family/font-size/line-height/color/text-shadow` 显式重置 | 阻断容器级继承 |
| 2 | `mermaid.css` `.arcaea-mermaid-box *` | `transition: none !important` | 阻断 `* { transition:all }` 穿透 SVG |
| 3 | `mermaid.css` `pre.mermaid foreignObject *` | `all: initial` + 显式 fontSize/lineHeight/boxSizing | 隔离 SVG 内 foreignObject |
| 4 | `mermaid.css` `.arcaea-mermaid-box` | `contain: layout paint` | CSS containment（限制重排范围） |
| 5 | `mermaid.css` `pre.mermaid svg` | SVG 自身 `padding:0; border:0; box-sizing:border-box; overflow:visible` | 避免 SVG 盒模型挤压和 Sakurairo `svg:not(:root)` 裁切 |
| 6 | `mermaid-init.js` `renderMermaid()` | 仅对极端异常 viewBox 做裁剪，裁剪时必须把 bbox 转到根 SVG 坐标 | 事后裁剪空白，避免误裁普通长图 |
| 7 | `mermaid-init.js` / `mermaid-enhance.js` | 正文自动 fit；点击/工具栏全屏按视口自动 fit，支持缩放和平移 | 常态无内部滚动，细节交给全屏 |

### 已知局限

viewBox 裁剪只能消除 **SVG 边缘不可见 edgePath 撑出的空白**。如果 dagre 因 foreignObject 污染而把节点真正推开了数千 px，裁剪无法消除（节点确实相隔那么远）。此时需要第 1-3 层的 CSS 隔离在 dagre 布局前切断污染。

viewBox 裁剪也不能无条件应用。普通长流程/超宽图本来就应该拥有较大的 viewBox；如果裁剪逻辑没有正确处理 `transform` 坐标系，会把内容误裁掉。实践策略：

- 原始 viewBox 未达到极端异常量级时，不裁剪。
- 需要裁剪时，不能直接合并局部 `getBBox()`；必须用 `getCTM()`/矩阵把 bbox 四角变换到根 SVG 坐标后再求并集。
- 裁剪结果如果小于原始 viewBox 的主要尺寸比例（例如宽或高低于 20%），视为可疑，放弃裁剪。

常态页面不再依赖 Mermaid 容器滚动。滚动条不是修复方向；长图应该缩放到合适大小，点击后在全屏里查看细节。

---

## 验证方法

1. 检查线上插件版本：浏览器 F12 → Sources → `mermaid-init.js`，搜索 `crop viewBox` —— 存在则含裁剪代码
2. 检查容器级隔离是否生效：选中 `.arcaea-mermaid-box` → Computed 面板，确认 `font-family` 不是 `"Zen Old Mincho"`，`transition` 不是 `all 0.4s`
3. 检查 foreignObject 是否出现：在页面源码中搜索 `<foreignObject` —— Mermaid 11.15+ 总是出现，正常
4. 检查 viewBox 量级：
   ```javascript
   var svg = document.querySelector('.arcaea-mermaid-box pre.mermaid svg');
   var vb = svg.viewBox.baseVal;
   console.log(vb.width, vb.height); // 应在 2000 以内，异常为 5000+
   ```
5. 定位 subgraph 膨胀：
   ```javascript
   document.querySelectorAll('.arcaea-mermaid-box .cluster rect').forEach(function(r, i) {
       var b = r.getBBox();
       console.log('subgraph', i, 'bbox', b.width, 'x', b.height);
   });
   ```

---

## 调试方式

### 1. Chrome 自动化现场检查

优先使用 Chrome 控制台或 Codex Chrome 自动化读取 DOM/CSS。不要只看截图，因为 Mermaid 异常通常由 viewBox、元素样式、滚动尺寸共同决定。

核心检查脚本：

```javascript
Array.from(document.querySelectorAll('.arcaea-mermaid-box')).map(function(box, i) {
  var pre = box.querySelector('pre.mermaid');
  var svg = box.querySelector('svg');
  return {
    i: i,
    scaleMode: box.dataset.bacMermaidScaleMode,
    box: {
      clientWidth: box.clientWidth,
      scrollWidth: box.scrollWidth,
      clientHeight: box.clientHeight,
      scrollHeight: box.scrollHeight,
      overflowX: getComputedStyle(box).overflowX,
      overflowY: getComputedStyle(box).overflowY
    },
    pre: pre && {
      clientWidth: pre.clientWidth,
      scrollWidth: pre.scrollWidth,
      overflowX: getComputedStyle(pre).overflowX,
      overflowY: getComputedStyle(pre).overflowY
    },
    svg: svg && {
      rect: svg.getBoundingClientRect().toJSON ? svg.getBoundingClientRect().toJSON() : null,
      style: svg.getAttribute('style'),
      viewBox: svg.getAttribute('viewBox'),
      overflow: getComputedStyle(svg).overflow,
      padding: getComputedStyle(svg).padding,
      border: getComputedStyle(svg).border,
      boxSizing: getComputedStyle(svg).boxSizing
    }
  };
});
```

判定标准：

- 正常常态：`.arcaea-mermaid-box` 不应是内部滚动容器，`overflow` 应避免 `auto/auto`。
- 正常常态：`pre.mermaid` 不应抢滚轮，`overflow` 应为 `visible`。
- 正常常态：SVG `padding` 应为 `0px`，`border` 应为 `0px`，`box-sizing` 应为 `border-box`，`overflow` 应为 `visible`。
- 如果 `scrollWidth == clientWidth` 但内容看起来缺失，优先怀疑 viewBox 已被误裁，而不是滚动条失效。

### 2. 控制台与资源版本

检查控制台：

```javascript
// DevTools Console 或 Chrome 自动化读取 warn/error
// 期望：没有 Mermaid 相关 error/warn
```

检查资源版本：

```javascript
Array.from(document.querySelectorAll('link[href*="mermaid"], script[src*="mermaid"]'))
  .map(function(n) { return n.href || n.src; });
```

线上曾确认过：

- `mermaid.css?ver=1.6.26`
- `mermaid-enhance.css?ver=1.6.26`
- `mermaid-init.js?ver=1.6.26`
- `mermaid-enhance.js?ver=1.6.26`

资源版本由插件发布/构建流程自动提升。调试时不要为了缓存手动改版本号；如果确实要验证新资源，走正常构建或部署流程。

### 3. 判断 viewBox 是否被误裁

检查当前 viewBox：

```javascript
var svg = document.querySelector('.arcaea-mermaid-box svg');
console.log(svg.getAttribute('viewBox'));
```

异常特征：

- 图明显还有右侧/下方内容，但 viewBox 宽高只等于当前可见区域附近，例如 `789 x 550`。
- 容器没有滚动条，因为 SVG 的可滚动内容在 viewBox 层已经不存在。
- 全屏克隆 SVG 后仍显示不全，因为全屏复用的是同一个被裁坏的 viewBox。

裁剪逻辑调试原则：

```javascript
// 错误方向：直接合并局部 getBBox()
var b = node.getBBox();

// 正确方向：把局部 bbox 四角转到根 SVG 坐标
var matrix = node.getCTM();
[
  new DOMPoint(b.x, b.y),
  new DOMPoint(b.x + b.width, b.y),
  new DOMPoint(b.x, b.y + b.height),
  new DOMPoint(b.x + b.width, b.y + b.height)
].map(function(p) { return p.matrixTransform(matrix); });
```

Chrome 自动化的只读执行环境可能不支持直接调用 SVG `getBBox()`/`getCTM()`，这时以线上 SVG 源码、viewBox 数值、DOM transform 属性和截图综合判断。

### 4. 判断页面卡顿是否来自嵌套滚动

现场指标：

- `.arcaea-mermaid-box` 为 `overflow: auto`
- `pre.mermaid` 也为 `overflow: auto`
- 多个 Mermaid 图 `scrollHeight > clientHeight`
- 鼠标在图表区域滚动时，整页滚动被内部容器截获

修复方向：

- 常态下禁用 Mermaid 内部滚动。
- SVG 按容器宽度自动缩放完整显示。
- 点击图表或工具栏进入全屏，初始按视口 fit，之后允许滚轮缩放和拖拽平移。

---

## 改动历史

| 日期 | 提交 | 内容 |
|------|------|------|
| 2026-06-01 | `46626a4` | 修正过期注释 (+ foreignObject CSS 隔离) |
| 2026-06-01 | `c9bf4bf` | `.arcaea-mermaid-box` 容器级 CSS 隔离 (font/color/text-shadow/contain) |
| 2026-06-02 | `2e21eb7` | `.arcaea-mermaid-box * { transition: none }` 阻断 `*` 泄漏 |
| 2026-06-02 | 未提交 | 修正 SVG padding/border/overflow 造成的内框挤压与边缘裁切 |
| 2026-06-02 | 未提交 | viewBox 裁剪改为只处理极端异常尺寸，避免普通长图被误裁 |
| 2026-06-02 | 未提交 | 常态禁用 Mermaid 内部滚动，正文自动 fit，全屏初始按视口 fit |

---

## 禁止在文章正文中做的

- 内联 `window.mermaid.initialize()` / `window.mermaid.run()` / `unwrapMermaidCodeBlocks()` — 会导致插件和文章脚本**二次接管**，渲染结果不可预期
- 内联 Mermaid 兼容 CSS（如 `.mermaid foreignObject * { ... }`） — 与插件 CSS 互相覆盖，特异性竞跑
- 用 `.arcaea-wrap` + `.bg-glow` 包裹博客文章 — 新文章统一用 `.arcaea-article-content`

渲染统一交给 `babel-arcaea-code` 插件。正文只保留 Mermaid 源码块（```` ```mermaid ```` 或 `[mermaid]` 短代码）。
