# Mermaid Style 语句兼容性参考

## 概述

Mermaid 的 `style` 语句不是浏览器 CSS 解析器。在 WordPress + Sakurairo + Mermaid 11.x 环境下，`style` 仅支持有限的属性和值。本文档汇总了实际踩坑中发现的 6 个常见问题及其修复方案。

---

## 1. `rgba()` 逗号被 Mermaid 解析为 style 属性分隔符

**现象**：

```
Parse error on line XX:
...stroke:rgba(255,145,145,0.55),c
-----------------------^
Expecting ...
```

**根因**：Mermaid Parser 将 `rgba(255,145,145,0.55)` 内部的逗号识别为 style 属性之间的分隔符，导致后续解析失败。

**错误写法**：
```mermaid
style PART6 fill:transparent,stroke:rgba(255,145,145,0.55),color:#eef4ff
```

**修复**：改为 6 位或 8 位 HEX，透明度值直接嵌入颜色。
```mermaid
style PART6 fill:transparent,stroke:#ff9191,color:#eef4ff
```

**规范**：Mermaid `style` 语句中禁止使用以下 CSS 函数：
- `rgba()` → 改用 `#RRGGBB` 或 `#RRGGBBAA`
- `hsla()` → 改用 HEX
- `calc()` → 计算后写入固定值
- `var()` → 直接使用实际值

---

## 2. HTML 标签（`<br/>`）被 WordPress 提前处理

**现象**：节点文本中的换行标签被 WordPress 的 wpautop 或 Markdown 解析器提前处理，导致 Mermaid 收到的源码中 `<br/>` 已损坏。

**注意**：部分 Mermaid 版本支持 `<br/>` 换行，部分仅支持 `<br>`（非自闭合）。在 WordPress 环境下，`<br/>` 极易被误处理。

**推荐写法**：
```mermaid
CH1["第一章\n启动流程"]
```
或统一使用 `<br>`（非自闭合）：
```mermaid
CH1["第一章<br>启动流程"]
```

**结论**：避免 `<br/>` 自闭合形式，优先使用 `\n` 或 `<br>`。

---

## 3. 节点 ID 含特殊字符

**现象**：节点 ID 中包含 `-`、`(`、`)`、`.`、`/` 等字符时，Mermaid 将它们解析为语法元素（如连线、圆角节点标记、子图分隔符等）。

**错误示例**：
```mermaid
A-B["节点"]          # - 被解析为连线符号
CPU(0)["节点"]       # () 被解析为圆角节点
UART/DMA["节点"]     # / 被解析为路径分隔符
```

**修复**：ID 严格限制为以下字符集：
- `A-Z`（大写字母）
- `a-z`（小写字母）
- `0-9`（数字）
- `_`（下划线）

```mermaid
CPU0["Core0"]
UART_DMA["UART + DMA"]
SOC_REG["soc/ip 寄存器"]
HPM_SDK_LIB["HPM_SDK_LIB"]
```

**额外注意**：节点 ID 不能以数字开头（某些 Mermaid 版本有此限制）。推荐格式：`大写字母 + 数字 + _`。

---

## 4. WordPress 破坏 Mermaid 代码块结构

**现象**：Mermaid 代码块在页面中显示为纯文本或空白框，JS 未执行渲染。

**根因**：WordPress 将 ` ```mermaid ` 围栏代码块转换为 `<pre><code>` 标签，Mermaid JS 的 `mermaid.run()` 默认查找 `.mermaid` 类选择器，找不到目标元素。

**这是 babel-arcaea-code 插件的核心职责**：在 PHP 服务端（`the_content` filter priority 11）用 `preg_replace_callback` 将 `<pre><code class="language-mermaid">` 替换为 `<div class="arcaea-mermaid-box"><pre class="mermaid">...</pre></div>`。

**诊断方法**：
1. 打开页面，查看 HTML 源码
2. 搜索 `language-mermaid`
3. 如果存在 → PHP filter 未生效（插件未启用或 filter 执行顺序问题）
4. 如果不存在且页面里能看到 `.arcaea-mermaid-box > pre.mermaid`（或已渲染出的 SVG）→ filter 正常工作

**禁止发布到文章正文的做法**：

不要在文章内容里内联任何 Mermaid 前端兜底脚本，例如：

```js
document.querySelectorAll('pre code.language-mermaid')
window.mermaid.initialize(...)
window.mermaid.run(...)
```

这些脚本只适合临时本地调试。一旦正文里同时存在 `babel-arcaea-code` 插件和旧兜底脚本，就会出现二次接管：

1. 插件先把 `language-mermaid` 代码块转换并渲染
2. 正文残留脚本再次扫描 `.mermaid`
3. 旧脚本用不同配置重新 `initialize()` / `run()`
4. 最终出现布局错乱、图被重复包裹、viewBox 异常放大

**唯一允许的正式方案**：只保留 Mermaid 源码块（```` ```mermaid ```` 或 `[mermaid]`），前端渲染全部交给 `babel-arcaea-code`。

---

## 5. Sakurairo 主题 CSS 污染 `foreignObject`

**现象**：Mermaid 节点尺寸异常、SVG viewBox 被纵向拉长、流程图整体变形。

**根因**：Sakurairo 主题的全局样式规则（如 `.entry-content div { font-size: 24px; }`）穿透到 Mermaid SVG 内部的 `foreignObject` 元素，导致节点内的 HTML 文本被放大。

**修复**：如果只是做本地样式实验，可临时在文章包裹层 CSS 中限制 Mermaid 渲染区域：
```css
.mermaid foreignObject * {
    font-size: 14px !important;
    line-height: 1.4 !important;
}
```

但正式发布时，不要把这类 Mermaid 兼容 CSS 零散复制进文章正文。应优先：

1. 修插件渲染逻辑
2. 修主题通用样式污染
3. 保持文章正文只包含内容，不包含 Mermaid 临时补丁脚本

此规则如果确实需要长期保留，应收敛到统一模板或插件样式中，而不是散落在单篇文章里。

---

## 6. `transparent` 关键字兼容性

**现象**：`fill:transparent` 在某些 Mermaid 版本或主题下渲染为黑色背景或不生效。

**根因**：Mermaid 11.x 的 `theme: "base"` 模式下，`transparent` 关键字的处理行为不一致——部分版本正确渲染为透明，部分版本回退为默认背景色（黑色）。

**推荐做法**：统一使用 8 位 HEX 或 `none`：
```mermaid
style A fill:#00000000,stroke:#9db4ff,color:#eef4ff
```
或：
```mermaid
style A fill:none,stroke:#9db4ff,color:#eef4ff
```

---

## 发布前检查清单

在发布包含 Mermaid 图表的文章前，对全文执行以下搜索：

| 搜索项 | 查找模式 | 替换为 | 优先级 |
|--------|---------|--------|--------|
| `rgba(` | CSS 颜色函数 | HEX: `#RRGGBB` | P0 阻断 |
| `transparent` + `fill:` | 颜色关键字 | `#00000000` 或 `none` | P1 高 |
| style 行中 `(` | 可能的 CSS 函数 | 手动检查，改为 HEX | P1 高 |
| 节点 ID 含 `-` `/` `(` `)` | 特殊字符 | `_` 替代 | P1 高 |
| `<br/>` | HTML 自闭合换行 | `<br>` 或 `\n` | P2 中 |

---

## 最终规范

在 WordPress + Sakurairo + Mermaid 11.x + `theme: "base"` 环境下，Mermaid style 语句应严格遵循：

```mermaid
style NODE_ID fill:#00000000,stroke:#9db4ff,color:#eef4ff
```

**允许的值类型**：
- 颜色：`#RRGGBB` 或 `#RRGGBBAA`（8 位 HEX 带透明度）
- 关键字：`none`（推荐）、`transparent`（不推荐，兼容性不稳定）
- 属性：`fill`、`stroke`、`color`、`stroke-width`、`stroke-dasharray`

**禁止的值类型**：
- CSS 函数：`rgba()`、`hsla()`、`calc()`、`var()`
- 复杂表达式：`linear-gradient()`、`radial-gradient()`

> Mermaid 不是浏览器 CSS 解析器。`style` 语句只支持非常有限的属性和值。统一使用 HEX 颜色、简单节点 ID、避免 CSS 函数是兼容性最高的策略。
