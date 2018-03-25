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

# 中断号

在内核里，对于一个中断有2个id来进行标识。

1、irq number。这个跟硬件无关。可以理解为一个索引值。

2、硬件中断号。

对于驱动工程师，我们看到的视角跟CPU是一样的，我们只希望得到一个irq number，而不是具体的硬件中断号。

这里面就需要中断子系统来建立这2个id的映射关系。

如果系统里只有一个中断控制器，那么irq number和硬件中断号就一一映射的关系。

随着系统的复杂度增加，外设中断的增加，系统中可能需要多个中断控制器进行级联。

于是就产生了irq domain的概念。

irq number和硬件中断号的映射有3种：

1、线性映射。

是用irq_domain_add_linear接口来做的。

前提是：硬件中断号比较连续，而且数值不是很大。因为就是建立了一个全局数组来对应的，如果数字很大，数组就很大了。

```
struct irq_desc irq_desc[NR_IRQS];
```



2、radix tree映射。

只有powerpc和mips需要这种。

3、不映射。也是powerpc的可能用到。



request_irq的过程

```
request_irq
	request_threaded_irq
		desc = irq_to_desc(irq);
		__setup_irq(irq, desc, action);
			
```





看mini2440的中断注册过程。

```
start_kernel
	s3c2440_init_irq
		s3c24xx_init_intc 调用了2次，注册2个s3c_intc，一个是普通中断，一个是extint。
			irq_domain_add_legacy，这里把s3c24xx_irq_ops带进去了。
```

一个中断发生后，调用的流程是：

```
asm_do_IRQ 这个就是在中断向量那里。
	handle_IRQ
		__handle_domain_irq
			generic_handle_irq
				generic_handle_irq_desc
					desc->handle_irq(desc) 这个就是request_irq注册进来的了。
```

从System.map文件里，可以看到，中断后，就是转到asm_do_IRQ里了。

```
   25 c0008214 T cpu_arm920_reset
   26 c0008238 T __idmap_text_end
   27 c0009000 T __exception_text_start
   28 c0009000 T __hyp_idmap_text_end
   29 c0009000 T __hyp_idmap_text_start
   30 c0009000 T asm_do_IRQ
   31 c0009018 T do_undefinstr
   32 c0009248 T handle_fiq_as_nmi
   33 c0009274 T do_DataAbort
   34 c0009328 T do_PrefetchAbort
   35 c00093c0 T s3c24xx_handle_irq
```

# 为什么说tasklet是中断上下文？





# 参考资料

1、

http://www.wowotech.net/linux_kenrel/interrupt_subsystem_architecture.html

2、

https://blog.csdn.net/droidphone/article/details/7467436

3、linux驱动之中断处理过程C程序部分

https://www.cnblogs.com/amanlikethis/p/6941666.html?utm_source=itdadao&utm_medium=referral