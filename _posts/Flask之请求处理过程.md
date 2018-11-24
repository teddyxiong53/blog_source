---
title: Flask之请求处理过程
date: 2018-11-24 16:45:51
tags:
	- Flask
typora-root-url: ..\
---



wsgi就是定义了web容器和web app之间通信的协议。

一个简单的使用wsgi的app的例子。

```
def application(environ, start_response):
	start_response('200 OK', [('content-type', 'text/html')])
	return [b'hello web']
```

代码分析：

environ参数：这个是wsgi容器把http请求封装后得到的。包含了http request的所有内容。

start_response函数：这个是wsgi 容器提供的函数。函数在返回前必须调用一次。

交互过程如下图：

![](/images/wsgi交互过程.jpg)

# Flask的上下文对象

Flask的上下文有两种：

1、Request上下文。包括Request和Session。

2、App上下文。	全局变量g和current_app。

current_app的生命周期最长。只要当前程序还在运行。

Request和g的生命周期是一次请求。请求处理完了，也就销毁了。

Session，则是有时效性的。











参考资料

1、Flask的核心机制！关于请求处理流程和上下文

https://www.jianshu.com/p/2a2407f66438