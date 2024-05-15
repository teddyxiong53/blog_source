---
title: Flask（1）
date: 2018-06-18 22:17:08
tags:
	- Flask

---



Flask是一个web框架，跟Django、web.py是一个类型的东西。

安装很简单，就pip install flask就好了。

# 简介

Flask是一个轻量级的Python Web框架，由Armin Ronacher于2010年创建。

它基于Werkzeug WSGI工具箱和Jinja2模板引擎构建。

Flask被设计为简单、易扩展、灵活，并且具有优雅的代码风格。

虽然它是轻量级的，但Flask拥有强大的扩展能力，

可以满足各种Web应用的需求。

Flask的核心思想是“微框架”，

它提供了基本的工具和库，

开发者可以根据自己的需求选择适当的扩展。

Flask被广泛应用于构建Web应用程序、RESTful API以及其他各种网络服务。

# 发展历史

以下是Flask的发展历史：

| 时间   | 事件                                                         |
| ------ | ------------------------------------------------------------ |
| 2010年 | Armin Ronacher创建了Flask，作为一个轻量级的Python Web框架。Flask的首个版本发布。 |
| 2012年 | Flask 0.9发布，引入了模块化的Blueprints。这使得Flask应用可以更好地组织和扩展。 |
| 2013年 | Flask 0.10发布，增加了对Python 3的支持。                     |
| 2017年 | Flask 1.0发布，标志着Flask稳定版的推出。这个版本引入了一些重要的改进和更新，包括对Python 3.7的支持。 |
| 2019年 | Flask 1.1发布，增加了更多的改进和新特性，包括对Websockets的原生支持。 |
| 至今   | Flask一直在持续发展，社区活跃，不断有新的扩展和工具涌现，为开发者提供更好的开发体验和功能支持。 |

这就是Flask的主要发展历史，展示了它如何从一个简单的微框架成长为一个功能强大且受欢迎的Python Web框架。

# 基于flask的项目有哪些

基于Flask的项目有很多，以下是其中一些知名的项目：

1. **Flask本身的应用**：包括网站、博客和API等，Flask的官方文档中提供了一些示例。

2. **Reddit**：曾经使用了基于Flask的API作为其后端。

3. **Airbnb**：Airbnb的一些内部工具和服务使用了Flask。

4. **Netflix**：Netflix的一些内部工具和服务也使用了Flask。

5. **Lyft**：Lyft的一些后端服务也是使用了Flask框架。

6. **Pinterest**：Pinterest的一些内部工具和服务也使用了Flask。

7. **Uber**：Uber的一些后端服务也使用了Flask框架。

这些只是一小部分基于Flask开发的项目，Flask作为一个灵活、轻量级的Web框架，被广泛应用于各种规模和类型的Web应用和服务中。

# flask架构分析

Flask的架构相对简单而灵活，主要由以下几个组件构成：

1. **核心组件**：Flask的核心组件包括路由器、WSGI应用程序和模板引擎。路由器负责将HTTP请求映射到相应的处理函数，WSGI应用程序处理HTTP请求和响应，而模板引擎则负责生成动态内容。

2. **扩展**：Flask的功能可以通过各种扩展来扩展，例如数据库集成、表单处理、身份验证等。这些扩展为开发者提供了丰富的功能，同时保持了Flask本身的轻量级和灵活性。

3. **Blueprints**：Blueprints是一种模块化的组织方式，允许开发者将应用拆分成多个模块，每个模块包含一组相关的路由和视图函数。这种模块化的设计使得应用更易于维护和扩展。

4. **中间件**：Flask可以与各种中间件和其他框架集成，例如WSGI中间件、数据库中间件等。这些中间件可以在请求处理过程中执行额外的逻辑，例如日志记录、性能监控等。

5. **应用结构**：Flask并没有强制要求特定的应用结构，开发者可以根据自己的需求和偏好组织应用。通常，Flask应用由一个主应用对象和一系列蓝图组成，每个蓝图对应一个功能模块。

总体来说，Flask的架构设计简单灵活，使得开发者可以快速搭建Web应用并根据需求灵活扩展功能。

# flask大型项目的目录架构最佳实践

针对大型项目，以下是一个通用的Flask项目目录结构的最佳实践：

```
my_project/
│
├── app/
│   ├── __init__.py
│   ├── models.py            # 数据库模型定义
│   ├── views.py             # 视图函数和路由
│   ├── forms.py             # 表单定义
│   ├── templates/           # Jinja2模板文件
│   ├── static/              # 静态文件（CSS, JavaScript等）
│   └── ...
│
├── migrations/              # 数据库迁移脚本
│
├── config.py                # 应用配置
├── requirements.txt         # 项目依赖
├── run.py                   # 应用启动脚本
└── ...
```

解释一下这个目录结构：

- `app/` 目录是主要的应用程序目录，包含了所有的应用代码。
  - `__init__.py` 初始化应用程序和各种扩展。
  - `models.py` 包含数据库模型定义。
  - `views.py` 包含视图函数和路由定义。
  - `forms.py` 包含表单定义。
  - `templates/` 包含Jinja2模板文件。
  - `static/` 包含静态文件，如CSS、JavaScript等。
- `migrations/` 目录包含数据库迁移脚本，使用Flask-Migrate等工具管理数据库模式变化。
- `config.py` 包含应用的配置信息，例如数据库连接、密钥等。
- `requirements.txt` 文件列出了项目所需的依赖包及其版本。
- `run.py` 是应用的启动脚本，通常用于开发环境下的快速启动。

这种目录结构使得项目模块化、可维护性高，并且易于扩展。同时，它也符合了Flask社区的通用约定，使得其他开发者更容易理解和参与到项目中。

# flask的模板引擎

Flask使用Jinja2作为默认的模板引擎，Jinja2是一个功能强大且灵活的模板引擎，具有以下特点：

1. **语法简洁**：Jinja2的模板语法简洁清晰，易于学习和使用。它使用双大括号`{{ }}`表示变量插值，使用`{% %}`表示控制流和逻辑。

2. **模板继承**：Jinja2支持模板继承，允许开发者定义一个基础模板，并在子模板中继承和扩展它。这种结构化的模板组织方式使得页面布局和代码重用更加方便。

3. **过滤器和函数**：Jinja2支持过滤器和函数，可以对变量进行格式化、过滤和转换。开发者还可以自定义过滤器和函数，以满足特定需求。

4. **模板控制流**：Jinja2支持条件语句、循环语句和宏，可以实现复杂的模板控制逻辑。

5. **模板包含**：Jinja2支持模板包含，允许开发者将一个模板包含到另一个模板中，实现模板的复用和模块化。

在Flask中，使用Jinja2模板引擎非常简单，只需要在模板文件中编写Jinja2语法，然后在视图函数中渲染模板并传递需要的数据即可。例如：

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    name = 'John'
    return render_template('index.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
```

在`index.html`模板文件中：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```

这段代码会在浏览器中显示"Hello, John!"。

## 模板引擎的方式还是没有实现前后端分离

如果你想要实现前后端分离，可以考虑使用Flask作为后端API服务器，而不是生成完整的HTML页面。在这种情况下，Flask只负责提供数据，而前端框架（如Vue.js、React.js等）则负责渲染页面。

具体来说，你可以按照以下步骤进行：

1. **后端：Flask API**：
   - 使用Flask编写API接口，通过路由处理HTTP请求，并返回JSON格式的数据。
   - 不使用Jinja2模板引擎生成HTML页面，而是直接返回数据。

2. **前端：Vue.js/React.js等**：
   - 使用前端框架编写页面，并通过Ajax请求后端API获取数据。
   - 在前端框架中渲染页面，展示后端提供的数据。

这样做的好处是前后端分离，提高了项目的灵活性和可维护性，使得前端和后端可以独立开发和部署。同时，前端框架可以提供更加丰富和动态的用户界面，增强用户体验。

# flask shell命令

在Flask中，可以使用`flask shell`命令进入交互式Python shell环境，从而可以在应用上下文中执行Python代码，包括访问应用的对象和数据库等。

要使用`flask shell`命令，首先需要确保你的应用已经设置了一个或多个可用的shell上下文处理器。这可以通过在应用工厂函数或应用实例上注册`shell_context_processor`装饰器来完成。例如：

```python
from flask import Flask
from myapp import create_app, db, models

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'models': models}

if __name__ == '__main__':
    app.run()
```

在这个例子中，`make_shell_context`函数返回了一个字典，该字典包含了需要在shell中使用的对象，比如应用实例`app`、数据库实例`db`以及模型类`models`。

接下来，你可以在命令行中执行以下命令进入交互式shell：

```
flask shell
```

然后你就可以在shell中访问应用对象和数据库对象，执行Python代码，调试和测试应用。

# flask routes命令

`flask routes`命令用于显示当前Flask应用中定义的所有路由信息，包括HTTP方法、路由规则、端点和对应的处理函数。这个命令在开发和调试阶段特别有用，可以帮助开发者快速查看应用中的路由配置。

要使用`flask routes`命令，只需在命令行中执行以下命令：

```
flask routes
```

执行此命令后，Flask将会列出应用中定义的所有路由信息，例如：

```
Endpoint     Methods    Rule
------------ ---------- -------------------------------------
index        GET        /
login        GET, POST  /login
logout       GET        /logout
user_profile GET        /user/<username>
```

这个输出显示了每个路由的端点（Endpoint）、支持的HTTP方法（Methods）和路由规则（Rule）。

通过`flask routes`命令，你可以方便地查看Flask应用中所有的路由信息，从而更好地理解应用的结构和功能。

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

