---
title: linux的网络设备驱动分析
date: 2016-12-03 14:06:22
tags:
	- linux
	- 网络
---
网络设备是linux里与字符设备、块设备并列的3种设备类型之一。
与字符设备和块设备不同，网络设备在/dev目录下没有节点。网络设备不太符合“一切都是文件”的思想。


从全局来看，Linux对网络驱动的框架体系设计如下，分为4层。：
```
-------------------
协议接口层。这个就是跟tcpip对接的那一层，提供一个发送一个接收函数给tcpip调用。
-------------------
设备接口层。核心就是net_device这个结构体。
-------------------
设备驱动实现层。这个就是写驱动的时候，主要做的事情，在这里实现一堆函数，通过net_device注册到内核里。
-------------------
媒介层。
-------------------
```
# 1. 协议接口层
核心数据结构是`sk_buff`。是socket buffer的意思。
这个结构体可以叫做Linux网络子系统的中枢神经，网络数据在各层之间传递全靠它了。
针对这个结构体，Linux提供一些接口来进行操作，如下：
分配：`alloc_skb`和`dev_alloc_skb`。对应的释放函数`kfree_skb`和`dev_kfree_skb`，以及`dev_kfree_skb_irq`和`dev_kfree_skb_any`。
驱动里建议使用以dev开头的接口。
另外还有修改的接口。
`skb_put`：这个是往tail上增加数据。
`skb_push`：这个是往head上增加数据。
`skb_reserve`：这个是把数据整个往tail的方向挪动一段，在前面腾出一些空间出来。

# 2. 设备接口层
这一层的核心结构体是net_device。
net_device实现了对所有网络设备的抽象。达到对上提供统一接口的目的。
结构体内容较多，定义的代码有300行左右。我们总结重要的如下：
1. 全局信息类。
有个name字符数组。
2. 硬件信息类。
共享内存的起始和结束地址、中断号。
3. 接口信息类。
就是包头长度，MTU值，设备地址这些。
4. 设备操作函数。
5. 其他。


# 3. 以dm9000为例来分析

入口函数，非常简单如下：
```
static int __init
dm9000_init(void)
{
	printk(KERN_INFO "%s Ethernet Driver, V%s\n", CARDNAME, DRV_VERSION);

	return platform_driver_register(&dm9000_driver);
}

static void __exit
dm9000_cleanup(void)
{
	platform_driver_unregister(&dm9000_driver);
}
```
以太网设备属于平台设备，所以其初始化和去初始化函数，就是平台设备的注册和反注册。
入口函数涉及的结构体是`platform_driver`，定义一个变量如下：
```
static struct platform_driver dm9000_driver = {
	.driver	= {
		.name    = "dm9000",
		.owner	 = THIS_MODULE,
		.pm	 = &dm9000_drv_pm_ops,
	},
	.probe   = dm9000_probe,
	.remove  = __devexit_p(dm9000_drv_remove),
};
```
所以需要实现的总共是4个函数：
probe、remove、suspend、resume。
probe相当于初始化函数，我们重点分析一下。
probe函数原型是：`int (*probe)(struct platform_device *);`。`platform_driver`和`platform_device`是如何关联起来的呢？

过程是这样的：`platform_driver`里面有一个`device_driver`，`device_driver`有2个需要注意的成员变量name和owner。写驱动的时候，一般是把owner写出`THIS_MODULE`。
然后在`platform_device`的name与`device_driver`的name值一样的时候，就被关联起来了。






