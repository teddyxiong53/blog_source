---
title: Linux内核之device代码文件分析
date: 2018-04-08 20:37:45
tags:
	- Linux内核

---

--

我们从device.h开始看。

# linux/device.h

1、包含了linux/ioport.h。

```
1、定义了struct resource。和相关的宏。
2、比较重要的函数，request_resource，devm_request_resource。
```

2、包含了linux/kobject.h。这个就不用说了。

3、包含linux/klist.h。这个跟普通的list有什么区别呢？专门写一篇文章分析。

4、包含arm/device.h。这个是跟CPU架构相关的了。例如arm的是这样的。

```
struct dev_archdata {
	struct dma_map_ops	*dma_ops;
	bool dma_coherent;
};
```

而arm-generic/device.h是这样的。

```
struct dev_archdata {
};
struct pdev_archdata {
};
```

5、定义了这些结构体：

```
bus_attribute
bus_type
device_driver
class
device_type
device
device_attribute
```



然后我们要看drivers/base目录下的文件。

这里的，我们先看base.h文件。

# base.h

```
1、定义了subsys_private结构体。
2、定义了driver_private
3、定义了device_private
4、声明了devices_init、buses_init、classes_init这些函数。
```

然后我们从bus.c开始看吧。因为设备、驱动都要依附于bus。

# bus.c

这里的入口函数是buses_init。这个是被rest_init调用do_basic_setup调用driver_init调用到的。

就是用kset_create_and_add创建了/sys/bus和/sys/system这2个目录。

主要的对外接口有：

1、subsys_system_register。这有几个地方调用了。

```
struct bus_type s3c2440_subsys = {
	.name		= "s3c2440-core",
	.dev_name	= "s3c2440-core",
};
static int __init s3c2440_core_init(void)
{
	return subsys_system_register(&s3c2440_subsys, NULL);
}
core_initcall(s3c2440_core_init);
```

这个的效果，就是在sys目录下产生了对应的目录。

```
/sys/bus/s3c2440-core # ls
devices            drivers_autoprobe  uevent
drivers            drivers_probe
```

2、bus_add_driver。这个函数就是被driver_register函数调用了。

我们以spi的为例，看看调用的流程。

在enc28j60.c里。

```
enc28j60_init
	spi_register_driver
		__spi_register_driver
			driver_register
				bus_add_driver
```

主要就这些，我们接下来看哪个呢？

看class.c。

# class.c

1、入口函数是classes_init。就是创建/sys/class目录。

2、对外接口class_compat_register。

这个函数被i2c_init函数调用了。用来产生了/sys/class/i2c-adapter目录。

```
i2c_adapter_compat_class = class_compat_register("i2c-adapter");
```

目录情况是这样的。

```
/sys/class # cd i2c-adapter/
/sys/class/i2c-adapter # ls
i2c-0
```

3、对外接口class_compat_create_link。

这个在i2c-core.c里也调用了。

```
res = class_compat_create_link(i2c_adapter_compat_class, &adap->dev,
				       adap->dev.parent);
```

4、接口class_find_device。在spi里用到了。

```
struct spi_master *spi_busnum_to_master(u16 bus_num)
{
	struct device		*dev;
	struct spi_master	*master = NULL;

	dev = class_find_device(&spi_master_class, NULL, &bus_num,
				__spi_master_match);
	if (dev)
		master = container_of(dev, struct spi_master, dev);
	/* reference got in class_find_device */
	return master;
}
```

5、接口class_register。也是在spi.c里调用了。

在spi_init里。

```
status = class_register(&spi_master_class);
```

然后可以看core.c了。从这个名字就可以看出，这个是很核心的东西。

代码也比较多，有2200行。

# core.c

这个这样接口都是device_xxx这个格式的。

1、入口函数是devices_init。创建了/sys/devices、/sys/dev、/sys/dev/block、/sys/dev/char这4个目录。

主要接口有device_create、device_add、device_register。

2、device_create。

在i2c-dev.c里的i2cdev_attach_adapter里有调用。调用栈是：

```
i2c_dev_init被内核初始化调用。
	i2c_for_each_dev(NULL, i2cdev_attach_adapter);//绑定到已经存在的adapter上。
		device_initialize
		device_add。
		就是产生了/dev/i2c-0这样的节点。
```

3、device_register。这个函数是对device_add的封装。

```
int device_register(struct device *dev)
{
	device_initialize(dev);
	return device_add(dev);
}
```

# init.c

这个里面就一个函数。相当于是这个base目录的一个对外总接口。

```
void __init driver_init(void)
{
	devtmpfs_init();
	devices_init();
	buses_init();
	classes_init();
	firmware_init();
	hypervisor_init();
	platform_bus_init();
	cpu_dev_init();
	memory_dev_init();
	container_dev_init();
	of_core_init();
}
```

# platform.c

这个文件也是非常重要的，平台设备相关的内容都在这里了。

1、定义了平台总线。

```
struct device platform_bus = {
	.init_name	= "platform",
};
```



# 参考资料

1、linux内核部件分析（四）——更强的链表klist

https://blog.csdn.net/qb_2008/article/details/6845854