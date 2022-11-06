---
title: flask之项目目录结构组织
date: 2022-11-06 14:08:32
tags:
	- flask

---

--

写简单的程序，一个app.py就搞定了。

如果要写复杂一些的程序，就必须要考虑项目的目录结构。

django这样的框架，已经规定好了目录结构。

而flask则没有规定。

所以大家都各行其是。

其实还是需要一个好的目录结构来组织代码。

先到网上找一找别人的实践。



代码组织的首要问题，就是不用产生循环依赖问题。

我在编写模块和包时，总是保持这个特定的规则:

> 不要从根目录下的 `__init__.py` 中逆向导入



目录分类的方式

# 基于功能的结构

```
project/
	__init__.py
	models/
		__init__.py
		base.py
		users.py
		posts.py
	routes/
		__init__.py
		home.py
		account.py
		dashboard.py
	templates/
		base.html
		index.html
	services/
		__init__.py
		google.py
		mail.py
		
```

一切都是安装功能进行分类的。

在`projects/__init__.py`里创建一个create_app的工厂函数。

所是我的技巧是在每个目录下的 `__init__.py` 中定义一个 `init_app` 函数，并且统一初始化进程:

# 基于应用的结构

还有一种分目录的方式是，安装应用来分目录。

```
project/
	__init__.py
	db.py
	auth/
		__init__.py
		route.py
		models.py
		templates/
	blog/
		__init__.py
		routes.py
		models.py
		templates/
```

这个方式不是很好。

虽然django默认就是用这种方式来组织的。

# 项目的配置参数

目录这样放：

```
conf/
	dev_config.py
	test_config.py
project/
	__init__.py
	settings.py
app.py
```

在`project/__init__.py`里。这样来加载配置。

```python
# project/__init__.py
import os
from flask import Flask

def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object('project.settings') # 对应project/settings.py文件。
    if 'FLASK_CONF' in os.environ:
        app.config.from_envvar('FLASK_CONF')
    if config is not None:
        if isinstanceof(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)
    return app
```

FLASK_CONF对应一个包含配置项的python文件。你可以随便指定这个名字。

## 另外一个实践

```
project/
  forms/
    myform.py
    ...
  models/
    __init__.py
    profile.py
    user.py
    ...
  routes/
    __init__.py
    home.py
    profile.py
    ...
  static/
    ...
  services/
    __init__.py
    ...
  templates/
    createprofile.html
    profile.html
    ...
  __init__.py
  config.py
```

### 初始化

按功能划分开，比较容易理解，不过将分开的部分有机结合起来是个问题， 推荐的方式是，在每个目录下创建一个 `__init__.py` 文件，有两个作用:

1. 将目录变为包（package），方便其他地方引入
2. 做些初始化工作，例如将目录下的内容统一起来，提供一站式装载

#### 初始化模型

数据模型放在 `models` 目录下，一般数据模块需要和数据库交互，另外每个模型需要有个数据库实例，来创建模型以及字段定义

首先，创建目录的 `__init__.py` 代码文件：

```
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)
    return db
```

模型代码示例 `project/models/profile.py` ：

```
from . import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    birthday = db.Column(db.Date())
    createtime = db.Column(db.DateTime())
    about = db.Column(db.Text())
```

#### 初始化路由

当路由处理代码被分开之后，在主程序代码中初始化会变得比较麻烦，幸好 Flask 有个 blueprint（蓝图）的概念，能很好的将分离出来的代码管理起来，确切的说 blueprint 的作用不止于此，这里只是需要用到它的部分功能

> Web 项目被分成多个部分之后，每个部分可以单独成为一个子应用，blueprint 的作用就是可以让子应用的编写方式用在主应用中一样，比如注册路由，处理请求等，使用前，先创建一个 blueprint 实例，然后再将实例注册到 Flask app 实例中就好了。

路由处理定义示例，`project/routes/home.py`:

```
from flask import Blueprint

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World!", 200
```

再看看路由模块的初始化，`routes/__init__.py`:

```
from .home import home_bp
from .profile import profile_bp

def init_app(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp)

```

### Flask app 工厂方法

在之前的介绍中，在 `app.py` 中编写所有的东西，并且通过 `app.run()` 来启动应用，在实际项目中，推荐用 app 工厂方法的方式来启动，好处是：

1. 便于测试，可以在不同的测试用例中创建特别的 app 实体
2. 多实例运行，如果需要一个应用的多个版本，**可以在一个应用进程中运行多个实例**，而不必部署多个 Web 服务器（将在 Flask 部署中介绍）

创建 Flask app 写在 `project/__init__.py` 中：

```
from flask import Flask
from .config import config
from . import models, routes

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    models.init_app(app)
    routes.init_app(app)

    return app
```

工厂方法比单个文件写法更清爽，修改起来也更简单，另外这样定义还可以避免循环依赖问题，

> 循环依赖：如果在工厂方法中直接定义数据库模块 db，在模型中需要引用 db，而工厂方法又需要用模型来初始化 Flask app，就会引起循环依赖问题

### 启动项目

通过工厂方法创建的应用，因为没有明确的 `app.run()` 调用，不能直接像在前一样直接运行文件，而是要用 flask 命令行方式来启动

#### 正常启动

启动之前，需要先设置 FLASK_APP 环境变量，指定需要运行的 Flask 项目， 值为项目文件夹名，即项目名:

```
export FLASK_APP=project
```

然后在项目目录的上一层目录下执行命令，启动项目:

```
flask run
```

#### 设置启动参数

前面工厂方法可以定义一些参数，如何来指定呢？其中一种方法是设置环境变量 `FLASK_APP`，例如将 congfig_name 参数设置为 testing：

- Linux 或者 Mac

```
export FLASK_APP=project:create_app('testing')
```

# flaskr

flask源代码里的flaskr，就是一个简单而典型的目录结构。

# 参考仓库

https://github.com/hsuanchi/flask-template/blob/master/template-flask-login/app/__init__.py



# 参考资料

1、Flask 项目目录结构

这篇是来自于flask核心开发者的实践。所以参考价值非常大。

https://www.jianshu.com/p/49dc66141d20

2、

这篇写的也不错。

https://www.justdopython.com/2020/01/18/python-web-flask-project-125/