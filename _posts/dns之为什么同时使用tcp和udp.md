---
title: dns之为什么同时使用tcp和udp
date: 2019-01-11 11:35:51
tags:
	- dns
---



dns同时占用tcp和udp的53号端口。

这种单个应用协议同时使用两种传输协议的情况，在tcpip协议栈里也是比较少见的。

如果你抓包分析一下，可以看到基本上是在用udp。

但是当包长度超过512字节后，就会失败，然后就会改用tcp进行传输。





参考资料

1、DNS分别在什么情况下使用UDP和TCP

https://www.cnblogs.com/549294286/p/5172435.html