---
title: flask-movie项目分析
date: 2020-11-20 11:27:30
tags:
	- flask
---

1

```
mysql -u root -p -D flask_movie < movie.sql
```

需要先到mysql命令行下创建数据库：

```
mysql > create database flask_movie;
```

执行movie.sql，是失败的。

因为里面有utf-8的中文。

我安装的mysql8.0的，又没有my.ini文件。所以从网上找一份修改。

用这个命令查看到的就是my.ini应该放的路径。

```
mysql> show variables like 'datadir';
+---------------+----------------+
| Variable_name | Value          |
+---------------+----------------+
| datadir       | D:\mysql\data\ |
+---------------+----------------+
1 row in set, 1 warning (0.00 sec)
```

mysql比较麻烦。

我还是想办法转到sqlite的来做。



python代码里也有不少的问题。

不跑了。看看代码就好了。



放到Linux下运行看看。

我还是基于sqlite来做。

表格设计，sql语法不熟练。

先用sqlite expert来设计table。

然后用sqlite的命令执行insert语句。

修改数据库地址：

```
basedir = os.path.abspath(os.path.dirname(__file__)) + '/../'
SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db')
```

然后可以跑起来。

运行命令：

```
python movie.py
```

但是感觉数据库并没有生效。

配置是有读取到。

但是所有操作，都没有对数据库产生影响。

有影响的。app.db这个文件的目录不对。

有2个，起作用的那个在app目录下。

是我目录指定不对。

而且我发现一个问题，就是app.db里的表格，我不需要自己来用sqlite expert来自己写。

ORM会帮我们生成对应的表格。

现在数据都正常了。



不对。进行登陆操作：admin/a123456

则会打印出错堆栈。

```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) NOT NULL constraint failed: userlog.id
[SQL: INSERT INTO userlog (addtime, user_id, ip) VALUES (?, ?, ?)]
```

userlog这个表格插入数据出错。

操作日志的id，是空的。所以出错了。

我之前用sqlite expert做的table不完全对。

所以，应该把自己生成的app.db。然后进行insert数据的操作。

这样可以了。

这份代码基本是可以投入实际使用的。

代码有值得学习的地方。

数据库部分。

为了方便提交和出错回滚。这样来做。

```
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try: #开启事务
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
```

自己扩展SQLAlchemy。增加一个auto_commit。是一个上下文。

使用的时候，就这样用：

```
	with db.auto_commit():
            admin=Admin()
            admin.set_attr(form.data)
            admin.is_super=AdminTypeEnum.NO_SUPER
            db.session.add(admin)
            Oplog('添加管理员:' + admin.name)
```

这样就不用每次都去处理回滚逻辑了。

在app.models.base.py里，创建数据库实例。

```
db=SQLAlchemy()
```

在`app/__init__.py`里，进行import，然后再init_app

而对于所有数据库，都有一条addtime。

也采取了自己扩展db.Model的方式。

```
class BaseModel(db.Model):
    __abstract__=True
    addtime=Column(db.DateTime,index=True)
    #1
    def set_attr(self,attrs):
        for key,value in attrs.items():
            if hasattr(self,key) and key!='id':
                setattr(self,key,value)
    def __init__(self):
        self.addtime=datetime.datetime.now()
```

所有的model都继承BaseModel。

虽然使用了bootstrap，但是没有用flask_bootstrap模块。

弹幕功能，需要打开redis。redis配置可以不用。因为不配置的话，默认的host和port就可以。

windows下载redis，执行redis-server监听就好了。

发送弹幕，redis这边就可以看到打印的。



可以登陆后台管理界面，进行影片的上传等处理。看起来界面挺不错的。

登陆：admin/a123654。注意是654。而不是456

这个的大概逻辑清楚了。



参考资料

1、mysql 8.0找不到my.ini配置文件解决方案

https://blog.csdn.net/to_perfect/article/details/107009110