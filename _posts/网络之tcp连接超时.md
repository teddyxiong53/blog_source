---
title: 网络之tcp连接超时
date: 2018-06-18 22:17:08
tags:
	- 网络

---



超时时间是127秒。因为按2的幂来依次backoff的，总共7次。1s、2s、到64s。加起来就是127秒。

如何测试端口的连通性？



用nmap和nc都可以。



http://www.chengweiyang.cn/2017/02/18/linux-connect-timeout/

