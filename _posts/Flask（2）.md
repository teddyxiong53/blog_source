---
title: Flask（2）
date: 2018-06-22 23:42:22
tags:
	- Flask

---



现在看一个实例的教程。

# 环境准备

我基于python2.7的来做。因为这个版本稳定很久了。

我不想被一些乱七八糟的问题干扰。

安装虚拟环境。

```
sudo pip install virtualenv
```

创建一个虚拟环境，名字就叫flask。

```
virtualenv flask
```

得到目录下的情况是这样：

```
teddy@teddy-ubuntu:~/work/test/flask$ tree  -L 2  
.
└── flask
    ├── bin
    ├── lib
    └── pip-selfcheck.json
```

但是，默认是把Python3.6的拷贝进来了。

为什么？怎么指定Python版本呢？

这样就可以了。因为我的默认Python是2.7的。

```
virtualenv -p /usr/bin/python flask
```

然后我们进入到这个虚拟环境。

```
teddy@teddy-ubuntu:~/work/test/flask/flask$ source bin/activate
(flask) teddy@teddy-ubuntu:~/work/test/flask/flask$ 
```

安装需要的软件。

```
pip install flask flask-login flask-openid flask-mail flask-sqlalchemy sqlalchemy-migrate flask-whooshalchemy flask-wtf flask-babel guess_language flipflop coverage
```

安装很顺利。

# helloworld

创建目录。

```
(flask) teddy@teddy-ubuntu:~/work/test/flask$ tree -L 2 -d
.
├── app
│   ├── static
│   └── templates
├── flask
│   ├── bin
│   ├── include
│   ├── lib
│   └── local
└── tmp
```

在app目录下，新建一个`__init__.py`文件。

```
from flask import Flask

app = Flask(__name__)
from app import views
```

在app目录下，新建一个views.py文件。

```
from  app import app

@app.route('/')
@app.route('/index')
def index():
	return 'hello flask'
	
```

在app的上一层目录。就是项目的根目录。新建一个run.py文件。

```
#!flask/bin/python

from app import app
app.run(debug=True)

```

然后运行：

```
./run.py
```

# 加入模板

在templates目录里加入index.html文件。内容如下：

```
<html>
	<head>
		<title>{{title}} - xhl blog</title>
	</head>
	<body>
		<h1>hello, {{user.nickname}}</h1>
	</body>
</html>
```

然后我们修改views.py的内容如下：

```
from  app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'teddy'}
	return render_template("index.html", title='Home', user=user)
```

我们修改一下run.py。

```
from app import app
app.run(host="0.0.0.0", port=8000, debug=True)
```

模板加入控制语句。

修改index.html文件。

```
<html>
	<head>
		{%  if title %}
		<title>{{title}} - xhl blog</title>
		{%  else %}
		<title>welcome to xhl blog</title>
		{%  endif %}
	</head>
	<body>
		<h1>hello, {{user.nickname}}</h1>
	</body>
</html>
```

加入循环，对于博客来说，就是把所有的文章都展示 出来。

先修改views.py文件。

```
@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'teddy'}
	posts = [ #这些现在是假数据，后续是从数据库读取出来的。
		{
			"author": {'nickname':'allen'},
			"body":'allen info',
		},
		{
			"author": {'nickname':'bob'},
			"body":'bob info',
		},
	]
	return render_template("index.html", title='Home', user=user, posts=posts)
```

修改index.html文件。

```
<html>
	<head>
		{%  if title %}
		<title>{{title}} - xhl blog</title>
		{%  else %}
		<title>welcome to xhl blog</title>
		{%  endif %}
	</head>
	<body>
		<h1>hello, {{user.nickname}}</h1>
		{%  for post in posts %}
		<p>{{post.author.nickname}} says: <b>{{post.body}}</b></p>
		{%  endfor %}
	</body>
</html>
```

看到的网页内容是：

```
hello, teddy

allen says: allen info

bob says: bob info
```

接下来看模板继承。

在我们的这个博客程序里，页面的顶部要有导航栏。在导航栏上有编辑账号，退出等链接。

如果在每个界面都写一次，无疑是很麻烦的。jinja2模板有继承机制。

现在我们新建一个base.html文件。

```
<html>
	<head>
		{%  if title %}
		<title>{{title}} - xhlblog</title>
		{%  else %}
		<title>welcome to xhlblog</title>
		{%  endif %}
	</head>
	<body>
		<div>xhlblog: <a href="/index">Home</a></div>
		<hr>
		{%  block content %}{%  endblock %}
	</body>
</html>
```

注意block语句这里。是用来控制继承了base.html的，内容插入的地方。

现在我们修改index.html。

```
{%  extends "base.html" %}
{%  block content %}
<h1>hi, {{user.nickname}}</h1>
{%  for post in posts %}
<div><p>{{post.author.nickname}} says: <b>{{post.body}}</b></p></div>
{%  endfor %}
{%  endblock %}
```

# web表单

web表单是web应用的最基础的部分。

为了可以处理web表单。我们现在要使用前面安装的flask-wtf。

很多的flask扩展，需要大量的配置，所以现在我们在项目的根目录下创建一个配置文件。名字就叫config.py。

暂时写入下面的内容。

```
CSRF_ENABLED = True
SECRET_KEY = '88889999'
```

现在修改`app/__init__.py`内容。

```
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from app import views
```

现在我们要创建一个登陆表单，我们采用OpenID的方式。

OpenID登陆只需要一个字符串，叫做OpenID。

写app/forms.py文件。

```
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)
```

写对应的模板。login.html。

```
{%  extends "base.html" %}
{%  block content %}
<h1>sign in</h1>
<form action="" method="post" name="login">
	{{form.hidden_tag()}}
	<p>
		please enter your openid:<br>
		{{form.openid(size=80)}}<br>
	</p>
	<p>{{form.remember_me}} Remember Me</p>
	<p><input type="submit" value="Sign In"></p>
</form>
{%  endblock %}
```

然后在views.py里修改。

```
from  app import app
from flask import render_template, flash, redirect
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	user = {'nickname': 'teddy'}
	posts = [
		{
			"author": {'nickname':'allen'},
			"body":'allen info',
		},
		{
			"author": {'nickname':'bob'},
			"body":'bob info',
		},
	]
	return render_template("index.html", title='Home', user=user, posts=posts)
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('login requested for openid=' + form.openid.data + ", remember_me=" + str(form.remember_me.data))
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)
```

现在我们访问http://192.168.190.137:8000/login

可以看到登陆界面了。

我们随便填入一些内容，点击提交。

这时候，就调整到index界面了。

有一行内容：

```
login requested for openid=XXX, remember_me=True
```

毫无疑问，当前没有对用户提交的内容进行验证。我们现在需要进行验证。

修改login.html文件。

```
{%  extends "base.html" %}
{%  block content %}
<h1>sign in</h1>
<form action="" method="post" name="login">
	{{form.hidden_tag()}}
	<p>
		please enter your openid:<br>
		{{form.openid(size=80)}}<br>
		{%  for error in form.openid.errors %} <!-- 添加了这3行代码。-->
			<span style="color:read;">[{{ error }}]</span>
		{% endfor %}
	</p>
	<p>{{form.remember_me}} Remember Me</p>
	<p><input type="submit" value="Sign In"></p>
</form>
{%  endblock %}
```

很多用户都不知道他们有一些openid。事实上，如果你了有了谷歌、腾讯、百度这些公司的账号，你就有了OpenID。

为了方便用户更加方便地用这些常用的OpenID登陆到我们的网站，我们把他们的链接转成短名称。用户不必手动地输入这些OpenID。

我们把这些内容写入到config.py里。

我看了下教程里提供的地址，只有雅虎的我能访问。就加入雅虎的吧。

```
OPENID_PROVIDERS = [
	{"name": "Yahoo", "url": "https://me.yahoo.com"},
]
```

然后修改login.html文件。

```
{%  extends "base.html" %}
{%  block content %}
<script type="text/javascript">
function set_openid(openid, pr)
{
	u = openid.search('<username>')
	if(u != -1) {
		user = prompt("Enter your " + pr + " username:")
		openid = openid.substr(0, u) + user
	}
	form = document.forms['login']
	form.elements['openid'].value = openid
	
}
</script>
<h1>sign in</h1>
<form action="" method="post" name="login">
	{{form.hidden_tag()}}
	<p>
		please enter your openid:<br>
		{{form.openid(size=80)}}<br>
		{%  for error in form.openid.errors %}
			<span style="color:read;">[{{ error }}]</span>
		{% endfor %}
		|{% for pr in providers %}
			<a href="javascript:set_openid('{{ pr.url }}', '{{  pr.name }}');">{{ pr.name }}</a>
		{% endfor %}
	</p>
	<p>{{form.remember_me}} Remember Me</p>
	<p><input type="submit" value="Sign In"></p>
</form>
{%  endblock %}
```

# 数据库

我们将使用flask-sqlalchemy这个扩展来管理我们的web应用的数据。

这个是对sqlalchemy的封装。它是一个ORM。

alchemy的字面含义是炼金术。

ORM的意义，就是允许数据库应用跟对象一起工作，而不是跟表和sql语句。

这样就屏蔽了sql语句这些内容。

接下来我们将使用sqlite。

我们要往config.py里加入内容。

我们设计一个简单的数据库表。

users表：id、nickname、email。

新建一个app/models.py文件。

```
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	
	def __repr__(self):
		return '<User %r>' % (self.nickname)
```

在`app/__init__.py`里加入：

```
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
```

在config.py里加入。

```
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
```

然后我们创建数据库。

新建一个脚本，db_create.py。

```
#!flask/bin/python

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
	api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
	api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
		api.version(SQLALCHEMY_MIGRATE_REPO))

```

执行这个脚本，得到一个app.db的数据库文件。

我们需要进行一次迁移，把一个空的数据库迁移到一个能存储用户的数据库上。

写一个脚本db_migrate.py。

```
#!flask/bin/python
import imp
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))

tmp_module = imp.new_module('old_module')
old_module = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

exec(old_module, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)

open(migration, 'wt').write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'new migration saved as ' + migration
print 'current db version: ' + str(v)
```

执行这个脚本。

```
new migration saved as /home/teddy/work/test/flask/db_repository/versions/001_migration.py
current db version: 1
```



我们再加入数据库升级和降级的脚本。

db_upgrade.py。

```
#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO )
print 'current db version : ' + str(v)
```

db_downgrade.py。

这个脚本一次只降级一级，要降低多级，就运行多次就好了。

```
#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO )

api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v-1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO )
print 'current db version : ' + str(v)
```

现在我们增加一个posts表。表示发表的文章。

posts：

id、body、timestamp、user_id。

在models.py里修改。

```
from app import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic') #注意这一行。
	def __repr__(self):
		return '<User %r>' % (self.nickname)
		
		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post %r>' % (self.body)
```

现在我们的数据库有变化了。

所以第一件事情就是运行迁移脚本。

```
./migrate_db.py
```

现在我们需要给我们的web应用，加入初始用户。

写一个脚本。add_user.py。

```
#!flask/bin/python
from app import db, models

u = models.User(nickname='carl', email='carl@xxx.com')
db.session.add(u)
u = models.User(nickname='david', email='david@xxx.com')
db.session.add(u)
db.session.commit()

users = models.User.query.all()
for u in users:
	print str(u.id ) + ": " + u.nickname
```

```
1: carl
2: david
```

现在我们要添加文章。

add_post.py。

```
#!flask/bin/python
from app import models,db

import datetime

u = models.User.query.get(1)
p = models.Post(body='my first post', timestamp=datetime.datetime.utcnow(), author=u)
db.session.add(p)
db.session.commit()
```

# 用户登录

接下来，我们将要使用2个扩展。flask-login和flask-openid。

在`app/__init__.py`里修改。

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir

import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models
```

现在要修改models.py里的User类。增加这几个函数。

```
	@property
	def is_authenticated(self):
		return True
		
	@property
	def is_active(self):
		return True
	@property
	def is_anoymous(self):
		return False
		
	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)
```

然后我们要实现user_load回调。

在app/views.py里写。

```
@lm.user_load
def load_user(id):
	return User.query.get(int(id))
```

我们还需要修改login函数。

```

```

这一部分增加了很多的东西。不一一描述了。



因为后续的都基于OpenID这一步操作ok。但是我这一步过不去，暂时就不继续这个教程了。

