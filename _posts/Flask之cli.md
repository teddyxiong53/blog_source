---
title: Flask之cli
date: 2018-06-24 17:16:32
tags:
	- Flask

---

1

安装：

```
pip install flask-cli
```



在较老的版本的flask里，是使用一个manager.py的文件来进行相关操作的。这个脚本被称为flask-script。

后面引入了click模块来做flask的命令行支持。所以flask-script被淘汰了。

运行一个flask app就这样：

```
export FLASK_APP=hello
flask run
```

如果没有设置FLASK_APP环境变量，那么会去找wsgi.py或者app.py。

如果找不到任何实例，就会去找名字为create_app或者make_app的工厂函数。

flask run是运行开发服务器，在生产环境不要用。

flask shell，会启动一个shell，可以在shell里进行相关变量的查看。







参考资料

1、Flask-CLI

https://pythonhosted.org/Flask-CLI/

2、 Flask 命令行模式

https://www.cnblogs.com/liaojiafa/p/6730855.html

3、从Flask-Script迁移到Flask-Cli

https://www.cnblogs.com/lynsyklate/p/7693169.html

4、Flask内置命令行工具—CLI

http://www.xampp.cc/archives/3857