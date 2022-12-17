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

# 系列文章

先照着这个系列文章学习一下。

https://blog.csdn.net/qq769651718/category_7480207.html

## 编译代码

先下载代码搭建环境。

git clone了代码。

```
git clone https://github.com/cloudwu/skynet.git
cd skynet
make linux
```

需要clone的方式，因为依赖了一个git submodule，jemalloc。

make的时候，会先去把jemalloc的代码下载。

看了一下Makefile的写法，很简单实用的做法。

用的是gnu99的标准。

## 运行测试

启动example服务端：

```
./skynet ./examples/config
```

然后运行一个测试服务端。

client是lua脚本。我的系统已经安装了lua程序的。

但是当前skynet要求的是lua5.4的。

所以还是用skynet里自带的吧。

```
3rd/lua/lua ./examples/client.lua
```

可以正常连接通信。

## 写一个test.lua

就在examples目录下，新建一个test.lua。



# 参考资料

1、

https://zhuanlan.zhihu.com/p/161865024

2、

这里面有张图不错。

https://domicat.me/2020/05/04/learn-skynet-framework/

http://forthxu.com/blog/usr/uploads/2014/07/1456960310.pdf

这篇文章就已经非常全面了。

https://toutiao.io/posts/u045z3/preview