---
title: nodejs之打印对象的方法
date: 2018-12-24 14:42:17
tags:
	- nodejs
---



```
//方法1：打印格式比较好，有颜色。
//console.dir(process.env)
//方法2：格式跟上面一样，没有颜色
//var inspect = require('util').inspect
//console.log(inspect(process.env))
//方法3：格式不太好，但是使用最简单
//console.log("%j", process.env)
```



参考资料

1、node打印对象的2种方法

https://cnodejs.org/topic/54bfc3972d19f08315f355bb