# Sakurairo Arcaea 风格化方案

> 基于 [Sakurairo 主题](https://github.com/AKCX2002/sakurairo-theme) 的 Arcaea 风格化 WordPress 建站方案。

## 仓库结构

本仓库是一个 **Git 子仓库聚合**，包含三个子模块：

| 子模块 | 说明 |
| ------ | ------ |
| [`babel-arcaea-code`](./babel-arcaea-code) | Babel Arcaea Code — WordPress 插件，提供代码高亮、Mermaid 图表、Markmap 思维导图、MathJax 渲染等功能 |
| [`sakurairo-theme`](./sakurairo-theme) | Sakurairo 主题 — 多彩、轻量级的 WordPress 主题，Arcaea 风格化的基础主题框架 |
| [`sakurairo-arcaea-blog-skill`](./sakurairo-arcaea-blog-skill) | Sakurairo Arcaea Blog Skill — 博客配置技巧与参考文档集合 |

## 快速开始

```bash
# 克隆主仓库（含子模块）
git clone --recursive https://github.com/AKCX2002/sakurairo-arcaea-styling.git

# 如果已克隆但未拉取子模块
git submodule update --init --recursive
```

## 更新子模块

```bash
# 拉取所有子模块的最新版本
git submodule update --remote --merge

# 拉取特定子模块
git submodule update --remote --merge babel-arcaea-code
```

## 本地开发

```bash
# 克隆所有子模块
git submodule update --init --recursive
```

各子模块可独立开发，在主仓库中更新子模块引用后提交即可。

## 许可

各子模块遵循其各自的许可协议。
