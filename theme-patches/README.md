# Sakurairo 原生导航修复

`navigation-accessibility.diff` 修改主题自己的 `header.php`、`js/nav.js`、`css/responsive.css`、`functions.php`，不向文章或插件注入导航补偿脚本。

- 源码：工作区 `Sakurairo`，上游 `mirai-mamori/Sakurairo`，基准提交 `365dabc1024513948f1b3705f3ae8aa2abc97a3b`。
- 本地分支：`fix/navigation-accessibility`。
- 移动菜单使用原生按钮、`aria-expanded` 和 `aria-controls`；关闭菜单使用 `inert`，Escape 关闭并恢复焦点。
- 移除禁止页面缩放的 viewport 属性。
- 本地 PHP lint、JavaScript 语法检查以及 390px 下的 Enter/Escape/焦点检查通过。
- 本地导航脚本和样式包 URL 随文件修改时间变化，避免新 HTML 与访客缓存的旧脚本混用。
- 2026-09-05 22:24（北京时间）已通过公网部署插件 v1.6.83 和前三个主题文件。真实 STM32 文章直接访问及首页往返后均有 1 个图表 SVG、1096 个代码高亮 token，未记录浏览器错误。
- 线上复核发现旧 `nav.js` 浏览器缓存会使新菜单的 ARIA/inert 状态不同步；后续缓存版本修复已完成本地 PHP lint，但尚未部署：公网随后拒绝现有 root 密钥，等待当前管理用户名。不能将移动菜单线上验收标记为通过。
- VPS 部署备份：`/root/blog-page-fix-20260905/plugin-before.tar`、`theme-before.tar`；主题路径为 `/opt/1panel/apps/wordpress/wordpress/data/wp-content/themes/Sakurairo`。

新部署前必须读取实际主题路径和版本，备份上述四个文件，然后在目标主题目录执行 `git apply --check` 检查差异是否仍匹配；匹配后才应用。已部署前三个文件的站点只应用后续缓存差异，并额外备份 `functions.php` 和当前 `header.php`。回滚使用原始文件。主题更新后需重新核对差异，不能盲目覆盖新版本文件。

注意：聚合仓库中的 `sakurairo-theme` 子模块实际是主题使用技能，不包含运行主题 PHP/JS；不能把它当作可部署主题。插件版本在 `babel-arcaea-code` 子模块固定为 v1.6.83，其修复与 GitHub 自动发布流程已发布。
