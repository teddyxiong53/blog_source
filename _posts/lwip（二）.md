---
title: lwip（二）
date: 2018-02-03 17:11:15
tags:
	- lwip

---



先从入口函数开始读。

我阅读的是移植到rt-thread里的lwip。

调用顺序是：

```
lwip_system_init
	1、以太网的初始化。在ethernetif.c里。
	2、tcpip_init。
		等初始化完成，用netif_up把网卡启动。
	3、设置网卡ip地址。
```

# tcpip_init

1、lwip_init。

2、创建size为8的一个mbox，这个是API用的邮箱。

3、创建一个锁定tcpip_thread的Mutex。

4、创建线程tcpip_thread。

# lwip_init

这个是lwip的初始化。所有的初始化都在这里做了。

1、stats_init。留空。

2、sys_init。给os适配用的。一般是空的。

3、mem_init。动态内存初始化。跟rt-thread的分配算法一样的。

4、memp_init。内存池初始化。

5、pbuf_init。空的宏。预留位置。

6、netif_init。

7、ip_init。

8、etharp_init。

9、raw_init。

10、udp_init。

11、tcp_init。

12、sys_timeouts_init。



# memp

1、先看memp_desc结构体。

```
size
num
base
**tab：这个是指向空闲的块的。
```

2、关于memp_pools的定义，我觉得真的没有必要这么绕。让人比较费解。如果要达到便于维护的效果，有很多的其他方式可以做到。

相当于有一个枚举：

```
MEMP_RAW_PCB
...
MEMP_MAX
```

```
struct memp_desc *memp_pools[MEMP_MAX] = 
{
  &memp_RAW_TCB,
  ...
};
```

就是分配了一堆固定大小的数组块。然后分别指派各种用途。

块的尺寸是由sizeof结构体算出来，个数是有在opt.h里配置的。

3、对外的接口就是memp_malloc和memp_free。

#netif

ip地址的定义和赋值。

定义：ip4_addr_t ipaddr

赋值：IP4_ADDR(&ipaddr, 127,0,0,1);

1、初始化，就是把loop这netif初始化并且启动了。

