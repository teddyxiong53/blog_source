---
title: Linux驱动之NAPI机制
date: 2018-02-28 18:26:11
tags:
	- Linux驱动

---



#什么是napi

NAPI是New API的缩写。这个名字真是够奇怪的。在内核2.5版本开始引入。

napi是Linux上采用的一种提高其网络处理效率的技术。

核心思路就是不用中断的方式读取数据，而是首先用中断唤醒数据接收的服务程序，然后poll的方法来轮询数据。

目前napi技术已经在网卡驱动层和网络层得到广泛的应用。

简单来说，napi是综合了中断方式和轮询方式的技术。

在数据量少的时候，就用中断方式，在数据量大的时候，就用轮询技术。



处理外部事件是CPU必须要做的事情。

因为CPU和外设的不平等性，导致外设的事件被CPU当做是外部事件，其实他们是平等的，只是冯诺依曼机器不这么认为。

既然要处理外部事件，那么就要按照一定的方法，常用的方法是：

轮询、中断、dma。

中断处理方式，CPU是被动的。CPU必须在中断时停下自己的事情来处理。

轮询的方法，CPU是主动的。

中断方式，看起来好像很高效，但是可能会丢失一些数据。

轮询则会多做很多徒劳无功的事情。但是轮询不会遗漏事情。

中断在有很多中断的时候，产生的遗漏现象就很严重。

二者都有好有坏。能不能取长补短呢？

有，就是现在的napi这个东西。

在数据不频繁的是，用中断处理，中断频繁的时候，就用轮询的方式来处理。

napi解决了什么问题？

1、限制了中断的数量。

2、CPU也不会做很多无用功。



# 如何实现？

我们看napi方式和非napi方式的区别。

1、支持napi的网卡驱动必须提供轮询方法poll。

2、非napi的内核接口为netif_rx，napi的内核内核接口为napi_schedule。

# 代码分析

dm9000的是这样。

```
dm9000_interrupt
	dm9000_rx
		netif_rx
			netif_rx_internal
				enqueue_to_backlog
					____napi_schedule
						这里就是触发了net_rx的软中断了。
```

# napi和netpoll区别

netpoll主要目的是让内核在网络和io子系统还不能使用的时候，依然可以收发数据。

主要用在网络控制台net console和远程内核调试里。

实现netpoll函数，主要是要实现kernel里的poll_controller函数。







# 参考资料

1、NAPI 技术在 Linux 网络驱动上的应用和完善

https://www.ibm.com/developerworks/cn/linux/l-napi/

2、NAPI之（一）——原理和实现

https://blog.csdn.net/hejin_some/article/details/72722555

3、6410 linux DM9000收包机制

https://blog.csdn.net/chengwenyang/article/details/52187715

4、napi和netpoll区别

http://www.360doc.com/content/11/1023/09/7975692_158366329.shtml