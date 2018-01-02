---
title: java之rpc了解
date: 2018-01-01 18:04:02
tags:
	- java
	- 分布式

---



在大型互联网公司历来，公司的系统都是有很多个服务组成，各个服务部署在不同的服务器上，由不同的团队进行维护。

很自然的，就会遇到下面的问题：

1、你的服务，要依赖其他人的服务，现在其他人的服务在远端，怎么才能调用到？

2、如果别人要用我们写的服务，我们怎么提供给别人？



我们先按照基本的思路来。其他人的服务在其他的机器上，我们要调用到，应该是用网络通信来做。但是如果这样，那么每次调用服务的时候，都要写一堆网络通信的代码，又复杂又容易出错。

# 自己来写一个rpc调用示例

新建两个工程，一个Test，一个Test2。

Test里放rpc server的相关代码。

```
 HelloService.java
 HelloServiceImpl.java
 RPCServer.java
 Test.java
```

Test2里放rpc client的代码。

```
 HelloService.java
 HelloServiceImpl.java
 RPCClient.java
```

代码我放在github目录这里：（注意这个代码运行还有点问题，暂时不管）。

https://github.com/teddyxiong53/Java/tree/master/practice/rpc

现在只是做了一个很简单的调用，代码就已经比较繁杂了。所以网络通信这部分代码，肯定是可以进行一次提取的。很多公司已经做了这个事情了。也把成果开源出来了。所以我们没有必要再自己做一遍。

# rpc框架有哪些？

## netty

Jboss开源的。

netty是一个高性能、异步事件驱动的NIO框架。

# rpc的依赖技术

注意依赖序列化、反序列化、传输协议。





# rpc和rmi区别？

rmi只在java上有。rpc是一个通用的东西。

