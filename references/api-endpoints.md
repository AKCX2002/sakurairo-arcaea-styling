# REST API 功能端点参考

所有自定义 API 端点注册在 `sakura/v1` 命名空间下。

## AI 文章摘要（管理员专用）

```
GET /wp-json/sakura/v1/chatgpt?post_id={文章ID}
```

为文章自动生成 AI 摘要。摘要存储到 `ai_summon_excerpt` 字段中，在前台单页文章顶部以蓝色框显示。

## AI 名词注释（管理员专用）

```
GET /wp-json/sakura/v1/chatgpt/annotate?post_id={文章ID}
```

自动识别文章中的复杂术语并生成浮动注释。注释数据存储在 `iro_chatgpt_annotations` 字段中。

## 图片上传

```
POST /wp-json/sakura/v1/image/upload
```

上传图片到配置的图床（Imgur / SM.MS / Chevereto / Lsky Pro）。

## QQ 信息查询

```
GET /wp-json/sakura/v1/qqinfo/json
```

获取 QQ 用户信息，用于评论区头像展示。

## 验证码生成

```
GET /wp-json/sakura/v1/captcha/create
```

生成 CAPTCHA 验证码，用于评论表单。

## 音乐数据

```
GET /wp-json/sakura/v1/meting/aplayer
```

获取网易云/QQ 音乐数据供 APlayer 播放器使用。

## 归档信息

```
GET /wp-json/sakura/v1/archive_info
```

获取文章归档统计（缓存 30 秒）。

## 追番数据

```
POST /wp-json/sakura/v1/bangumi/bilibili
POST /wp-json/sakura/v1/bangumi
```

Bilibili 和 Bangumi.tv 追番数据。

## Steam 游戏库

```
POST /wp-json/sakura/v1/steam
```

获取 Steam 游戏库数据。

## Bilibili 内容

```
POST /wp-json/sakura/v1/movies/bilibili
GET  /wp-json/sakura/v1/favlist/bilibili
GET  /wp-json/sakura/v1/favlist/bilibili/folders
```

## 画廊

```
GET /wp-json/sakura/v1/gallery
```

## 缓存说明

外部 API 数据通过 WordPress Transients 缓存，可在后台「缓存设置」页面管理。
