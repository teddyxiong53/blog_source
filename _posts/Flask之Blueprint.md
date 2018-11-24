---
title: Flask之Blueprint
date: 2018-11-24 15:04:51
tags:
	- Flask
---



在使用flask进行项目编写的时候，可能会有多个模块，例如一个普通的saas云办公应用。

会有用户管理、部门管理、账号管理等模块。

如果把所有的视图都放在一个views.py文件，那么views.py文件一定很大，不方便阅读和维护。

为了解决这种问题，所以有了Blueprint的概念。



我把例子上传在这里：https://github.com/teddyxiong53/Python/tree/master/flask/blueprint_test

目录结构是这样的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/flask/blueprint_test$ tree
.
├── app
│   ├── dept
│   │   ├── __init__.py
│   │   ├── __init__.pyc
│   │   ├── views.py
│   │   └── views.pyc
│   ├── __init__.py
│   ├── __init__.pyc
│   └── user
│       ├── __init__.py
│       ├── __init__.pyc
│       ├── views.py
│       └── views.pyc
├── __init__.py
└── run.py

```



参考资料

1、Modular Applications with Blueprints

http://flask.pocoo.org/docs/0.12/blueprints/

2、flask使用Blueprint进行多模块应用的编写

https://blog.csdn.net/u012734441/article/details/67631564