---
name: connected-photo-grid
description: Turn a collection of photographs into a coherent 3x3 connected photo composition. Select the strongest nine images, analyze visual relationships between neighboring images, and create cross-grid continuity through matching shapes, colors, directions, objects, textures, and spatial forms.
---

# Connected Photo Grid

将多张照片组织成一个具有跨格视觉连续性的 3×3 摄影作品。

核心原则：

> 九张照片不是九个独立画面，而是一张被切成九块的整体视觉作品。

## Decision Priority

发生冲突时，按以下优先级：

1. 摄影主体可识别
2. 原始照片质感保持
3. 相邻照片之间形成明确视觉连接
4. 整体构图优先于单张照片
5. 色彩关系统一
6. 避免过度 AI 化
7. 避免为了连接而破坏原始照片

---

# Workflow

## Step 1 — Analyze All Images

分析全部输入照片，而不是只分析前 9 张。

为每张照片提取：

- main subject
- dominant colors
- horizon direction
- major diagonal lines
- strong shapes
- foreground
- middle ground
- background
- sky / mountain / water / road regions
- human / animal / architecture
- distinctive local cultural elements
- visual movement
- possible incoming connection
- possible outgoing connection

---

## Step 2 — Select the Best Nine

不要默认选择前九张。

综合考虑：

- photographic quality
- subject diversity
- visual compatibility
- color compatibility
- directional compatibility
- connection potential
- narrative value

避免九张照片内容高度重复。

---

## Step 3 — Build the Connection Graph

建立 3×3 网格：

```text
A B C
D E F
G H I
```

分析 12 条主要邻接关系：

```text
A-B
B-C
D-E
E-F
G-H
H-I
A-D
D-G
B-E
E-H
C-F
F-I
```

每条连接评估：

- direction continuity
- shape continuity
- color continuity
- object continuity
- texture continuity
- spatial continuity
- narrative continuity

---

## Step 4 — Identify Connection Anchors

每张图片寻找：

- incoming anchor
- outgoing anchor

连接可以通过：

- continuation
- extension
- overlap
- visual echo
- color bridge
- shape bridge
- directional movement

实现。

例如：

```text
mountain ridge
      ↓
prayer flag
      ↓
river
      ↓
waterfall
      ↓
road
      ↓
grassland
```

这里的例子不是固定模板。Agent 应根据实际照片寻找真实存在的视觉关系。

---

## Step 5 — Compose the 3×3

优先保证整体构图。

允许：

- 山脊跨越边界
- 道路方向延伸到下一格
- 河流从一格流入另一格
- 经幡颜色跨格呼应
- 云层形状跨格延续
- 花、草、石头形成视觉接力
- 建筑轮廓与下一张照片形成形状呼应

不要让每张图片都只是独立的“照片卡片”。

---

## Step 6 — Preserve Photographic Reality

默认：

- 保留真实摄影质感
- 保留原始光影
- 保留真实纹理
- 保留自然颜色
- 不把照片变成插画
- 不加入没有来源的幻想物体
- 不使用过度超现实元素

如果用户指定风格，再进行风格化。

---

## Step 7 — Apply Global Color Direction

当用户指定整体色彩方向时，优先进行全局统一，而不是逐张强行上色。

例如用户指定：

```text
black + dark red
```

可以通过：

- 深红经幡
- 红色衣物
- 红色建筑
- 暗红夕阳
- 黑色山体
- 深色阴影

形成整体色彩关系。

同时保留原照片中的少量自然颜色作为视觉跳色。

---

# Quality Gate

最终输出前检查：

## Composition

- 是否真的形成 3×3 整体？
- 是否存在明确的视觉流动？
- 中心区域是否过重？

## Connections

检查全部 12 条邻接关系。

每条关系都应该有明确的视觉理由；如果连接明显失败，应优先重新排列照片，而不是强行添加装饰。

## Photography

- 原照片是否仍然真实？
- 主体是否被破坏？
- 是否出现明显 AI 生成痕迹？

## Color

- 是否具有统一的整体色彩方向？
- 是否仍保留自然照片中的颜色？

## Local Identity

如果照片来自特定地区：

- 地貌是否真实？
- 建筑是否真实？
- 文化元素是否真实？
- 是否加入了不存在的“旅游符号”？

## Final Test

缩小到手机屏幕尺寸观看。

如果只能看到“9 张漂亮照片”，而看不到“一张完整作品”，则需要重新排列。

---

# Output Principle

默认优先输出最终视觉作品。

如果用户要求解释，则说明：

1. 为什么选择这九张
2. 主要视觉连接是什么
3. 整体构图的视觉动线是什么
4. 色彩策略是什么

不要默认输出完整内部推理或冗长过程。
