---
title: Flask（3）
date: 2018-06-23 16:45:59
tags:
	- Flask

---



现在找到一本书《Flask Web开发：基于Python的web应用开发实战》。

参考这本书再进行学习。



Flask从客户端收到请求的时候，要让view处理函数可以访问一些对象，这样才方便处理请求。

request对象就是一个重要的。它封装了客户端发送的http请求。

request对象是通过参数传递进去的。

为了避免大量可有可无的参数把view处理函数弄乱，Flask使用了上下文临时把某些对象变成全局可访问的。

一个例子：

```
@app.route('/')
def index():
	user_agent = request.headers.get('User-Agent')
	return 'your browser is %s' % user_agent
```

我们看到，这index这个view处理函数里，把request当成了全局变量使用。

事实上，request不可能是全局变量。

因为多线程处理的时候，每个线程看到的request对象是不一样的。

Flask使用上下文让特定的变量在一个线程中全局可访问。同时不会影响其他的线程。

在Flask里，有2种上下文，一个是程序上下文，一个是请求上下文。

current_app和g：程序上下文。

request和session：请求上下文。

这4个变量很有用。

看下面演示的例子。

先写一个hello.py。

```
#!/usr/bin/python

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
	return 'hello flask'
if __name__ == '__main__': #必须这样，不然被import的时候，就会执行了。
	app.run(host='0.0.0.0', port=8000, debug=True)
```

然后我们开启Python命令行。

```
>>> from hello import app
>>> from flask import current_app
>>> current_app.name
Traceback (most recent call last): #会报错。因为这里还没有激活上下文。
。。。。。
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
'hello'
>>> app_ctx.pop()
```

```
>>> app.url_map
Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
 <Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>])
```



请求钩子函数。

有4个钩子函数。

before_first_request。

before_request。

after_request。

teardown_request。

在请求钩子函数和view函数之间共享数据一般用变量g。

例如，before_request可以从数据库加载已经登陆的用户，把它保存到g.user里。

在view函数里，用g.user来取得。



作者给了一个完整的例子，https://github.com/miguelgrinberg/flasky

