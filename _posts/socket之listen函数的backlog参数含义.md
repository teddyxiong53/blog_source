---
title: socket之listen函数的backlog参数含义
date: 2019-01-12 09:38:59
tags:
	- socket
---



一直没有仔细去理解listen的backlog这个参数的本质含义，现在看到了，就深入了解一下。

可以简单理解为一个队列的容量，限制连接过来的连接的数量，减轻服务器的负担。



参考资料

1、

https://blog.csdn.net/ordeder/article/details/21551567