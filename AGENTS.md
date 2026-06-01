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
- `babel-arcaea-code` → https://github.com/AKCX2002/babel-arcaea-code.git
- `sakurairo-arcaea-blog-skill` → https://github.com/AKCX2002/sakurairo-arcaea-blog-skill.git
- `sakurairo-theme` → https://github.com/AKCX2002/sakurairo-theme.git

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
  ├── Headers/Health/Blocks     ← 安全头 / 健康检查 / Gutenberg 块
  └── Admin                     ← 设置页面
```

### 渲染管线

| Filter | Priority | 职责 |
|--------|----------|------|
| `normalizeCodeBlocks` | 0 | 修复 Sakurairo 裸 `<pre>`，补 `language-xxx` |
| `protectKatex` | 0 | `$$…$$` → `<div class="katex-display">` 防 wpautop |
| `filterMermaid` | 11 | `<pre><code class="language-mermaid">` → `<div class="arcaea-mermaid-box"><pre class="mermaid">` |
| `wrapBareMermaidPre` | 12 | 包裹 MerPress 裸 `<pre class="mermaid">` |
| `filterLatexBlocks` | 11 | LaTeX 代码块转换 |

### Mermaid 防御体系（5 层）

| 层 | 文件 | 规则 | 目标 |
|----|------|------|------|
| 1 | `mermaid.css` | `.arcaea-mermaid-box` 显式 `font-family/font-size/color/text-shadow` | 阻断 Sakurairo 容器级继承 |
| 2 | `mermaid.css` | `.arcaea-mermaid-box * { transition: none !important }` | 阻断 `* { transition:all 0.4s }` 穿透 SVG |
| 3 | `mermaid.css` | `pre.mermaid foreignObject * { all: initial }` | SVG 内 foreignObject CSS 隔离 |
| 4 | `mermaid.css` | `.arcaea-mermaid-box { contain: layout paint }` | CSS containment 限制重排 |
| 5 | `mermaid-init.js` | 渲染后 `getBBox()` 逐节点裁剪 viewBox | 消除 Mermaid 生成的不可见边缘空白 |

### JS Pjax 收缩保护

```javascript
// mermaid-init.js — applyResponsiveSvgSize()
if (hostWidth < 10) return;  // Pjax 过渡中容器不可见时跳过
```

---

## sakurairo-arcaea-blog-skill (v1.14.0)

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

---

## 工作流约定

1. **改 skill 先改 repo，再同步到 `~/.hermes/skills/`**
2. **CSS 的 source of truth 在 reference 文件**，不在 SKILL.md 中重复粘贴
3. **子模块提交顺序**：先子模块 push → 再主仓库 bump 指针 + push
4. **不要往文章正文放任何 Mermaid 调试脚本**——渲染统一交给插件
5. **新文章模板**：`.arcaea-article-content` 包裹 + 代码块带 `language-xxx` + excerpt 字段
