---
title: Linux内核之网络子系统（二）总体框架
date: 2018-04-18 10:08:55
tags:
	- Linux内核
typora-root-url: ..\
---



本文主要参考《Linux内核源码剖析 TCPIP实现》第二章。



我们看看Linux网络协议栈的框架。

![](/images/Linux内核之网络子系统（二）-协议栈框架.png)

# 系统调用接口

网络子系统提供了2种调用接口给用户进程。

第一种：

通过系统特有的网络调用接口进入内核。

sendmsg、recvmsg。

第二种：

通过普通文件操作来访问网络子系统。

read、write这种。

# socket

核心就是struct socket。代表了通信链路的一端。

socket是协议无关的。

里面有一个struct sock结构。

# 传输层协议

socket结构体里的struct sock，这个就是跟协议相关的了。

```
socket->sk->sock_common->skc_prot
这个下面就是一堆的函数指针。
connect、sendmsg那些。
```



# 套接口缓存

就是sk_buff。简称skb。

最大的优点：

1、很容易在头部、尾部添加和删除数据。

2、尽量避免了数据拷贝。



# 设备无关接口

用dev_queue_xmit进行发送。

用netif_rx进行接收。



#设备驱动程序

net_device结构体。register_netdevice。

在收取数据包的时候，支持NAPI的驱动，需要实现net_device的poll接口。



# 涉及的代码目录

1、drivers/net。

2、net下面的：

```
bridge
core
ethernet
ipv4
netlink
```

3、include。

