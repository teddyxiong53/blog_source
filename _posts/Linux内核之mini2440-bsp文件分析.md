---
title: Linux内核之mini2440 bsp文件分析
date: 2018-04-07 14:28:35
tags:
	- Linux内核

---



这4个函数，调用的位置和先后顺序是怎样的？

```
.map_io		= mini2440_map_io,
.init_machine	= mini2440_init,
.init_irq	= s3c2440_init_irq,
.init_time	= mini2440_init_time,
```

1、map_io是非常底层的，所以最靠前。是显式调用的。

调用栈是：

```
start_kernel
	setup_arch：这个在非常靠前的位置。很基础的函数。
		paging_init
			devicemaps_init
				if (mdesc->map_io)
					mdesc->map_io();
```
这个函数里做了什么？

```
mini2440_map_io里做了什么。
1、初始化io和CPU。
	1）建立静态的映射。对gpio、irq、memctl、uart。
2、初始化串口。
3、设置时钟源。
```
2、init_irq

调用栈：

```
start_kernel
	init_IRQ：大概在中间位置。
		machine_desc->init_irq();
```

做了什么？

```
初始化中断芯片irq_chip等内容。
```

3、init_time

```
start_kernel
	time_init：在irq的后面。
		machine_desc->init_time();
```

做了什么

```
1、初始化时钟频率为12M。
```



4、init_machine

调用栈：

```
init_machine是通过arch_initcall调用的。是到后面的内核线程里才调用的，比较靠后。
调用栈是：
start_kernel
	rest_init在最后面了。
		kernel_init
			kernel_init_freeable
				do_basic_setup
					do_initcalls();
```
这个函数里做了？

```
1、注册各种平台设备的platdata。
2、i2c_register_board_info。
3、platform_add_devices。这里才产生平台设备的节点。
```



# vexpress ca9x4

用2.6版本的看一下，4.4的，已经没有什么内容，全部挪到设备树里去了。

看一下这个，主要是方便梳理思路，三星的封装层数太多了。看不清本来的样子了。

