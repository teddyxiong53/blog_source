---
title: Linux之systemctl命令
date: 2017-10-05 16:08:05
tags:
	- Linux
	- 命令

---



systemctl是Linux下一个用来管理守护进程的工具和库的集合。是用来取代system V、service和chkconfig命令的。

下面列出常用的命令。我在树莓派上进行验证。

1、 列出各个选项。

有一组systemctl list-xxx的命令。xxx部分可以用tab键进行补全处理。不细讲了。

2、对服务进行启动、停止、查询等操作。

servicectl start xxx

stop

restart

reload

status

3、对服务进行激活、设置开机启动。

systemctl is-active mysql.server

systemctl enable xxx

systemctl disable xxx



这个命令很强大，其他的使用后续补充。当前这些对我来说够用了。



