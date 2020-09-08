---
title: css之flex布局
date: 2019-04-17 11:57:25
tags:
	- css

---

1

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



参考资料

1、Flex 布局教程：语法篇

http://www.ruanyifeng.com/blog/2015/07/flex-grammar.html

2、微信小程序开发:Flex布局

这个里面的图片很直观。

https://www.jianshu.com/p/f82262002f8a