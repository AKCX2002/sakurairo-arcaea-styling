# Sakurairo Arcaea 风格化方案

> 基于 [Sakurairo 主题](https://github.com/AKCX2002/sakurairo-theme) × [Babel Arcaea Code](https://github.com/AKCX2002/babel-arcaea-code) 的 Arcaea 风格化 WordPress 建站完整方案。

![GitHub](https://img.shields.io/github/license/AKCX2002/sakurairo-arcaea-styling)
![GitHub last commit](https://img.shields.io/github/last-commit/AKCX2002/sakurairo-arcaea-styling)

---

## 目录

- [项目概述](#项目概述)
- [仓库结构](#仓库结构)
- [快速开始](#快速开始)
- [本地开发](#本地开发)
- [子模块管理](#子模块管理)
- [部署指南](#部署指南)
- [许可](#许可)

---

## 项目概述

本仓库是 **Sakurairo Arcaea 风格化方案**的聚合主仓库，采用 Git 子模块（submodule）机制将三个核心仓库整合为一个整体：

| 组件 | 角色 |
| ---- | ---- |
| **Sakurairo 主题** | 多彩、轻量级 WordPress 主题，提供 Arcaea 风格化的基础主题框架 |
| **Babel Arcaea Code** | WordPress 插件，提供代码高亮（Prism.js）、Mermaid 图表、Markmap 思维导图、MathJax 渲染等功能 |
| **Sakurairo Arcaea Blog Skill** | AI 辅助配置技巧与参考文档集合，帮助快速搭建与调优 |

## 仓库结构

```text
sakurairo-arcaea-styling/
├── .gitmodules                    ← 子模块配置
├── .gitignore                     ← 通用忽略规则
├── README.md                      ← 本文件
├── babel-arcaea-code/             ← 子模块①: 代码增强插件
├── sakurairo-arcaea-blog-skill/   ← 子模块②: 博客配置技巧
└── sakurairo-theme/               ← 子模块③: 主题框架
```

### 各子模块详细介绍

| 子模块 | 目标目录 | 说明 |
| ------ | -------- | ---- |
| [`babel-arcaea-code`](./babel-arcaea-code) | `wp-content/plugins/babel-arcaea-code` | 代码高亮（Prism.js，30+ 语言 + 20+ 插件）、Mermaid 图表渲染、Markmap 思维导图、MathJax 数学公式 |
| [`sakurairo-theme`](./sakurairo-theme) | `wp-content/themes/sakurairo-theme` | 多彩轻量级主题，支持自定义色调、响应式布局、暗色模式、字体自定义、社交图标等 |
| [`sakurairo-arcaea-blog-skill`](./sakurairo-arcaea-blog-skill) | 参考文档 | AI 辅助配置文件、Skill 参考及安装脚本，涵盖 Arcaea Lite Wrapper、Visual Tokens、Mermaid 注入模式等 |

## 快速开始

```bash
# 克隆主仓库（含子模块）
git clone --recursive https://github.com/AKCX2002/sakurairo-arcaea-styling.git

# 如果已克隆但未拉取子模块
cd sakurairo-arcaea-styling
git submodule update --init --recursive
```

### WordPress 目录映射

```bash
# 建立软链接将插件和主题链接到 WordPress 目录（示例）
# 插件
ln -s /path/to/sakurairo-arcaea-styling/babel-arcaea-code /var/www/html/wp-content/plugins/babel-arcaea-code
# 主题
ln -s /path/to/sakurairo-arcaea-styling/sakurairo-theme /var/www/html/wp-content/themes/sakurairo
```

## 本地开发

### 开发工作流

各子模块可以独立开发，在主仓库中更新子模块引用后提交即可：

```bash
# 1. 进入子模块目录
cd babel-arcaea-code

# 2. 在子模块中正常开发
git checkout -b feature/my-feature
# ... 修改代码 ...
git add .
git commit -m "feat: add new feature"

# 3. 回到主仓库，更新子模块指针
cd ..
git add babel-arcaea-code
git commit -m "chore: bump babel-arcaea-code"
```

### 快速切换到最新版本

```bash
git submodule foreach 'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch || echo main) && git pull'
```

## 子模块管理

### 更新到子模块最新提交

```bash
# 更新所有子模块到最新
git submodule update --remote --merge

# 或更新特定子模块
git submodule update --remote --merge babel-arcaea-code

# 提交子模块引用变更
git add .
git commit -m "chore: update submodules to latest"
```

### 查看各子模块当前状态

```bash
git submodule status
```

## 部署指南

### 生产环境

```bash
git clone --recursive --depth 1 https://github.com/AKCX2002/sakurairo-arcaea-styling.git
cd sakurairo-arcaea-styling

# 将插件和主题部署到 WordPress
cp -r babel-arcaea-code /var/www/html/wp-content/plugins/
cp -r sakurairo-theme /var/www/html/wp-content/themes/sakurairo
```

### Docker 环境

```bash
docker-compose up -d
# 然后将插件和主题通过 volume 或 Dockerfile COPY 挂载到对应目录
```

---

## 许可

| 组件 | 许可 |
| ---- | ---- |
| 本仓库聚合 | [MIT](./LICENSE) |
| `babel-arcaea-code` | [GPL-3.0](./babel-arcaea-code/LICENSE) |
| `sakurairo-theme` | [GPL-3.0](./sakurairo-theme/LICENSE) |
| `sakurairo-arcaea-blog-skill` | [MIT](./sakurairo-arcaea-blog-skill/LICENSE) |
