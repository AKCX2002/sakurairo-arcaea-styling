# Arcaea Lite — Hub/Index Page Wrapper (v5.5)

用于非内容密集型页面（关于、工具箱、嵌入式专题、游记等）的轻量 Arcaea 包裹层，不作为常规博客文章正文模板。**仅当外部样式注入不可行时，作为过渡方案临时内联 CSS。**

**v5.5 关键变更**：移除 bg-overlay（backdrop-filter 模糊层）和 ::before 噪声纹理——这些 fixed 定位元素会覆盖正文使其不可读。Games/Music 页面保留 overlay（有卡片衬底提供对比度），Lite 页面不可用。

## 设计原则

- 不重构页面内容，仅包裹 + 着色
- 无 bg-overlay（无 backdrop-filter 模糊层）
- 无 ::before 噪声（无 fixed 遮挡层）
- 保留 bg-glow 光晕（低透明度，非遮挡，仅氛围）
- 统一 :root 颜色变量覆盖
- 参考 Games 排版体系：section-kicker / section-title / section-desc
- 使用 card-group 和 entry-card 替代固定卡片系统
- 覆盖所有内容元素（li, code, strong, p, h2, blockquote）的 Sakurairo 默认颜色

## CSS 模板（Lite 页面专用；仅外部注入不可行时再临时内联，CSS 需紧凑防 wpautop）

```css
:root{--theme-skin:#0a0e18;--theme-skin-dark:#05070d;--global-font-weight:300}
.bg-glow-1{position:fixed;width:1000px;height:1000px;top:-200px;right:-150px;background:radial-gradient(circle,rgba(120,180,255,0.04),transparent 70%);filter:blur(120px);pointer-events:none;z-index:-1;animation:floatGlow 20s ease-in-out infinite}
.bg-glow-2{position:fixed;width:800px;height:800px;bottom:-150px;left:-100px;background:radial-gradient(circle,rgba(167,139,250,0.03),transparent 70%);filter:blur(100px);pointer-events:none;z-index:-1;animation:floatGlow 24s ease-in-out infinite reverse}
@keyframes floatGlow{0%{transform:translate(0,0) scale(1)}50%{transform:translate(50px,-30px) scale(1.06)}100%{transform:translate(0,0) scale(1)}}
.arcaea-wrap{position:relative;z-index:1;max-width:1380px;margin:0 auto;padding:0 clamp(24px,6vw,60px);color:#f0f6ff}
.arcaea-wrap .section-kicker{font-size:0.78em;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:rgba(157,180,255,0.55);margin-bottom:4px}
.arcaea-wrap .section-title{font-size:2em;font-weight:700;color:#f3f0ff;margin:0 0 4px;text-shadow:0 0 10px rgba(180,150,255,0.55),0 2px 4px rgba(0,0,0,0.75)}
.arcaea-wrap .section-desc{color:#c8ddf5;font-size:1em;margin:0 0 12px;font-weight:300}
.arcaea-wrap .card-group{background:rgba(10,14,24,0.42);border:1px solid rgba(255,255,255,0.06);border-radius:18px;padding:16px 20px;margin:24px 0}
.arcaea-wrap .entry-card{background:rgba(8,12,20,0.82);border-radius:18px;padding:20px 24px;margin:12px 0;border:1px solid rgba(160,220,255,0.16);box-shadow:0 8px 32px rgba(0,0,0,0.32),inset 0 0 0 1px rgba(255,255,255,0.06)}
.arcaea-wrap .entry-card h3{display:flex;align-items:center;gap:10px;color:#e2f4ff;font-size:1.2em;font-weight:700;margin:0 0 6px 0;text-shadow:0 0 12px rgba(126,200,255,0.45),0 2px 4px rgba(0,0,0,0.75)}
.arcaea-wrap .entry-card h3::before{content:"#";color:rgba(255,145,145,0.75);font-size:0.95em;font-weight:700;flex-shrink:0}
.arcaea-wrap h1,.arcaea-wrap h2{color:#f3f0ff;text-shadow:0 0 10px rgba(180,150,255,0.35),0 2px 4px rgba(0,0,0,0.7)}
.arcaea-wrap h2{margin-top:36px;padding-bottom:8px;border-bottom:1px solid rgba(158,207,255,0.10);font-size:1.75em}
.arcaea-wrap p{color:#d8e8f8;line-height:1.85;font-size:1.02em;text-indent:2em}
.arcaea-wrap blockquote{background:linear-gradient(135deg,rgba(40,70,120,0.22),rgba(20,30,50,0.14))!important;border-left:3px solid rgba(126,200,255,0.55)!important;border-radius:12px!important;padding:16px 28px 16px 36px!important;margin:18px 0!important;color:#f8fbff!important;font-size:1.06em!important;line-height:1.85!important;text-indent:0!important}
.arcaea-wrap blockquote::before{content:"(^^)"!important;position:absolute;left:-6px;top:-3px;font-size:0.8em;color:rgba(157,200,255,0.30)}.arcaea-wrap blockquote::after{display:none!important;content:none!important}
.arcaea-wrap blockquote p{margin:0!important;padding:0!important;border:none!important;background:none!important;text-indent:0!important}
.arcaea-wrap hr{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(158,207,255,0.10),transparent);margin:28px 0}
@media(prefers-reduced-motion:reduce){.bg-glow-1,.bg-glow-2{animation:none}}
pre,code{font-family:"FiraCode Nerd Font","Fira Code","JetBrainsMono Nerd Font",monospace!important;font-size:14px;line-height:1.6}
*:focus-visible{outline:2px solid rgba(139,167,255,0.7);outline-offset:2px}
```

## HTML 包裹结构

```html
<style>/* 仅在当前页面无法复用共享模板时，才内联这段 Lite CSS */</style>
<div class="arcaea-wrap">
<div class="bg-glow-1"></div>
<div class="bg-glow-2"></div>
<!-- 原有页面内容 -->
</div>
```

## 架构对比

| 页面类型 | Overlay | Noise | 卡片系统 | 适用页面 |
|----------|---------|-------|---------|---------|
| Arcaea 完整 (Games/Music) | 有 | 有 | game-entry | 内容密集、有卡片衬底 |
| Arcaea Lite (Hub) | 无 | 无 | card-group/entry-card | 文本为主、无卡片 |
