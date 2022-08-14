---
title: uniapp之nvue
date: 2022-07-31 14:56:28
tags:
	- uniapp
---

--

uni-app一共有两种渲染方式:

一种是写 .vue 最后以 web-view 渲染出页面, 这种模式因是基于浏览器所以很容易做到在ios和Android页面保持一致, 但是这种模式有一个致命的缺点: 性能问题

第二种是写 .nvue文件, 采用 weex 技术渲染成原生组件, 这种模式性能没得话说, 但是因为局限于 weex 本身的原因, 在有些方法很难做到ios和Android页面保持一致



list是app端**nvue**专用组件。在**app-nvue**下，如果是长列表，使用`list`组件的性能高于使用**view**或**scroll-view**的滚动。原因在于`list`在不可见部分的渲染资源回收有特殊的优化处理。





参考资料

1、uni-app中nvue如何制作侧滑菜单, 安卓机解决方案, 低端机型解决方案

https://blog.csdn.net/qq_54690422/article/details/120943712