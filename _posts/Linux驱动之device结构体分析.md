---
title: Linux驱动之device结构体分析
date: 2018-03-29 10:29:12
tags:
	- Linux驱动

---



基于linux2.6.35分析。

include/linux/device.h里。

```
结构体
	1、struct bus_attribute 
	2、struct bus_type 
	3、struct device_driver 
	4、struct driver_attribute
	5、struct class 
	6、struct class_attribute
	7、struct class_interface
	8、struct device_type
	9、struct device_attribute
	10、struct device
	
函数声明：
	1、基于bus_attribute的bus_create_file和bus_remove_file。
	2、基于bus_type的bus_register和bus_unregister。
	3、基于device_driver的driver_register和driver_unregister。
	4、基于driver_attribute的driver_create_file
	5、基于class的class_register和class_register。
	6、基于class_attribute的class_create_file和class_remove_file。
	7、基于class_interface的class_interface_register和class_interface_unregister。
	8、基于device_attribute的device_create_file。
	
```

在base目录下。只有base.h这一个头文件。其余都是C文件。

```
base.h里：
	1、struct bus_type_private 
	2、struct driver_private 
	3、struct class_private 
	4、struct device_private
```



struct klist，只有drivers/base里的core.c和bus.c才用到，是内部的。

node是这样的。封装了引用计数。

```
struct klist_node {
	void			*n_klist;	/* never access directly */
	struct list_head	n_node;
	struct kref		n_ref;
};
```

引用计数定义在include/linux/kref.h里。就是一个原子数。

```
struct kref {
	atomic_t refcount;
};
```



看看系统里device_type有哪些。

```
1、net/bridge/br_if.c
static struct device_type br_type = {
	.name	= "bridge",
};
2、fs/partitions/check.c
struct device_type part_type = {
	.name		= "partition",
	.groups		= part_attr_groups,
	.release	= part_release,
	.uevent		= part_uevent,
};
3、net/wireless/core.c
static struct device_type wiphy_type = {
	.name	= "wlan",
};
4、drivers/i2c/i2c-core.c
static struct device_type i2c_client_type = {
	.groups		= i2c_dev_attr_groups,
	.uevent		= i2c_device_uevent,
	.release	= i2c_client_dev_release,
};
static struct device_type i2c_adapter_type = {
	.groups		= i2c_adapter_attr_groups,
	.release	= i2c_adapter_dev_release,
};
5、drivers/input/input.c
static struct device_type input_dev_type = {
	.groups		= input_dev_attr_groups,
	.release	= input_dev_release,
	.uevent		= input_dev_uevent,
#ifdef CONFIG_PM
	.pm		= &input_dev_pm_ops,
#endif
};
```

我们就用i2c里的i2c_adapter_type来看看怎么用的。

```
i2c-s3c2410.c里的probe
	i2c_add_numbered_adapter
		i2c_register_adapter
			adap->dev.type = &i2c_adapter_type;
```

我发现一个规律，就是xxx_type的构成都差不多。

bus_type、device_type、kobj_type。

一般都有这几个成员。

```
name
attribute
uevent函数
release函数
```

内核里的bus_type又有哪些呢？

```
./sound/ac97_bus.c:52:struct bus_type ac97_bus_type
./sound/aoa/soundbus/core.c:153:static struct bus_type soundbus_bus_type
./drivers/i2c/i2c-core.c:338:struct bus_type i2c_bus_type 
./drivers/mmc/core/bus.c:139:static struct bus_type mmc_bus_type
./drivers/amba/bus.c:109:static struct bus_type amba_bustype 
./drivers/media/video/soc_camera.c:1110:static struct bus_type soc_camera_bus_type
./drivers/base/platform.c:1011:struct bus_type platform_bus_type
```

我们还是看一下i2c的和platform的。

```
struct bus_type i2c_bus_type = {
	.name		= "i2c",
	.match		= i2c_device_match,
	.probe		= i2c_device_probe,
	.remove		= i2c_device_remove,
	.shutdown	= i2c_device_shutdown,
	.pm		= &i2c_device_pm_ops,
};
	//device结构体里，同时包含了bus_type和device_type。
	adap->dev.bus = &i2c_bus_type;
	adap->dev.type = &i2c_adapter_type;
	
```

就是bus_type把device和driver连接起来的。

我们看platform的情况。

在platform_device_add函数里。

```
pdev->dev.bus = &platform_bus_type;
```

在platform_driver_register里。

```
int platform_driver_register(struct platform_driver *drv)
{
	drv->driver.bus = &platform_bus_type;//这里。
	if (drv->probe)
		drv->driver.probe = platform_drv_probe;
	if (drv->remove)
		drv->driver.remove = platform_drv_remove;
	if (drv->shutdown)
		drv->driver.shutdown = platform_drv_shutdown;

	return driver_register(&drv->driver);
}
```

我们现在还是回到struct device结构体。

里面主要的成员有：

```
1、struct device *parent 。建立层次关系的。在sysfs里。
2、struct device_private *p。
3、struct kobject kobj。
4、char *init_name。
5、struct device_type *type。
6、struct bus_type *bus。
7、struct device_driver *driver。
8、void *platform_data。//一般在bsp里定义。注册进来。
9、dev_t devt。
10、struct class *class。
11、struct attribute_group **groups。
12、void (*release)(struct device *dev)
```

device的主要操作函数是在drivers/base/core.c里。

驱动开发首先用到的是device_register函数。

相关调用情况是：

```
i2c-s3c2410.c里调用i2c_add_adapter
	i2c_register_adapter
		res = device_register(&adap->dev);
			device_initialize(dev);
			return device_add(dev);
```

device_add里做的事情：

```
1、如果device->p没有，就分配一个。
2、如果device->init_name有，就赋值给kobject里的name。
3、拿到dev->parent。建立kobject的层次关系。用kobject_add。
4、调用device_create_file（就是封装了对sysfs_create_file）。创建uevent。
5、device_create_file创建devt_attr。
6、其他各种sysfs软链接创建。
```

现在看看struct device_driver。

还是以i2c的为例。i2c-dev.c里。这里是对应/dev/i2c-0这种节点的。

```
i2c_dev_init
	i2c_add_driver(&i2cdev_driver);
		i2c_register_driver
			driver_register(&driver->driver);
				bus_add_driver
				driver_add_groups
```

platform也是类似的。

```
int platform_driver_register(struct platform_driver *drv)
{
	drv->driver.bus = &platform_bus_type;
	if (drv->probe)
		drv->driver.probe = platform_drv_probe;
	if (drv->remove)
		drv->driver.remove = platform_drv_remove;
	if (drv->shutdown)
		drv->driver.shutdown = platform_drv_shutdown;

	return driver_register(&drv->driver);
}
```



