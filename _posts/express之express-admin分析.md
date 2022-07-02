---
title: express之express-admin分析
date: 2021-12-04 10:28:25
tags:
	- express

---

--

我是在github上搜索nodejs操作sqlite的代码的时候，找到了这个程序。

感觉不错。

代码在这里：

https://github.com/simov/express-admin

安装依赖

```
npm i
npm i sqlite3
```

执行：

```
node app.js
```

会提示你输入一些信息，选择数据库类型，我选择sqlite的。

密码要2个大写字母、2个小写字母、2个数字。我就用AAbb11

现在是提示“Empty Schema”的错误。

先看看文档。

这个程序在csdn上是找不到任何信息的。

express-admin是一个nodejs工具，用来管理mysql、sqlite、postgresql这三种数据库的。

基于express、mysql、bootstrap、hogan.js。

配置是通过编辑json文件来做的。

特性：

1、支持所有类型的sql 表关系。

2、国际化。

3、自定义view和event。

4、支持bootswatch这个网站的所有主题。

这个还可以作为一个全局命令进行安装

```
npm i -g express-admin
```

得到的工具是：

```
admin dir_name
```

回到前面的命令

```
node app.js
```

我在这里找到一篇操作sqlite的文章，里面有个db.sql脚本。

https://www.computerhope.com/issues/ch002076.htm

我直接给test.db里执行这个脚本，导入这些表，

```
sqlite3 ./test.db
> .read db.sql
> .exit
```

然后执行node app.js就正常了。

访问http://localhost:4000（端口是自己配置的）

输入用户名和密码进入系统，就可以看到对应的表格了。

然后就是一个数据库的管理软件。

支持换皮肤，支持多种语言。



这个是官方的example。

https://github.com/simov/express-admin-examples

参考资料

1、官方文档

https://simov.github.io/express-admin/