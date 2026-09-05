# Sakurairo 原生导航修复

`navigation-accessibility.diff` 修改主题自己的 `header.php`、`js/nav.js`、`css/responsive.css`、`functions.php`，不向文章或插件注入导航补偿脚本。

- 源码：工作区 `Sakurairo`，上游 `mirai-mamori/Sakurairo`，基准提交 `365dabc1024513948f1b3705f3ae8aa2abc97a3b`。
- 本地分支：`fix/navigation-accessibility`。
- 移动菜单使用原生按钮、`aria-expanded` 和 `aria-controls`；关闭菜单使用 `inert`，Escape 关闭并恢复焦点。
- 移除禁止页面缩放的 viewport 属性。
- 本地 PHP lint、JavaScript 语法检查以及 390px 下的 Enter/Escape/焦点检查通过。
- 本地导航脚本和样式包 URL 随文件修改时间变化，避免新 HTML 与访客缓存的旧脚本混用。
- 2026-09-05 22:24（北京时间）已通过公网部署插件 v1.6.83 和前三个主题文件。真实 STM32 文章直接访问及首页往返后均有 1 个图表 SVG、1096 个代码高亮 token，未记录浏览器错误。
- 线上复核发现旧 `nav.js` 浏览器缓存会使新菜单的 ARIA/inert 状态不同步；2026-09-05 公网 root 密钥恢复后，已部署后续缓存版本修复，容器内 PHP lint 通过。真实首页已使用带修改时间的导航和样式 URL；390px 下 Enter 打开、Escape 关闭、ARIA/inert 同步及按钮焦点恢复均通过，viewport 允许缩放。随后进入 STM32 文章仍有 1 个 SVG、1096 个高亮 token、23 个插件脚本，无浏览器错误或警告。
- VPS 部署备份：`/root/blog-page-fix-20260905/plugin-before.tar`、`theme-before.tar`；主题路径为 `/opt/1panel/apps/wordpress/wordpress/data/wp-content/themes/Sakurairo`。
- 后续缓存修复前的 `header.php`、`functions.php` 备份为 `/root/blog-page-fix-20260905/theme-cache-before.tar`。完整回退到本次部署前时，先还原此备份，再还原 `theme-before.tar`，插件使用 `plugin-before.tar` 恢复。

新部署前必须读取实际主题路径和版本，备份上述四个文件，然后在目标主题目录执行 `git apply --check` 检查差异是否仍匹配；匹配后才应用。已部署前三个文件的站点只应用后续缓存差异，并额外备份 `functions.php` 和当前 `header.php`。回滚使用原始文件。主题更新后需重新核对差异，不能盲目覆盖新版本文件。

注意：聚合仓库中的 `sakurairo-theme` 子模块实际是主题使用技能，不包含运行主题 PHP/JS；不能把它当作可部署主题。插件版本在 `babel-arcaea-code` 子模块固定为 v1.6.85（`1e5765e004deca8a7fd91156144ad5337a91f64f`）。此前 v1.6.84 渲染生命周期重构已发布并部署：首次加载/PJAX 统一调度，按正文释放观察器、D3 动画和图片绑定；两种公式引擎及页面往返回归已在本地和 GitHub Actions 通过。线上 STM32 文章图表、高亮和单一全屏入口验证通过。该轮插件回滚包为 `/root/blog-lifecycle-20260905/plugin-before.tar`（v1.6.83）。

## v1.6.85 部署记录（2026-09-06）

- 正式发布已部署至 `/opt/1panel/apps/wordpress/wordpress/data/wp-content/plugins/babel-arcaea-code`，本次同步前通过 SSH 再次确认线上插件头为 `Version: 1.6.85`，并确认回滚包存在。
- 更新 `linkify-it` 至 5.0.2、`undici` 至 6.28.1；该轮 `npm audit` 为 0 漏洞。此结果针对 npm 依赖树，不等于浏览器预打包文件已重新构建或 GitHub 历史告警全部关闭。
- 修复 Markmap CLI 预渲染失败后缺少浏览器运行时的问题；仅存在待渲染源码时加载客户端资源。该轮本地回归、容器 PHP lint 及 GitHub Actions 的 Validate、Release & Sync 均通过。
- 线上鼠标点击顶部“嵌入式专题”时，页面 `performance.timeOrigin` 保持不变，目标页面请求为 fetch，确认真实 PJAX。公式文章（ID 796）验证得到 3 个 KaTeX 公式、0 个公式错误；插件保持 KaTeX，主题 MathJax 保持关闭。
- 已扫描的 55 篇已发布文章/页面没有 Markmap 源码，图片缩放也尚无有效线上内容样本；这两项真实内容验收仍待补充，不以自动化结果替代。
- 设置页文字显示修复已按用户要求撤回，未发布该显示改动。
- 本轮回滚包：`/root/blog-dependency-20260906/plugin-before.tar`（v1.6.84）。本次仅同步集成仓库和记录，不再次部署或修改线上配置。
