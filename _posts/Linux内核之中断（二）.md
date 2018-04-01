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



https://blog.csdn.net/melo_fang/article/details/78224326

http://www.wowotech.net/irq_subsystem/request_threaded_irq.html



1、