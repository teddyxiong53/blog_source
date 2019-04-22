---
title: 网页之viewport
date: 2019-03-18 14:57:32
tags:
	- 网页

---





viewport是用户网页的可见区域。

手机浏览器是把页面放在一个虚拟的窗口里。

通常这个虚拟的窗口比真实的手机屏幕要宽。

这样用户可以通过拖动页面来看网页内容，对于那些没有针对移动端优化的网页来说，这种特性还是很有用的。

这个是针对固定宽度布局的网站。

而对于流动布局的，那么体验会非常糟糕。

设想一下，一个30%的侧边栏，对于320px的手机屏幕，只有96px，只能容纳8个12px的汉字。

为了让手机也能获得良好的网页浏览体验，Apple找到了一个办法：

在ios版本的Safari里，定义了viewport的标签。

它的作用就是创建一个虚拟的窗口。





一个常用的针对移动端优化过的页面的meta标签这样设置：

```
<meta name="viewport" content="width=device-width, initial-scale=1.0" >
```



跟viewport相关的单位是vw。

一个viewport的宽度是100vw。



参考资料

1、响应式 Web 设计 - Viewport

http://www.runoob.com/css/css-rwd-viewport.html

2、什么是viewport，为什么需要viewport

https://www.cnblogs.com/diantao/p/5292652.html

3、

https://www.html.cn/book/css/values/length/vw.htm