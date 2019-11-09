---
title: Flask之FlaskWeb开发读书笔记
date: 2019-11-02 11:55:49
tags:
	- Flask

---

1

我开始读的是第一版的，但是代码是第二版的，后面还是找到了第二版的电子书。

第二版的改动，主要有：

1、把flask_script换成了click的方法。

所以进shell应该这么进：

```
export FLASK_APP=flasky
export FLASK_ENV=development
flask shell
```

2、把伪造数据的库，由forgerypy换成了faker。



首先下载源代码：

https://github.com/miguelgrinberg/flasky

这个代码里打了很多的tag。跟书的章节是一一对应的。

可以根据需要checkout对应的版本。

首先需要创建一个名为venv的虚拟环境。

```
virtualenv venv
```

激活这个虚拟环境。

```
source ./venv/bin/activate
```

安装flask依赖：

```
pip install flask
```

现在基本环境准备好了。

checkout 2c这个tag。

```
git checkout 2c
```

启动程序：

```
python hello.py
```

出错了，提示flask_script找不到。

因为flask_script在0.11版本后被移除了。我当前的flask版本是1.1.1的。

所以先降级到0.9版本。

```
pip install flask==0.9
```

再运行，还是不行。所以把flask恢复回来。

```
pip install flask==1.1.1
```

另外安装flask_script：

````
pip install flask_script
````

然后运行，提示要带参数shell或者runserver。使用runserver。可以跑起来了。

```
python hello.py runserver
```

打印如下：

```
(venv) hlxiong@hlxiong-VirtualBox:~/web/flasky$ python hello.py runserver
 * Serving Flask app "hello" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [02/Nov/2019 13:18:49] "GET / HTTP/1.1" 200 -
```

既然我切换到了flask 1.1.1版本，那么就可以使用flask命令来运行了。

```
export FLASK_ENV=hello
flask run
```

这样hello.py里就不用写main函数了。

flask_script也算是一个flask插件。

安装插件：

```
pip install flask_bootstrap flask_moment
```

git checkout 3e，这个版本集成了bootstrap。可以查看一下效果。

```
pip install flask_wtf
```

flask_wtf可以保护素有表单免受跨站请求伪造攻击。

```
pip install flask_sqlalchemy
pip install flask_migrate
```

电子邮件：

```
pip install flask_mail
```

```
pip install flask_login
pip install python-dotenv
pip install flask_pagedown
pip install markdown
bleach
flask_httpauth
```

# 2

flask应用可以在debug mode运行。

在debug mode下，开发服务器默认会加载2个工具：reloader和debugger。

reloader会自动监视项目所有的源代码文件，如果文件有变动，自动重启服务器。

debugger就是在出错上，在网页上把堆栈打印出来。

调试模式的开关：

```
export FLASK_DEBUG=1
```

flask常用命令：

```
flask run --host 0.0.0.0 --port 5000
--reload
--debugger
--eager-loading/--lazy-loading
--with-threads
```

## flask request对象的属性

```
form
	一个字典。存储所有表单字段。
args
	一个字典。存放通过url传递的参数。
values
	一个字典。form和args的合集。
cookies
	一个字典。存放请求带的cookie
headers
	一个字典，存放http headers内容。
files
	一个字典。存放上传的文件。
get_data()
	返回请求主体缓冲的数据。
get_json()
	返回一个字典。包含解析请求body得到的json。
blueprint
	request对应的蓝图的名字。
endpoint
	处理函数的名字。
method
	请求方法，GET或者POST
scheme
	是http还是https
is_secure()
	https的时候，返回True。
host
	请求的host。
path
	url里的path部分。
query_string
	url里的参数部分。
full_path
	path和query_string的合集。
url
	完整的url。
base_url
	不包括query_string部分的url。
remote_addr
	客户端的ip地址。
environ
	wsgi环境变量。
```



## response

response由3部分组成。默认只给第一个字符串也可以。

1、字符串。

2、状态码。不指定就是默认200 。

3、headers。不指定就是用默认的。

response对象的属性

```
status_code
	状态码。
headers
	响应的头部。
set_cookie()
	为响应添加一个cookie。
delete_cookie()
	删除一个cookie。
content_length
	响应的body的长度。
content_type
	响应的body的类型。
set_data()
	使用字符串或者二进制设置响应内容。
get_data()
	获取响应的body。
```

响应有种特殊情况，叫做重定向。

这种响应没有页面文档，只是告诉浏览器一个新的url。重定向经常在web表单里使用。

因为这个场景是非常常见的，所以flask为我们提供了一个函数redirect。

另外404也是常见的，flask也提供了一个对应的函数abort。



# 3

jinja2的变量过滤器

```
safe
	渲染的时候不进行转义。
	转移是指把字符转成安全字符。例如把<转义成&lt;
capitalize
	首字母大写。
lower
	转小写 。
upper
	转大写。
title
	每个单词的首字母都大写。
trim
	去掉前后的空格。
striptags
	把html标签都去掉。
```

复用模板代码的方式：

1、定义宏。

2、继承模板。



时间显示

一般做法：

服务器端只用utc时间，浏览器这边的，靠自己本地化一下。



# 4 表单

前面提到的，都是从服务器向浏览器发送信息。

如果要从浏览器往服务器发送信息，就需要使用表单。

flask_wtf就是用来简化表单的编写工作的。

flask_wtf跟其他的插件不同，它不需要在应用层进行初始化。

但是它需要配置一个秘钥。

```
app.config['SECRET_KEY'] = 'xxx'
```

之所以要这个秘钥，是为了避免跨站攻击。

秘钥用来生成令牌。

而秘钥应该写入到环境变量，而不是配置文件。这样才不容易泄露。



有一个可用性问题。

就是刷新的时候，提示会丢失当前表单里的内容。

这个是因为是一个请求是post请求导致的。

普通用户看到这个会很困惑的。

所以就是web应用不要把post请求作为浏览器发送的最后一个请求。

怎么实现呢？

用重定向。



# 5 数据库



运行最后一个版本的。

```
./boot.sh
```

注意，需要在venv里安装gunicorn，不然会调用其他地方的gunicorn，例如我的gunicorn就是python3.6的。

导致运行失败，还提示python3.6的相关打印。让我感到困惑不解。

现在可以正常运行了。

注册有的问题，因为配置的邮件相关的是谷歌的服务，当然是访问不到的。

注册的东西是已经到数据库了。

```
hlxiong@hlxiong-VirtualBox:~/web/flasky$ sqlite3 ./data-dev.sqlite 
SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .tables
alembic_version  follows          roles          
comments         posts            users          
sqlite> select * from users;
1|teddyxiong53|3|1073167306@qq.com|pbkdf2:sha256:150000$eWYVFsKu$a9c5afadc38df5aa9692a86a78c4914eb06098275186453e7c641ee0e6b9d6ae|0||2019-11-02 07:14:21.936403||2019-11-02 07:14:21.936397||efa2a90d4561bb6a540a46dc8ebb6dee
```

现在界面上是提示我确认邮件。

我把smtp的改成QQ邮箱的smtp.qq.com。点击发送邮件，打印了这些。

```
send: u'mail FROM:<flasky@example.com> size=1959\r\n'
reply: '503 Error: need EHLO and AUTH first !\r\n'
reply: retcode (503); Msg: Error: need EHLO and AUTH first !
```

需要配置一下这2个环境变量。

```
MAIL_USERNAME
MAIL_PASSWORD
```

我设置了，再点击发送邮件，qq邮箱这边收到邮件了，但是邮件内容是说授权错误。

MAIL_SERVER这个也用环境变量的 方式来设置，不要直接改代码了。

还是有不少的错误。根据提示一点点解决。

还是qq邮箱的坑比较多。以后做这种测试，尽量用网易邮箱。

我发送者配网为tom邮箱，接收者配置为网易邮箱，很容易就成功了。

但是接收者配置为qq邮箱，一直收不到邮件。

不是qq邮箱没有收到，而是被自动拦截了，当成了垃圾邮件了。

```
app.config['MAIL_SERVER'] = 'smtp.tom.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "xhl_cloud_test@tom.com"
app.config['MAIL_PASSWORD'] = "xx"

from flask_mail import Mail
from flask_script import Manager

manager = Manager(app)
mail = Mail(app)

if __name__ == '__main__':
    manager.run()
```

然后进入到命令行：

```
python hello.py shell
```

```
>>> from flask_mail import Message
>>> from hello import mail
>>> msg = Message('flask test mail', sender='xhl_cloud_test@tom.com', recipients=['1073167306@qq.com'])
>>> msg.body='hello flask mail'
>>> with app.app_context():
...     mail.send(msg)
```

这样就可以进行邮件测试。

Flasky是一个有实用价值的代码了。



flask不强制要求大型项目的组织方式，我们找一种最佳实践。

在单个文件里开发很方便，但是有个很大的缺点，因为程序在全局作用域创建，所以无法动态修改配置。

运行脚本时，程序实例已经创建，再修改配置已经为时已晚。

这一点对于单元测试尤其重要，因为有时候为了提高测试覆盖度，必须在不同的配置环境中运行程序。



这个问题的解决方法是延迟创建程序实例。把创建过程放到一个函数里。

这种方法不仅可以给脚本流出配置程序的时间，还能够创建多个程序实例。

就是create_app函数。这个函数有一个参数，就是config_name。

```
一般放在app/__init__.py里做。
创建的插件类，先都不带app参数。
在create_app函数里，再init_app把app传递进去。
```

使用工厂函数的方式，让定义路由变得不方便。

在单脚本程序里，app实例存在于全局作用域。路由可以直接用app.route来装饰。

但是现在app在运行时才创建，只有调用create_app之后才能使用app.route装饰器。

这个时候定义路由就太晚了。

类似地，定义错误处理页面也面临同样的问题。

因为需要使用app.errorhandler装饰器。

不过，flask已经为我们提供了解决方案了。就是使用Blueprint。

Blueprint跟app类似，也可以定义路由。

不同的是，在Blueprint里定义的路由处于休眠状态，直到Blueprint被注册给app。

跟app一样，Blueprint也可以在单个文件里定义。也可以使用更加结构化的方式在多个文件里。

为了获得最大的灵活性，创建一个子包。

例如：

```
在app/main/__init__.py里
from flask import Blueprint
main = Blueprint('main', __name__)
from . import views, errors #注意放在最后，因为views和errors还会导入main，这是为了避免循环导入。
```

然后处理放在views.py和errors.py文件里。

然后在

```
app/__init__.py里
def create_app(config_name):
	# ...
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
```

```
# app/main/errors.py里
from flask import render_template
from . import main
@main.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404
```

注意是app_errorhandler这个装饰器，而不是errorhandler。app_errorhandler这样才是全局有效的。

```
# app/main/views.py

from . import main
@main.route('/', methods=['GET', 'POST'])
def index():
	# ...
```





大多数程序都要进行用户跟踪。

用户连接程序时会进行身份认证，通过这个过程，让程序知道用户的身份。

这样程序就可以提供针对性的服务。

最常用的认证方法是要求用户提供一个身份证明（用户的邮箱或者用户名）和一个密码。

现在我们看看如何开发一个完整的认证系统。



优秀的python认证包有很多，但是没有一个能实现所有功能。

现在我们就结合多个包来实现。

需要：

flask_login：管理已登陆用户的session。

werkzeug：计算密码的hash以及检查是否匹配。

itsdangerous：生成并核对加密安全令牌。用来发送验证邮件时有用。

除了认证相关的包之外，还需要使用这些包：

flask_mail：发送认证邮件。

flask_bootstrap：html模板。

flask_wtf：web表单。



密码的安全性

很多用户会是一个密码走天下，这样如果一个网站泄露了用户的密码，那么用户所有的网站账号都就处于危险之中。

开发者怎么避免这种问题？就是不要用明文存储密码，使用密码的hash值来存入。

校验的时候，也是跟hash值对比。

只要输入一样，校验就能过。

werkzeug的security模块就可以很方便地进行hash的计算。

涉及到2个函数，一个是在注册阶段用，一个是在登陆的时候用。

```
generate_password_hash
check_password_hash
```

即使2个用户使用了相同的密码，他们的密码散列后的值也不同。

创建auth的Blueprint。

新建一个auth包。

flask_login要求用户实现的方法：

```
is_authenticated
	用户已经登陆，返回True
is_active
	如果允许用户登陆，返回True
is_anonymous
	对普通用户必须返回False
get_id
	必须返回用户的标识符。使用Unicode编码。
```

这4个方法可以在模型类里直接实现，不过有一种更方便的方法，flask_login提供了一个UserMixin类，默认实现了这些方法，我们继承这个类就好了。



# docker方式部署

靠的是boot.sh来启动。

```
sudo docker build -t flasky:lastest .
```

运行：

```
sudo docker run --name flasky -d -p 8000:5000 \
  -e SECRET_KEY=57d40f677aff4d8d96df97223c74d217 \
  -e MAIL_USERNAME=teddyxiong53@163.com \
  -e MAIL_PASSWORD=53xhl040253 flasky:latest
```



参考资料

1、

