---
title: Linux内核之网络子系统（一）学习策略
date: 2018-04-02 16:49:03
tags:
	- Linux内核

---



我上网搜索了一下，没有发现网上有成系列的文章。我就自己尝试写一下吧。其实就是我自己的学习记录。

网络子系统，因为不是内核本来的一部分，而且比较独立，加上又非常复杂，所以一般讲内核的书是不会讲网络子系统的。网络这部分专门有书来讲解。

关于参考书的选择，我觉得应该从国内人写的书籍入手，国外的书籍虽然经典，但是我感觉不是很接地气，应该在有一定的了解之后在阅读，会比较合适。

所以我选择了国人写的《Linux内核源码剖析：TCPIP实现》这本书。是基于Linux2.6.20来讲解的。出版时间是2010年。

我们先把目录列出来，心里有个大概的印象。

```
1、预备知识
	1）应用层配置诊断工具。
	2）内核空间和用户空间的接口
		procfs、sysctl、sysfs、ioctl、netlink。
	3）网络io加速。
		TSO/GSO、IO AT
	4）其他。
		slab、RCU。
2、网络体系结构概述。
3、套接口缓存。
4、网络模块初始化。
5、网络设备。
6、IP编址。
7、接口层的输入。
8、接口层的输出。
9、流量控制。
10、Internet协议族。
11、IP协议。
12、IP选项处理。
13、IP分片和组装。
14、icmp。
15、IP组播。
16、igmp。
17、邻居子系统。
18、arp协议
19、路由表
---------------------上面的是上册的。
20、路由缓存。
21、路由策略。
22、socket层。
23、socket io
24、socket选项。
25、传输控制块。
26、tcp协议。
27、tcp定时器。
28、tcp连接的建立。
29、tcp拥塞控制。
30、tcp的输出。
31、tcp的输入。
32、tcp连接的终止。
33、udp协议。
```



下面我们把第一章的内容学习一下。

我用来查阅代码的linux版本是2.6.35 。我不想再去下载2.6.20的代码，再去建立工程。



# 应用层配置工具

## iputils

包括ping、arping、tftpd这些。

## net-tools

ifconfig、route、netstat等。

## iproute2

这个是最新的，也是最强大的。

包括很多命令，其中ip这个命令最常用。

# 内核和用户空间的接口

procfs和sysctl都可以导出内核内部信息，二者的区别是：

1、procfs主要是导出只读的信息。sysctl导出的都是可写的。

2、如果导出只读的信息的话，用哪个呢？数量多，就用procfs，几个的话，就用sysctl。

## procfs

网络子系统的在/proc/net目录下，下面文件很多，有一种比较特殊的文件，例如tcp、udp、arp。

```
/proc/800/net # cat tcp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode                                                     
   0: 00000000:0017 00000000:0000 0A 00000000:00000000 00:00000000 00000000     0        0 4151 1 be440000 100 0 0 10 0                              
/proc/800/net # cat udp
  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode ref pointer drops             
/proc/800/net # 
```

这种文件的格式比较固定，叫做综合文件（synthetic files）。最大的特点就是由一系列的记录组成，类似数据库里的记录。这种格式用来描述系统的一些统计或者状态是很合适的。

创建这样的文件，需要特别的接口。

```
proc_net_fops_create(net, "arp", S_IRUGO, &arp_seq_fops)
```

## sysctl

sysctl可以操作的内核参数，都在/proc/sys目录下面。



## sysfs

sysfs最初是叫做driverfs，因为最初的设计用途就是用来管理设备驱动的。

后面大家发现这个文件系统对于内核的其他子系统也很有用。于是被改成了sysfs。



## ioctl

net-tools就是通过ioctl来和内核进行交互的。

## netlink

netlink是网络应用程序和内核通信最常用的接口。iproute2就是用这种方式的。



# 网络io加速

这么多年，虽然CPU在一直进步，但是tcpip协议栈变化不大。

这就导致不能充分利用CPU的性能。

例如，tcpip传输过程中，需要封装、解封装，这个虽然不复杂，但是会占用CPU处理周期。网络带宽越高，这个问题就越严重。

以前，网络流量低，所以这个问题不严重。现在已经不能不解决了。

目前有这么几种解决方案：

1、TSO。TCP Segment Offload。

这种解决方案只对具有某些特征的数据包有效。

2、RDMA。Remote DMA。

这个不太好。没有什么竞争力。

3、Onloading技术。

这种思想被Intel采用了。

## TSO

只针对tcp协议。这种概念可以推广开来，就是GSO 。Generic Segment Offload。

## IO AT

Intel的网络io加速技术。

