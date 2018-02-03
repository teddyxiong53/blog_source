---
title: rt-thread（八）中断系统分析
date: 2018-02-03 14:41:32
tags:
	- rt-thread

---



看看如何接管芯片的中断的。

1、入口是rt_hw_interrupt_init。这个函数在系统的最前面调用。

```
1、rt_hw_vector_init。这个就是指定到最前面。
2、把isr_talbe清零。这个表的长度是96，有个宏IRQ_PBA8_GIC_START是32，就认为是从32号开始吧。64个，就是到96结束。这么理解先。看门狗中断是33号。timer中断是35号这样。
	这个isr-table的结构体下面再分析。很重要。
3、gic_dist_base初始化。gic是通用中断控制器。dist代表分发。这个地址是0X1E00 1000
4、gic_cpu_base初始化。这个地址是0x1E00 0100
```

2、rt_hw_interrupt_install。这个是提供给其他模块、驱动使用的接口。

```
就把传递进来的handler、param赋值到isr_table里。
```

我们就看rt_hw_timer_init里是怎么做的。

```
    rt_hw_interrupt_install(IRQ_PBA8_TIMER2_3, rt_hw_timer_isr, RT_NULL, "tick");
    rt_hw_interrupt_umask(IRQ_PBA8_TIMER2_3);
```

这样，就把中断注册到系统里去了。

3、现在看看中断产生后的处理流程。

中断就是看isr_table被谁用到了。我们依次搜索。找到对应的调用流程是这样的：

```
1、ldr pc, _vector_irq。产生中断后，首先肯定是到vector里找到irq的处理。
2、在start_gcc.S里。
vector_irq:
    stmfd   sp!, {r0-r12,lr}

    bl      rt_interrupt_enter
    bl      rt_hw_trap_irq 
    bl      rt_interrupt_leave
3、rt_hw_trap_irq。就是这个在处理。
	1）先拿到中断号。
	2）调用对应的注册的函数进行处理。
```

其实也并不复杂。



