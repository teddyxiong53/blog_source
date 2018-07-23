---
title: seafile（1）
date: 2018-07-20 21:28:50
tags:
	- 云计算
typora-root-url: ..\
---



seafile是一个开源的云存储平台。

发布时间是2012年10月。

提供的功能：

1、文件存储和共享。

2、消息通信和群组讨论。

3、协作编辑。

官网：https://www.seafile.com/home/

这个是demo：https://demo.seafile.top/

社区版本是免费的。

树莓派服务器代码：https://github.com/haiwen/seafile-rpi/releases

目前最新的是6.3.2版本。基于Django1.8 。

github上下载太慢。这个是码云上的。

https://gitee.com/lins05/seafile

这个文档全是英文写的。也比较长。

https://manual.seafile.com/build_seafile/server.html

这个是树莓派服务器的编译方法。

https://manual.seafile.com/build_seafile/rpi.html



树莓派版本安装比较慢。我先在Ubuntu下试一下。

新建一个名字叫seafile的用户。

```
sudo useradd -m -s /bin/bash seafile
```

然后设置用户的密码。

```
sudo passwd seafile
```

切换到seafile用户。

```
su - seafile
```

下载安装包。

```
wget http://seafile-downloads.oss-cn-shanghai.aliyuncs.com/seafile-server_6.0.8_x86-64.tar.gz
```

这个下载很快。

解压。进入目录。执行：

```
./setup-seafile-mysql.sh
```

提示要安装：

```
sudo apt-get install python-mysqldb
```

```
---------------------------------
This is your configuration
---------------------------------

    server name:            xhl_seafile
    server ip/domain:       192.168.190.137

    seafile data dir:       /home/seafile/seafile-data
    fileserver port:        8082

    database:               create new
    ccnet database:         ccnet-db
    seafile database:       seafile-db
    seahub database:        seahub-db
    database user:          seafile
```

然后执行：

```
./seafile.sh start
./seahub.sh start
```

然后会提示你输入邮箱和密码。是用来登陆用的。

然后在浏览器输入这个网址进行访问。

http://192.168.190.137:8000/

![](/images/seafile（1）界面.png)



看了一下压缩包里的内容，内容挺多的。不适合做为学习材料。

暂且放下。



# 参考资料

1、ubuntu服务器 安装 seafile 个人网盘

我主要参考了这篇。

https://www.cnblogs.com/Anani-leaf/p/8796832.html