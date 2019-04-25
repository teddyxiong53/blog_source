---
title: nodejs之crypto模块
date: 2018-12-28 11:55:17
tags:
	- nodejs
---

1

crypto模块的功能就是加密解密。

借助的是openssl的实现。

包括了md5、sha1等算法。

crypto.createHash

这个函数是创建一个hash实例，这个函数接收字符串参数。

字符串可以是：md5、sha1、sha256、sha512。



```
const crypto = require("crypto");
function sha256(value) {
    let shasum = crypto.createHash("sha256");
    shasum.update(value);
    return shasum.digest('hex');
}
console.log(sha256("12"));
console.log(sha256("34"));
```

 参考资料

1、浅谈nodejs中的Crypto模块

https://cnodejs.org/topic/504061d7fef591855112bab5

2、crypto模块

http://nodejs.cn/api/crypto.html