---
title: Linux之driver、device对接过程
date: 2018-03-06 15:17:06
tags:
	- Linux

---



以enc28j60为例，分析一下driver和device的对接过程。

1、我们insmod enc28j60.ko。这个时候。

会调用到我们驱动里用`__init`修饰的init函数。

spi_register_driver注册的时候，会通过name去查找有没有device存在，存在的话，就会调用driver的probe函数。

```
而device是怎么存在的呢？之前的做法就是在bsp文件里，用spi_board_info定义的结构体得到的。
所以在实际操作上来说，就是编译内核的时候，就要知道你的spi总线上要接什么设备了。
如果我要增加一个spi设备到系统里，就要把内核重新编译？
不用。使用了设备树之后，就不用了。
以树莓派为例。你配dtoverlay=enc28j60，重启就可以了。
有了设备树，kernel会把设备树里的设备先系统启动开始的地方都建立设备的。
```

```
是不是可以这样理解：
1、device先于driver存在。
2、不管是否加载driver，device的结构体一定存在于系统中了。
```

probe函数是在driver和device绑定之后执行的。

具体的调用栈是这样的：

```
insmod enc28j60命令
	enc28j60_init函数
		spi_register_driver
			driver_register
				bus_add_driver
					driver_attach
						bus_for_each_dev
							__driver_attach
								driver_match_device
								driver_probe_device
									really_probe
										drv->probe(dev);就是这里调用的。
```

