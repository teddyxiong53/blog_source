---
title: mysql基本用法
date: 2018-08-01 23:03:25
tags:
	- 数据库

---



# 解决localhost root访问不允许的问题

1、停止服务。

```
sudo /etc/init.d/mysql stop
```

2、跳过密码认证。

```
admin@ubuntu:~$ sudo mysqld_safe --skip-grant-tables
2018-08-01T15:07:34.123441Z mysqld_safe Logging to syslog.
2018-08-01T15:07:34.127543Z mysqld_safe Logging to '/var/log/mysql/error.log'.
2018-08-01T15:07:34.130859Z mysqld_safe Directory '/var/run/mysqld' for UNIX socket file don't exists.
```

3、无密码登陆进去。

```
mysql -u root
```

进不去，网上的资料对于当前版本的mysql似乎不管用了。



执行sql文件命令

```
mysql –uroot –p040253 users<users.sql
```



sql脚本文件里注释怎么写？

```
单行：--
多行：/**/
```

# 修改默认root密码

默认密码不知道是多少。反正随便输入字符都能进去。



要改一下。

```
alter user 'root'@'localhost' identified by '123';
flush privileges;
```



# MySQL Connection Error: (2002) Connection refused

如果使用localhost，就使用unixdomain，文件路径就是参数中的socket，

但如果这个参数是空，那么写死/tmp/mysql.sock。

这么说来上面报错不存在的地址就是在源代码中给写死了，所以需要自己手动设置为正确的值。于是修改mysqli的参数再次测试。

当然解决这个问题其实很简单，网上有非常多的文章都有写如何解决，比如将mysqli.default_socket的值改为正确的路径，或者将localhost改成127.0.0.1等。主要还是想知道为什么不配置socket会出现错误，要找到问题的根源才好对症下药。



# 参考资料

1、解决linux-mysql Access denied for user 'root'@'localhost'

https://blog.csdn.net/hhj724/article/details/73277506

2、MySQL 数据库常用命令小结

https://blog.csdn.net/ithomer/article/details/5131863

3、Ubuntu下执行mysql的sql文件

https://blog.csdn.net/Liucheng417/article/details/50902657

4、mysql 5.7 修改账号密码

https://blog.csdn.net/qq_33472557/article/details/77726094