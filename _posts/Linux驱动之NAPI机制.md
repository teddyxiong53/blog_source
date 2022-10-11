---
title: Linux驱动之NAPI机制
date: 2018-02-28 18:26:11
tags:
	- Linux驱动
typora-root-url: ..\
---



# 什么是napi

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

# 实用场景

如果流量非常不稳定，经常在中断和轮询之间切换，反而效率会下降。



# 如何实现？

我们看napi方式和非napi方式的区别。

1、支持napi的网卡驱动必须提供轮询方法poll。

2、非napi的内核接口为netif_rx，napi的内核内核接口为napi_schedule。

3、非napi适应共享的CPU队列softnet_data->input_pkt_queue，而napi使用设备内存。



# 代码分析

1、NAPI对应的数据结构。

看注释说，类似tasklet。

```
struct napi_struct {
  struct list_head poll_list;
  ulong state;
  int weight;
  uint gro_count;
  int (*poll)(struct napi_struct *, int);
  struct net_device *dev;
  struct sk_buff *gro_list, *skb;
  struct hrtimer timer;
  struct list_head dev_list;
  struct hlist_head napi_hash_node;
  uint napi_id;
};
```

2、初始化。

在net/core/dev.c里的netif_napi_add函数。

这个在驱动的probe函数里调用。

```
for (i = 0; i < MAX_DMA_CHAN; i++) {
		if (IS_TX(i))
			netif_napi_add(dev, &priv->ch[i].napi,
				ltq_etop_poll_tx, 8);
		else if (IS_RX(i))
			netif_napi_add(dev, &priv->ch[i].napi,
				ltq_etop_poll_rx, 32);
		priv->ch[i].netdev = dev;
	}
```



3、调度。

是napi_schedule()函数。在中断处理函数里做。

```
static irqreturn_t
ltq_etop_dma_irq(int irq, void *_priv)
{
	struct ltq_etop_priv *priv = _priv;
	int ch = irq - LTQ_DMA_CH0_INT;

	napi_schedule(&priv->ch[ch].napi);
	return IRQ_HANDLED;
}
```



4、轮询方法。

就是注册进去的。ltq_etop_poll_tx这个。

```
netif_napi_add(dev, &priv->ch[i].napi,
				ltq_etop_poll_tx, 8);
```



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

# NAPI和非NAPI处理流程区别

![](/images/napi流程.png)

# napi和netpoll区别

netpoll主要目的是让内核在网络和io子系统还不能使用的时候，依然可以收发数据。

主要用在网络控制台net console和远程内核调试里。

实现netpoll函数，主要是要实现kernel里的poll_controller函数。

netpoll可以绕过协议栈去收取skb。可以在debug的时候使用。







# 参考资料

1、NAPI 技术在 Linux 网络驱动上的应用和完善

https://www.ibm.com/developerworks/cn/linux/l-napi/

2、NAPI之（一）——原理和实现

https://blog.csdn.net/hejin_some/article/details/72722555

3、6410 linux DM9000收包机制

https://blog.csdn.net/chengwenyang/article/details/52187715

4、napi和netpoll区别

http://www.360doc.com/content/11/1023/09/7975692_158366329.shtml

5、Linux NAPI/非NAPI 网卡驱动部分

https://blog.csdn.net/hui6075/article/details/51236203

6、数据包接收系列 — NAPI的原理和实现

https://blog.csdn.net/zhangskd/article/details/21627963