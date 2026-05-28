# 自定义字段（Post Meta）参考

主题使用 WordPress 自定义字段存储一些特殊数据。

## AI 相关字段

| 字段名 | 类型 | 说明 |
|---|---|---|
| `ai_summon_excerpt` | 文本 | ChatGPT 生成的文章摘要 |
| `iro_chatgpt_annotations` | 数组 | ChatGPT 生成的名词注释数据 |

## 文章相关字段

| 字段名 | 类型 | 说明 |
|---|---|---|
| `post_words_count` | 整数 | 文章字数统计 |
| `license` | 文本 | 单篇文章的许可协议覆盖 |

## 友链检测字段

| 字段名 | 类型 | 说明 |
|---|---|---|
| `_link_check_status` | 文本 | 链接状态检测结果 |
| `_link_check_time` | 文本 | 上次检测时间 |
| `_link_failure_count` | 整数 | 连续失败次数 |
| `_link_status_code` | 整数 | HTTP 状态码 |
| `_link_error_message` | 文本 | 错误信息 |

## 数据缓存（Transients）

| 缓存键 | 缓存内容 | 默认有效期 |
|---|---|---|
| `bangumi_cache` | Bilibili/Bangumi 追番数据 | 后台可配置 |
| `steam_cache` | Steam 游戏库数据 | 后台可配置 |
| `time_archive` | 归档页统计信息 | 30 秒 |
