---
title: Linux之软中断
date: 2018-03-08 17:22:38
tags:
	 - Linux

---



软中断是tasklet的基础。



## 原理

说原理，我们就要先说来由。

在之前的linux版本里，并没有软中断。说软中断，我们还是得先从中断说起。

一般来说，中断都不允许嵌套。嵌套后变得很复杂了。所以，实用的做法是不允许嵌套。

不允许嵌套，就是关闭中断。这个时间一定要短，不然就会错过一些中断。

但是中断往往处理并不快，怎么办？就有了top half和bottom half（简称BH）。

但是BH有2个缺点：

1、在任意时刻，系统只能有一个CPU执行BH代码。

2、BH函数不能嵌套。

这2个缺点，对于单CPU系统是没有关系的。但是在smp系统里，却非常致命。这样严格串行化的操作，没有发挥SMP的作用。

所以linux2.4内核就进行了扩展，增加了软中断的机制。

软中断跟smp两者密不可分。

软中断的设计一个重要原则就是：谁触发，谁执行。是的是各个CPU。



##数据结构的定义

软中断目前有10个。定义在include/linux/interrupt.h里。

```
enum
{
	HI_SOFTIRQ=0,
	TIMER_SOFTIRQ,
	NET_TX_SOFTIRQ,
	NET_RX_SOFTIRQ,
	BLOCK_SOFTIRQ,
	BLOCK_IOPOLL_SOFTIRQ,
	TASKLET_SOFTIRQ,
	SCHED_SOFTIRQ,
	HRTIMER_SOFTIRQ, /* Unused, but kept as tools rely on the
			    numbering. Sigh! */
	RCU_SOFTIRQ,    /* Preferable RCU should always be the last softirq */

	NR_SOFTIRQS
};
```

被这个全局变量管理。

```
static struct softirq_action softirq_vec[NR_SOFTIRQS];
```

## 软中断的注册

用open_softirq函数。

例如，网络系统注册了收发数据的软中断处理函数。

```
open_softirq(NET_TX_SOFTIRQ, net_tx_action);
open_softirq(NET_RX_SOFTIRQ, net_rx_action);
```

## 软中断的激活

```
typedef struct {
	unsigned int __softirq_pending;
#ifdef CONFIG_SMP
	unsigned int ipi_irqs[NR_IPI];
#endif
}  irq_cpustat_t;
```

smp系统里，每个cpu都有32个bit来维护本cpu的软中断是否激活。

激活的第一个时机是在irq_exit里。

```
void irq_exit(void)
{
	//...
	//条件是：1.不能在硬中断里，因为要等硬中断处理完。
	//2.不能在软中断里，因为软中断不能嵌套。
	if (!in_interrupt() && local_softirq_pending())
		invoke_softirq();
```

激活的第二个时机是在raise_softirq里。

网卡收包方式从非NAPI方式进化到NAPI方式，就充分体现了软中断的优点。

把收包任务最大限度地交给软中断处理。

激活的第三个时机是ksoftirqd。每个CPU都有一个ksoftirqd专门在软中断很多的时候来专门处理软中断。

## 软中断的核心处理函数

do_softirq。



所谓tasklet基于softirq，就是指的这个。

```
void __tasklet_schedule(struct tasklet_struct *t)
{
	unsigned long flags;

	local_irq_save(flags);
	t->next = NULL;
	*__this_cpu_read(tasklet_vec.tail) = t;
	__this_cpu_write(tasklet_vec.tail, &(t->next));
	raise_softirq_irqoff(TASKLET_SOFTIRQ);//激活一个软中断。
	local_irq_restore(flags);
}
```







# 参考文章

1、Linux软中断原理浅析

https://linux.cn/article-5431-1.html

2、linux软中断的实现原理

http://blog.csdn.net/liangjingbo/article/details/2817939