---
name: sakurairo-arcaea-blog-skill
description: Use when working on a Sakurairo-based WordPress blog that needs Arcaea-style page design, article packaging, theme conflict fixes, code block rendering fixes, or safe WordPress draft/publish updates.
version: 1.18.0
---

# Sakurairo Arcaea Blog Skill

## Purpose

Use this skill for one of four task types:

1. Write or polish a technical blog post for a Sakurairo site
2. Build an Arcaea-styled article page or landing page
3. Fix Sakurairo / Prism / Mermaid / blockquote / wrapper conflicts
4. Safely create or update WordPress content through REST API

This file is the primary workflow. `references/` are optional deep material, not hard dependencies.

## Local Skill Bindings

When this skill is used in a local agent environment, treat the following installed skills under `/root/.agents/skills` as the default companion set.

### Priority Set For This Repository

These are the most relevant local skills for this repository and should be checked first:

- `sakurairo-arcaea-blog-skill`
- `blog-post`
- `blog-writing-guide`
- `technical-blog-writing`
- `sakurairo-theme`
- `wordpress-pro`

### Skill Groups

#### Direct blog writing

- `blog-post`
- `blog-writing-guide`
- `technical-blog-writing`
- `sakurairo-arcaea-blog-skill`

#### Writing and content production

- `copywriting`
- `writing-fragments`
- `writing-plans`
- `writing-skills`
- `tech-doc-style-chinese`
- `gws-docs-write`
- `doc-coauthoring`

#### Markdown and document processing

- `obsidian-markdown`
- `baoyu-format-markdown`
- `baoyu-markdown-to-html`
- `baoyu-url-to-markdown`
- `baoyu-danger-x-to-markdown`
- `docs-changelog`
- `code-documenter`
- `api-documentation-generator`
- `docx`

#### Blog site, theme, and presentation layer

- `sakurairo-theme`
- `theme-factory`
- `wordpress-pro`
- `website-to-hyperframes`
- `web-design-guidelines`
- `modern-web-design`
- `frontend-design`

### Binding Rules

Apply these bindings by task type:

1. For article drafting, load `blog-post`, `blog-writing-guide`, and `technical-blog-writing`.
2. For Chinese technical polish, load `tech-doc-style-chinese` first, then add `copywriting` only if tone adjustment is needed.
3. For outline-first or fragmented ideation workflows, load `writing-fragments` and `writing-plans`.
4. For Markdown to publishable HTML flows, load `baoyu-format-markdown` and `baoyu-markdown-to-html`.
5. For WordPress publishing, theme behavior, shortcode behavior, or site-level content structure, load `sakurairo-theme` and `wordpress-pro`.
6. For page visual redesign, add `frontend-design`; only escalate to `theme-factory` or `modern-web-design` when the task is broader than a normal blog page.

### Installation Assumption

Assume these skills are installed locally at:

```text
/root/.agents/skills/<skill-name>/SKILL.md
```

If a named companion skill is missing, continue with this file as the primary authority and only degrade the missing capability area, not the whole workflow.

## Fast Routing

Choose the path first. Do not mix page wrappers or publishing modes.

| Task | Default wrapper | Output form |
|---|---|---|
| Technical article / long-form post | `.arcaea-article-content` | Single HTML body |
| Hub / landing / about / toolbox page | `.arcaea-wrap` | Single HTML body |
| Games / Music showcase page | `.games-arcaea-wrap` | Single HTML body |
| Existing post repair | Keep current wrapper unless wrong | Minimal patch |
| WordPress publish/update | Keep article wrapper choice above | `content.raw` update |

## P0 Rules

1. Default to `draft`. Only use `publish` when the user explicitly asks to publish.
2. Never use `curl -u "user:pass"` for WordPress. Use Python `urllib` with Application Password in memory.
3. Never write WordPress credentials into repo files, scripts, or the skill.
4. When editing an existing post or page, fetch `?context=edit` and modify `content.raw`, never `content.rendered`.
5. For batch changes: dry-run summary first, backup original raw, default limit `3`, then execute.
6. Before delete, show `title`, `slug`, and `status`, then wait for confirmation.
7. If exact site state is unknown, inspect first. Do not invent current wrapper classes or plugin state.

## Core Writing Standard

Apply these rules to every technical article.

### Opening

- Start with a real problem, hard conclusion, or engineering tension.
- Do not start with company history, hype, or “本文将介绍”.
- Add one `TL;DR` paragraph after the opening when the article is long.

### Structure

Pick one structure and stay consistent.

| Type | Required sections |
|---|---|
| Tutorial | Result first, prerequisites, step-by-step build, complete code, next steps |
| Deep dive | Why it matters, simple mental model, detailed mechanics, real example, trade-offs, limitations |
| Architecture | Problem, constraints, options considered, chosen architecture, trade-offs, lessons |
| Benchmark | What was compared, methodology, results, analysis, recommendation, reproducibility |
| Postmortem | Summary, timeline, root cause, fix, prevention, lessons learned |

### Developer Quality Bar

- Numbers beat adjectives. Write `p99 from 340 ms to 45 ms`, not “显著优化”.
- Explain trade-offs and failed attempts.
- Code blocks should be real, attributable, and path-labeled when possible.
- If a system has more than two interacting parts, include a diagram.
- If the article contains claims, make them verifiable.

### Voice

- Direct, specific, technical.
- No buzzwords, no corporate tone, no empty slogans.
- Keep personality in the body, not only in the opening and closing.

### Banned Patterns

- `赋能` `抓手` `闭环` `沉淀` `打通`
- “我们很高兴宣布”
- “在当今快速发展的技术世界里”
- “显著提升” without numbers
- “这很简单” / “只需”
- three-beat AI rhetoric like “不是 A，不是 B，而是 C”

## Chinese Technical Writing Rules

1. Add spaces between CJK and English or numbers in visible prose: `支持 JSON 格式`。
2. Use `「」` in Chinese visible text, not straight quotes.
3. Do not address the reader as `你` or `您`.
4. Keep correct casing: `CMake`, `FreeRTOS`, `STM32`, `HTTP`, `JSON`, `API`, `AI`, `LLM`, `RAG`.
5. Fix common mistakes: `阀值 -> 阈值`, `布署 -> 部署`, `配制 -> 配置`, `登陆 -> 登录`.
6. Do not apply spacing or typography rules inside code, paths, URLs, JSON, shell commands, or identifiers.

## Wrapper Selection

This is the most important layout decision.

### `.arcaea-article-content`

Use for normal blog posts and long technical articles.

- Reading-first
- Stable headings, lists, tables, code blocks
- Local CSS variable scope only inside the wrapper
- Default shared stylesheet lives at `../babel-arcaea-code/assets/reading/arcaea-article-content.css`

### `.arcaea-wrap`

Use for hub, landing, about, toolbox, or lighter content pages.

- Lighter visual shell
- Good for mixed blocks and short sections
- Do not use it as the default wrapper for long technical posts

### `.games-arcaea-wrap`

Use for full showcase pages such as Games or Music.

- Supports glow, overlay, hero, category cards
- This is page-level presentation, not article-body styling

## Arcaea Visual Rules

Use these style constraints even when writing custom CSS.

1. Arcaea is cold, sparse, restrained, and low-saturation. Not neon cyberpunk.
2. Prefer many light glass layers, not one giant glass slab.
3. Visual weight should increase from outer section to inner card.
4. Strong red, fluorescent green, rainbow gradients, and over-bright blue are forbidden.
5. Reading surfaces must stay darker and more solid than outer containers.
6. For technical articles, readability beats atmosphere. Arcaea is the tone, not the excuse to make tables hard to read.

### Token Reference

All design tokens are defined and maintained in the production CSS:

`babel-arcaea-code/assets/reading/arcaea-article-content.css`

The canonical token namespace is `--arcaea-*` (25+ variables). Do **not** use `--c-primary`, `--bg-deep`, or any other invented namespace. See `references/visual-tokens.md` for a human-readable summary of the current token values.

### Non-Negotiable CSS Behaviors

- Scope variables inside the wrapper, not global `:root`, unless the task is explicitly full-page skinning.
- Blockquotes need explicit override because Sakurairo may inject unwanted decoration.
- The `#` marker for headings/cards should come from `::before`, never from stray text nodes.
- Glass tables belong on the wrapper or table container, not on a broken raw table setup that kills readability.
- Default article tables should use low-grid comparison styling; function or module breakdowns should use `table.arcaea-feature-matrix`.
- Do not make line numbers louder than purpose text. Row hierarchy should read: function name → purpose → signature → source line.

## Sakurairo Theme Integration

When the task touches theme behavior, assume these defaults:

1. Prefer Sakurairo content style plus Arcaea override, not GitHub style plus extra patching.
2. Use the theme’s automatic TOC when the article has meaningful `h2` / `h3` structure.
3. AI Excerpt is optional. Sakurairo's AI summary feature (`inc/chatgpt/`) requires the site owner to configure an OpenAI-compatible API key in theme options. It is not an out-of-the-box REST endpoint — calls will fail silently if no key is configured.
4. Category / tag images, exhibition blocks, and homepage components belong to theme configuration, not article CSS.

## Babel Arcaea Code Integration

Use `babel-arcaea-code` as the default rendering stack when available.

What it should own:

- Prism highlighting
- Mermaid rendering
- MathJax / KaTeX rendering
- Markmap rendering
- Shared article wrapper stylesheet for `.arcaea-article-content`

Do not duplicate plugin-owned front-end CSS inline unless:

1. The site does not have the plugin enabled
2. The task is a one-off external HTML artifact
3. You are testing a temporary patch before upstreaming it

## Article Assembly Pattern

For WordPress technical posts, default to a single HTML body:

```html
<div class="arcaea-article-content">
  <p><strong>TL;DR：</strong>...</p>
  <h2>...</h2>
  <p>...</p>
  <pre><code class="language-cmake"># path/to/file.cmake
...</code></pre>
</div>
```

Rules:

1. Prefer one HTML artifact, not `post.md + index.html` split publishing.
2. If plugin shared CSS is available, keep the body clean and avoid repeating full inline style blocks.
3. If inline CSS is required, keep it local to the wrapper.

## WordPress Publish Flow

Use this sequence for create or update.

1. Determine target type: `posts` or `pages`.
2. Build the body with the correct wrapper.
3. If updating, fetch current raw content with `context=edit`.
4. Prepare a draft payload first.
5. Validate wrapper, code blocks, and obvious rendering markers before pushing.
6. Publish only on explicit instruction.

### Safe Python Pattern

```python
import base64
import json
import urllib.request

site = "https://example.com"
user = "username"
app_password = "xxxx xxxx xxxx xxxx xxxx xxxx"
auth = base64.b64encode(f"{user}:{app_password}".encode()).decode()

payload = {
    "title": "Article Title",
    "status": "draft",
    "content": "<div class=\"arcaea-article-content\">...</div>",
}

req = urllib.request.Request(
    f"{site}/wp-json/wp/v2/posts",
    data=json.dumps(payload).encode(),
    headers={
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
    },
)
```

Do not store credentials in committed files. Move them to environment variables or local ignored config when executing.

## Validation Checklist

Before finishing, verify the relevant subset of these checks.

1. Wrapper class is correct for the content type.
2. No accidental global CSS pollution.
3. Headings have meaningful structure and TOC-friendly hierarchy.
4. `<pre>` code blocks remain visible and readable.
5. Mermaid / Prism / Math rendering is not broken by wrapper CSS.
6. Blockquote overrides suppress unwanted theme ornaments.
7. Article tone is direct and technical, not marketing-heavy.
8. Chinese typography and terminology are consistent.
9. If publishing, response is success and the saved content still contains the intended wrapper.

## Common Failure Modes

### Wrong wrapper

- Long article wrapped in `.arcaea-wrap`
- Showcase page wrapped in `.arcaea-article-content`

Fix by switching wrapper before touching detailed CSS.

### Global bleed

- Variables declared globally
- `body`, raw `h1`, raw `p` selectors used for article-local styling

Fix by rescoping to the wrapper.

### Theme conflict

- Sakurairo blockquote icons or decoration leak into Arcaea cards
- GitHub content style washes out the dark reading surface
- `body.dark .entry-content` color rules override Arcaea text colors
- `* { transition: all 0.4s }` bleeds into all pseudo-element animations

Fix by forcing wrapper-scoped overrides and preferring the Sakura content style baseline.
For a per-rule defense matrix, see `references/sakurairo-css-defenses.md`.

### Render stack conflict

- Mermaid or Prism styles duplicated inline
- Plugin already owns the same responsibility

Fix by deferring to `babel-arcaea-code` unless this is an explicit temporary patch.

## Optional Deep References

Open these only if the task needs exact source material:

- `references/article-wrapper-css.md` for the long article wrapper CSS template
- `references/visual-tokens.md` for exact tokens and page-level style direction
- `references/sakurairo-css-defenses.md` for Sakurairo CSS invasion defense matrix (per-rule source-level verification)
- `references/table-techniques.md` for Arcaea technical-document table patterns
- `references/publishing-python-pattern.md` for fuller WordPress API examples
- `references/mermaid-viewbox-root-cause.md` for Mermaid SVG viewBox inflation root cause analysis
- `references/troubleshooting.md` for Mermaid / Prism / wrapper debugging cases

The default expectation is that this file alone is enough to route and execute normal Arcaea blog tasks.
