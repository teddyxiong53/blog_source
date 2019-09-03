---
title: Python之wsgi
date: 2018-06-22 22:49:36
tags:
	- Python

---



web应用的本质就是：

1、浏览器发送一个http request。

2、服务器收到request，生成一个html文档。

3、服务器把html文档作为http response的body发送给浏览器。

4、浏览器收到http response，从http body里取出html文档并显示。



所以，最简单的web应用，就是把html文档提前准备好，接收到用户请求后，从文件里读取内容直接返回给用户。

这个就是静态的web server做的时候，例如Apache。



如果html内容是动态的生成的，自己构造html内容，是非常繁琐的。所以有一些库帮我们做这个苦力活，这些库给我们提供了一些接口，让我们可以专注于web业务的开发。

这些接口，就是wsgi。全称是Web Server Gateway Interface。



wsgi的接口定义非常简单，只需要开发者实现一个函数，就可以响应http请求了。

```
def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')]) #header
	return 'hello web' #body
```

上面这个application函数，就是一个服务号wsgi标准的http处理函数。

它接收2个参数：

environ：一个dict，包含了http request的信息。

start_response：发送http response的函数。



Python内置了一个wsgi服务器，叫wsgiref。

这个是python官方提供的参考实现。



# helloworld

我们先写一个hello.py。

```
def application(environ, start_response):
	start_response('200 OK', [('Content-Type', 'text/html')]) #header
	return 'hello web' #body
```

再写一个server.py，负责启动wsgi服务器。加载application函数。

```
from wsgiref.simple_server import make_server
from hello import application

httpd = make_server('', 8000, application)
print 'start server on 8000 ...'
httpd.serve_forever()
```



wsgi里一个非常重要的概念，就是每个python web应用都是一个可调用的对象。

在flask里，就是app=Flask(name)得到的app。

wsgi就是定义web容器和app的通信规则的。

我们的flask真正使用的时候，还需要部署到web容器里去。这个web容器需要支持wsgi。



werkzeug包括：

```
1、一个交互debugger。可以在浏览器里进行代码跟踪。
2、一个功能完整的request对象。
3、一个response对象。
4、一个路由系统。
5、http util函数，
6、一个wsgi server。
7、一个test client。
默认支持Unicode。

```



官网教程，是实现一个类似tinyurl功能的网站。

安装依赖

```
pip install Jinja2 redis
```

新建目录结构如下：

```
.
├── shortly.py
├── static
└── templates
```



shortly.py内容：

```
import os
import redis
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader


class Shortly(object):

    def __init__(self, config):
        self.redis = redis.Redis(
            config['redis_host'], config['redis_port'])

    def dispatch_request(self, request):
        return Response('Hello wsgi!')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self. wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    app = Shortly({
        'redis_host':       redis_host,
        'redis_port':       redis_port
    })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/static':  os.path.join(os.path.dirname(__file__), 'static')
        })
    return app
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('192.168.56.101', 5000, app, use_debugger=True, use_reloader=True)

```

我们直接运行python shortly.py，就可以进行访问了。



官方代码在这里。这里面有例子。

https://github.com/pallets/werkzeug



werkzeug代码分析



# 参考资料

1、WSGI接口

https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/001386832689740b04430a98f614b6da89da2157ea3efe2000

2、Flask的核心机制！关于请求处理流程和上下文

https://www.jianshu.com/p/2a2407f66438

3、werkzeug官网

https://palletsprojects.com/p/werkzeug/

4、Werkzeug 文档

https://werkzeug-docs-cn.readthedocs.io/zh_CN/latest/