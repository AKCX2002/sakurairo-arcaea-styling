# Sakurairo 原生导航修复

`navigation-accessibility.diff` 修改主题自己的 `header.php`、`js/nav.js`、`css/responsive.css`，不向文章或插件注入导航补偿脚本。

- 源码：工作区 `Sakurairo`，上游 `mirai-mamori/Sakurairo`，基准提交 `365dabc1024513948f1b3705f3ae8aa2abc97a3b`。
- 本地分支：`fix/navigation-accessibility`。
- 移动菜单使用原生按钮、`aria-expanded` 和 `aria-controls`；关闭菜单使用 `inert`，Escape 关闭并恢复焦点。
- 移除禁止页面缩放的 viewport 属性。
- 本地 PHP lint、JavaScript 语法检查以及 390px 下的 Enter/Escape/焦点检查通过。线上尚未部署：2026-09-05 公网 SSH 在握手前关闭，NAS 到 VPS WireGuard 地址无握手且连接超时。

部署前必须读取实际主题路径和版本，备份上述三个文件，然后在目标主题目录执行 `git apply --check` 检查差异是否仍匹配；匹配后才应用。回滚使用三个原始文件。主题更新后需重新核对差异，不能盲目覆盖新版本文件。

注意：聚合仓库中的 `sakurairo-theme` 子模块实际是主题使用技能，不包含运行主题 PHP/JS；不能把它当作可部署主题。插件版本在 `babel-arcaea-code` 子模块固定为 v1.6.83，其修复与 GitHub 自动发布流程已发布。
