# Sakurairo Arcaea 风格化方案 🎨

> 基于 [Sakurairo 主题](https://github.com/AKCX2002/sakurairo-theme) 的 Arcaea 风格化 WordPress 建站方案 —— 主题 + 插件 + 配置，一站聚合。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 方案组成

本仓库是 **Git 子模块聚合主仓库**，将三个核心组件组合为完整的 Arcaea 风格化方案：

```text
sakurairo-arcaea-styling/
├── babel-arcaea-code/             ← 插件：代码高亮/图表/数学渲染
├── sakurairo-theme/               ← 主题：Arcaea 风格基础框架
└── sakurairo-arcaea-blog-skill/   ← 配置：AI 辅助技巧与参考文档
```

| 子模块 | 版本 | 说明 |
| ------ | ---- | ---- |
| [`babel-arcaea-code`](https://github.com/AKCX2002/babel-arcaea-code) | v1.4.x | WordPress 插件 — Prism.js 代码高亮、Mermaid 图表、Markmap 思维导图、MathJax 数学渲染 |
| [`sakurairo-theme`](https://github.com/AKCX2002/sakurairo-theme) | v1.0.x | Sakurairo 主题 — 多彩轻量 WordPress 主题，Arcaea 风格化基础框架 |
| [`sakurairo-arcaea-blog-skill`](https://github.com/AKCX2002/sakurairo-arcaea-blog-skill) | v1.2.x | 博客配置技巧集 — AI 辅助参考文档与注入模式 |

## 快速开始

```bash
# 克隆主仓库（含所有子模块）
git clone --recursive https://github.com/AKCX2002/sakurairo-arcaea-styling.git

# 如果已克隆但未拉取子模块
git submodule update --init --recursive
```

## 日常工作流

### 更新到最新版本

```bash
# 拉取所有子模块的最新提交
git submodule update --remote --merge

# 更新特定子模块
git submodule update --remote --merge babel-arcaea-code

# 提交更新
git add . && git commit -m "chore: 更新子模块" && git push
```

### 在子模块中开发

```bash
cd babel-arcaea-code     # 进入子模块
# ... 开发、提交、推送 ...
cd ..
git add babel-arcaea-code
git commit -m "chore: bump babel-arcaea-code to v1.4.x"
git push
```

## 仓库说明

- **主仓库**仅维护聚合配置（`.gitmodules`、`README`、`AGENTS.md` 等），不含业务代码
- 各子模块保留独立的版本号、CI/CD 和发布流程
- Issue 请按所属子模块归类提交

## 更多文档

- [`AGENTS.md`](./AGENTS.md) — AI 代理开发指引
- [Issue 模板](./.github/ISSUE_TEMPLATE/) — Bug 报告 / 功能请求

## 许可

主仓库采用 [MIT License](LICENSE)。各子模块遵循其各自的许可协议。
