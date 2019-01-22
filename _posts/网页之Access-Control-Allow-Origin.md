---
title: 网页之Access-Control-Allow-Origin
date: 2019-01-22 13:25:55
tags:
	- 网页

---



看vue-zhihu-daily的代码，看到这个：

```
app.use(function(req, res, next) {
    res.set({
        'Access-Control-Allow-Origin': '*'
    })
    next()
})
```

Access-Control-Allow-Origin代表的内涵是什么？

从名字上看，是访问控制，Allow-Orgin又代表了什么呢？

这里涉及的知识点就是跨域访问。

# CORS

CORS是Cross-Origin Resource Sharing。

这是一个W3C标准。

它允许浏览器要跨源服务器，发出XMLHttpRequest。从而克服了ajax只能同源使用的限制。

cors需要浏览器和服务端同时支持。

目前所有浏览器都支持。

整个cors通信过程，都是浏览器自动完成的。不需要用户干预。

对于开发者来说，cors通信跟同源的ajax通信没有区别。代码完全一样。

浏览器一旦发现ajax请求跨源，就会自动在http头部加上一些信息，有时候还会多发出一次附加的请求。

但是用户不能感知。

所以实现cors的关键是服务端。只要服务端实现了cors接口，就可以实现跨源通信。

## 两种cors

浏览器把cors请求分为2两种：

1、简单请求。

2、非简单请求。

简单请求：

```
只要同时满足下面2个条件，就属于简单请求。
1、请求方法是：HEAD/GET/POST。
2、http头部信息不超出下面的字段：
	Accept
	Accept-Language
	Content-Language
	Last-Event-ID
	Content-Type
```

对简单请求的处理：

```
浏览器直接在http头部加上Origin字段

GET / HTTP/1.1
Origin: http://yy.com
Host: xx.com

```

服务端处理：

```
如果服务端支持，就会在在回复内容的头部加上Access-Control-Allow-Control字段。

```



这个东西还不少，我暂时先看这么点。后面再学习。





参考资料

1、ajax 设置Access-Control-Allow-Origin实现跨域访问

https://blog.csdn.net/fdipzone/article/details/46390573

2、跨域资源共享 CORS 详解

http://www.ruanyifeng.com/blog/2016/04/cors.html