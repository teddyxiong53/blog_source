---
title: 阿里云ifconfig看不到公网ip
date: 2020-03-24 10:02:02
tags:
	- 阿里云

---

1

在阿里云上新建的esc机器，会有一个公网ip地址。

但是你在机器里执行ifconfig，却只能看到一个172.16网段的内网地址。

这个具体是什么原因？

这里就涉及到一个概念：弹性IP。



参考资料

1、为何 ifconfig 看不到外网地址？

https://www.v2ex.com/t/379531

2、弹性IP地址

https://baike.baidu.com/item/%E5%BC%B9%E6%80%A7IP%E5%9C%B0%E5%9D%80