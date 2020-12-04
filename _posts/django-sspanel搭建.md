---
title: django-sspanel搭建
date: 2020-12-01 17:49:30
tags:
	- docker
---

1

```
 Cannot create container for service web: Conflict. The container name "/web" is already in use by container
```

这样是要删除掉本地的所有container再试。

需要clone，然后切换到master分支。

然后docker-compose版本太低了。所以升级docker-compose到最新的。

```
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

需要退出再登陆终端才能看到替换生效。

现在可以跑起来。但是无法访问。

web没有起来。

我是直接用docker-compose up来启动的。

看看readme的说明。

还是按照这个来。

```
# 进入项目根目录
cd django-sspanel

# 复制环境变量文件
cp .env.sample .env

# 将你的自定义配置写在里面
vim .env

# 收集静态资源
docker-compose run --rm web python manage.py collectstatic --noinput

# 创建数据库表
docker-compose run --rm web python manage.py migrate

# 创建超级用户账号
docker-compose run --rm web python manage.py create_admin --email "admin@ss.com" --username "admin1" --password "adminadmin"


# 关闭刚才创建的脚本服务
docker-compose down

# 开启程序并放在后台运行
docker-compose up -d
```

执行收集静态资源这一步，连接数据库有问题。

```
django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'172.21.0.4' (using password: YES)")
```



需要给172.21.0.4这个地址开数据库访问权限。

```
grant all privileges on *.* to root@'%' identified by 'your password';
grant all privileges on *.* to root@'your IP' identified by 'your password';
flush privileges;
```

执行了这些还是不行。

进入mysql命令行，use mysql。切换到这个数据库。

查询一下

```
mysql> select host,user from user;
+------------+------------------+
| host       | user             |
+------------+------------------+
| %          | opensips         |
| %          | root             |
| 172.21.0.4 | root             |
| localhost  | ampache          |
| localhost  | debian-sys-maint |
| localhost  | mysql.session    |
| localhost  | mysql.sys        |
| localhost  | opensips         |
| localhost  | root             |
+------------+------------------+
9 rows in set (0.02 sec)
```

这样权限应该就是没有问题的。

那么现在的问题，应该就不是权限问题了。

这样再看看。

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourPassword';
FLUSH PRIVILEGES;
```

还行不行。

我从windows下，访问Ubuntu数据库是可以的。说明远程访问权限没有问题。

切换到dev版本，问题还是一样的。

暂时先不做了。



1、官方说明

https://github.com/Ehco1996/django-sspanel/wiki/docker%E9%83%A8%E7%BD%B2

2、sqoop报错:Access denied for user 'root'@'172.16.21.22' (using password: YES)

https://blog.csdn.net/weixin_39445556/article/details/80313148

3、【踩坑】Django django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password:

https://www.cnblogs.com/webDepOfQWS/p/12836901.html