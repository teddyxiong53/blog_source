---
title: Linux内核之中断（一）
date: 2018-03-24 10:13:24
tags:
	- Linux内核
typora-root-url: ..\
---



这个打算写一个系列文章来梳理内核的中断子系统。

在内核驱动的编写中，中断是非常重要的一块。中断处理是否得当，对于系统的稳定性和效率都有很大影响。

只有深刻理解了中断子系统，才能用合理的方法包含临界区资源，正确使用tasklet等方法来处理中断。



# 中断涉及的硬件

中断涉及了3个硬件：

1、CPU。

2、外设。外设的中断信号发给中断控制器。

3、中断控制器。可以控制中断的开关，优先级等。arm架构下，以前用的多的是VIC。进入多核时代后，GIC应用比较多。



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



# 通用中断子系统

架构图是这样的。

![Linux内核之中断-图1](/images/Linux内核之中断-图1.png)





中断子系统内部定义了几个重要的数据结构，这些数据结构的各个字段控制或影响着中断子系统和各个irq的行为和实现方式。例如：irq_desc，irq_chip，irq_data，irqaction，等等。其中 irq_desc[NR_IRQS]数组是linux内核中用于维护IRQ资源的管理单元，它记录了某IRQ号对应的流控处理函数，中断控制器、中断服务程序、IRQ自身的属性、资源等，是内核中断子系统的一个核心数组，中断驱动接口“request_irq()”就是通过修改该数组以实现中断的注册。

## 硬件封装层

所有跟CPU架构有关的内容都在这里抽象统一。

这部分的主要工作是：

这一层的结构体是：

struct irq_chip

```
除了name和flag之外，全部都是函数指针。
```

是对中断控制器的接口抽象。





## 中断通用逻辑

这一层实现了对中断系统几个重要数据的管理。并提供了几个辅助管理函数。

还实现了中断线程的实现和管理。

共享中断、嵌套中断也在这里处理。

## 中断流控层

所谓中断流控，就是指合理并且正确地处理连续发生的中断。

例如，一个中断在处理的时候，下一个中断来了，应该怎么安排。

这一层实现了跟硬件无关的流控。

asm_do_IRQ就是这一层的。



## 驱动程序api

这一层就是封装接口给驱动程序用的。

就是request_irq这一套接口。

```
驱动开发者使用irq，只需要包含linux/interrupt.h就好了。
里面主要就是：
1、request_irq和free_irq。
2、tasklet结构体和函数。
```

另外，还有一个setup_irq可以用。这个传递参数，是都整合到一个结构体irqaction里了。

跟request_irq一样，都是调用到`__setup_irq`函数。

```
static struct irqaction samsung_clock_event_irq = {
	.name		= "samsung_time_irq",
	.flags		= IRQF_TIMER | IRQF_IRQPOLL,
	.handler	= samsung_clock_event_isr,
	.dev_id		= &time_event_device,
};
```



struct irq_desc。中断描述符，整个中断子系统都是以这个为中心的。



# 看mini2440里对中断如何处理

```
1、bsp里的init_irq指向s3c2440_init_irq
2、s3c2440_init_irq在drivers/irqchip/irq-s3c2440.c里。
	这里面就是初始化了2个中断控制器。s3c_intc[0]和s3c_intc[1]
	s3c_intc[0]指向基本的。
	s3c_intc[1]指向二级的。

```



串口中断是如何处理的？

看看mini2440里的这些中断都是在哪里注册进去的。中断处理函数做了些什么。

```
/dev/input # cat /proc/interrupts 
           CPU0       
 29:    2140301       s3c  13 Edge      samsung_time_irq
 32:          0       s3c  16 Edge      s3c2410-lcd
 43:          0       s3c  27 Edge      s3c2440-i2c.0
 55:          0   s3c-ext   7 Edge      eth0
 56:          0   s3c-ext   8 Edge      Button 1
 59:          0   s3c-ext  11 Edge      Button 2
 61:          0   s3c-ext  13 Edge      Button 3
 62:          0   s3c-ext  14 Edge      Power
 63:          0   s3c-ext  15 Edge      Button 5
 74:        148  s3c-level   0 Edge      s3c2440-uart
 75:        375  s3c-level   1 Edge      s3c2440-uart
 87:          0  s3c-level  13 Edge      s3c2410-wdt
Err:          0
```

总共12个中断。

## samsung_time_irq

这个中断号是29 。

是在bsp里的init_time回调做的。是系统tick中断。

## s3c2410-lcd

```
./arch/arm/mach-s3c24xx/include/mach/irqs.h:43:#define IRQ_LCD         S3C2410_IRQ(16)      /* 32 */
```

这个是平台设备的resource里注册进去的。

加载fb的驱动的时候，

```
./drivers/video/fbdev/s3c2410fb.c:1106:         .name   = "s3c2410-lcd",
```

在probe里会request_irq的。

在drivers/video/fbdev/s3c2410fb.c里。

```
ret = request_irq(irq, s3c2410fb_irq, 0, pdev->name, info);
```

## s3c2440-i2c.0

在drivers/i2c/busses/i2c-s3c2410.c里。

```
ret = devm_request_irq(&pdev->dev, i2c->irq, s3c24xx_i2c_irq, 0,
				dev_name(&pdev->dev), i2c);
```

## eth0



## Button 1

这些都是在gpio-keys.c里。



## s3c2440-uart

```
./drivers/tty/serial/samsung.c:2346:            .name           = "s3c2440-uart",
```

```
static struct platform_driver samsung_serial_driver = {
	.probe		= s3c24xx_serial_probe,
	.remove		= s3c24xx_serial_remove,
	.id_table	= s3c24xx_serial_driver_ids,
	.driver		= {
		.name	= "samsung-uart",
		.pm	= SERIAL_SAMSUNG_PM_OPS,
		.of_match_table	= of_match_ptr(s3c24xx_uart_dt_match),
	},
};
```



```
static int s3c24xx_serial_init_port(struct s3c24xx_uart_port *ourport,
				    struct platform_device *platdev)
	ret = platform_get_irq(platdev, 1);
	if (ret > 0)
		ourport->tx_irq = ret;
```





# 为什么说tasklet是中断上下文？

因为tasklet本质上是软中断，软中断不能打断软中断。

也就是说，以网络收包为例，当前收包没有处理完，是不能收下一个包的。





```
从bsp开始看中断相关。
drivers/irqchip/irq-s3c24xx.c

struct irq_chip s3c_irq_chip
struct irq_chip s3c_irq_level_chip 
struct irq_chip s3c_irqext_chip 
struct irq_chip s3c_irq_eint0t4

这几种irq_chip，各有什么区别呢？
以s3c_irqext_chip这个为例，看看是如何被系统处理的。
irq_set_chip_and_handler(virq, &s3c_irqext_chip, handle_edge_irq);
每一种irq_chip对应一个特别的handler。

s3c2440_init_irq
	1、s3c_intc[0] = s3c24xx_init_intc(NULL, &init_s3c2440base[0], NULL,0x4a000000);
		这里做了这些事情：
		1）kzmalloc了一个s3c_irq_intc。初始化。
		2）intc->domain = irq_domain_add_legacy
			这里牵涉到s3c24xx_irq_ops
				irq_ops可以做：map和xlate。
		3）set_handle_irq(s3c24xx_handle_irq);
			s3c24xx_handle_irq这就是注册给了全局函数变量handle_arch_irq
			这会在arch/arm/kernel/entry-armv.S里调用。
				.macro	irq_handler
					ldr	r1, =handle_arch_irq
					mov	r0, sp
					badr	lr, 9997f
					ldr	pc, [r1]
			s3c24xx_handle_irq本身做的事情是：
				handle_domain_irq
					generic_handle_irq
						desc->handle_irq(desc);//这个就是request_irq注册进来的了。
							//不是，request_irq注册的在irqaction->handle。
							//这里这个是通用的，handle_edge_irq这种。
							//handle_edge_irq这种函数里，就调用芯片的ack，就是清中断。
	2、注册外部中断。也是子中断。
	s3c24xx_init_intc(NULL, &init_eint[0], s3c_intc[0], 0x560000a4);
	3、s3c_intc[1] = s3c24xx_init_intc(NULL, &init_s3c2440subint[0],s3c_intc[0], 0x4a000018);
		这个是做子中断的注册。
```



# 参考资料

1、

http://www.wowotech.net/linux_kenrel/interrupt_subsystem_architecture.html

2、

https://blog.csdn.net/droidphone/article/details/7467436

3、linux驱动之中断处理过程C程序部分

https://www.cnblogs.com/amanlikethis/p/6941666.html?utm_source=itdadao&utm_medium=referral

4、Linux中断（interrupt）子系统之一：中断系统基本原理

https://blog.csdn.net/droidphone/article/details/7445825

5、Linux的IRQ中断子系统分析

这篇文章特别好。

http://blog.sina.com.cn/s/blog_c91863e60102w48u.html