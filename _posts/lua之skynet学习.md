---
title: lua之skynet学习
date: 2022-12-11 22:38:19
tags:
	- lua

---

--

先看这个视频教程，有一个初步的了解。

https://www.bilibili.com/video/BV1C3411T7Qt



在之前的skynet目录结构的文章中，也已经提到。

skynet框架用C语言写的部分，主要是为了性能和可靠，

一些基础的服务是通过C语言来编写，

这部分功能不容易发生变动，需要精干的语言去编写实现后，再以后就调用即可。

外面的服务或者库，需要变动，或者开发效率要求较高，则用Lua语言代替。



skynet 是一个为网络游戏服务器设计的轻量框架，采用单进程，多线程架构。

skynet 由一个或多个进程构成，每个进程被称为一个 skynet 节点。

skynet可以形成集群，在配置表中，可以确定一个主节点和其他的副节点，一个进程为一个节点，节点之间的服务，通过消息进行传递。



这个是一个示例代码。

https://github.com/cloudwu/skynet-demo



总的代码还是没有那么复杂的，属于实战派的风格。



这里有个ppt介绍skynet

https://pan.baidu.com/s/1i3qp7b3

基于skynet的聊天室

https://github.com/forthxu/talkbox

参考资料

1、

https://zhuanlan.zhihu.com/p/161865024

2、

这里面有张图不错。

https://domicat.me/2020/05/04/learn-skynet-framework/

http://forthxu.com/blog/usr/uploads/2014/07/1456960310.pdf

这篇文章就已经非常全面了。

https://toutiao.io/posts/u045z3/preview