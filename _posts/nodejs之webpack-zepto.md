---
title: nodejs之webpack-zepto
date: 2021-01-05 11:34:11
tags:
	- nodejs

---

1

# zepto

Zepto是一个轻量级的针对现代高级浏览器的JavaScript库， 它与jquery有着类似的api。 如果你会用jquery，那么你也会用zepto。

设计的目的是提供jquery的类似的APIs，但并不是100%覆盖jquery为目的。



webpack-zepto是为了给zepto增加import这种模块语法。



既然zepto跟jquery类似，那么zepto存在的意义是什么？

zepto更加适合在移动端使用。

我们先看jquery是什么。

jquery是一个js函数库。特点是：写得少做得多。还有丰富的插件。

可以做：html元素选取、html元素操作、css操作、html事件函数、js动画、html dom遍历和修改。ajax等等。



zepto的设计目标是：

一个5到10K大小的通用库。

有你熟悉的api。



zepto是为智能手机浏览器推出的js框架。

zepto不支持IE浏览器，因为手机端没有这个浏览器。

重点对tap、swipe操作进行优化。



总的来说，zepto就是移动端的jquery。精简实用版本。



参考资料

1、关于webpack-zepto的一个问题

https://segmentfault.com/q/1010000011348799

2、zepto文档

http://www.wenshuai.cn/manual/zepto/

3、zepto.js 源码解析

https://www.runoob.com/w3cnote/zepto-js-source-analysis.html

4、Zepto和Jquery的区别，以及在做移动端开发时，我们为什么选择使用zepto

https://juejin.cn/post/6844903793197318151

5、为什么我们放弃了 Zepto

https://neveryu.github.io/2017/02/14/why-we-dropped-zepto/