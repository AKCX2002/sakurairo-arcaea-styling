# WordPress 插件 CI/CD 模式 — 本地资产 + 完整克隆 + 自动更新

## 适用场景

WordPress 插件需要本地化前端依赖（Prism、Mermaid、MathJax 等），并且希望：
- 不依赖 CDN（避开 Tracking Prevention 拦截）
- 资产版本自动追踪上游更新（而非硬编码下载列表）
- GitHub push 自动构建 release zip + 自动 bump patch
- WordPress 后台可见更新提示（PUC library）

## 仓库结构

```
plugin-name/
├── plugin-name.php              # 主插件
├── assets/
│   ├── prism/
│   │   ├── prism.js             # 核心 (下载)
│   │   ├── prism.css            # Arcaea × Night Owl 主题 (版本控制)
│   │   ├── prism-*.js           # 27 个插件 (jsDelivr API 发现+下载)
│   │   ├── prism-*.css          # 插件配套 CSS
│   │   └── components/
│   │       └── prism-*.js       # 298 种语言组件 (jsDelivr API 发现+下载)
│   ├── mermaid/
│   │   ├── mermaid.esm.min.mjs  # 主入口 (下载)
│   │   ├── mermaid.css          # Arcaea 玻璃容器 (版本控制)
│   │   ├── mermaid-init.js      # 初始化脚本 (版本控制)
│   │   └── chunks/mermaid.esm.min/
│   │       └── *.mjs + *.map    # N 个 chunk (数量随版本变化，jsDelivr API 发现+下载)
│   ├── mathjax/es5/
│   │   └── tex-chtml.js         # MathJax 3.x (jsDelivr 下载)
│   └── js/
│       └── medium-zoom.min.js   # 图片灯箱 (jsDelivr 下载)
├── lib/                          # PUC library (版本控制)
│   └── plugin-update-checker.php
├── .github/workflows/
│   └── release.yml              # CI: 刷新资产 → bump → release + 每日同步
├── download-prism.sh             # Prism 完整克隆脚本 (版本控制)
├── download-mermaid.sh           # Mermaid 完整克隆脚本 (版本控制)
└── README.md
```

## CI 工作流

### Job 1: bump-and-release（每次 push main）

```yaml
on: push
branches: [main]
paths-ignore: ['**.md', '.gitignore']
```

步骤：
1. **Refresh Prism** — `bash download-prism.sh $(current_version)` — 下载所有缺失的插件/语言
2. **Refresh Mermaid** — `bash download-mermaid.sh $(current_version)` — 下载所有缺失的 chunk
3. **Refresh MathJax** — `curl` 下载 tex-chtml.js
4. **Auto-bump** — 读取 `Version: x.x.x` → patch+1 → commit `[skip ci]` → push
5. **Build zip** — `cp -r plugin-name.php assets lib` → `zip`（注意内部目录名需匹配 slug）
6. **Create Release** — `gh release create "v$VER" "/tmp/$ZIPNAME"`

### Job 2: sync-deps（每日 06:00 / workflow_dispatch）

```yaml
on:
  schedule:
    - cron: '0 6 * * *'
```

步骤：
1. 始终运行 `download-mermaid.sh $LATEST_VERSION`（无论版本是否变化）
2. 始终运行 `download-prism.sh $LATEST_VERSION`
3. 始终下载最新 MathJax
4. 如果版本变化 → 更新 PHP 版本常量 → 创建 PR

### 完整克隆脚本

#### download-prism.sh

不依赖硬编码列表，通过 jsDelivr API 自动发现所有文件：

```bash
curl -sL "https://data.jsdelivr.com/v1/packages/npm/prismjs@${VER}" | python3 -c "
import json, os, urllib.request
d = json.load(sys.stdin)
# 递归遍历所有文件，过滤出:
# - plugins/xxx/prism-xxx.min.js  → flat 到 assets/prism/prism-xxx.js
# - plugins/xxx/prism-xxx.min.css → flat 到 assets/prism/prism-xxx.css
# - components/prism-xxx.min.js   → 放到 assets/prism/components/prism-xxx.js
# 跳过已存在的文件（仅下载缺失的）
"
```

路径 bug 注意：jsDelivr API 返回的嵌套目录结构中，前两个层级无前导 `/`，第三层级开始有 `/`。检查路径时应使用 `'plugins/' in name`（不带前导 `/`），而非 `'/plugins/' in name`（带前导 `/`）。后者在第二层级子目录名称中匹配不到文件路径。

#### download-mermaid.sh

原理同 Prism，但过滤 chunk 文件：

```bash
curl -sL "https://data.jsdelivr.com/v1/packages/npm/mermaid@${VER}" | python3 -c "
# 过滤 dist/chunks/mermaid.esm.min/*.mjs
# 同时下载 .mjs.map 文件
# 跳过已存在的文件
"
```

## 插件自动更新（PUC）

集成 [YahnisElsts/plugin-update-checker](https://github.com/YahnisElsts/plugin-update-checker)：

```php
require_once 'lib/plugin-update-checker.php';
$uc = PucFactory::buildUpdateChecker(
    'https://github.com/user/plugin-name/', __FILE__, 'plugin-name'
);
$uc->getVcsApi()->enableReleaseAssets();     // 启用 zip 附件检测
$uc->getVcsApi()->setAuthentication($token);  // 推荐，提速率 60→5000 req/h
```

Release zip 三要素：
1. 内部目录名匹配插件 slug（不带版本号），否则解压路径错误
2. 包含 `lib/` 目录（PUC 库本身），否则更新后 PUC 丢失
3. `enableReleaseAssets()` 开启 zip 附件检测

## 关键教训

1. **Mermaid「Syntax error in text」→ 先查 Console 404**：缺失 ESM chunk 文件时 Mermaid 报 `Syntax error in text`（而非 404 警告），极易被误判为图表语法错误。打开 F12 → Console → 搜索 `Failed to load resource`。

2. **不要硬编码下载列表，用 API 全量发现**：`data.jsdelivr.com/v1/packages/npm/xxx@${VER}` 返回完整文件树。遍历 + 过滤让 CI 自动适配新版本的文件结构调整，无需手动更新下载脚本。

3. **「仅下载缺失的」vs「完整克隆」**：版本不变时只需补缺失文件（快）；版本变化时新 hash 文件名导致所有文件被视为「缺失」，实际等价于完整克隆。两全其美。

4. **PHP filter 必须在 Prism 之前**：`add_filter('the_content', $fn, 1)`（priority 1）确保在 Prism autoloader 扫描前替换 language-mermaid。JS DOM 方案无法解决 Prism 异步回调的 race condition。

5. **LightGallery 主题冲突**：Sakurairo 主题自带 LightGallery v2，需抑制 license 警告：
   ```js
   console.warn = function(){/* filter 'license key' */};
   ```

6. **APlayer 空容器**：主题在无播放器页面也尝试初始化，需 patch prototype：
   ```js
   APlayer.prototype.init = function(){if(!container exists) return};
   ```

7. **设置页显示实时资产数**：WordPress 后台设置页用 `glob()` 扫描插件目录，动态显示语言和 chunk 数量，便于运维确认：
   ```php
   $langs = glob(BAC_PLUGIN_DIR . 'assets/prism/components/prism-*.js');
   echo count($langs) . ' 种语言';
   ```
