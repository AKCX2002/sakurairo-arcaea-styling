# 服务集成类功能参考

主题集成了多种外部服务，通过 REST API 和页面组件实现功能。

## 媒体服务

### Bilibili
- 视频嵌入（短代码 `[bilibili bvid="..."]`）
- 追番数据展示
- 收藏夹展示
- 电影数据

### 音乐播放（APlayer + Meting）
- 在文章中嵌入音乐播放器
- 支持网易云音乐、QQ 音乐等
- 通过 Meting API 代理获取

### 图片画廊
- 图片集合展示
- 通过 REST API 获取图库数据

## 社交服务

### QQ
- 获取 QQ 用户头像和信息
- 用于评论区用户头像自动匹配

### Gravatar
- 支持配置 Gravatar 代理镜像
- 自定义代理地址

## 游戏服务

### Steam
- 展示 Steam 游戏库
- 需要 Steam API Key

### MyAnimeList
- 展示 MAL 动漫列表

## 安全服务

| 服务 | 说明 |
|---|---|
| CAPTCHA | 内置验证码，通过 API 生成 |
| Cloudflare Turnstile | 隐私友好替代方案 |
| Vaptcha | 语音/图片验证 |

## 工具服务

### 图片上传
支持多个后端图床：Imgur、SM.MS、Chevereto、Lsky Pro

### 缓存
外部数据通过 Transients 缓存，后台可管理缓存时长

### IP 定位
自动检测访客地理位置
