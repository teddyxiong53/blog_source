---
title: docker之entrypoint和cmd指令区别
date: 2021-05-13 19:17:34
tags:
	- docker
---

--

1。在Dockerfile中，只能有一个ENTRYPOINT指令，如果有多个ENTRYPOINT指令则以最后一个为准。
2。在Dockerfile中，只能有一个CMD指令，如果有多个CMD指令则以最后一个为准。
3。在Dockerfile中，ENTRYPOINT指令或CMD指令，至少必有其一。



参考资料

1、

https://blog.csdn.net/qq_45300786/article/details/103947527

