# Sakurairo CSS 入侵防御对照表

本文档逐一列出 Sakurairo 3.0.10 主题 CSS 对 Arcaea 插件容器的入侵规则，以及 `arcaea-article-content.css`、`mermaid.css`、`content-enhance.css` 的对应防御。

每条防御均经过源码级验证：Sakurairo 规则来自 `style.css`、`css/content-style/sakura.css`、`css/dark.css`；防御来自 `babel-arcaea-code/assets/`。

---

## 一、全局规则入侵（style.css）

### 1.1 `* { transition: all 0.4s }`

**入侵源**：`style.css` 第 18 行

```css
* {
  transition: all 0.4s cubic-bezier(0.07, 0.53, 0.65, 0.95);
}
```

**影响**：所有元素（包括 SVG 内部 `<rect>`、`<path>`、`<text>`）的任何属性变化都附带 400ms 过渡，触发 Forced reflow。

**防御**：`mermaid.css` — 容器级全覆盖阻断

```css
.arcaea-mermaid-box * {
  transition: none !important;
}
```

**现状**：✅ Mermaid SVG 内部已阻断。❌ `pre` 代码块、`table`、`blockquote`、`h2::after` 动画等元素仍受此规则影响——所有 `::before`/`::after` 变化附带 400ms 过渡。

---

### 1.2 `body { text-shadow }`

**入侵源**：`style.css` 第 81 行

```css
body {
  text-shadow: 0 0 1px rgba(0, 0, 0, .1);
}
```

**影响**：所有文本通过继承获得一层肉眼可辨的模糊阴影。

**防御**：`arcaea-article-content.css` — wrapper 显式重置

```css
.arcaea-article-content {
  text-shadow: 0 1px 0 rgba(6, 10, 18, 0.18);
}
```

```css
.arcaea-mermaid-box {
  text-shadow: none;
}
```

**现状**：✅ wrapper 和 Mermaid 容器已重置。

---

### 1.3 `body { font-family: system-ui ...; font-size: 15px; color: var(--theme-skin) }`

**入侵源**：`style.css` 第 72、83、80 行

```css
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Roboto, Ubuntu, "Helvetica Neue", Arial, sans-serif;
  font-size: 15px;
  color: var(--theme-skin, #505050);
}
```

**影响**：所有未显式声明字体/字号的元素继承主题默认值。

**防御**：`arcaea-article-content.css` + `mermaid.css` — 每层显式声明

```css
.arcaea-article-content pre {
  font: 15px/1.72 "FiraCode Nerd Font", "Fira Code", "JetBrains Mono", Consolas, monospace !important;
}

.arcaea-article-content h2 {
  font-size: 1.65em !important;
  font-weight: 700 !important;
  line-height: 1.32 !important;
}

.arcaea-mermaid-box {
  font-family: "FiraCode Nerd Font", "Fira Code", "JetBrains Mono", "Noto Sans SC", sans-serif;
  font-size: 15px;
  line-height: 1.6;
}
```

**现状**：✅ 所有 wrapper 和容器已显式声明。

---

### 1.4 `li, ul, ol { cursor: pointer }`

**入侵源**：`style.css` 第 27 行

```css
li, ul, ol {
  cursor: pointer;
  padding-inline-start: unset;
}
```

**影响**：文章内的有序/无序列表全部显示为手型指针，暗示可点击但实际不可交互。

**防御**：主题自带覆盖（`style.css` 第 34 行）

```css
.entry-content li,
.entry-content ul,
.entry-content ol {
  cursor: unset;
}
```

**现状**：✅ 主题自身的 `.entry-content` 规则已修正。`.arcaea-article-content` 包裹在 `.entry-content` 内，继承此修正。

---

## 二、`.entry-content` 内容样式入侵（sakura.css）

### 2.1 列表：浅色边框 + 浅灰文字

**入侵源**：`sakura.css` 第 29-60 行

```css
.entry-content ul {
  border: 1px solid #E4E4E4;
  color: #616161;
  padding: 15px 10px 30px 50px;
  border-radius: 10px;
}
.entry-content ol {
  border: 1px solid #E4E4E4;
  color: #616161;
  padding: 15px 10px 30px 50px;
  border-radius: 10px;
}
```

**影响**：亮色浅灰边框和文字色突兀出现在深色 Arcaea 暗色面板上。

**防御**：`arcaea-article-content.css`

```css
.arcaea-article-content p,
.arcaea-article-content li {
  color: var(--arcaea-text);
  line-height: 1.82;
}
.arcaea-article-content ul,
.arcaea-article-content ol {
  margin: 1em 0;
  padding-left: 1.5em;
}
.arcaea-article-content li::marker {
  color: var(--arcaea-accent-strong);
}
```

**现状**：✅ 颜色和间距已覆盖。⚠️ 主题的 `border: 1px solid #E4E4E4` 未被显式移除——Arcaea 的 `color` 覆盖后视觉上不突出，但 DOM 中边框仍在。

---

### 2.2 H2：主题 highlight bar 伪元素

**入侵源**：`sakura.css` 第 74-93 行

```css
.entry-content h2:after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 30%;
  width: 70%;
  height: 0.7em;
  background-color: var(--article-theme-highlight, var(--theme-skin-matching));
  opacity: 0.4;
  border-radius: 30px;
}
```

**影响**：Sakurairo 用 `h2::after` 放置一条半透明主题色条作为装饰。

**防御**：`arcaea-article-content.css` — 用自己的 highlight bar 替代

```css
.arcaea-article-content h2::after {
  content: "" !important;
  position: absolute !important;
  left: 30%; right: 0; top: 55%;
  width: 70%; height: 0.7em;
  background: linear-gradient(90deg,
    rgba(169, 123, 255, 0.52),
    rgba(95, 212, 255, 0.38),
    rgba(95, 212, 255, 0.12)) !important;
  opacity: 0.72 !important;
  animation: arcaea-h2-glow 3.6s ease-in-out infinite;
}
```

**现状**：✅ 已用 Arcaea 冷紫/冰蓝渐变条替代主题色条。

---

### 2.3 H3/H4/H5：主题装饰符号伪元素

**入侵源**：`sakura.css` 第 101-122 行

```css
.entry-content h3:after {
  content: "#";
  position: absolute;
  left: 0;
}
.entry-content h4:after {
  content: ">";
  position: absolute;
  left: 0;
}
.entry-content h5:after {
  content: "~";
  position: absolute;
  left: 0;
}
```

**影响**：每个 H3 前面出现一个 `#`，H4 前面出现 `>`，H5 前面出现 `~`。

**防御**：`arcaea-article-content.css` — 全面抑制，用自定义装饰替代

```css
/* H3: 左侧梯度光柱 */
.arcaea-article-content h3::before {
  content: "" !important;
  position: absolute !important;
  left: 0; top: 0.22em;
  width: 4px !important;
  height: 1.05em !important;
  background: linear-gradient(180deg,
    rgba(139, 227, 255, 0.95),
    rgba(169, 123, 255, 0.75)) !important;
}
.arcaea-article-content h3::after {
  content: none !important;
  display: none !important;
}

/* H4: 菱形标记 */
.arcaea-article-content h4::before {
  content: "\25C7" !important;
  position: absolute !important;
  color: rgba(139, 227, 255, 0.92);
}
.arcaea-article-content h4::after {
  content: none !important;
  display: none !important;
}
```

**现状**：✅ H3 用光柱替代 `#`，H4 用菱形替代 `>`，H5 的 `~` 被抑制。

---

### 2.4 表格：白色条纹 + 蓝色表头

**入侵源**：`sakura.css` 第 164-193 行

```css
.entry-content tr:nth-child(even) {
  background-color: #f2f2f2;
}
.entry-content th {
  color: white;
}
.entry-content table {
  border-collapse: collapse;
  width: 100%;
}
```

**影响**：偶数行白色背景、表头白色文字，在暗色 Arcaea 面板上极其突兀。

**防御**：`arcaea-article-content.css` — 全面重置 + body.dark 前缀

```css
.arcaea-article-content table tbody tr:nth-child(odd),
.arcaea-article-content table tbody tr:nth-child(odd) td,
body.dark .entry-content .arcaea-article-content table tbody tr:nth-child(odd),
body.dark .entry-content .arcaea-article-content table tbody tr:nth-child(odd) td {
  background: var(--arcaea-surface-row) !important;
  color: rgba(236, 243, 255, 0.90) !important;
}

.arcaea-article-content table tbody tr:nth-child(even),
.arcaea-article-content table tbody tr:nth-child(even) td,
body.dark .entry-content .arcaea-article-content table tbody tr:nth-child(even),
body.dark .entry-content .arcaea-article-content table tbody tr:nth-child(even) td {
  background: var(--arcaea-surface-row-alt) !important;
  color: rgba(236, 243, 255, 0.90) !important;
}
```

**现状**：✅ 白色条纹已完全覆盖，深色奇偶行交替。

---

### 2.5 代码块：macOS 窗口红绿灯装饰

**入侵源**：`sakura.css` 第 197-260 行

```css
.entry-content .highlight-wrap:before {
  content: " ";
  border-radius: 50%;
  background: #fc625d;
  width: 12px;
  height: 12px;
  box-shadow: 20px 0 #fdbc40, 40px 0 #35cd4b;
}
.entry-content .highlight-wrap {
  background: #21252b;
  padding-top: 30px;
  color: #000;
}
```

**影响**：代码块上方出现 macOS 风格红黄绿圆点，且文字为黑色（暗底黑字不可见）。

**防御**：`arcaea-article-content.css` 的 pre 选择器优先级更高，不使用 `.highlight-wrap` class

```css
.arcaea-article-content pre {
  background: linear-gradient(180deg,
    rgba(15, 25, 44, 0.66),
    rgba(10, 18, 34, 0.54)) !important;
  color: var(--arcaea-text) !important;
}
```

**现状**：✅ Babel Arcaea Code 的 `normalizeCodeBlocks` 不输出 `.highlight-wrap` class，绕过此规则。

---

### 2.6 Blockquote：引号装饰伪元素

**入侵源**：`sakura.css` 第 1-2 行

```css
.entry-content blockquote:before,
.entry-content blockquote:after {
  display: block;
}
```

**影响**：Sakurairo 在 blockquote 前后显示 Font Awesome 引号图标（通过全局 blockquote:before/after 样式）。

**防御**：`arcaea-article-content.css`

```css
.arcaea-article-content blockquote::before {
  display: none !important;
  content: none !important;
}
.arcaea-article-content blockquote::after {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 3px;
  background: linear-gradient(180deg,
    rgba(160, 220, 255, 0.86),
    rgba(160, 220, 255, 0));
}
```

**现状**：✅ 引号装饰被替换为左侧渐变光柱。

---

## 三、暗色模式入侵（dark.css）

### 3.1 段落/列表文字色

**入侵源**：`dark.css` 第 154-160 行

```css
body.dark .entry-content p,
body.dark .entry-content ul,
body.dark .entry-content ol {
  color: var(--dark-text-secondary) !important;  /* #999999 */
}
```

**影响**：暗色模式下段落文字变成 `#999`（中灰），在 Arcaea 深蓝底上几乎不可读。

**防御**：`arcaea-article-content.css` — 更高特异性选择器

```css
body.dark .entry-content .arcaea-article-content p,
body.dark .entry-content .arcaea-article-content li {
  color: var(--arcaea-text);  /* rgba(242, 246, 252, 0.94) */
}
```

特异性对比：
- Sakurairo：`body.dark .entry-content p` = (0, 0, 2, 1)
- Arcaea：`body.dark .entry-content .arcaea-article-content p` = (0, 0, 3, 1)

**现状**：✅ 文字色已用更高特异性覆盖。

---

### 3.2 标题文字色

**入侵源**：`dark.css` 第 189-194 行

```css
body.dark .entry-content h1,
body.dark .entry-content h2,
body.dark .entry-content h3,
body.dark .entry-content h4,
body.dark .entry-content h5,
body.dark .entry-content h6 {
  color: var(--dark-text-primary);  /* #CCCCCC */
}
```

**影响**：暗色模式下标题变成 `#CCC`（中灰），丢失 Arcaea 冰蓝/冷白气质。

**防御**：`arcaea-article-content.css` — 同等特异性 + `!important`

```css
body.dark .entry-content .arcaea-article-content h2,
body.dark .entry-content .arcaea-article-content h3,
body.dark .entry-content .arcaea-article-content h4 {
  color: var(--arcaea-heading) !important;  /* #f2f6fc */
}
```

**现状**：✅ 标题色已覆盖为冷白。

---

### 3.3 行内代码背景

**入侵源**：`dark.css` 第 514-515 行

```css
body.dark .entry-content code:not(pre code),
body.dark .entry-content code {
  background: var(--inline_code_background_color_in_dark_mode, #505050);
}
```

**影响**：暗色模式下行内代码背景变成 `#505050`（中灰），与 Arcaea 冰蓝风格不协调。

**防御**：`arcaea-article-content.css`

```css
body.dark .entry-content .arcaea-article-content code {
  background: rgba(180, 198, 234, 0.12);
  color: rgba(225, 235, 250, 0.94) !important;
}
```

**现状**：✅ 已覆盖为低透明度冰蓝底。

---

## 四、Mermaid SVG 专项防御

### 4.1 foreignObject 文字隔离

**入侵源**：Sakurairo 的 `font-family`、`text-shadow`、`font-size` 通过继承穿透到 Mermaid SVG 内的 `<foreignObject>`。

**防御**：`mermaid.css` — `all: initial` 全重置

```css
pre.mermaid foreignObject,
pre.mermaid foreignObject div,
pre.mermaid foreignObject span,
pre.mermaid foreignObject p {
  all: initial;
  display: block;
  font-family: inherit;
  line-height: 1.4;
  box-sizing: border-box;
  font-size: 14px;
  padding: 0.18em 0.36em;
  overflow: visible;
}
```

**现状**：✅ Mermaid 11.15+ 的 flowchart 无论 `htmlLabels` 设什么值都输出 `<foreignObject>`，此层防御必须保留。

---

### 4.2 SVG 盒模型保护

**入侵源**：Sakurairo 可能对 `svg:not(:root)` 施加 `overflow: hidden`。

**防御**：`mermaid.css`

```css
pre.mermaid svg {
  display: block;
  height: auto;
  width: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  box-shadow: none;
  box-sizing: border-box;
  overflow: visible;
}
```

**现状**：✅ SVG 不会被 Sakurairo 裁切边缘内容。

---

### 4.3 CSS Containment

**防御**：`mermaid.css`

```css
.arcaea-mermaid-box {
  contain: layout paint;
}
```

**目标**：限制 Mermaid 容器的重排范围，减少 Forced reflow 对页面其他区域的影响。

**现状**：✅ 已启用。

---

## 五、插件运行时防御（Compat 模块）

### 5.1 Sakurairo 自带 Prism 高亮禁用

**入侵源**：Sakurairo `swicher.php` 第 131-142 行

```php
if (iro_opt('code_highlight_method', 'hljs') == 'prism') {
    $iro_opt['code_highlight_prism'] = [...];
}
```

**防御**：`class-bac-compat.php` — `Compat::disablePrism()`

```php
public function disablePrism(): void {
    $handles = ['prism-', 'code-highlight', 'highlight-', 'highlightjs-', 'sakurairo-prism', 'sakura-prism'];
    // 遍历所有已注册的 style/script，匹配前缀后 dequeue + deregister
}
```

**现状**：✅ 通过句柄名前缀匹配禁用。⚠️ 如果 Sakurairo 更新后更名句柄，此防御会失效。

---

### 5.2 MerPress / Githuber MD 资源接管

**防御**：`class-bac-compat.php` — `Compat::disableLegacyPluginAssets()`

```php
// 遍历所有已注册的 script/style，检查 src 是否包含 /githuber-md/ 或 /merpress/
// 匹配到的全部 dequeue + deregister
```

**现状**：✅ 已接管。旧插件只保留内容格式，前台渲染由 BAC 统一。

---

## 六、仍存在的隐患（未完全防御）

| # | 隐患 | Sakurairo 来源 | 影响 | 优先级 |
|---|------|--------------|------|--------|
| 1 | `* { transition: all 0.4s }` 仍影响 pre/table/blockquote/h2::after | `style.css:18` | 所有 CSS 变化附带 400ms 过渡 | 🟡 |
| 2 | `.entry-content ul/ol` 仍保留 `border: 1px solid #E4E4E4` | `sakura.css:29,49` | 亮色边框在暗底上可见（虽然颜色不突出） | 🟢 |
| 3 | `.entry-content h2::after` 仍有 Sakurairo 的 `transition: all 0.3s ease` | `sakura.css:86` | highlight bar 动画带额外过渡 | 🟢 |
| 4 | `.highlight-wrap:before` 的红绿灯装饰 | `sakura.css:197` | BAC 不输出此类名，但第三方插件可能输出 | 🟢 |

---

## 七、防御体系总览

```
Sakurairo 入侵层                    Arcaea 防御层
─────────────────────────────────────────────────────────────
* { transition: all 0.4s }          mermaid.css: .arcaea-mermaid-box * { transition: none !important }
body { text-shadow }                arcaea-article-content.css: text-shadow 重置
body { font-family/size }           mermaid.css + article-content: 每层显式声明
.entry-content p { color: #3d3d3d } article-content: color: var(--arcaea-text)
.entry-content h2::after { 主题色 } article-content: h2::after 用 Arcaea 渐变替换
.entry-content h3::after { "#" }    article-content: h3::after { content: none !important }
.entry-content tr:nth-child(even)   article-content: 全行覆盖 + body.dark 前缀
.entry-content .highlight-wrap      BAC normalizeCodeBlocks 不输出此 class
body.dark .entry-content p { #999 } article-content: body.dark .entry-content .arcaea-article-content p
body.dark .entry-content h1-h6      article-content: 同等特异性 + !important
body.dark .entry-content code       article-content: 覆盖背景色
Sakurairo Prism 模块                Compat::disablePrism() dequeue
MerPress / Githuber MD              Compat::disableLegacyPluginAssets() dequeue
foreignObject 继承污染              mermaid.css: all: initial 全重置
SVG overflow 裁切                   mermaid.css: overflow: visible
```
