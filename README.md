# Sakurairo WordPress Theme — Usage Skill

Sakurairo 是一款基于 Sakura V3 Series 重构开发的 WordPress 主题，具有 AI 辅助阅读、多服务 API 集成（B站、Steam、QQ、Bangumi）、丰富的页面构建能力、灵活的首页组件系统、多样的文章展示样式等特性。

本仓库提供完整的使用指导，涵盖主题的**所有功能模块**。

## 内容

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 主技能文件（742行 / 24KB）— 全功能使用指南 |
| `references/api-endpoints.md` | REST API 端点参考 |
| `references/hooks-filters.md` | 主题 Hook / Filter 参考 |
| `references/service-classes.md` | 服务类参考 |
| `references/template-hierarchy.md` | 模板层级参考 |
| `references/theme-options.md` | 主题选项参考 |
| `scripts/update-pot.py` | 翻译 POT 文件更新脚本 |

## SKILL.md 章节

1. **文章写作与内容展示** — AI 摘要、AI 名词注释、文章目录、字数统计、许可协议、内容样式、代码高亮
2. **短代码（Shortcodes）** — APlayer/Meting 音乐播放器、Bilibili 视频、画廊、Gutenberg 块
3. **页面创建** — 首页组件系统、归档页面、友情链接、展示区、分类图片
4. **首页与封面** — 视频/图片封面、个人头像、文本 Logo
5. **社交媒体集成** — Bilibili、Steam、QQ、Bangumi、MyAnimeList、音乐播放器、图片上传
6. **评论系统** — AJAX 评论、验证码（CAPTCHA/Turnstile/Vaptcha）、QQ 头像
7. **导航与交互** — 导航菜单、Pjax 无刷新、实时搜索、灯箱效果、平滑滚动
8. **打赏** — 打赏二维码、爱发电/Ko-fi、文章底部作者信息
9. **主题外观** — 色彩系统、暗黑模式、纪念模式、自定义 CSS、字体
10. **页脚** — 一言、站点统计、CDN 赞助、樱花 SVG
11. **性能** — CDN 资源加载、缓存管理、PHP 错误级别、资源预加载
12. **更新维护** — 更新源配置、无缝更新

## 使用

### 作为技能加载

```text
skill_view(name="sakurairo-theme")
```

### 查看参考文件

```text
skill_view(name="sakurairo-theme", file_path="references/api-endpoints.md")
skill_view(name="sakurairo-theme", file_path="references/theme-options.md")
```

## 安装

```bash
git clone --depth 1 https://github.com/AKCX2002/sakurairo-theme.git
cp -r sakurairo-theme ~/.agents/skills/sakurairo-theme/
```

## 许可

[MIT](LICENSE)
