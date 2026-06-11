# 🌌 Sakurairo Arcaea Blog Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skill](https://img.shields.io/badge/Hermes-Skill-8A2BE2)](https://hermes-agent.nousresearch.com)
[![WordPress](https://img.shields.io/badge/WordPress-Sakurairo_3.0.10-21759B)](https://babel36acl.xyz)

> **在 Sakurairo 主题博客上应用 Arcaea 风格的完整指南。**  
> 一个文件解决全部——从设计哲学、CSS 体系、主题集成到 WordPress 发布。

---

## 🎯 用途

- **设计**：在 babel36acl.xyz 上创建 Arcaea 风格页面（冷色层级、深色面板、技术文档优先）
- **美化**：对已有页面应用「容器轻 + 卡片重」层级体系
- **修复**：Sakurairo 主题 CSS 冲突（blockquote FontAwesome 图标、暗色模式覆盖等）
- **发布**：通过 MCP 桥安全发布文章/页面到 WordPress
- **写作**：中文技术文档规范 + 博客文章风格指南

## ✨ 核心内容

| 章节 | 说明 |
|------|------|
| **前置技能加载** | 13 个关联技能（Hermes 本地 + skills.sh 生态）加载顺序 |
| **CSS 设计体系** | Arcaea 哲学总览、颜色 Token、统一表格规范、Prism 代码块、Light/Conflict 配色分工 |
| **Sakurairo 主题集成** | CSS 变量覆盖、暗黑模式适配、!important 冲突覆盖、短代码兼容、REST API |
| **文章风格** | 中文技术文档规范、技术教程/随笔/游戏页三种写作指南、WordPress 发布约定 |
| **WordPress 发布** | MCP 工具、凭证安全、紧急模式、验证步骤、已知页面/分类 |
| **工作流** | 设计新页面 → 美化已有页面 → 修复冲突 → 发布内容 |
| **网站落地状态** | https://babel36acl.xyz 首页和 Games 页面的实际部署对比，CSS 版本差异表 |
| **Pitfalls** | 8 条陷阱（!important、wpautop、暗色模式、backdrop-filter 性能、表格可读性等） |

## 🎨 设计哲学

Arcaea 风格不是普通二次元 UI，而是一种 **"未来感 × 情绪化 × 极简秩序 × 崩坏诗意"**（Cyber Minimalism + Emotional Futurism）。

| 核心原则 | 说明 |
|---------|------|
| **"空"** | 大面积留白、半透明、漂浮元素、低密度布局 |
| **宇宙中的 UI** | 元素漂浮在虚空/数据空间/记忆层中 |
| **柔光非霓虹** | 模糊辉光，环境光，非 RGB 电竞风 |
| **Glassmorphism** | 毛玻璃只做壳层，不让正文表格和代码块被背景图吃掉 |
| **三层分离** | 背景图 → bg-overlay(blur+brightness+saturate) → 内容容器 |
| **轻重分配** | 容器轻(~0.42) + 卡片重(~0.82) + 强调更重(~0.88) |
| **技术优先** | API 表、对比表、功能矩阵首先解决扫读效率，再谈氛围感 |

## 📥 安装

### 方式 1：Git Clone（推荐）

```bash
git clone --depth 1 https://github.com/AKCX2002/sakurairo-arcaea-blog-skill.git
cp sakurairo-arcaea-blog-skill/SKILL.md ~/.hermes/skills/sakurairo-arcaea-blog-skill/
```

### 方式 2：安装脚本

```bash
bash <(curl -sL https://raw.githubusercontent.com/AKCX2002/sakurairo-arcaea-blog-skill/main/install.sh)
```

### 方式 3：Hermes Skills（即将支持）

```bash
hermes skills install sakurairo-arcaea-blog-skill
```

## 🔧 使用

在 Hermes 会话中，加载 skill 后即可使用：

```text
skill_view(name="sakurairo-arcaea-blog-skill")
```

然后按提示执行工作流：
- 「帮我设计一个 Arcaea 风格的 xx 页面」
- 「美化现有的 xx 页面」
- 「blockquote 图标怎么去掉」
- 「发布文章到博客」

## 🧩 依赖技能

### Hermes 本地（必装）
| 技能 | 用途 | 源码 |
|------|------|------|
| `glassmorphism-ui` | 毛玻璃 CSS 模式库 | — |
| `ui-beautify` | Arcaea v5 精确 CSS | — |
| `ui-designer` | 整页布局生成 | — |
| `css-master` | 设计 Token、Sakurairo 冲突诊断 | — |
| `wordpress-content-management` | MCP 发布桥 | — |
| `web-design-guidelines` | Vercel Web 界面规范审查 | — |

### Skills.sh 生态（可选增强）
| 技能 | 安装量 | 用途 | 仓源码 |
|------|--------|------|--------|
| `sakurairo-theme` | — | Sakurairo 主题功能完整指南 | [`AKCX2002/sakurairo-theme`](https://github.com/AKCX2002/sakurairo-theme) |
| `wordpress-pro` | 4.9K ⭐ | WordPress 专业开发 | — |
| `ckm:design` / `ui-ux-pro-max` | 21.2K ⭐ | UI/UX 设计综合 | — |
| `tailwind` | 46.7K ⭐ | Tailwind CSS v4 | — |
| `animejs` | 634 ⭐ | 动画库 | — |

## 🌐 线上落地

该 skill 的 CSS v5.2 值已在 [babel36acl.xyz](https://babel36acl.xyz) 的以下页面落地验证：

- **Games 页面**（/games/）— 完整 v5.2 ✅
- **Music 页面**（/emotional-artcore/）— 完整 ✅
- **全站 Prism 代码块** — 玻璃卡片风格 ✅

首页 Arcaea 玻璃卡片待实现。

## 📄 许可

[MIT](LICENSE)
