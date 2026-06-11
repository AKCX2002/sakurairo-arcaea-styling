# Prism/Mermaid 冲突调试记录

> ⚠️ **仅限历史参考**
> 本文档记录的是 babel-arcaea-mermaid 旧版本的 Prism/Mermaid 冲突调试过程。
> **当前 babel-arcaea-code 插件已通过 PHP `the_content` filter 在服务端解决此问题。**
> 本文输出格式和 JS 方案均为旧版做法，**不可直接复制为当前实现**。

## 问题

WordPress 页面中 `<pre><code class="language-mermaid">` 无法渲染为 Mermaid SVG，
且在浏览器控制台报错：
```
prism-toolbar.js:101 Uncaught TypeError: Cannot read properties of null (reading 'classList')
```

## 根因

Prism.js autoloader 异步加载 `prism-mermaid.min.js` 组件。
其 `setTimeout` 回调持有原始 `<pre>` 元素引用。
当 Mermaid 插件的前端原型方案将 `<pre>` 替换为 Mermaid 容器后，
Prism 回调尝试在已不存在的 `<pre>` 上操作 → null 错误。

## 失败方案（按尝试顺序）

| 方案 | 结果 |
|------|------|
| MutationObserver 拦截 head inline script | ❌ Prism 在此之前已发起请求 |
| `classList.add('no-highlight', 'language-none')` | ❌ Autoloader 闭包持原引用 |
| `pre.style.display = 'none !important'` | ❌ 仍触发 toolbar hook |
| Patch `Prism.highlightElement` | ❌ toolbar 插件直接访问 `env.element.parentNode` |
| 两遍遍历（先标记 no-toolbar，再 replaceWith） | ❌ 时序不可控 |

## 最终方案 ✅：PHP 服务端替换

```php
add_filter('the_content', function ($content) {
    $pattern = '/<pre[^>]*>\s*<code[^>]*class="[^"]*language-mermaid[^"]*"[^>]*>(.*?)<\/code>\s*<\/pre>/si';
    return preg_replace_callback($pattern, function ($m) {
        $code = trim(html_entity_decode($m[1], ENT_QUOTES | ENT_HTML5, 'UTF-8'));
        if (!$code) return $m[0];
        return '<div class="arcaea-mermaid-box"><pre class="mermaid">'
            . esc_html($code) . '</pre></div>';
    }, $content);
}, 1);  // priority 1: before wpautop (10)
```

页面 HTML 源码中永远不出现 `language-mermaid` 字符串，
Prism autoloader 扫描不到 → 不会加载 prism-mermaid 组件 → 无冲突。

## 附录：Sakurairo 主题的 Prism 加载链

```
Sakurairo page.js (webpack bundle)
  → code-highlight.js
    → Prism.highlightElement(element)
      → prism-autoloader.js
        → fetch prism-mermaid.min.js from CDN
          → setTimeout callback → insertHighlightedCode
            → prism-toolbar.js → toolbar.hook → classList null
```

Mermaid 插件在 footer 用 `wp_enqueue_script(..., true)` 加载，
但 Sakurairo 的 `code-highlight.js` 已经在 header 执行。
任何 JS 方案都无法在 Prism 发起请求前完成标记。
