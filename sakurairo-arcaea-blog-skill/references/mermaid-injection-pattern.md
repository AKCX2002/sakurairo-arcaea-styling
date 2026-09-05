# Mermaid 批量注入模式

为技术文章批量添加 Mermaid 架构图/状态图/时序图。

## 图类型选择

| 文章主题 | 图类型 | 说明 |
|---------|--------|------|
| 架构/分层/BSP | `flowchart TB` | 子系统上下排列 |
| 工具链/流程 | `flowchart LR` | 左右流程 |
| 状态机/RTOS | `stateDiagram-v2` | 状态迁移 |
| 协议/通信/时序 | `sequenceDiagram` | 参与者交互 |
| 数据流/依赖 | `flowchart TD/flowchart LR` | 依赖关系 |
| bug 复盘 | `flowchart` + 高亮节点 | 因果链 |

## 节点样式

所有节点加 `style` 适配 Arcaea 深色毛玻璃背景：

```css
style NodeName fill:transparent,stroke:#8dc7ff,color:#eaf4ff
```

决策/条件节点（菱形）用 `stroke:#ffd700`（金色醒目），问题节点用 `stroke:#ff6b6b`（红色警告）。

## 插入位置

Mermaid 代码块插入在文章第一个 `</p>` 之后（引言段落后），第一个 `<h2>` 之前。

```python
first_p_end = content.find('</p>')
first_h2 = content.find('<h2')
if first_h2 > 0 and first_h2 < first_p_end + 10:
    first_p_end = content.find('</p>', first_h2)
insert_pos = first_p_end + 4
```

## 注入检查

注入前检查 `'mermaid' in content`，跳过已有图表的文章，避免二次注入。

## 格式

Mermaid 代码块的正确格式（插件 PHP filter 识别并转换这种输入）：

```html
<pre><code class="language-mermaid">flowchart TD
    A --> B
</code></pre>
```

**禁止**用 `<p>\`\`\`mermaid</p>`——wpautop 会在每行插 `<br />`，插件 JS 匹配不到，永不渲染。

## 批量更新

通过 WordPress REST API `context=edit` 获取 `content.raw`（原始 HTML），修改后 POST 回同一端点。

```python
# 读取 raw
req = urllib.request.Request(f"{site}/wp-json/wp/v2/posts/{pid}?context=edit&_fields=id,content", headers=headers)
p = json.loads(urllib.request.urlopen(req).read())
raw = p['content']['raw']

# 修改后 POST
data = json.dumps({"content": new_raw}).encode()
urllib.request.urlopen(urllib.request.Request(f"{site}/wp-json/wp/v2/posts/{pid}", data=data, headers=headers, method="POST"), timeout=60)
```
