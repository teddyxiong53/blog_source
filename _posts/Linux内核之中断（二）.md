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



# 参考资料

1、https://blog.csdn.net/melo_fang/article/details/78224326

2、http://www.wowotech.net/irq_subsystem/request_threaded_irq.html



