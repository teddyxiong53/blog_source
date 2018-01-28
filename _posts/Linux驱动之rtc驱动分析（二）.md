---
title: Linux驱动之rtc驱动分析（二）
date: 2018-01-28 17:26:56
tags:
	- Linux驱动
	- rtc

---



在Linux驱动之rtc驱动分析（一）里，我们已经简单把设计的6个c文件过了一遍。

现在我们来看第二遍。这次我们的目标是把platform_driver_register这种接口一直跟下去读透。

#platform_driver_register

1、bus类型赋值为platform_bus_type。

2、把函数指针拷贝下来。如果没有给，就用默认的platform_drv_probe这一套。

3、调用drivers/driver.c里的driver_register函数。



# driver_register

1、driver_find("s3c-rtc", platform_bus_type )

2、put_driver

3、bus_add_driver，就是把驱动加到bus上去。

4、driver_add_groups。



# platform_bus_init

调用树是这样的。

```
start_kernel
	-- rest_init
		-- kernel_init
			-- do_basic_setup
				-- driver_init
					-- platform_bus_init
```

1、device_register( platform_bus)。平台总线是定义成一个struct device的。不过platform_bus定义的时候，只有init_name给了个“platform”。其他属性都没有定义。

2、bus_register(platform_bus_type)。



# platform_driver结构体

1、5个函数指针。

2、struct device_driver driver。这个相当于是它的父类。

3、struct platform_device_id *id_table。有用的是里面的name成员，在match的时候有用。



这些内容都集中在drivers/base目录。这个是很重要很基础的东西。

```
1、platform.c
2、driver.c
```



我们只写了platform_driver结构体，platform_device在哪里写呢？

在arch/arm/mach-s3c24xx里的mach-at2440evb.c里写的。

```
static struct platform_device *at2440evb_devices[] __initdata = {
	&s3c_device_ohci,
	&s3c_device_wdt,
	&s3c_device_adc,
	&s3c_device_i2c0,
	&s3c_device_rtc,
	&s3c_device_nand,
	&s3c_device_sdi,
	&s3c_device_lcd,
	&at2440evb_device_eth,
};

```



# drivers/base/platform.c

总的来说，这里面的函数分为3部分：

1、platform_device_xxx。这部分用得不多。

2、platform_driver_xxx。这部分用得多。

3、platform_pm_xx。不常用。

函数接口：

1、platform_get_resource。常用接口。s3c-rtc.c里有用这个来get mem寄存器区域。

platform_get_irq是对这个函数是简单封装。把resource类型默认为IRQ的。

platform_get_resource_byname、platform_get_irq_byname都是变种。

2、platform_add_devices。常用接口。在mach-at2440evb.c里使用。

把定义的platform_device[]添加到内核。

对应的接口还有platform_device_add，这个是一个一个地添加。删除的是platform_device_del。

3、platform_device_put。销毁平台设备。不常用。

```
rtc_sysfs_add_device
	device_create_file
		sysfs_create_file
			sysfs_add_file
				sysfs_add_file_mode
					
```



```
start_kernel
	vfs_caches_init(totalram_pages);
		mnt_init
			sysfs_init
				sysfs_dir_cachep = kmem_cache_create
					
```

