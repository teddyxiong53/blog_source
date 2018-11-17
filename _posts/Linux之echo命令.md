---
title: Linux之echo命令
date: 2018-11-17 16:37:28
tags:
	 - Linux

---



本来以为echo命令没有什么。但是在使用中还是碰到了问题。

我把一串json字符串echo到一个文件，但是发现没有成功。

发现echo对于单引号和双引号有一些需要注意的地方。

所以我需要把json字符串用单引号括起来，这样就可以正常输出了。





# 参考资料

1、echo命令，不带引号，单引号，双引号的区别

https://blog.csdn.net/daxus/article/details/8280928