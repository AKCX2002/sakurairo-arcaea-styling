# Sakurairo Arcaea 风格化方案 — AGENTS.md

## 项目概述

本仓库是 **Sakurairo Arcaea 风格化方案**的 Git 子模块聚合主仓库。将三个核心组件组合为一份完整的 Arcaea 风格 WordPress 建站方案。

## 仓库结构

| 路径 | 类型 | 说明 |
| ---- | ---- | ---- |
| `babel-arcaea-code/` | submodule | WordPress 插件，Prism.js 代码高亮、Mermaid 图表、Markmap、MathJax |
| `sakurairo-arcaea-blog-skill/` | submodule | AI 配置技巧与参考文档集合 |
| `sakurairo-theme/` | submodule | Sakurairo 主题框架 |

## 工作流

### 更新子模块

```bash
git submodule update --remote --merge  # 更新所有
git submodule update --remote --merge <name>  # 更新单个
```

### 在子模块中开发后提交

```bash
cd <submodule>
# 开发...
git add -A && git commit -m "msg"
git push
cd ..
git add <submodule>
git commit -m "chore: bump <submodule>"
git push
```

## 子模块远程仓库

| 子模块 | 远程 |
| ------ | ---- |
| `babel-arcaea-code` | https://github.com/AKCX2002/babel-arcaea-code.git |
| `sakurairo-arcaea-blog-skill` | https://github.com/AKCX2002/sakurairo-arcaea-blog-skill.git |
| `sakurairo-theme` | https://github.com/AKCX2002/sakurairo-theme.git |

## 代码质量

- 本仓库仅维护聚合配置和文档，不包含业务代码
- 各子模块的代码风格遵循其各自仓库规范
- README 和 AGENTS.md 保持中英双语或中文优先
