---
title: Linux内核之中断（一）
date: 2018-03-24 10:13:24
tags:
	- Linux内核
typora-root-url: ../
---



这个打算写一个系列文章来梳理内核的中断子系统。

在内核驱动的编写中，中断是非常重要的一块。中断处理是否得当，对于系统的稳定性和效率都有很大影响。

只有深刻理解了中断子系统，才能用合理的方法包含临界区资源，正确使用tasklet等方法来处理中断。



# 中断涉及的硬件

中断涉及了3个硬件：

1、CPU。

2、外设。外设的中断信号发给中断控制器。

3、中断控制器。可以控制中断的开关，优先级等。**arm架构下，以前用的多的是VIC。进入多核时代后，GIC应用比较多。**



CPU的中断入口位置

arm的中断向量表有2种选择，一个是低端向量（放在0x0的位置），一种是高端向量（放在0xFFFF 0000处）。就寄存器的一个bit来控制的。

**linux选择了高端向量的模式。**



内核启动中断子系统的过程

1、early_trap_init，**完成中断向量的拷贝和重定位的工作。**

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





中断子系统内部定义了几个重要的数据结构，

这些数据结构的各个字段控制或影响着中断子系统和各个irq的行为和实现方式。

例如：irq_desc，irq_chip，irq_data，irqaction，等等。

其中 irq_desc[NR_IRQS]数组是linux内核中用于维护IRQ资源的管理单元，

它记录了某IRQ号对应的流控处理函数，中断控制器、中断服务程序、IRQ自身的属性、资源等，

是内核中断子系统的一个核心数组，

中断驱动接口“request_irq()”就是通过修改该数组以实现中断的注册。

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



# arm linux的中断响应过程

1、当一个中断发生的时候，CPU切换到irq模式。

2、pc跳转到0x18，就是irq的中断入口。

```
	.macro	irq_handler
	get_irqnr_preamble r5, lr
1:	get_irqnr_and_base r0, r6, r5, lr
	movne	r1, sp
	@
	@ routine called with r0 = irq number, r1 = struct pt_regs *
	@
	adrne	lr, BSYM(1b)
	bne	asm_do_IRQ //这个函数在汇编里调用，实现是在C语言里。
```

看这个注释。

```
/*
 * do_IRQ handles all hardware IRQ's.  Decoded IRQs should not
 * come via this function.  Instead, they should provide their
 * own 'handler'
 */
asmlinkage void __exception asm_do_IRQ(unsigned int irq, struct pt_regs *regs)
{
```



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



## mini2440如何处理中断共享

发生中断的时候，内核并不判断共享中断线上的哪个设备发生了中断。

它会循环执行该中断号上注册的handler链表。

所以需要handler自己来判断是不是自己的中断。

2440里，是如何处理的呢？

我们知道，4到10号的外部中断，8到23号外部中断，分别共用了一个中断。

在arch/arm/mach-2410/include/mach里。

```
#define IRQ_EINT4t7    S3C2410_IRQ(4)	    /* 20 */
#define IRQ_EINT8t23   S3C2410_IRQ(5)


....
/* interrupts generated from the external interrupts sources */
#define IRQ_EINT4      S3C2410_IRQ(32)	   /* 48 */
#define IRQ_EINT5      S3C2410_IRQ(33)
#define IRQ_EINT6      S3C2410_IRQ(34)
#define IRQ_EINT7      S3C2410_IRQ(35)
#define IRQ_EINT8      S3C2410_IRQ(36)
#define IRQ_EINT9      S3C2410_IRQ(37)
```

4到7这些子中断，可以看到也是单独给分配了一个中断号了。

具体怎么处理的呢？

在arch/arm/plat-s3c24xx/irq.c里。

```
void __init s3c24xx_init_irq(void)
	set_irq_chained_handler(IRQ_EINT4t7, s3c_irq_demux_extint4t7);
	set_irq_chained_handler(IRQ_EINT8t23, s3c_irq_demux_extint8);
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



# 软中断

作为软中断，从内核同步的角度来说它有两个特点：

一是软中断总是和cpu绑定在一起的。

二是除了中断或是异常（一般内核太不会出现异常）没有什么东西能够抢占它。

因为和cpu绑定，软中断喜欢使用cpu变量，这样就不用考虑SMP的竞争，因为不会被其他软中断或是内核抢占，使得不用在嵌套上太过于小心。

一般而言，软中断是在中断的下半部分执行的，优先级大于进程。

不过大量的软中断会阻塞进程的正常进行。

因此内核有一个机制，软中断如果连续出现多次后就不再继续在中断下半部分执行软中断，而是将其放ksoftirqd内核线程中继续执行。

这个在代码里的表现就是，有2个地方调用了do_softirq函数。

一个是在`_local_bh_enable_ip`函数里，一个是在run_ksoftirqd函数里。

每一个CPU对应一个ksoftirqd内核线程。

内核线程跟中断底半部的执行环境是不同的。那么内核线程里是如何完成软中断的呢？

先看看绑定CPU的问题。



每个处理器都有一个这样的线程，名字为ksoftirqd/n，n为处理器的编号。

```
static DEFINE_PER_CPU(struct task_struct *, ksoftirqd);
```



```
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
  930   786 root     R     1676  0.1   2  4.0 top
    8     2 root     RW       0  0.0   3  0.8 [rcu_sched]
    1     0 root     S     1676  0.1   1  0.0 init
  786     1 root     S     1676  0.1   1  0.0 -/bin/sh
  782     1 root     S     1676  0.1   2  0.0 telnetd
  448     2 root     IW       0  0.0   3  0.0 [kworker/3:1]
    3     2 root     IW       0  0.0   0  0.0 [kworker/0:0]
  764     2 root     SW       0  0.0   3  0.0 [mmcqd/0]
  928     2 root     IW       0  0.0   2  0.0 [kworker/2:2]
  927     2 root     IW       0  0.0   2  0.0 [kworker/2:0]
    7     2 root     SW       0  0.0   0  0.0 [ksoftirqd/0]
  240     2 root     IW       0  0.0   0  0.0 [kworker/u8:3]
   68     2 root     IW       0  0.0   2  0.0 [kworker/u8:2]
   14     2 root     SW       0  0.0   1  0.0 [ksoftirqd/1]
  313     2 root     SW       0  0.0   3  0.0 [khungtaskd]
   13     2 root     SW       0  0.0   1  0.0 [migration/1]
   18     2 root     SW       0  0.0   2  0.0 [migration/2]
    2     0 root     SW       0  0.0   2  0.0 [kthreadd]
   10     2 root     SW       0  0.0   0  0.0 [migration/0]
   23     2 root     SW       0  0.0   3  0.0 [migration/3]
```





# request_threaded_irq

跟request_irq参数区别基本一致，多了一个irq_handler_t（request_irq函数只有一个，而本函数有2个）。

2个irq_handler_t函数指针，一个是上半部，一个是下半部。

上半部是在中断上下文。

下半部是在进程上下文。

2个函数指针，可以只有其中一个，看你的实际需求了。

如果只有上半部，不需要下半部，那么上半部的处理函数返回值就是IRQ_HANDLED，否则返回IRQ_WAKE_THREAD。

上半部举例：

```
static irqreturn_t xx_top_half(int irq, void *p) {
	return IRQ_WAKE_THREAD;
}
```

下半部举例：

```
static irqreturn_t xx_bottom_half(int irq, void *p) {
	return IRQ_HANDLED;
}
```



# kernel中断通知应用





参考资料

Linux驱动实践：中断处理函数如何【发送信号】给应用层？

https://cloud.tencent.com/developer/article/1922135

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

6、ksoftirqd内核线程是如何补充实现软中断功能的

https://blog.csdn.net/sdulibh/article/details/51453843

7、ARM+Linux中断系统详细分析

http://blog.chinaunix.net/uid-26215986-id-3333236.html

8、linux-3.4.2中断机制分析——asm_do_IRQ  

http://liu1227787871.blog.163.com/blog/static/205363197201281011450559/