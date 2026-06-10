# AGENTS.md — Sakurairo Arcaea 风格化方案

## 项目概述

Sakurairo 主题 + Arcaea 玻璃拟态风格 WordPress 博客的完整建站方案。三个 Git 子模块聚合为一个主仓库。

## 仓库结构

```
sakurairo-arcaea-styling/          ← 主仓库（聚合）
├── babel-arcaea-code/             ← 子模块：统一插件（Prism/Mermaid/Markmap/KaTeX）
├── sakurairo-arcaea-blog-skill/   ← 子模块：AI Agent 配置技能（含 CSS 规范/发布流程）
├── sakurairo-theme/               ← 子模块：Sakurairo v3.0.10 主题框架
└── tmp/                           ← 临时输出（gitignore 忽略）
```

子模块远程：

- `babel-arcaea-code` → <https://github.com/AKCX2002/babel-arcaea-code.git>
- `sakurairo-arcaea-blog-skill` → <https://github.com/AKCX2002/sakurairo-arcaea-blog-skill.git>
- `sakurairo-theme` → <https://github.com/AKCX2002/sakurairo-theme.git>

## 更新子模块

```bash
# 更新所有
git submodule update --remote --merge

# 更新单个
git submodule update --remote --merge <name>
```

## 在子模块中开发

```bash
cd <submodule>
git add -A && git commit -m "msg"
git push
cd ..
git add <submodule>
git commit -m "chore: bump <submodule>"
git push
```

## babel-arcaea-code 插件架构

```
Plugin::init() [Singleton]
  ├── self::$instance = $this   ← 必须在 loadModules() 首行（防止无限递归）
  ├── Options                   ← 默认值 + 合并 + 缓存
  ├── Detector                  ← save_post → 扫描 → 写入 post meta flag
  ├── Assets                    ← wp_enqueue_scripts → 条件加载
  ├── Renderer                  ← the_content filters (priority 0/11/12)
  ├── Markmap/MathJax/KaTeX     ← 预渲染 + 前端渲染
  ├── Compat                    ← 禁用 Sakurairo Prism + APlayer 空容器补丁
  ├── Abilities                 ← `wp_abilities_api_init` → 注册 `bac/*` WordPress abilities 供 MCP Adapter 发现/执行
  ├── Headers/Health/Blocks     ← 安全头 / 健康检查 / Gutenberg 块
  └── Admin                     ← 设置页面
```

### 渲染管线

| Filter | Priority | 职责 |
|--------|----------|------|
| `normalizeCodeBlocks` | 0 | 修复 Sakurairo 裸 `<pre>`，补 `language-xxx` |
| `protectKatex` | 0 | `$$…$$` → `<div class="katex-display">` 防 wpautop |
| `filterMermaid` | 11 | `<pre><code class="language-mermaid">` → `<div class="arcaea-mermaid-box"><pre class="mermaid">` |
| `filterLatexBlocks` | 11 | `language-katex/latex/mathjax/tex` 代码块 → `<div class="bac-latex-block">`，按 `latex_renderer` 选项选择 KaTeX 或 MathJax |
| `wrapBareMermaidPre` | 12 | 包裹 MerPress 裸 `<pre class="mermaid">` |

### KaTeX/MathJax 互斥

`katex_enabled` 和 `mathjax_enabled` 通过 Options 的 `latex_renderer` 字段互斥选择（`katex` 或 `mathjax`）。两者不会同时加载。内联公式 `$...$` 可能被 wpautop 破坏——当前插件只保护 `$$...$$`（display math）的 `protectKatex` 过滤。

### MCP / Abilities 集成

- `babel-arcaea-code` 现内置 `Abilities` 模块，在 `wp_abilities_api_init` 上注册 `bac/*` abilities，供 `wordpress/mcp-adapter` 默认 server 通过 `discover-abilities` / `execute-ability` 使用。
- 命名采用显式分组，不使用统一 `content_type` 抽象：`bac/posts/*`、`bac/pages/*`、`bac/media/*`、`bac/terms/*`、`bac/users/*`、`bac/comments/*`、`bac/plugins/*` 等。
- `meta.mcp.public = true` 只表示 MCP 可发现；执行层必须继续按当前 WordPress 用户的对象级 capability 校验内容、媒体、用户、评论、术语、meta 和插件操作。
- ability 层是纯数据层：保存文章时只接受原始 HTML / Gutenberg blocks，不注入 Mermaid 初始化脚本、不自动转换 Markdown、不包裹文章样式壳。
- 首版只服务当前 WordPress 站点，不实现 InstaWP 风格的多站点 `site-management`。

### Mermaid 防御体系（5 层）

| 层 | 文件 | 规则 | 目标 |
|----|------|------|------|
| 1 | `mermaid.css` | `.arcaea-mermaid-box` 显式 `font-family/font-size/color/text-shadow` | 阻断 Sakurairo 容器级继承 |
| 2 | `mermaid.css` | `.arcaea-mermaid-box * { transition: none !important }` | 阻断 `* { transition:all 0.4s }` 穿透 SVG |
| 3 | `mermaid.css` | `pre.mermaid foreignObject * { all: initial }` | SVG 内 foreignObject CSS 隔离 |
| 4 | `mermaid.css` | `.arcaea-mermaid-box { contain: layout paint }` | CSS containment 限制重排 |
| 5 | `mermaid-init.js` | 渲染后 `getBBox()` 逐节点裁剪 viewBox | 消除 Mermaid 生成的不可见边缘空白 |

### Mermaid 布局与可读性

- Mermaid 外层 `.arcaea-mermaid-box` 透明度要比普通玻璃卡片更深，当前采用约 `rgba(8,16,30,0.86)` 到 `rgba(6,12,24,0.84)` 的纵向渐变，避免背景图吃掉图表。
- Flowchart 节点文字容易和边框挤压；`mermaid-init.js` 的 `flowchart` 配置应保持较宽松：`padding: 14`、`nodeSpacing: 28`、`rankSpacing: 34`、`subGraphMargin: 18`。
- SVG 内节点文字需要明确 `line-height` 和少量 padding；对应 CSS 在 `mermaid.css` 的 `.node .label/.nodeLabel/foreignObject` 覆盖中维护。
- 不要在文章正文内手写 Mermaid 初始化或临时 CSS，避免和插件统一渲染路径竞态。

### JS Pjax 收缩保护

```javascript
// mermaid-init.js — applyResponsiveSvgSize()
if (hostWidth < 10) return;  // Pjax 过渡中容器不可见时跳过
```

---

## sakurairo-arcaea-blog-skill (v1.18.0)

安装路径：`~/.hermes/skills/sakurairo-arcaea-blog-skill/`

### 核心规范

- 常规博客文章：`.arcaea-article-content` 包裹 + 统一模板 CSS
- Hub/landing 页面：`.arcaea-wrap` (Arcaea Lite)
- Games/Music 页面：`.games-arcaea-wrap` + `bg-glow` + `bg-overlay`

### 禁止在文章正文中做的事

| 禁止 | 原因 |
|------|------|
| 内联 `window.mermaid.initialize()` / `mermaid.run()` / `unwrapMermaidCodeBlocks()` | 与插件二次接管，渲染错乱 |
| 内联 Mermaid 兼容 CSS（如 `.mermaid foreignObject *`） | 与插件 CSS 特异性竞跑 |
| 每篇新文章粘贴大段 `<style>` | CSS 应走统一模板/全局注入 |
| 用 Arcaea Lite (`.arcaea-wrap`) 写博客 | 博客用 `.arcaea-article-content` |
| `curl -u "user:pass"` | 凭证泄漏到 shell history |

### 发布流程（Python urllib + Application Password）

```python
# 新文章
data = json.dumps({"title":"T","slug":"s","content":html,"categories":[1],"status":"publish"}).encode()
urllib.request.urlopen(urllib.request.Request(f"{site}/wp-json/wp/v2/posts",data=data,headers=h,method="POST"))

# 更新已有 — 先 GET context=edit 拿 raw, 修改后 POST 回
req = urllib.request.Request(f"{site}/wp-json/wp/v2/posts/{id}?context=edit",headers=h)
raw = json.loads(urllib.request.urlopen(req).read())['content']['raw']
```

### Reference 文件

| 文件 | 用途 |
|------|------|
| `references/article-wrapper-css.md` | `.arcaea-article-content` 完整 CSS 模板 |
| `references/arcaea-lite-wrapper.md` | Hub 页面 Arcaea Lite CSS |
| `references/sakurairo-css-defenses.md` | **Sakurairo CSS 入侵防御对照表**（逐条源码级验证） |
| `references/publishing-python-pattern.md` | Python REST API 发布模板 |
| `references/mermaid-viewbox-root-cause.md` | Mermaid SVG viewBox 膨胀根因分析 |
| `references/mermaid-compatibility.md` | Mermaid style 语句兼容性（rgba 禁止等） |
| `references/prism-mermaid-conflict.md` | ⚠️ 历史参考，非当前实现 |
| `references/visual-tokens.md` | 11 变量设计 Token 体系 |

---

## 关键经验

### CSS 继承链阻断

Sakurairo 主题的全局规则会穿透到插件容器内。需要在每一层显式 reset：

- 容器级：`font-family/font-size/color/text-shadow`
- 子级：`transition: none !important`
- SVG 内：`all: initial` on foreignObject

### Mermaid 11.15+ 的 foreignObject

`htmlLabels: false` 对 flowchart 图不生效——Mermaid 11 内部总是用 `<foreignObject>` 绘制节点文字。必须依靠 CSS 隔离（第 3 层）而非指望 JS 选项关掉它。

### subgraph viewBox 膨胀

只有带多层 subgraph 的架构图才会触发（dagre 布局逐层放大边界框）。直线流程图不受影响。

### Pjax 收缩

Pjax 过渡时容器宽度为 0，`applyResponsiveSvgSize()` 会把 SVG 钉死在极小宽度。加 `hostWidth < 10` 的 early return 保护。

### 文章标题透明度

- `.arcaea-article-content h1` 使用 `background-clip: text` 的 SVG 纹理图片标题；不要用 `h1::before` 做装饰，也不要为了突出 H1 给整个 `.arcaea-article-content` 新增黑色背景壳层。
- Sakurairo 会用 `h1-h6::before` 做目录锚点占位。Arcaea 的 H2/H3/H4 视觉伪元素不能被末尾 guard 重新覆盖为 `height: 80px`。
- 如果标题看不清，只提高标题纹理、描边、drop-shadow 或标题光带的不透明度；正文 wrapper 保持透明，不额外制造大面积黑底。
- 需要 Games 风格的文章开头时，用 `.arcaea-title-hero` 结构：左侧 `.arcaea-title-main h1`，下方 `.arcaea-title-quote span`，右下 `.arcaea-title-tags li`。不要指望裸 `h1` 自动生成引文或 TAG。

---

## 工作流约定

1. **改 skill 先改 repo，再同步到 `~/.hermes/skills/`**
2. **CSS 的 source of truth 在 reference 文件**，不在 SKILL.md 中重复粘贴
3. **子模块提交顺序**：先子模块 push → 再主仓库 bump 指针 + push
4. **不要往文章正文放任何 Mermaid 调试脚本**——渲染统一交给插件
5. **新文章模板**：`.arcaea-article-content` 包裹 + 代码块带 `language-xxx` + excerpt 字段

---

## ⚠️ 技能系统性审查报告（2026-06-03）

> 以下内容基于 SKILL.md v1.18.0 + references/ 全量 + babel-arcaea-code 插件 v1.6.0 源码 + Sakurairo 3.0.10 源码的逐文件对比审查。

### 发现总览

| 类别 | 数量 | 严重性 |
|------|------|--------|
| 严重误导性内容 | 3 | 🔴 1, 🟡 2 |
| 版本漂移（Reference vs 生产） | 5 | 🟡 3, 🟢 2 |
| 结构问题 | 4 | 🟡 2, 🟢 2 |
| SAKURAiro 主题交互隐患 | 2 | 🔴 1, 🟡 1 |

### 🔴 P0：CSS Token 声明与实际生产代码完全不符

SKILL.md `## Arcaea Visual Rules > Minimal Token Direction` 中的变量：

```css
--c-primary: #dbe8ff; --c-accent: #9db4ff;
--c-skyblue: #8ad8ff; --c-violet: #c7b6ff;
--bg-deep: #05070b; --bg-mid: #0b1020;
--bg-surface: #111827; --bg-dark: #09090f;
```

**这些变量从未在任何生产 CSS 中使用。** 实际 `.arcaea-article-content` 使用 `--arcaea-*` 命名空间（25+ 变量），如 `--arcaea-bg-main: #0a1220`、`--arcaea-accent-light: #5fd4ff` 等。

**行动**：此段应立即删除，替换为指向 `babel-arcaea-code/assets/reading/arcaea-article-content.css` 的引用。

### 🟡 Reference 文件漂移（3 个位置互相不一致）

同一组 CSS 规则分布在三个位置且互相不一致：

| 位置 | 状态 | 用途 |
|------|------|------|
| `babel-arcaea-code/assets/reading/arcaea-article-content.css` | ✅ **Source of Truth** | 被执行的生产代码 |
| `references/article-wrapper-css.md` | ❌ 60%+ 变量值漂移 | 应改为简短说明 + 指针 |
| `references/visual-tokens.md` | ⚠️ 缺少 10+ 个变量 | 应同步生产 CSS |

具体差异（article-wrapper-css.md vs 实际 CSS）：

- `--arcaea-border`: `rgba(214,226,245,0.28)` vs `rgba(120,160,220,0.18)`
- `--arcaea-heading`: `rgba(243,247,255,0.95)` vs `#f2f6fc`
- `--arcaea-accent`: `rgba(173,194,245,0.82)` vs `rgba(95,212,255,0.84)`
- H2 `::after`：reference 中设为 `display: none !important`，实际 CSS 使用 Highlight bar 动画

### 🟡 渲染管线遗漏

AGENTS.md 现有渲染表中缺少 `filterLatexBlocks`（Priority 11）的完整描述。该过滤处理 ````katex/latex/mathjax 代码块的转换，是渲染管线中重要的一环。

### 🟡 KaTeX/MathJax 互斥关系未说明

`katex_enabled` 和 `mathjax_enabled` 在 Options 中通过 `latex_renderer` 互斥选择，AGENTS.md/SKILL.md 均未记载。内联公式 `$...$` 可能被 wpautop 破坏——当前插件只保护 `$$...$$`（display math）。

### 🟡 SAKURAiro `* { transition: all 0.4s }` 仍为全局隐患

Sakurairo `style.css` 第 18 行的 `* { transition: all 0.4s }` 会穿透到所有插件容器。当前：

- Mermaid SVG 内部有 `!important` 阻断（第 2 层防御）✅
- Prism 代码块、表格、blockquote 等其他元素无此防御 ❌
- 导致 `::before`/`::after` 伪元素变化都附带 400ms 过渡

### 🟡 SKILL.md 中 AI Excerpt 描述不准确

> "AI Excerpt can be generated through Sakurairo REST endpoints after publish"

实际 Sakurairo 的 AI 摘要功能（`inc/chatgpt/`）需要用户自行配置 OpenAI API key，不是一个开箱即用的 REST 端点。未配置 key 时调用会直接失败。

### 🟢 References 分类优化建议

| 文件 | 建议 |
|------|------|
| `article-wrapper-css.md` | 标记为「历史参考」，删除重复 CSS 块 |
| `prism-mermaid-conflict.md` | 已标注「非当前实现」，可归档 |
| `mermaid-viewbox-root-cause.md` | 保持现状（内容完善） |
| `publishing-python-pattern.md` | 替换 `babel36acl.xyz` 为 `example.com` |

### 完整审查报告

详细分析见 `tmp/skill-review-report-v1.18.0.md`。
