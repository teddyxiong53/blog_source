---
title: html之脚本放在head和body的区别
date: 2021-01-22 11:47:11
tags:
	- html

---

--

放在body中：在页面加载的时候被执行

放在head中：在被调用时被执行

原因：

1、浏览器是从上到下解析HTML的。 

2、放在head里的js代码，会在body解析之前被解析；放在body里的js代码，会在整个页面加载完成之后解析。



参考资料

1、script放在body和放在head的区别

https://www.cnblogs.com/hh-kk/p/7775261.html