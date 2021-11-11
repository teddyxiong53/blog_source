---
title: nodejs之get和post操作
date: 2018-12-24 15:20:17
tags:
	- nodejs
---



在很多场景，我们的服务器都需要跟用户的浏览器打交道，例如表单提交。

表单提交到服务器，一般都是使用get和post请求。

post会有body。而get不会有。

现在我们看看怎么来做。

# 获取get请求数据

```
var http = require('http')
var url = require("url")
var util = require("util")

http.createServer(function(req, res) {
	res.writeHead(200, {'Content-Type': 'text/plain; charset=utf-8'})
	res.end(util.inspect(url.parse(req.url, true)))
}).listen(8080)

```

访问：http://127.0.0.1:8080/?a=1&b=2

得到：

```
Url {
  protocol: null,
  slashes: null,
  auth: null,
  host: null,
  port: null,
  hostname: null,
  hash: null,
  search: '?a=1&b=2',
  query: [Object: null prototype] { a: '1', b: '2' },
  pathname: '/',
  path: '/?a=1&b=2',
  href: '/?a=1&b=2' }
```



# 获取post请求内容

post请求的内容全部都在请求体里。

http.ServerRequest并没有一个属性内容是这个东西。

原因是：等待请求体的传输是一件很耗时的事情。

例如上传文件。

很多时候，我们不需要理会请求体的内容，恶意的post请求会大量消耗服务器资源。

所以nodejs默认都不会解析的。

当你有这个需要的时候，你要自己来做。

如下。

```
var http = require('http')
var querystring = require('querystring')

http.createServer(function(req, res) {
	var post = ''
	req.on('data', function(chunk) {
		post += chunk
	})
	req.on('end', function() {
		post = querystring.parse(post)
		res.end(util.inspect(post))
	})
})

```

上面只是一个基本的代码结构。



参考资料

1、Node.js GET/POST请求

http://www.runoob.com/nodejs/node-js-get-post.html