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

# 代码阅读和测试

## websocket

这个提供了一个websocket的index.html前端和一个简单的测试后端。

websocket没有单独的一个class，而是使用with_websocket这个装饰器来修饰函数就可以。

给处理函数加上了一个ws的参数。

## run方法分析

```
run
	1、创建socket，bind，listen。
	2、accept。
	3、create_thread(self.handle_request 创建一个线程来处理连接。
```

```
handle_request
	1、创建一个req = Request.create
		看看请求对象是怎么构造出来的。
		需要的参数是：app本身，socket。
		是把请求的内容readline逐行解析。
		得到method、headers信息。
	2、处理请求，返回响应。res = self.dispatch_request(req)
	3、关闭socket。
```

```
dispatch_request
	1、如果请求的内容长度超过16K，返回413错误。
		res = 'Payload too large', 413
	2、find_route。就从url_map里查找。找到处理函数。
	3、在调用handler之前，先把before_request_handlers执行一遍。
	4、执行handler。
	5、把after_request_handlers执行一遍。
	6、把生成的res返回。
```



# 实现httpbin

新建一个microdot-httpbin的仓库。

microdot全局安装就好。

先实现这个

```
@app.route("/get", methods=("GET",))
def view_get():
    return jsonify(get_dict("url", "args", "headers", "origin"))
```

jsonify需要自己实现一下。

看看flask jsonify的实现。

https://blog.csdn.net/Duke_Huan_of_Qi/article/details/76064225

```
def jsonify(*args, **kwargs):
    if __debug__:
        _assert_have_json()
    return current_app.response_class(json.dumps(dict(*args, **kwargs),
        indent=None if request.is_xhr else 2), mimetype='application/json')
```

本质上还是json.dumps。

可以看出jsonify实际上也是使用了json.dumps来序列化json形式的数据，作为响应正文返回。

indent表示json格式化的缩进，

若是Ajax请求则不缩进（因为一般Ajax数据没必要直接展示），否则缩进2格。

但想必从第一部分的实验结果我们已经看出来了，

使用jsonify时响应的Content-Type字段值为application/json，

而使用json.dumps时该字段值为text/html。

Content-Type决定了接收数据的一方如何看待数据，如何处理数据，

如果是application/json，则可以直接当做json对象处理，

若是text/html，则还要将文本对象转化为json对象再做处理（个人理解，有误请指正）。



最后，我们可以使用flask中的make_response方法或者直接通过Response类，

通过设置mimetype参数来达到和使用jsonify差不多的效果，

但少写点代码何乐而不为呢？

况且简洁一点更不容易出错，参数越多调试和维护就越麻烦。

当然，使用哪个并不是绝对的，必要时要根据前端的数据处理方式来决定。



# 用chatgpt来辅助分析代码

## tox.ini

### envlist=flake8,py36,py37,py38,py39,py310,upy,benchmark 这个说明了什么

在 `tox.ini` 文件中，`envlist` 是一个用于指定要运行的测试环境的配置选项。它列出了可以在 `tox` 命令中指定的环境名称。

具体到你提供的示例中，`envlist` 包含了以下环境名称：

- `flake8`: 表示运行 Flake8 代码风格检查。
- `py36`, `py37`, `py38`, `py39`, `py310`: 表示运行 Python 版本为 3.6、3.7、3.8、3.9 和 3.10 的测试环境。
- `upy`: 表示运行 MicroPython 的测试环境。
- `benchmark`: 表示运行基准测试环境，用于性能评估。

通过在 `tox` 命令中指定所需的环境名称，你可以选择性地运行特定的测试环境。例如，运行以下命令可以仅执行 Flake8 代码风格检查：
```
tox -e flake8
```
而如果你运行以下命令，则会运行所有列出的环境的测试任务：
```
tox
```

使用 `envlist` 可以方便地定义和管理多个测试环境，并根据需要选择性地运行它们。这对于在不同的 Python 版本、不同的操作系统或不同的测试需求下进行测试是非常有用的。



# 参考资料

1、

