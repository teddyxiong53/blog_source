---
title: nodejs之error-first回调参数
date: 2019-05-13 15:02:11
tags:
	- nodejs

---

1

如果说v8引擎是nodejs应用的心脏，那么回调就是它的血管。

为了让回调之间配合好，需要约定一些东西。

error-first回调就是这样的一个约定。

所谓error-first，就是回调函数的第一个参数，一定是表示error的对象。

而第二个参数，是正常返回的数据。





参考资料

1、The Node.js Way - Understanding Error-First Callbacks

http://fredkschott.com/post/2014/03/understanding-error-first-callbacks-in-node-js/

2、为何Node.js的回调函数第一个参数是err

https://segmentfault.com/q/1010000004261509