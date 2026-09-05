# Arcaea 技术文档表格技巧

适用于 Sakurairo + Babel Arcaea Code 的长文、API 文档、架构拆解文。

目标不是把表格做成游戏界面截图，而是保留 Arcaea 的冷静秩序感，同时让读者能快速扫读信息。

## 核心原则

1. 表格优先服务信息分层，不优先服务氛围。
2. 技术文档默认使用低网格、强表头、弱行分隔。
3. 毛玻璃放在表格外层容器，不直接压在原生 `<table>` 原语上。
4. 表格内部只保留必要的层级：表头、行分隔、hover、重点标签。
5. 如果内容是“函数模式 / 组件职责 / API 摘要”，优先用增强型 `arcaea-feature-matrix`。

## 默认对比表

适用场景：

- 概念对比
- 参数说明
- 优缺点汇总
- 约束条件表

视觉规则：

- 外层容器使用深色实底渐变，降低背景图干扰
- `thead` 用 Arcaea Light 冰蓝渐变
- `tbody` 去掉纵向网格，只保留横向分隔
- hover 用低强度蓝色铺底，不做重发光

推荐结构：

```html
<div class="arcaea-table-wrap">
  <table>
    <thead>
      <tr><th>场景</th><th>推荐方案</th><th>原因</th></tr>
    </thead>
    <tbody>
      <tr><td>长文对比</td><td>统一对比表</td><td>信息密度稳定，读者容易扫读</td></tr>
    </tbody>
  </table>
</div>
```

## 增强型功能矩阵

适用场景：

- Widget / 组件模式
- API 功能区拆解
- 插件模块职责对照
- 函数签名 + 用途 + 行号索引

推荐结构：

```html
<table class="arcaea-feature-matrix">
  <thead>
    <tr>
      <th>模式</th>
      <th>签名 / 行号</th>
      <th>用途</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span class="func-name">_buildCard()</span></td>
      <td>
        <div class="signature">
          (<span class="sig-type">String</span> <span class="sig-name">title</span>,
          <span class="sig-type">Widget</span> <span class="sig-name">child</span>)
        </div>
        <span class="line-badge">L3496</span>
      </td>
      <td class="purpose">
        <span class="purpose-title">统一卡片容器</span>
        <span class="purpose-tag">容器</span>
        <span class="purpose-tag purple">布局</span>
        负责标题、内容和尾部操作区的共同外壳。
      </td>
    </tr>
  </tbody>
</table>
```

## 层级约定

从高到低：

1. 函数名 / 模式名
2. 用途标题
3. 签名块
4. 行号 badge

不要把“行号”做成第一视觉焦点。它是索引信息，不是正文。

## 颜色语义

- `Light / 冰蓝`：输入、结构、正文主强调
- `Conflict / 冷紫`：切换、动作、源码索引、次强调
- `Green / 绿色`：成功、状态正常、已连接
- `Orange / 橙色`：风险、告警、注意项

## 禁止事项

- 禁止传统 Excel 式强网格
- 禁止高透明表格导致背景图穿透文字
- 禁止在每个单元格里重复叠重阴影
- 禁止把函数签名直接写成一长行灰底文本
- 禁止让行号比用途说明更显眼

## 快速判断

如果读者需要“左右比较”，用默认对比表。  
如果读者需要“逐项理解组件职责”，用 `arcaea-feature-matrix`。  
如果一个表已经开始塞函数名、签名、标签、行号四类信息，就不要再把它当普通 `<table>` 处理。
