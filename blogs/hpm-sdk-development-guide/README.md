# HPM SDK 开发手册 — 博客系列规划

> 博客结构遵循 blog-post skill: Hook → Context → Solution → Application → Conclusion
> 技术深度遵循 technical-blog-writing skill: 可运行代码、开发者视角、诚实谈取舍

## 系列总览（8 篇，目标 5~8 万字）

| # | 标题 | 类型 | 预估字数 | 核心 Mermaid | 重点表格 |
|---|------|------|----------|-------------|---------|
| 1 | 为什么选择 HPM——当 RISC-V 双核遇上 CMake | 对比/深度 | 5,000~8,000 | 架构分层图 | STM32 vs HPM 主频表 |
| 2 | 开发环境搭建——从零开始配置 HPM SDK | 教程 | 4,000~6,000 | 安装顺序图 | 工具版本表 |
| 3 | 第一个工程——cmake -B build 到底发生了什么 | 教程+深度 | 6,000~10,000 | 构建生命周期图 | SDK 函数 vs CMake API 映射表 |
| 4 | CMake 构建体系——HPM_SDK_LIB、Component、Board 机制 | 深度 | 8,000~12,000 | Target 传播图、依赖解析图 | 6 个 SDK 函数表 |
| 5 | HPM6800 启动流程与内存架构——从 Reset 到 main() | 深度 | 6,000~10,000 | 启动调用链、内存布局图 | 7 个内存区域表 |
| 6 | 双核开发实战——Core0 + Core1 产品分工 | 教程+架构 | 6,000~10,000 | 双核架构图、sec_core_img 流程 | 分工矩阵 |
| 7 | 从 Sample 到量产——企业级工程实践 | 架构 | 5,000~8,000 | 推荐项目结构图 | 升级检查清单 |
| 8 | SDK 源码深挖——build_linked_project.py、application.cmake、Linker Script | 深度 | 8,000~12,000 | 构建生命周期的 11 步图 | 各阶段输入/输出表 |

## 写作流程（每篇按 blog-post skill）

1. **Research** → 回顾 SDK 源文件、确认代码引用
2. **Hook** → 提出问题或场景，吸引读者
3. **Context** → 为什么这个问题重要
4. **Main Content** → 3~5 个 H2 节，每节含 Mermaid 图 + 代码
5. **Practical Application** → 读者可以立刻用的东西
6. **Conclusion + CTA** → 关键收获 + 下一篇预告

## 当前文件

- `tmp/.HPM SDK 开发手册.html` — 已有 78KB 内容（Parts 1-7 填充、Parts 8-12 大纲、7 个 Patch）
- `blogs/hpm-sdk-development-guide/` — 最终博客系列目录
