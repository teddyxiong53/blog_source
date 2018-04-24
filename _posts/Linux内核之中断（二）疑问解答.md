---
title: Linux内核之中断（二）
date: 2018-03-31 16:02:10
tags:
	- Linux内核

---



#request_threaded_irq接口的使用

一般我们都是用request_irq，request_irq是对request_threaded_irq的封装，把thread_fn设置为NULL的。

```
int request_threaded_irq(unsigned int irq, irq_handler_t handler,
			 irq_handler_t thread_fn, unsigned long irqflags,
			 const char *devname, void *dev_id)
```

##什么时候使用request_threaded_irq？



##有什么需要注意的？

1、一定要加上IRQF_ONESHOT。表示在thread_fn处理过程中，不会触发下一次。这是保证功能正常。

# local_irq_enable的实现

```
local_irq_enable
	raw_local_irq_enable
		arch_local_irq_enable
			

static inline void arch_local_irq_enable(void)
{
	asm volatile(
		"	cpsie i			@ arch_local_irq_enable"
		:
		:
		: "memory", "cc");
}
```

就是把所有的中断都禁止了。

# irq_enter做了什么

看注释里写的是，进入一个中断环境。



# ksoftirqd内核线程

每一个CPU核心，都有一个ksoftirqd来辅助处理中断。

当内核出现大量的软中断的时候，ksoftirqd就会进行辅助处理。

## 引入ksoftirqd的原因

对于软中断，内核会选择在几个特殊的时机进行处理。

最常见的，就是在中断处理程序返回的时候。

但是有时候，中断的频率会特别高。

而且更加要命的是，某些特殊的处理程序，还会自动重复触发。

这就带来一个严重的问题，就是用户空间程序得不到CPU运行时间。

在桌面程序上的表现就是，下载的时候，你的应用会不响应。

这肯定是无法接受的。

但是，也不能直接采用不立即处理的方式。

那怎么办呢？

实现的解决方案是这样的，不立即处理**重新触发**的软中断。**也就是不允许软中断嵌套。**

作为改进，当出现大量的软中断的时候，内核会唤醒一组ksoftirqd来处理。

ksoftirqd的优先级是19，就是最低的优先级。



ksoftirqd作为一个内核线程，它和中断的底半部的执行环境是不一样的。

那他为什么可以完成软中断呢？

重点分析do_softirq函数。

```
asmlinkage void do_softirq(void)
{
    __u32 pending;
   unsigned long flags;
   // 这个函数判断，如果当前有硬件中断嵌套，或者软中断被禁止时，则马上返回。在这个入口判断主要是为了与 ksoftirqd 互斥。
   if (in_interrupt())
       return;
   // 关中断执行以下代码
   local_irq_save(flags); 
   // 判断是否有 pending 的软中断需要处理。
   pending = local_softirq_pending();
   // 如果有则调用 __do_softirq() 进行实际处理
   if (pending)
       __do_softirq();
   // 开中断继续执行
   local_irq_restore(flags);
}
```

软中断频繁的判断标准是10次。

```
	pending = local_softirq_pending();
	if (pending && --max_restart)
		goto restart;

	if (pending)//如果连续处理了10个软中断，说明现在软中断很频繁，所以要唤醒ksoftirqd来处理。
		wakeup_softirqd();
```



# 软中断和tasklet

1、tasklet基于软中断实现。

2、软中断是静态的，编译内核时就确定了。

3、tasklet是动态的，可以在insmod的时候注册。

软中断必须是可重入的，所以编写难度更大，一般建议使用tasklet。内核已经对tasklet的处理进行了更加严格的保护，保证了同类型的tasklet总是被串行地执行。这样主要是为了降低开发难度。

# 参考资料

1、https://blog.csdn.net/melo_fang/article/details/78224326

2、http://www.wowotech.net/irq_subsystem/request_threaded_irq.html

3、ksoftirqd内核线程

https://blog.csdn.net/suncess1985/article/details/7343490

4、Linux系统中的知名内核线程(1)——ksoftirqd和events

这篇文章对软中断讲解比较好。

http://blog.chinaunix.net/uid-28541347-id-5716840.html