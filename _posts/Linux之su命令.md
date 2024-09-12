---
title: Linux之su命令
date: 2020-03-24 15:54:11
tags:
	- Linux

---



su 后面跟一个`-`，也就是`su -`。这个表示以root身份进行登陆。

这个是必要的，不然直接su过去，/etc/profile是不会执行的，导致很多环境变量没有设置。



