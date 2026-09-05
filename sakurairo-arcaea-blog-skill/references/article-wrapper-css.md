# Arcaea Article Wrapper CSS

> ⚠️ **历史参考**：此文件中的 CSS 代码块是早期快照，与生产代码存在 60%+ 的变量值漂移。
> **Source of Truth** 是 `babel-arcaea-code/assets/reading/arcaea-article-content.css`。
> 本文保留设计原则、决策树、表格策略和 arcaea-title-hero 结构说明——这些仍然适用。
> Token 值请查阅 `references/visual-tokens.md`。

统一 Arcaea 文章阅读风格。目标是保留冷色、漂浮、轻玻璃的气质，同时优先保证长文可读性、表格稳定性和局部作用域安全。

## 设计原则

- 阅读优先：正文、列表、表格不能被装饰性效果抢走层级
- 局部作用域：变量放在 `.arcaea-article-content`，不要从 `:root` 污染整页
- 低饱和强调：只保留少量冰蓝/冷白，不使用突兀红色 marker
- 稳定优先：不要在原生 `<table>` 上直接叠 `overflow: hidden` + `backdrop-filter`
- 文档优先：Arcaea 是气质，不是牺牲表格可读性的理由

## Wrapper 选择决策树

```
写博客文章 / 技术长文    → .arcaea-article-content（本文模板）
Hub / Landing 页面       → .arcaea-wrap（arcaea-lite-wrapper.md）
Games / Music 分类页     → .games-arcaea-wrap + bg-glow + bg-overlay
站外分享 / 独立页面      → 单一 HTML + <style> 内联
```

**绝对禁止**：用 `.arcaea-wrap` 写博客文章正文。`.arcaea-wrap` 是 Hub/landing 页的轻量包裹，不具备长文阅读的稳定性。博客正文必须使用 `.arcaea-article-content`。

**禁止**：将一篇文章拆成 `post.md` + `index.html` 两个文件。正确做法是单一 HTML 文件，`<style>` 块在 `<div class="arcaea-article-content">` 之前。

## 使用方式

常规文章优先复用这份统一模板，不要为每篇文章各自发明一套内联样式。正文结构建议收敛为：

```html
<style>
/* 仅在当前发布链路还不能复用共享模板时，才保留这段局部 CSS */
</style>
<div class="arcaea-article-content">

<!-- 原始文章内容 -->

</div>
```

如果文章开头需要 Games 风格的“左侧标题 + 引文 + 右下 TAG”构图，使用：

```html
<header class="arcaea-title-hero">
  <div class="arcaea-title-main">
    <h1><span class="arcaea-title-icon">🎮</span>Games</h1>
  </div>
  <p class="arcaea-title-quote">
    <span>游戏对我来说，并不只是「消遣」。<br>
    更像是一种：情绪共鸣、世界观沉浸、<br>
    孤独探索、系统体验、抽象叙事的集合。</span>
  </p>
  <ul class="arcaea-title-tags">
    <li>废墟文明</li>
    <li>数字空间</li>
    <li>孤独感</li>
    <li>Meta</li>
    <li>存在主义</li>
    <li>碎片化叙事</li>
    <li>系统深度</li>
    <li>超现实</li>
  </ul>
</header>
```

当前仓库已经将这份样式收敛到共享资产 `../babel-arcaea-code/assets/reading/arcaea-article-content.css`。如果发布环境启用了 `babel-arcaea-code`，文章正文应尽量只保留 `.arcaea-article-content` 包裹和内容本身，避免重复内联整段 CSS。

## 表格策略

长文默认有两种表格形态：

1. **普通对比表**：用于概念对比、参数说明、约束清单
2. **功能矩阵**（`arcaea-feature-matrix`）：用于函数模式、模块职责、源码签名索引

普通对比表回退到旧版 skill 样式：表格外壳使用 `var(--arcaea-bg)` 玻璃底、`var(--arcaea-border)` 边框和轻 blur，表头使用 `rgba(164, 186, 236, 0.10)` 弱高亮；保持强表头、弱网格、轻奇偶行，不做首列光标、轨道光条或高透明重玻璃。

普通技术对比表优先按 4 列阅读模型处理：层次/对象列 18%、说明列 42%、方法/工具列 25%、状态列 15%。如果 Markdown 生成了空的首列表头占位，生产 CSS 会隐藏该空表头，使正文四列与「层次 / 方法 / 工具 / 当前状态」重新对齐。

功能矩阵使用 `table.arcaea-feature-matrix`，并在单元格内部配合这些类名：

- `.func-name`
- `.signature`
- `.line-badge`
- `.purpose`
- `.purpose-title`
- `.purpose-tag`

如果一张表已经同时出现函数名、签名、行号、用途四类信息，就不要再把它当普通 `<table>` 处理。

## 推荐版 CSS

> **此节已不再维护。** 完整且最新的 CSS 在生产代码中：
> `babel-arcaea-code/assets/reading/arcaea-article-content.css`
>
> 下面保留的设计原则、决策树、表格策略和 arcaea-title-hero 结构说明仍然适用。
> Token 值请查阅 `references/visual-tokens.md`。

推荐发布流程：

1. 正文中只保留 `.arcaea-article-content` 包裹和内容，不内联 CSS。
2. 共享样式由 `babel-arcaea-code` 插件自动注入。
3. 任何颜色或表格调整，先改生产 CSS（`assets/reading/arcaea-article-content.css`），再同步 `visual-tokens.md`。

## arcaea-title-hero 结构

如果文章开头需要 Games 风格的"左侧标题 + 引文 + 右下 TAG"构图，使用：

```html
<header class="arcaea-title-hero">
  <div class="arcaea-title-main">
    <h1><span class="arcaea-title-icon">🎮</span>Games</h1>
  </div>
  <p class="arcaea-title-quote">
    <span>游戏对我来说，并不只是「消遣」。</span>
  </p>
  <ul class="arcaea-title-tags">
    <li>废墟文明</li>
    <li>数字空间</li>
    <li>孤独感</li>
  </ul>
</header>
```

CSS 样式定义在生产 CSS 的 `.arcaea-title-hero` 系列选择器中。

## Mermaid 图表样式

Mermaid 图表渲染样式由 `babel-arcaea-code` 插件自动加载（`assets/mermaid/mermaid.css`），无需在文章正文中重复定义。

**不要在文章正文中粘贴或复制这些样式。** 正文只保留 Mermaid 源码块，渲染统一交给插件。
