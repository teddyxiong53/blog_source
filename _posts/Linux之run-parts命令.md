---
title: Linux之run-parts命令
date: 2021-06-04 11:06:11
tags:
	- Linux

---

--

在很多系统中，用户目录下都有cron.daily之类的文件夹，里面的可执行文件每天都会被执行一次。

也就是说如果想添加一个每天都被执行的任务的话，在目录下放置该任务的脚本即可。

使用很方便，原理是什么呢，就是run-parts命令。

在ubuntu下，该文件位于/bin/run-parts，是个二进制文件，功能更为强大，支持--test等参数。

 在centos5下，run-parts命令位于/usr/bin/run-parts，内容是很简单的一个shell脚本，就是遍历目标文件夹，执行第一层目录下的可执行权限的文件。

参考资料

1、

https://blog.csdn.net/qq_32352565/article/details/70878082

