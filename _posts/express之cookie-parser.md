---
title: express之cookie-parser
date: 2020-12-28 17:10:11
tags:
	- nodejs

---

1

先看一个简单的例子。

```
var express = require('express')
var cookieParser = require('cookie-parser')
var app = express()

app.use(cookieParser())
app.use(function(req, res, next) {
  console.log(req.cookies.nick)
  next()
})
app.use(function(req, res, next) {
  res.cookie('nick', 'xxx')
  res.end()
})
app.listen(8080)
```

可以没有路由。可以只有中间件。

设置cookie。

```
res.cookie('cookie_name', 'cookie_value')
```

读取cookie

```
req.cookies.cookie_name
```



为了安全，我们通常需要对cookie进行签名。

具体做法是：

1、在cookieParse初始化的时候，传入secret作为前面的密钥。

2、设置cookie的时候，把signed设置为true。

3、读取cookie的时候，可以用req.cookies，也可以用req.signedCookies

具体如下

```
var express = require('express')
var cookieParser = require('cookie-parser')
var app = express()

app.use(cookieParser('123456'))
app.use(function(req, res, next) {
  console.log(req.cookies.nick)
  console.log(req.signedCookies.nick)
  next()
})
app.use(function(req, res, next) {
  res.cookie('nick', 'xxx', {
    signed: true
  })
  res.end('ok')
})
app.listen(8080)
```



参考资料

1、

https://www.cnblogs.com/chyingp/p/express-cookie-parser-deep-in.html