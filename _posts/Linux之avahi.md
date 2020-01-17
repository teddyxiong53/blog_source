---
title: Linux之avahi
date: 2020-01-16 11:51:19
tags:
	- Linux
---

1

什么是avahi？有什么用？

要了解avahi，需要先了解zeroconf。

zeroconf，就是零配置。是一个网络技术。自动生成可用ip地址的网络技术。

zeroconf是apple公司提出的技术规范。

avahi就是zeroconf技术的开源实现，主要用在Linux上。



avahi允许程序在不手动配置网络的情况下，在一个局域网内发布和获取各种服务和主机。

例如，当一台计算机接入到某个局域网，这台计算机上运行了avahi程序，那么avahi就会自动进行广播，这样就可以从局域网里发现可用的打印机、共享文件等等。



avahi在Linux下的进程是avahi-daemon。





参考资料

1、linux服务——Avahi

https://blog.csdn.net/updba/article/details/7389733

2、维基百科

https://en.wikipedia.org/wiki/Avahi_%28software%29

3、

https://wiki.archlinux.org/index.php/Avahi