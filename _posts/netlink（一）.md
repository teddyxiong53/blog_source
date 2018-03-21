---
title: netlink（一）
date: 2018-03-11 16:36:35
tags:
	- Linux

---



# netlink发展历史

1、linux1.3的时候，就已经有netlink了。

2、linux2.1的时候，进行了改写，更加灵活、且更易于扩展。

3、2001年，IETF委员会开始对netlink进行标准化工作。不过很多建议没有被采纳，现在的netlink被设计为一种协议域，AF_NETLINK和AF_INET并列的。

整个的理念跟linux的一样，不是设计出来的，而是在不断的修改中成型的。



# 什么是netlink

1、面向数据报的无连接消息子系统。

2、基于通用的bsd socket架构而实现。

这让我们很容易联想到udp协议。

# netlink的优势是什么？

1、可以进行内核用户态的双向通信。但是系统调用也可以啊。

netlink的优势在于，你要给内核增加自己特有的东西的时候，不用冒着污染内核代码的风险。

你只需要再netlink.h里加上你自己定义的一个宏。

netlink是异步的，就跟普通的socket类似，可以有缓冲区。

系统调用则是同步的。



# netlink通信类型

支持两种通信类型：

1、单播。通常是App向kernel发送消息。

2、多播。通常是kernel向多个App发送消息。

# 消息格式

跟udp包类似。包头加消息。

包头16字节，消息内容长度不限。

包头结构：

```
struct nlmsghdr {
  u32 len;//包括头部16字节在内的长度。
  u16 type;//4种，NONE/ERROR/DONE/OVERRUN
  u16 flags;//16种最多。
  u32 seq;//控制丢包。
  u32 pid;
};
```

消息体，是TLV结构（Type Length Value）。

```
u16 type
u16 len
value.....
```

# 注意问题

有两种问题可能丢包：

1、内存耗尽。

2、App的的缓冲区溢出。App运行太慢，或者接受队列太小了。



# 接口

接口包括2类：

1、内核态的。

2、用户态。



socket failed 
Protocol not supported



netlink

# 参考文章

1、用户空间和内核空间通讯。这篇文章是基于linux2.6的，我现在是在4.14上做实验，所以有些地方需要自己改。

http://blog.csdn.net/varistor/article/details/25311177



2、

http://bbs.chinaunix.net/thread-2029813-1-1.html

3、

https://gist.github.com/arunk-s/c897bb9d75a6c98733d6





