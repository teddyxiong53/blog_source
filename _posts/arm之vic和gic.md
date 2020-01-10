---
title: arm之vic和gic
date: 2018-03-30 11:16:47
tags:
	- arm

---



vic和gic是arm架构下的两种中断控制器。

另外，还有一个nvic。

这三者是什么关系？



多核系统只能用gic。因为只有gic才支持多核。

一般的芯片都会使用vic，因为是向量中断处理器，处理中断的速度非常快。

nvic是对vic的改进，支持中断嵌套。



GIC的全称为general interrupt controller,
主要作用可以归结为：

接受硬件中断信号，并进行简单处理，通过一定的设置策略，分给对应的CPU进行处理。

这里面把硬件中断源分为了3类：
SPI:这是shared peripheral interrupt , 这是常见的外部设备中断，也定义为共享中断，比如按键触发一个中断，手机触摸屏触发的中断，共享的意思是说

可以多个Cpu或者说Core处理，不限定特定的Cpu。**一般定义的硬件中断号范围31~1019.**

**PPI:这里指的是private peripheral interrupt，16~31，私有中断**
私有中断，为什么这样说呢，这些中断一般是发送给特定的Cpu的，比如每个Cpu有自己对应的Physicaltimer,产生的中断信号就发送给这个特定的cpu进行处理。

**SGI:这个中断有些同学遇到的比较少，software generatedinterrupt，软件出发产生的中断，中断号范围0~15，也就是最前的16个中断。**

如果在X86平台上做过开发工作的同学可能有影响，其实这就是相当于IPI，简单的说Cpu_1要给Cpu_2发送特定信息，比如时间同步，全局进程调度信息，就通过软件中断方式，目标Cpu接受到这样的中断信息，可以获取到信息是哪个Cpu发送过来的，具体的中断ID是哪个数字，从而找到对应处理方式进行处理。

在现在市面上看到的手机或者其它设备产品中，既有老的V2版本的中断控制器，也有比较新的V3结构的，而且是在不断向后演进，我们有必要依照新的V3的来说明，毕竟，这是后面的趋势，比如现在大家现在可以看到GIC_V4的介绍了。

# 参考资料

1、Arm Generic Interrupt controler(通用中断GIC)

https://wenku.baidu.com/view/7d9318d75022aaea998f0f2b.html?rec_flag=default&mark_pay_doc=2&mark_rec_page=1&mark_rec_position=3&mark_rec=view_r_1&clear_uda_param=1

2、中断控制器GIC、VIC和NVIC的区别和联系，以及他们主要用于那些场合？？？

http://www.embsky.com/forum.php?mod=viewthread&tid=267

3、arm GIC介绍之一

这个是一个系列，写得很好。

https://blog.csdn.net/sunsissy/article/details/73791470