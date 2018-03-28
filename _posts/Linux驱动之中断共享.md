---
title: Linux驱动之中断共享
date: 2018-03-28 12:47:44
tags:
	- Linux驱动

---



假设有一个人，加载了模块test1.ko，申请了中断EINT1，但是我不知道，我也写了一个test2.ko，里面也申请了这个中断。

如果没有进行中断共享设置，那么就会报Device or resource busy。

这时候怎么办呢？一个办法是把test1.ko卸载掉，但是这样一般是不妥当的。

还能怎么办？共享。

让两个模块在request_irq的时候，都加上IRQF_SHARED。

但是如果直接这样写，还是不行的。

因为中断来了，到底算是谁的呢？内核如何进行分辨呢？

还差点东西。

我们看request_irq的原型：

```
request_irq(unsigned int irq, irq_handler_t handler, unsigned long flags,
	    const char *name, void *dev)
```

最后有个void *dev参数。可以在注册的时候传递进去。可以是一个int数。

共享一个中断的处理程序会形成一个链表，都会被调用到的。

共享，必须设置devid，不然直接返回错误。

```
if ((irqflags & IRQF_SHARED) && !dev_id)
		return -EINVAL;
```



其实，我还是没有弄清楚，为什么要这么做。

我在LDD3里的第10章找到一些解释。

中断冲突几乎是pc系统的同义词。

以前，在pc上的irq线不能服务多个设备，而且数量还不够。

现在的硬件已经在设计上支持了中断共享。

linux内核支持在所有总线上使用共享中断。



有这么几个注意事项：

1、void *dev必须唯一。

2、在中断处理函数里，不能disable这个中断。

3、必须检测中断标志。



# 参考资料

1、

https://www.cnblogs.com/sky-heaven/p/5633093.html

