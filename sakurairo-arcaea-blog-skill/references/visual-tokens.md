# Arcaea Visual Design Tokens

> **Source of Truth**: `babel-arcaea-code/assets/reading/arcaea-article-content.css`

This reference captures the design values used across Arcaea-styled pages and articles on the blog, with article-reading stability prioritized over decorative intensity.

## Article Wrapper Tokens (`.arcaea-article-content`)

Applied to blog post wrapper templates centered on `.arcaea-article-content`. Prefer a shared wrapper/template asset over per-post inline `<style>` blocks, and keep variables scoped to `.arcaea-article-content` instead of `:root`.

| Token | Value | Usage |
|-------|-------|-------|
| `--arcaea-bg-main` | `#0a1220` | Deepest reading background |
| `--arcaea-bg-panel` | `#101b2d` | Outer content shell |
| `--arcaea-bg-card` | `#16243b` | Stronger card / feature module |
| `--arcaea-accent-light` | `#5fd4ff` | Light system emphasis |
| `--arcaea-accent-light-soft` | `#8be3ff` | Code / structural highlight |
| `--arcaea-accent-conflict` | `#a97bff` | Conflict emphasis / badge |
| `--arcaea-accent-conflict-soft` | `#c9aeff` | Secondary violet highlight |
| `--arcaea-accent-neutral` | `#dce6f2` | Neutral cool contrast |
| `--arcaea-text-main` | `#f2f6fc` | Main text |
| `--arcaea-text-secondary` | `#b9c7da` | Secondary text |
| `--arcaea-text-dim` | `#8090a5` | Meta / low-priority text |
| `--arcaea-divider` | `rgba(120,160,220,0.18)` | Divider / subtle border |
| `--arcaea-bg` | `rgba(10,18,32,0.88)` | Wrapper base background |
| `--arcaea-surface` | `rgba(16,27,45,0.92)` | Elevated surface |
| `--arcaea-surface-soft` | `rgba(22,36,59,0.78)` | Softer surface variant |
| `--arcaea-surface-row` | `rgba(14,26,46,0.82)` | Table odd row |
| `--arcaea-surface-row-alt` | `rgba(20,34,58,0.82)` | Table even row |
| `--arcaea-surface-hover` | `rgba(42,68,104,0.72)` | Row hover |
| `--arcaea-border` | `rgba(120,160,220,0.18)` | Default border |
| `--arcaea-border-strong` | `rgba(170,205,255,0.34)` | Code block / highlighted border |
| `--arcaea-heading` | `#f2f6fc` | Heading text |
| `--arcaea-text` | `rgba(242,246,252,0.94)` | Body text |
| `--arcaea-muted` | `#b9c7da` | Muted / secondary |
| `--arcaea-accent` | `rgba(95,212,255,0.84)` | Accent color |
| `--arcaea-accent-strong` | `#8be3ff` | Strong accent |
| `--arcaea-glow` | `rgba(130,180,255,0.24)` | Glow effect |
| `--arcaea-link` | `#9fc6ff` | Link color |
| `--arcaea-line` | `rgba(120,160,220,0.18)` | Line / divider |

### Core visual pattern

```
background:
  linear-gradient(
    180deg,
    rgba(18,28,48,.95),
    rgba(14,22,38,.92)
  )                                       ← denser reading panel
border: 1px solid rgba(120,160,220,.18)   ← soft cool divider
border-radius: 12px~16px
backdrop-filter: blur(24px)               ← shell-level blur only
box-shadow:
  0 12px 30px rgba(0,0,0,0.22),            ← drop shadow
  inset 0 1px 0 rgba(255,255,255,0.04)     ← light inner highlight edge
```

### Element-specific overrides

| Element | Differences from base |
|---------|---------------------|
| `<h2>` | `color: #f2f6fc`, gradient light trail (`::before`), highlight bar behind text (`::after`), hover expands to full width |
| `<h3>` | Same heading color, `::before` is a left-side light pillar (gradient bar, no text content), hover intensifies glow |
| `<p>` | `color: var(--arcaea-text)`, `line-height: 1.82`; needs `body.dark .entry-content` specificity prefix to beat Sakurairo |
| `<pre>` code blocks | Uses stronger border + slightly deeper surface + local blur |
| `<code>` inline | `background: rgba(180,198,234,0.12)`, near-white text |
| `<pre><code>` | `background: transparent`, `color: inherit !important` |
| `<blockquote>` | Same base family but left border is only mildly brighter; no decorative icons |
| `<table>` | Classic skill table shell: `var(--arcaea-bg)` glass surface, `var(--arcaea-border)` border, weak header highlight, low-grid document table |
| `<li>` | Same tone as body text; no extra high-weight emphasis |
| `<hr>` | Gradient from transparent → soft cool line → transparent |
| `<img>` | `border-radius: 12px` |
| `.wp-block-group` | Same base card pattern, `padding: 16px` |

## Page-level Tokens (Games / Music pages)

### Overlay

```
.bg-overlay {
  background: rgba(0,0,0,0.62);
  backdrop-filter: blur(20px) brightness(0.68) saturate(60%);
  position: fixed; inset: 0;
}
```

### Ambient glow

```
.bg-glow-1: radial-gradient(circle, rgba(120,180,255,0.08), transparent 70%); blur(120px); top-right
.bg-glow-2: radial-gradient(circle, rgba(167,139,250,0.06), transparent 70%); blur(100px); bottom-left
@keyframes floatGlow: oscillate translate(0→50px,-30px) scale(1→1.06)
```

### Noise texture

```
games-arcaea-wrap::before: fractalNoise SVG data URI, opacity 0.4, z-index -2
```

### Category container (light)

```
background: rgba(10,14,24,0.42);
border: 1px solid rgba(255,255,255,0.06);
border-radius: 18px;
box-shadow: none;
```

### Entry card (heavy)

```
background: rgba(8,12,20,0.82);
border-radius: 18px;
border: 1px solid rgba(160,220,255,0.16);
box-shadow: 0 8px 32px rgba(0,0,0,0.32), inset 0 0 0 1px rgba(255,255,255,0.06);
```

## Color Palette

| Usage | Hex | Notes |
|-------|-----|-------|
| Deepest background | `#05070b` | Body/page base |
| Mid background | `#0b1020` | Section fills |
| Surface | `#111827` | Elevated surfaces |
| Dark overlay | `#09090f` | bg-overlay close match |
| Ice blue primary | `#dbe8ff` | Reading-safe cool white |
| Violet accent | `#9db4ff` | Reserved for page-level emphasis |
| Link blue | `#9fc6ff` | Links only |
| Article bg | `rgba(9,18,34,0.44)` | Main article fill |
| Article border | `rgba(214,226,245,0.28)` | Default article border |
| Article strong border | `rgba(226,236,250,0.46)` | Code block / highlighted shell |
| Body text (article) | `rgba(228,236,248,0.92)` | Near-white body text |
| Heading text (article) | `rgba(243,247,255,0.95)` | Higher contrast heading |

## Table Direction

### CSS Defense Layers (same pattern as Mermaid)

| Layer | Selector | Rule | Purpose |
|-------|----------|------|---------|
| 6 | `.arcaea-article-content table *` | `transition: none !important` | Block Sakurairo `* { transition:all 0.4s }` from animating table property changes |

### Default article table

- Use the shell on `.arcaea-table-wrap` or `.wp-block-table`
- Use the classic skill table shell: `var(--arcaea-bg)`, `var(--arcaea-border)`, and light blur
- Keep only very soft vertical separators; avoid heavy spreadsheet-like grid lines
- Keep only soft horizontal dividers in `tbody`
- Avoid decorative light rails, first-column cursors, and high-transparency HUD effects in normal article tables
- All colors use `--arcaea-*` token variables for consistency
- Four-column technical comparison tables use a stable 18% / 42% / 25% / 15% width model; blank first header cells are hidden so row-label tables do not create an empty final display column

### Feature matrix table

Use `table.arcaea-feature-matrix` when rows contain four layers of information:

1. Function or module name
2. Purpose summary
3. Signature block
4. Source line badge

This table is intentionally more “card-like” than a normal comparison table, but it should still behave like a document surface, not a game HUD.

## Typography

| Element | Font Stack |
|---------|-----------|
| Code / Mono | `"FiraCode Nerd Font", "Fira Code", "JetBrains Mono", Consolas, monospace` |
| Body / UI | `"Noto Sans SC", "Microsoft YaHei", -apple-system, sans-serif` |
| English titles | `Orbitron, Rajdhani, Exo 2, Space Grotesk` |

## Glassmorphism Layers

Maximum 2 layers of `backdrop-filter` blur to avoid scroll jank:

```
Background image (layer 0)
  ↓
.bg-overlay: blur(20px) brightness(0.68) saturate(60%)  (layer 1, fixed)
  ↓
.game-category: blur(10px)                                (layer 2)
.game-entry: blur(8px)
```

For article wrapper, keep blur on outer shells and cards. Avoid stacking strong blur on raw table primitives or every cell.

## Prohibited Styles

- High-purity red, fluorescent green, rainbow gradients, oversaturated cyan/purple (`#7dd3fc`, `#c084fc`)
- Bounce/cartoon animations (use float/fade/ambient only)
- Thick borders (>2px)
- RGB gaming-style glow
- Decorative article markers that read louder than headings
- `transition: all` (use specific properties; compositor-friendly)
