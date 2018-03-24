---
title: Linux内核之中断（一）
date: 2018-03-24 10:13:24
tags:
	- Linux内核

---



这个打算写一个系列文章来梳理内核的中断子系统。

在内核驱动的编写中，中断是非常重要的一块。中断处理是否得当，对于系统的稳定性和效率都有很大影响。

只有深刻理解了中断子系统，才能用合理的方法包含临界区资源，正确使用tasklet等方法来处理中断。



# 中断涉及的硬件

中断涉及了3个硬件：

1、CPU。

2、外设。

3、GIC。中断控制器。



CPU的中断入口位置

arm的中断向量表有2种选择，一个是低端向量（放在0x0的位置），一种是高端向量（放在0xFFFF 0000处）。就寄存器的一个bit来控制的。

linux选择了高端向量的模式。



内核启动中断子系统的过程

1、early_trap_init，完成中断向量的拷贝和重定位的工作。

2、early_irq_init。完成与具体硬件无关的通用逻辑代码的初始化。进行了irq_desc结构体的内存申请。该函数最后调用arch_early_irq_init。不过arm架构下的这个是空函数。

3、init_IRQ。这个会调用bsp里machine结构体里的init_irq回调。

我们看一下2.6.35里的s3c2410的里面是怎么做的。



# 参考资料

1、

http://www.wowotech.net/linux_kenrel/interrupt_subsystem_architecture.html

2、

https://blog.csdn.net/droidphone/article/details/7467436