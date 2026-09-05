# Sakurairo 本地主题修复与部署

`navigation-accessibility.diff` 修改主题自己的 `header.php`、`js/nav.js`、`css/responsive.css`、`functions.php` 和 `comments.php`，不向文章或插件注入补偿脚本。当前补丁基于 Sakurairo 3.0.11 的上游提交 `85ca5418e9e3280f6e2b9ed1ca9cab68d57bcaf3`；下列旧版本记录保留用于追溯。

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

新部署前必须读取实际主题路径和版本，备份受影响文件，再在干净的上游候选目录执行 `git apply --check`。线上已经应用补丁，不得再次盲目应用完整补丁。后续部署使用下述自动更新器保留本地修复。

注意：聚合仓库中的 `sakurairo-theme` 子模块实际是主题使用技能，不包含运行主题 PHP/JS；不能把它当作可部署主题。插件版本在 `babel-arcaea-code` 子模块固定为 v1.6.85（`1e5765e004deca8a7fd91156144ad5337a91f64f`）。此前 v1.6.84 渲染生命周期重构已发布并部署：首次加载/PJAX 统一调度，按正文释放观察器、D3 动画和图片绑定；两种公式引擎及页面往返回归已在本地和 GitHub Actions 通过。线上 STM32 文章图表、高亮和单一全屏入口验证通过。该轮插件回滚包为 `/root/blog-lifecycle-20260905/plugin-before.tar`（v1.6.83）。

## v1.6.85 部署记录（2026-09-06）

- 正式发布已部署至 `/opt/1panel/apps/wordpress/wordpress/data/wp-content/plugins/babel-arcaea-code`，本次同步前通过 SSH 再次确认线上插件头为 `Version: 1.6.85`，并确认回滚包存在。
- 更新 `linkify-it` 至 5.0.2、`undici` 至 6.28.1；该轮 `npm audit` 为 0 漏洞。此结果针对 npm 依赖树，不等于浏览器预打包文件已重新构建或 GitHub 历史告警全部关闭。
- 修复 Markmap CLI 预渲染失败后缺少浏览器运行时的问题；仅存在待渲染源码时加载客户端资源。该轮本地回归、容器 PHP lint 及 GitHub Actions 的 Validate、Release & Sync 均通过。
- 线上鼠标点击顶部“嵌入式专题”时，页面 `performance.timeOrigin` 保持不变，目标页面请求为 fetch，确认真实 PJAX。公式文章（ID 796）验证得到 3 个 KaTeX 公式、0 个公式错误；插件保持 KaTeX，主题 MathJax 保持关闭。
- 已扫描的 55 篇已发布文章/页面没有 Markmap 源码，图片缩放也尚无有效线上内容样本；这两项真实内容验收仍待补充，不以自动化结果替代。
- 设置页文字显示修复已按用户要求撤回，未发布该显示改动。
- 本轮回滚包：`/root/blog-dependency-20260906/plugin-before.tar`（v1.6.84）。本次仅同步集成仓库和记录，不再次部署或修改线上配置。

## 主题自动更新与评论修复（2026-09-06）

- 线上主题为 Sakurairo 3.0.11，上游 `85ca5418`，本地修复以 `/etc/sakurairo-theme/local-overrides.patch` 为部署输入。每日北京时间 04:20 起随机 30 分钟内检查上游 main；补丁冲突时保留当前主题。
- 更新器源码见 [`deployment/update-sakurairo-theme`](../deployment/update-sakurairo-theme)，服务器安装路径 `/usr/local/sbin/update-sakurairo-theme`；服务/定时器为 `sakurairo-theme-update.service`、`sakurairo-theme-update.timer`。
- 评论表单的 `submit_button` 会被 WordPress 当作 `sprintf` 模板；其中 nonce 隐藏字段的中文文章 referrer 带有百分号编码，导致 `Unknown format specifier`，截断页脚及插件脚本。`comments.php` 现在把模板中的字面百分号转义为 `%%`，输出时恢复原值，保留 nonce 与评论功能。该缺陷不在 KaTeX 配置中。
- 更新器遇到工作区修改或与已记录补丁不符的额外提交时停止，防止覆盖新增定制。修改主题后应先更新受版本控制的补丁，再同步服务器补丁，不能仅编辑线上文件。
- 部署后的健康检查同时验证文章 ID 796 的完整 HTML 和 `bac-content-loader-js`，避免 HTTP 200 掩盖评论模板中途崩溃。生产插件仍固定 v1.6.85，KaTeX 保持启用。
- 本次修复前的评论文件、补丁、更新器、提交号和补丁哈希位于 `/opt/1panel/backup/sakurairo-theme/comment-format-20260906/`。完整主题更新备份位于 `/opt/1panel/backup/sakurairo-theme/`。回滚必须同时恢复主题版本、对应补丁及哈希，避免自动更新状态不一致。
