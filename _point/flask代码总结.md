# 常用api

直接从`flask/__init__.py`里看。

```
class
	Request
	Response
	Blueprint
	Config
	
全局变量
	g
	current_app
	request
	session
	
全局函数	
	abort
	flash
	redirect
	send_file
	send_from_directory
	stream_with_context
	ulr_for
	
	jsonify
	
	render_template
```

有时候还需要从werkzeug里借用一些工具函数。

```
from werkzeug.exceptions import abort
```



# flask命令行

```
flask --help
```

查看一下帮助信息。

默认的app的指定方法：（下面4个方法任选其一就可以）

```
1、使用--app参数。
2、使用FLASK_APP环境变量。
3、有个默认的wsgi.py的文件。
4、有个app.py的文件。
```

可以使用--debug选项来进行调试模式。

子命令有：

```
flask routes
	查看当前应用的路由信息。
flask run
	运行一个develop server。
flask shell
	进入一个交互命令行。
```



locked_cached_property
	一个装饰器，用来把一个函数转化为一个lazy property。
	被装饰的函数，第一次被调用的时候，计算取得结果。
	下次直接返回这个缓存的结果。
	用到了线程锁，所以是线程安全的。
	
_AppCtxGlobals
	一个普通类。
	作为一个namespace存储app ctx的数据。
	创建一个app ctx的时候，自动就创建了一个这个对象。
	
	
flask_sqlalchemy
	连接数据库的url
		sqlite:
			sqlite:///path/xx.db
			主要是3个斜杠。
		mysql:
			mysql://user:pass@host/xx.db
		postgresql:
			postgresql://user:pass@host/xx.db
			
数据库迁移
为什么需要迁移？
因为有时候在开发过程中需要修改数据库模型，而之前是数据需要继续保留。
sqlalchemy的开发者写了一个迁移框架，叫做alembic。
另外，也可以用flask_migrate插件来做。这个插件是对alembic的包装。



flask_login

login_required

让Password只能写不能读的设置。

```
 @property 
def password(self):
	raise AttributeError("")
@password.setter
def password(self, password):
	self.password_hash = generate_password_hash(password)
```


	