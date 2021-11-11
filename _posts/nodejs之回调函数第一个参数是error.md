---
title: nodejs之回调函数第一个参数是error
date: 2019-04-28 15:06:25
tags:
	- nodejs

---



nodejs约定：

1、如果一个函数需要一个回调函数做参数，那么回调函数是放在最后面。

2、回调函数的第一个参数是error对象。如果没有错误，就是null。

setTimeout不受这个约束。它的回调不是最后一个参数。



参考资料

1、nodejs错误优先？

https://segmentfault.com/a/1190000012430647

2、Node.js 概述

https://javascript.ruanyifeng.com/nodejs/basic.html