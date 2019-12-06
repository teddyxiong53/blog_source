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



看驱动的。

梳理驱动的方法是，从mach-mini2440.c里看platform_device，找到name属性。

然后肯定有一个对应的platform_driver，那么属性的值，跟platform_device是一样的。



# led

使用了Linux的led子系统。了解一下即可。

# 按键

```
从platform_device看name属性：
.name		= "gpio-keys",
在源代码下grep gpio-keys。
可以找到是通用驱动框架的。
./drivers/input/keyboard/gpio_keys.c
```

看gpio_keys.c注释的第一行写着：

```
Driver for keys on GPIO lines capable of generating interrupts.
```

适合中断方式。



音频驱动

这个不在driver目录下，而是在sound目录下。





参考资料

1、

