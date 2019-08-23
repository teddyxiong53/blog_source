---
title: nodejs之redis
date: 2019-08-22 17:53:03
tags:
	- nodejs
---

1

redis是什么？主要用来解决什么问题？



使用ioredis这个模块。

#基本用法

set和get。

```
var Redis = require("ioredis")
var redis = new Redis()
redis.set("foo", "bar")
redis.get("foo", function(err, result) {
    console.log(result)
})
redis.del("foo")
```

如果get函数里，最后一个参数不是回调，那么返回一个promise。

```
redis.get("foo").then(function(result) {
    console.log(result)
})
```



参考资料

1、

https://www.npmjs.com/package/ioredis

