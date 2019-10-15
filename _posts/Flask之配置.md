---
title: Flask之配置
date: 2019-10-12 11:50:32
tags:
	- Flask

---

1

一般是使用config.py来做flask的配置。

config.py里面就是放key=val这种简单的赋值语句。

```
DEBUG=True
#其他
```

然后代码里这样用：

```
app = Flask(__name__)
app.config.from_object('config')
#要使用里面的配置项这样做：
print(app.config['DEBUG'])
```



#instance目录的作用

为什么需要instance目录？

是为了解决这些现实需求：

```
1、你有一些配置项，不适合写在全局的config.py配置里并对外发布。
2、多个配置文件管理。
```

instance目录就是来解决这个需求的。

使用了instance目录的项目结构如下：

```
config.py
requirements.txt
run.py
instance/
	config.py
yourapp/
	__init__.py
	models.py
	views.py
	templates/
	static/
```

如果你想要加载instance目录下的配置，使用这个来加载：

```
app = Flask(__name__, instance_relative_config=True) #需要指定instance_relative_config为True。
app.config.from_object('config') #先加载外面的，以便后面的进行覆盖。
app.config.from_pyfile('config.py') #这个就是使用了instance目录下的
```

在git管理时，一般选择过滤掉instance目录，以免把敏感信息泄露出去。

一般存放秘钥之类的。



如果你的生产环境和开发环境之间的差别很小。你可以使用instance目录下帮你抹平配置上的差异。



根据环境变量来配置

instance文件夹不在版本控制里，这意味着你将不能追踪里面的文件变化。

如果你有很多套配置，那么这种方式不是很合适。

flask也考虑到这种情况。当我们有多个配置文件的时候，是新建一个config目录。

```
config/
	__init__.py #需要这个空文件，
	default.py
	production.py
	development.py
	staging.py
instance/
	config.py
```

然后在代码里这样写：

```
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.default')
app.config.from_pyfile('config.py')
app.config.from_envvar('APP_CONFIG_FILE')
```

然后运行之前，我们先设置环境变量APP_CONFIG_FILE就可以了。



参考资料

1、Python flask中的配置

这篇文章写得很好。

https://www.cnblogs.com/m0m0/p/5624315.html