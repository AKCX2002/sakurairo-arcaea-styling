# 主仓库工作规则

## 维护边界

- `sakurairo-arcaea-blog-skill/`、`sakurairo-theme/`、`babel-arcaea-mermaid/` 已导入主仓库，直接在本仓库提交，不再作为子模块或推送旧仓库。
- `sakurairo-theme/` 是技能参考，运行主题来自上游 `mirai-mamori/Sakurairo`。
- `babel-arcaea-code/` 是独立生产插件子模块；先在其仓库完成实现、验证和发布，再固定主仓库指针。
- `wordpress-dm1-calculator/` 保持原有独立子模块边界。
- 保留导入历史、各组件许可证与外部子模块版本。不在整合时改动不相关的旧项目目录。

## 主题与渲染

- 生产状态、补丁基准及回滚位置以 `theme-patches/README.md` 为入口，并在部署前核实线上实际文件。
- 主题修复写入 `theme-patches/navigation-accessibility.diff`，更新器在 `deployment/update-sakurairo-theme`。同步服务器补丁后再部署；不绕过本地改动保护。
- 文章正文仅承载内容，不注入 Mermaid/PJAX 初始化、调试或补偿脚本。渲染由生产统一插件负责。
- KaTeX/MathJax 通过生产插件 `latex_renderer` 互斥；当前站点使用 KaTeX，主题 MathJax 关闭。
- 独立 Mermaid 插件用于其他站点，不与统一插件同时接管生产图表。

## 验证与发布

- 验证对应真实问题：PHP lint 不代表页面完整，HTTP 200 不代表未中途发生 Fatal。主题部署需验证真实文章的页脚加载器及 HTML 闭合。
- PJAX 需用页面 timeOrigin 和请求类型区分局部切换与整页加载。公式检查实际 `.katex`/`.katex-error`，不以配置开关代替渲染结果。
- 独立 Mermaid 的根工作流负责其版本与 zip；不要把主仓库源码包发布为 WordPress 插件。生产插件仍沿用自己的 Release & Sync。
- 技能安装器必须保留 references/scripts，不只复制 SKILL.md。修改技能内容时检查是否仍引用已迁移的旧仓库入口。
- 不自动安装技能到用户运行环境；仓库整合不等于授权改变全部代理配置。
