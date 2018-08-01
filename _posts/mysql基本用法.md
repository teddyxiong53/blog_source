---
title: mysql基本用法
date: 2018-08-01 23:03:25
tags:
	- 数据库

---



## 解决localhost root访问不允许的问题

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



# 参考资料

1、解决linux-mysql Access denied for user 'root'@'localhost'

https://blog.csdn.net/hhj724/article/details/73277506