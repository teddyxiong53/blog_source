---
title: nodejs之nodebb分析
date: 2019-04-16 14:43:28
tags:
	 - nodejs
---



配置mongodb。

输入mongo，进入到mongo命令行界面。

```
# 使用admin数据库
use  admin

#添加root用户。
db.createUser( { user: "admin", pwd: "040253", roles: [ { role: "root", db: "admin" } ] } )

#新建nodebb数据库
use nodebb

#添加用户
db.createUser( { user: "nodebb", pwd: "040253", roles: [ { role: "readWrite", db: "nodebb" }, { role: "clusterMonitor", db: "admin" } ] } )
```

然后退出mongo命令行。

修改/etc/mongod.conf文件。

这个文件当前不存在。加入这2行。

```
security:
  authorization: enabled
```

重启mongodb

```
sudo /etc/init.d/mongodb restart
```

看看能不能正常访问我们的admin数据库。正常则进入到mongodb命令行。然后我们直接退出。

```
mongo -u admin -p 040253 --authenticationDatabase=admin
```

然后我们下载好nodebb的源代码。

进入源代码目录，执行：

```
./nodebb setup    
```

这个是下载相关的模块。

然后会提示你进行输入，一路按回车就好了。修改反而会出错。

到了最后输入admin的相关信息的时候，才输入自己的信息。

```
./nodebb start
```

然后就可以访问了。

可以用./nodebb log查看日志。



然后看看代码。

代码挺多的。



参考资料

1、Installing on Ubuntu

https://docs.nodebb.org/installing/os/ubuntu/