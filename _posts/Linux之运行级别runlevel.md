---
title: Linux之运行级别runlevel
date: 2020-03-14 11:12:28
tags:
	- Linux

---

1

runlevel，就是靠不同的启动脚本目录来实现启动不同的程序的。

在/etc/目录下，有rc.x.d的名字。x取值为0到6 。

对应了Linux运行的7个level。

```
0： 关机。
1： 单用户。
2：多用户。
3：多用户，带网络。
4：未定义。
5：x11，图形界面启动。
6：reboot。重启。
```

在rc0.d下面，都是K字头的脚本，表示stop。这些脚本都是软连接，指向init.d目录。



参考资料

1、

https://www.liquidweb.com/kb/linux-runlevels-explained/