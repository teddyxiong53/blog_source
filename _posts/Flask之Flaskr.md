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





参考资料

1、flaskr例子的运行

https://blog.csdn.net/freefishly/article/details/50717088

2、运行 Flaskr 的正确姿势

https://www.jianshu.com/p/73d88183ef3b

3、flask 官方教程中的create_app是怎么运行的？

https://segmentfault.com/q/1010000016116693/a-1020000016119472

4、解决 "OperationalError: (sqlite3.OperationalError) no such table: ..."问题

https://www.cnblogs.com/qq952693358/p/6648352.html