---
title: wsgi（1）
date: 2019-01-16 15:47:59
tags:
	- wsgi
---



要真正掌握flask这些框架，还是需要把wsgi从头学习一遍。

wsgi规定应用程序是一个可调用的对象。

可调用的对象分为3种：

1、函数。

2、一个类，实现了`__call__`方法。

3、一个类的实例。



Python web应用结构。可以分为两种：

1、三级结构。

```
client <--> 代理服务器（nginx）<--> 中间件（uwsgi）<--> application（flask）
```

2、二级结构。

```
client <--> wsgi服务器（uwsgi、wsgiref）<--> application（flask）
```

二级结构是在开发阶段用的。

三级结构是生产阶段用的。

在二级结构里，uwsgi作为服务器，它用到了http协议和wsgi协议，flask应用实现了wsgi协议。

通常来说，flask框架等都会自己附带一个wsgi服务器，这也是flask应用可以直接运行的原因。

这个wsgi服务器，在生产阶段的不够用的。

在三级结构里，wsgi作为中间件，它用到了uwsgi协议与nginx通信。wsgi协议调用flask app。

当有客户请求发过来的时候，nginx先做处理（静态资源是nginx的强项），无法处理的请求（uwsgi）就给flask去做。

多了一层反向代理，有什么好处？

1、提高web server的性能。

2、nginx可以做负载均衡。

3、保护了实际的web服务器。

# uwsgi

什么是uwsgi？

是一个实现了wsgi、uwsgi、http协议的服务器。

有两种模式：

1、http模式。对应两层结构。

2、socket模式。对应三层结构。



# 简单的wsgi服务器和wsgi应用

根据PEP-3333的规定，一个基本的wsgi应用，应该实现以下功能：

```
1、必须是一个可调用对象。
2、接收2个必选参数：environ、start_response，一个可选参数exc_info。
3、返回值是字节类型的元组，表示http body。
```

所以一个简单的实现是这样的。

```
def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html")])
    body = ""
    for i,j in environ.items():
        body += str(i) + str(j) + "<br/>"
    return [body.encode('utf-8')]
```

用call方法的方式来实现是这样的。

```
class app1:
    def __call__(self, environ, start_response):
        start_response("200 OK", [("Content-Type":"text/html;charset=utf-8")])
        body = ""
        for i,j in environ.items():
            body += str(i) + str(j) + "<br>"
        return [body.encode("utf-8")]
```

用迭代法来实现的这样写。

```
class app2:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def __iter__(self):
        start_response("200 OK", [("Content-Type":"text/html;charset=utf-8")])
        body = ""
        for i,j in environ.items():
            body += str(i) + str(j) + "<br>"
        return [body.encode("utf-8")]
```

上面的3种写法效果是一样的。



看一下wsgiref的代码。



# 参考资料

1、WSGI的理解

https://www.cnblogs.com/eric-nirnava/p/wsgi.html

2、wsgiref 源码解析

http://python.jobbole.com/87390/