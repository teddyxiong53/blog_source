---
title: css之flex布局
date: 2019-04-17 11:57:25
tags:
	- css

---



布局的传统解决方案，基于[盒状模型](https://developer.mozilla.org/en-US/docs/Web/CSS/box_model)，依赖 [`display`](https://developer.mozilla.org/en-US/docs/Web/CSS/display) 属性 + [`position`](https://developer.mozilla.org/en-US/docs/Web/CSS/position)属性 + [`float`](https://developer.mozilla.org/en-US/docs/Web/CSS/float)属性。它对于那些特殊布局非常不方便，比如，[垂直居中](https://css-tricks.com/centering-css-complete-guide/)就不容易实现。

2009年，W3C 提出了一种新的方案----Flex 布局，可以简便、完整、**响应式地实现各种页面布局**。目前，它已经得到了所有浏览器的支持，这意味着，现在就能很安全地使用这项功能。

Flex 布局将成为未来布局的首选方案。

任何一个容器都可以指定为 Flex 布局。

行内元素也可以使用 Flex 布局。

注意，设为 Flex 布局以后，子元素的`float`、`clear`和`vertical-align`属性将失效。



看看骰子的布局。

一个骰子的一面最多9个点。

我们把各种情况都布局出来看看。





设置了display为flex或者display为block的元素，就是一个flex容器。

里面的元素就是flex item。



# flex布局

Flexbox（弹性盒子布局）是一种 CSS 布局模型，旨在为复杂的布局提供更简单和更高效的方式。它允许容器内的子元素（即弹性项目）灵活地排列、对齐和分配空间。以下是 Flexbox 的一些关键特点和概念：

### 1. **基本概念**
- **容器**：使用 `display: flex;` 或 `display: inline-flex;` 将元素定义为弹性容器。
- **项目**：弹性容器内的直接子元素称为弹性项目。

### 2. **主要属性**

#### 容器属性
- **`flex-direction`**：设置主轴的方向（行或列）。
  - `row`（默认）：从左到右排列。
  - `column`：从上到下排列。
  
- **`justify-content`**：定义主轴上的对齐方式。
  - `flex-start`：起始对齐。
  - `flex-end`：结束对齐。
  - `center`：居中对齐。
  - `space-between`：项目之间均匀分配空间。
  - `space-around`：项目周围均匀分配空间。

- **`align-items`**：定义交叉轴上的对齐方式。
  - `flex-start`：起始对齐。
  - `flex-end`：结束对齐。
  - `center`：居中对齐。
  - `baseline`：基线对齐。
  - `stretch`（默认）：拉伸以填满容器。

- **`flex-wrap`**：控制项目是否换行。
  - `nowrap`（默认）：不换行。
  - `wrap`：换行。
  - `wrap-reverse`：反向换行。

#### 项目属性
- **`flex-grow`**：定义项目的放大比例。
- **`flex-shrink`**：定义项目的缩小比例。
- **`flex-basis`**：定义项目的初始大小。
- **`align-self`**：允许单个项目在交叉轴上有不同的对齐方式。

### 3. **示例**

以下是一个简单的 Flexbox 示例：

```html
<div style="display: flex; justify-content: space-between; align-items: center;">
  <div style="flex: 1;">Item 1</div>
  <div style="flex: 2;">Item 2</div>
  <div style="flex: 1;">Item 3</div>
</div>
```

### 4. **优点**
- **响应式设计**：Flexbox 提供了更灵活的布局方式，适合不同屏幕尺寸。
- **简单易用**：通过少量的 CSS 属性，可以实现复杂的布局。
- **对齐与空间分配**：轻松控制项目的对齐和间距。

### 结论
Flexbox 是现代网页布局的重要工具，特别适合需要动态调整和对齐的场景。如果你有更具体的问题或需要进一步的示例，请告诉我！

# 参考资料

1、Flex 布局教程：语法篇

http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html

2、微信小程序开发:Flex布局

这个里面的图片很直观。

https://www.jianshu.com/p/f82262002f8a