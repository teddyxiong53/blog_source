---
title: nodejs之querystring
date: 2019-05-09 17:51:11
tags:
	- nodejs

---



这个模块是用来对url里的参数进行解析和生成的。

常用的就是2个方法。

parse

stringify

就跟JSON的那2个方法差不多。

```
var querystring = require("querystring")
console.log(querystring.parse("a=1&b=2"))
```

运行：

```
{ a: '1', b: '2' }
```

```
var querystring = require("querystring")
console.log(querystring.stringify({a:1,b:2}))
```

运行：

```
a=1&b=2
```



参考资料

1、Node基础：url查询参数解析之querystring

https://www.cnblogs.com/chyingp/p/6037406.html