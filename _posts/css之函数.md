---
title: css之函数
date: 2019-04-22 14:07:25
tags:
	- css

---



sass、less是两种css预处理器。

css3吸收了它们的一些东西。

也提供了一些函数。

目前css的函数有：

```
calc
toggle
```



calc

举例：

```
width: calc(100% - 100px);
```

注意，中间运算符左右都要有空格。



CSS 中有一些常用的函数，可以帮助你实现各种样式效果。以下是一些常用的 CSS 函数：

1. `calc()`: 计算函数，用于计算长度、宽度、高度等值。
2. `var()`: 自定义属性函数，用于访问自定义属性的值。
3. `rgb()`, `rgba()`: 颜色函数，用于定义 RGB 颜色值。
4. `hsl()`, `hsla()`: 颜色函数，用于定义 HSL 颜色值。
5. `url()`: URL 函数，用于定义背景图像或其他资源的 URL。
6. `linear-gradient()`, `radial-gradient()`: 渐变函数，用于定义线性渐变或径向渐变。
7. `transform()`: 变换函数，用于定义元素的变换效果，如旋转、缩放、平移等。
8. `translate()`, `scale()`, `rotate()`: 变换函数，用于定义元素的变换效果。
9. `filter()`: 滤镜函数，用于定义元素的滤镜效果，如模糊、饱和度等。
10. `clamp()`: 限制函数，用于限制值的范围。

这些函数可以帮助你实现各种样式效果，提高 CSS 代码的灵活性和可维护性。



参考资料

1、CSS3的函数和事件

https://blog.csdn.net/creabine/article/details/80967238