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



cmd给出的是一个容器的默认的可执行体。

也就是容器启动以后，默认的执行的命令。

**重点就是这个“默认”。**

意味着，如果docker run没有指定任何的执行命令或者dockerfile里面也没有entrypoint，

那么，就会使用cmd指定的默认的执行命令执行。

**同时也从侧面说明了entrypoint的含义，它才是真正的容器启动以后要执行命令。**



这也是为什么大多数网上博客论坛说的“cmd会被覆盖”，其实为什么会覆盖？因为cmd的角色定位就是默认，如果你不额外指定，那么就执行cmd的命令，否则呢？只要你指定了，那么就不会执行cmd，也就是cmd会被覆盖。





参考资料

1、

https://blog.csdn.net/qq_45300786/article/details/103947527

2、

https://blog.csdn.net/u013258415/article/details/80022224