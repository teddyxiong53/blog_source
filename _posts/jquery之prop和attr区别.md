---
title: jquery之prop和attr区别
date: 2019-03-04 10:56:03
tags:
	- jquery
---





jquery从1.6版本开始新增prop函数。

之前用的是attr函数。

为什么要新增prop函数？

因为attr函数有行为不一致的问题。

什么时候用attr？什么时候用prop？

官方的建议是：

具有true和false这2个属性的属性，例如checked、selected。就用prop。其余用attr。

尽量用prop函数。



什么是attribute？什么是property？

attributes 是 HTML 元素（标签）的属性，而 properties 是 DOM 对象的属性。



参考资料

1、jQuery 中 attr() 和 prop() 方法的区别

https://blog.wenzhixin.net.cn/2013/05/24/jquery_attr_prop/

2、jQuery 的 attr 与 prop 的区别

https://github.com/JChehe/blog/blob/master/posts/jQuery 的 attr 与 prop 的区别.md