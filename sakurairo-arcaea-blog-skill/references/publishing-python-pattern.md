# Python REST API 发布最小模板

> 适用于 babel-arcaea-code 插件的 WordPress 博客文章/页面发布。
> 使用 WordPress REST API + Application Password 认证，Python `urllib` 实现。
> **不依赖任何第三方包。**

## 发布新文章

```python
import base64, json, urllib.request

site = "https://example.com"
auth = base64.b64encode(b"user:app-password").decode()
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# 文章内容 — 使用 .arcaea-article-content 包裹，无需内联 Mermaid 补丁脚本
html = '''<div class="arcaea-article-content">
<p>正文内容...</p>
<pre><code class="language-c">int main() { return 0; }</code></pre>
</div>'''

data = json.dumps({
    "title": "文章标题",
    "slug": "article-slug",
    "content": html,
    "categories": [1],          # 分类 ID，先 GET /wp-json/wp/v2/categories 确认
    "status": "publish",
    "excerpt": "50-120 字的中文摘要"
}).encode()

req = urllib.request.Request(
    f"{site}/wp-json/wp/v2/posts",
    data=data, headers=headers, method="POST"
)
resp = json.loads(urllib.request.urlopen(req).read())
print(f"✅ #{resp['id']} {resp['title']['rendered']} — {resp['link']}")
```

## 更新已有文章

```python
import base64, json, urllib.request, time

site = "https://example.com"
auth = base64.b64encode(b"user:app-password").decode()
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

post_id = 123  # 目标文章 ID

# 1. 先用 context=edit 获取 raw 内容（未被 wpautop 污染）
req = urllib.request.Request(
    f"{site}/wp-json/wp/v2/posts/{post_id}?context=edit&_fields=id,content",
    headers=headers
)
p = json.loads(urllib.request.urlopen(req).read())
raw = p['content']['raw']

# 2. 修改 raw（字符串替换或正则）
new_raw = raw.replace('旧文本', '新文本')

# 3. POST 回同一端点
data = json.dumps({"content": new_raw}).encode()
req2 = urllib.request.Request(
    f"{site}/wp-json/wp/v2/posts/{post_id}",
    data=data, headers=headers, method="POST"
)
resp2 = json.loads(urllib.request.urlopen(req2).read())
print(f"✅ #{post_id} 更新成功")
time.sleep(0.5)  # 避免限频
```

## 列出所有文章（含分类/标签）

```python
import base64, json, urllib.request

site = "https://example.com"
auth = base64.b64encode(b"user:app-password").decode()
headers = {"Authorization": f"Basic {auth}"}

req = urllib.request.Request(
    f"{site}/wp-json/wp/v2/posts?per_page=100&context=edit&_fields=id,title,slug,content,categories,excerpt",
    headers=headers
)
posts = json.loads(urllib.request.urlopen(req).read())
for p in posts:
    print(f"#{p['id']} {p['title']['rendered']} — slug={p['slug']}")
```

## 安全注意

- **禁止**在命令行使用 `curl -u "user:pass"` — 凭证会泄露到 shell history
- **禁止**在代码中硬编码 Application Password — 使用环境变量或临时变量
- wpautop 不会破坏 `<pre>` 标签，但会在 `<style>` 块内插入 `<p>` — CSS 须紧凑单行
