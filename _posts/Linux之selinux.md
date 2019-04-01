---
title: Linux之selinux
date: 2018-09-20 11:52:04
tags:
	- Linux

---



什么是selinux？



selinux的se是Security Enhanced的意思。

主要价值是提供了一个灵活可配置的MAC机制。

构成：

1、内核里se模块。代码在linux-stable\security\selinux

CONFIG_SECURITY_SELINUX。

2、用户态工具。

selinux是NSA和selinux社区共同工作的结果。



#参考资料

1、SELINUX工作原理

https://www.cnblogs.com/gailuo/p/5041034.html

2、一文彻底明白linux中的selinux到底是什么

https://blog.csdn.net/weixin_42350212/article/details/81189717