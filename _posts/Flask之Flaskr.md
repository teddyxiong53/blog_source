---
title: Flask之Flaskr
date: 2018-06-24 11:47:32
tags:
	- Flask

---



现在根据flask里的文档，运行flaskr看看。

完整流程走一遍。

下载最新代码。

```
git clone https://github.com/pallets/flask
```

查看tag。

```
hlxiong@hlxiong-VirtualBox:~/work/test/flask/flask$ git tag
0.1
0.10
0.10.1
0.11
0.11.1
0.12
0.12.1
0.12.2
0.12.3
0.12.4
0.2
0.3
0.3.1
0.4
0.5
0.6
0.6.1
0.7
0.7.1
0.7.2
0.8
0.8.1
0.9
1.0
1.0.1
1.0.2
```

可以看到最新的tag是1.0.2的。我们就把这个版本取出来。

```
git checkout 1.0.2
```

进入到example目录。

```
cd examples/tutorial/
#生成一个名字venv的环境。就在当前目录下。
python3 -m venv venv
#激活这个环境
 . venv/bin/activate
#安装flaskr
pip install -e .
```

运行：

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run
```



自己在windows下，用pycharm，python3.7来写一遍。

首先安装flask和flask-cli。

新建一个项目，叫flaskr，然后新建一个db.py文件。

但是flask init-db自定义命令，我这里不能成功执行。

所以我改成手动生成数据库。

然后新建main.py。把这个替代`__init__.py`。作为入口文件。在pycharm里执行这个文件即可。

我把代码放在这里：

https://github.com/teddyxiong53/Python/tree/master/flask/myflaskr

现在问题，点击登陆，不能正常跳转到首页。

状态也没有变成登陆状态。

因为request.method是大小写敏感的。需要写成大写的才行。

现在可以正常跳转，但是没有变成登陆状态。

是因为这里：

```
@bp.before_app_request
def load_logged_in_user():
    pass
```

我把这个函数省略了。我以为是没有人调用，但是是通过装饰器在每次请求前被调用的。

所以需要实现这个。

过了一遍所有功能。都可以正常工作了。

仔细理解一遍所有的代码。



# flaskr是怎么运行起来的

因为看下面的代码，没有app.py。入口代码是在`__init__.py`里。

flask run怎么就能把它运行起来呢？

这个要看flask的源代码：

```
app = DispatchingApp(info.load_app, use_eager_loading=eager_loading)

    from werkzeug.serving import run_simple
    run_simple(host, port, app, use_reloader=reload, use_debugger=debugger,
               threaded=with_threads, ssl_context=cert)
```



# 编译打包

前面的代码和一切操作都安装官方教程来。

在venv环境下进行操作。

```
pip install flit
pip list # 查看当前的已经安装的包，可以看到没有flaskr的。
```

在flaskr的同一层目录，新建pyproject.toml文件。

内容如下：

```
[project]
name = "flaskr"
version= "1.0.0"
description = "the flaskr blog"
dependencies = [
    "flask",
]
[build-system]
requires = ["flit_core<4"]
build-backend = "flit_core.buildapi"
```

然后执行：

```
flit build
```

会在当前目录下生成一个dist目录，下面有：

```
dist
|-- flaskr-1.0.0-py2.py3-none-any.whl
`-- flaskr-1.0.0.tar.gz
```

这个whl文件就可以发给别人安装。

```
pip install dist/flaskr-1.0.0-py2.py3-none-any.whl
```

安装之后，就可以在任意的目录下执行：

```
flask --run flaskr run 
```



我后续做项目，都保持跟flaskr一样的目录结构模式就好了。

```
ls
dist  flaskr  instance  pyproject.toml  venv
```

# 通过gunicorn执行

```
./test/py-test/tuturial/venv/bin/python -m gunicorn  -w 4 'flaskr:create_app()'
```



# pytest和coverage test

https://flask.palletsprojects.com/en/3.0.x/tutorial/test

# 参考资料

1、flaskr例子的运行

https://blog.csdn.net/freefishly/article/details/50717088

2、运行 Flaskr 的正确姿势

https://www.jianshu.com/p/73d88183ef3b

3、flask 官方教程中的create_app是怎么运行的？

https://segmentfault.com/q/1010000016116693/a-1020000016119472

4、解决 "OperationalError: (sqlite3.OperationalError) no such table: ..."问题

https://www.cnblogs.com/qq952693358/p/6648352.html