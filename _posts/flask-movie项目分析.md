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



参考资料

1、mysql 8.0找不到my.ini配置文件解决方案

https://blog.csdn.net/to_perfect/article/details/107009110