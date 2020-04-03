---
title: Linux进程被杀掉后tcp连接还是established状态问题
date: 2020-04-02 15:54:19
tags:
	- Linux
---

1

我现在有个进程，已经被杀掉了，但是看到的tcp连接状态还一直是established的。

用kill -9 来杀掉进程，这个是不会关闭连接的。

  tcp_keepalive_interval:

Interval for sending keep-alive probes.  

参考资料

1、

https://community.hpe.com/t5/Networking/process-has-bean-killed-but-the-tcp-connection-still-established/td-p/4324643#.XoWaQGmHqJA