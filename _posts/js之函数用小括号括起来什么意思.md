---
title: js之函数用小括号括起来什么意思
date: 2018-12-27 10:02:27
tags:
	- js
---





```
(function() {
	//code
})();
```

这个叫做自执行匿名函数。

主要用途是限制作用范围的。避免命名冲突。

js库一般都是这么做的。





参考资料

1、JS中(function(){xxx})(); 这种写法是什么意思？

https://segmentfault.com/q/1010000000135703