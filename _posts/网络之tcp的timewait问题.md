---
title: 网络之tcp的timewait问题
date: 2018-09-14 10:47:27
tags:
	- 网络

---



我杀掉进程再重新启动，导致了网络连接出现问题。

查看netstat，发现端口处于TIME WAIT状态。

这种还是要靠REUSEADDR来避免问题。



# 参考资料

1、面试总结之time_wait状态产生的原因，危害，如何避免

https://blog.csdn.net/u013616945/article/details/77510925