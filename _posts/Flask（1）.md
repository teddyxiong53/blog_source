---
title: Flask（1）
date: 2018-06-18 22:17:08
tags:
	- Flask

---



Flask是一个web框架，跟Django、web.py是一个类型的东西。

安装很简单，就pip install flask就好了。

# helloworld

先看一个最简单的flask程序。

hello.py文件：

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'hello world'
```

运行打印：

```
teddy@teddy-ubuntu:~/work/test/flask$ export FLASK_APP=hello.py
teddy@teddy-ubuntu:~/work/test/flask$ flask run
 * Serving Flask app "hello.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

另外开一个shell窗口，访问：

```
teddy@teddy-ubuntu:~$ curl http://localhost:5000
hello world
```

这样运行，只能通过localhost来访问到。

我们可以这样运行：

```
flask run --host=0.0.0.0
```

# 打开调试模式

每次改动，如果都需要重启flask，无疑是一种效率很低的做法，flask的调试模式，可以在修改代码的时候，让代码自动重新加载，这样就不需要重启flask了。

而且打开调试模式会提供更加详细的出错信息。

打开的方法是：

```
export FLASK_ENV=development
```

打开之后，运行的打印是：

```
teddy@teddy-ubuntu:~/work/test/flask$ flask run --host=0.0.0.0    
 * Serving Flask app "hello.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 997-206-844
```

现在我们修改hello.py里的内容。然后刷新页面看看是否生效。

我们修改后，打印是这样：

```
 * Detected change in '/home/teddy/work/test/flask/hello.py', reloading
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 997-206-844
192.168.190.1 - - [20/Jun/2018 22:48:51] "GET / HTTP/1.1" 200 -
```

打开调试

```
export FLASK_ENV=development
flask run
```



# routing

这个我就叫路径吧。

flask用route装饰器，来把函数跟url绑定起来。

```
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
	return "this is the index page"
	
@app.route('/hello')
def hello():
	return 'hello'
```



# 变量规则

你可以添加一个变量section到一个url，方法就是用尖括号括起来。

```
from flask import Flask
app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
	return 'user: %s' % username
	
@app.route('/post/<int:post_id>')
def show_post(post_id):
	return 'post: %d ' % post_id
	
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
	return 'subpath: %s' % subpath
```



# 唯一的url和重定向

```
from flask import Flask
app = Flask(__name__)

@app.route('/projects/')
def projects():
	return 'the project page'
	
@app.route('/about')
def about():
	return 'the about page'
	
```



# url构造

使用url_for函数。



# http方法

```
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return do_the_login()
	else:
		return show_the_login_form()
```

# 静态文件

动态web应用也需要静态文件，一般是css文件和js文件。

一般就是建立一个static的目录，把文件都放在下面。



# 渲染模板

在Python代码里生成html文件，是一件很繁琐的事情。

flask默认提供了jinja2的模板给我们用。

渲染一个模板，就用render_template函数。

你需要做的事情就是：

1、提供模板的名字。

2、提供你想要传递给模板引擎的变量。

最简单的使用模板的例子：

```
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)
```

flask会从templates目录下去找模板。

你的目录组织可以是下面的情况：

一个模块的形式

```
/app.py
/templates
	/hello.html
```

一个包的形式。

```
/app
	/__init__.py
	/templates
		/hello.html
```

下面我们看一个hello.html模板的简单例子。

```
<!doctype html>
<title>hello from flask</title>
{%  if name %}
<h1>hello {{name}}</h1>
{%  else %}
<h1>hello nobody</h1>
{%  endif %}

```

hello.py内容：

```
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)
```

目录结构：

```
teddy@teddy-ubuntu:~/work/test/flask$ tree
.
├── hello.py
└── templates
    └── hello.html
```

# 访问request数据

一个web应用，需要响应client发来的数据。

flask提供了一个全局的request对象来做这个事情。



# 文件上传



# cookie



# 重定向和错误



# session



# 参考资料

1、官方文档

http://flask.pocoo.org/docs/1.0/







http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html



https://changsiyuan.github.io/2017/05/20/2017-5-20-flasgger/

