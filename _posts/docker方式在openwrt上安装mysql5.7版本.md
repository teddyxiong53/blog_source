---
title: docker方式在openwrt上安装mysql5.7版本
date: 2021-02-09 09:57:30
tags:
- docker
---

我的树莓派4b上安装了openwrt。现在要在这个上面用docker安装mysql5.7版本。

直接pull

```
docker pull mysql:5.7
```

这样是不行的。

会报错。

```
no matching manifest for linux/arm64/v8 in the manifest list entries
```

需要这个

```
docker pull biarms/mysql:5.7.30-linux-arm64v8
```

创建目录，给容器来挂载用。

```
mkdir -p /root/docker/server/mysql/data
```

还需要创建一个配置文件/root/docker/server/mysql/my.cnf

内容如下：

```
[mysqld]
## 
server_id=1
## 
binlog-ignore-db=mysql
## 
log-bin=replicas-mysql-bin
## 
binlog_cache_size=1M
## 
binlog_format=mixed
## 
expire_logs_days=7

max_allowed_packet=125M
max_connections=200
max_connect_errors=10000
datadir =/opt/mysql/data
socket  =/opt/mysql/data/mysql.sock
 
#Encoding
collation-server = utf8_unicode_ci
init-connect='SET NAMES utf8'
character-set-server = utf8
 
log_error=error.log
 
[client]
# default-character-set = utf8
socket  =/opt/mysql/data/mysql.sock
```



启动

```
docker run -itd \
--name mysqld -p 3306:3306 \
--restart always \
--privileged=true \
-e TZ=Asia/Shanghai \
-e MYSQL_ROOT_PASSWORD=123456 \
-v /root/docker/server/mysql/my.cnf:/etc/mysql/my.cnf \
-v /root/docker/server/mysql/data:/var/lib/mysql \
biarms/mysql:5.7.30-linux-arm64v8
```

然后进入到容器里。

```
docker exec -it mysqld mysql -uroot -p123456
```

这样可以支持操作。

但是我在另外一个容器里，怎样访问这个呢？



参考资料

1、树莓派4B使用docker安装mysql5.7.30

https://my.oschina.net/fastjrun/blog/4310625

