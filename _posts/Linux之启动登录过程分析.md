---
title: Linux之启动登录过程分析
date: 2022-04-08 13:56:11
tags:
	- Linux

---

--

unix/linux系统启动和登录过程：
1.init启动；
2.fork, exec执行getty；
3.getty打开终端，设置标准输入输出和标准错误输出；
4.getty再exec执行login；
5.login核对/etc/passwd中的用户名和密码，然后获得了各种信息初始化环境：起始目录、shell、用户名和path
6.login以exec执行bin/sh，shell先执行系统的初始化文件，再执行用户的初始化文件，初始化用户环境。



参考资料

1、unix/linux系统启动和登录过程

https://blog.csdn.net/preja2erec/article/details/1854237