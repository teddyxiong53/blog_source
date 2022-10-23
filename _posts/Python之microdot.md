---
title: Python之microdot
date: 2022-10-23 21:51:33
tags:
	- Python

---

--

microdot是一个很小的web框架，模仿flask。更简单，可以在micropython上跑起来。

https://github.com/miguelgrinberg/microdot

# 提交记录

先看一下提交记录。

第一个提交是2019年3月。第一个提交就是可用的。

就一个setup.py、一个microdot.py。

一个example/gpio.py，gpio.html。

microdot.py第一个版本281行。

对外提供的类有：

Request、Response、URLPattern、Microdot。

就依赖了json和socket。

所以就是很简单的解析字符串处理。

然后第二次提交就是解决micropython上的问题。

```
try:
    import ujson as json
except ImportError:
    import json
try:
    import ure as re
except ImportError:
    import re
try:
    import usocket as socket
except ImportError:
    import socket
```

micropython上的包名不一样。

后面增加了errorhandler。

这个整个编写过程还是非常好阅读了，每次改一点。可以学习这个节奏。

增加debugmode。

也就是一个flag，多一点打印。

然后增加了flake8支持，来检查格式。

然后引入了unittest支持。

引入了tox。这个是在不同的环境进行测试的。

unittest.py是自己写的。

把micropython的二进制文件直接放进来。方便运行测试。

在readme增加travis的徽章。

然后增加request和response的unittest。

这个代码真的写得太严谨了。

然后增加了g和before_request和after_request。

```
class Request():
    class G:
        pass

    def __init__(self, client_sock, client_addr):
        self.client_sock = client_sock
        self.client_addr = client_addr
        self.url_args = None
        self.g = Request.G()
```

然后调整了一下代码的结构。

然后增加了microdot_async.py来支持异步。

然后增加了thread mode。

后面切到了github action的方式进行build。

https://microdot.readthedocs.io/en/latest/

增加了wsgi 支持。

是单独一个microdot_wsgi.py。

然后是asgi支持。

增加对video这种stream的支持。

增加mount sub app的支持。

增加session支持。

2022年8月7日，到了v1.0.0版本。

增加websocket支持。

增加ssl支持。

可以支持jinja和bootstrap模板。

最新版本是v1.2.0的。







参考资料

1、

