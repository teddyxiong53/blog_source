---
title: Linux的设备模型分析
date: 2017-05-02 20:51:55
tags:
	- Linux驱动
typora-root-url: ..\
---





2.5版本的一个重要开发目标就是为内核创造一个统一的设备模型。

之前的系统没有一个单一的数据结构体，来获取系统的信息。

但是现在电源管理等复杂需求，迫切需要一个通用的抽象机制。

于是设备模型就被做出来了。



linux设备模型的核心是Bus、Class、Device、Driver四大概念。将不同的硬件设备，以树状结构的形式进行归纳抽象，方便kernel的统一管理。



设备模型现在可以支持这些功能：

1、电源管理和系统关机。

2、与用户空间的通信。就是sysfs。

3、热拔插。

4、device class。系统的其他部分对于设备是如何连接起来的没有兴趣，但是他们需要知道哪种设备可用。设备模型包括了一种机制，把device指派为class，可用再用户空间发现设备。

class描述的是功能。

5、object生命周期。

上面描述的功能，包括热拔插、sysfs，都把生成和操作object复杂化了。

我们看一个简单的例子，以usb鼠标为例。在sysfs里的情况是这样的：

![linux设备模型1](/images/linux设备模型1.png)

不过幸运的是，驱动开发者对此不需要太多关注，跟设备模型直接打交道的是总线和其他的内核子系统。

但是，理解设备模型对于驱动开发者还是很有好处的。



设备模型太复杂，从上往下，难以看清，所以我们从下往上看。



# kobject

kobject是linux设备模型的基础。也是设备模型中最难理解的一部分。官方的文档在Documentation/kobject.txt。

kobject是对所有设备的抽象。

kobject目前主要提供这些功能：

1、通过parent指针，可以将所有kobject以层次结构的形式组合起来。

2、使用引用计数，记录kobject的被引用次数，在引用次数变为0的时候释放。

3、和sysfs配合，将每一个kobject及其特性，以文件的形式，开放到用户空间。

```
在linux中，kobject几乎不会单独存在。它的主要功能就是嵌入在其他的大型数据结构里，为它们提供一些底层功能。
所以，kobject的相关接口，驱动开发者一般也不会用到。
```

一个kobject对应/sys目录下的一个目录。

kobj_type代表了kobject的属性操作集合。

kset是一个特别的kobject。



# kobject、kset和subsystem

kobject最初只是一个引用计数，不过后面功能逐渐复杂了。

现在kobject包括：

1、引用计数。

2、sysfs呈现。

3、数据结构粘合。

4、热拔插处理。

kobject不会单独存在，都是嵌入到其他的结构体里起作用。

按照面向对象的术语来说，kobject是一个顶级的基类，其他的类都继承了它。

我们可以看一下cdev这个结构体。



kobject_init：其实没有做太多事情，就是把结构体初始化了一下，ref设置为1 。

引用计数的操作：

kobject_get（引用加1）和kobjet_put（引用减1）。

释放函数和kobject类型。

当一个kobject的ref减到0的时候，会发生什么？

每个kobject都必须有一个释放函数，这个函数没有存储在kobject里，而是在kobj_type里，我们简称为ktype。

**ktype里有一个release函数。**

每个kobject都需要一个关联的kobj_type。实际上，在kobject里有2个地方可以找到kobj_type。一个是kobject包含的，一个是kset里包含的。

kobject里的parent指针，是用来建立sysfs的层级关系的。

一个kset对应sysfs里的一个目录。

**kset里也包含了kobject，所以kset相当于kobject的子类。**

kset还包含了一个kobject的链表。

kset相当于文件夹，kobject相当于文件，文件夹是一种特殊的文件。

subsystem是kset的容器。



kobject_add的作用：

1、建立kobj对象间的层次关系。

2、在sysfs里建立一个目录。

parent为NULL的话，则是在/sys目录下。



# class

class相当于device，它是对设备进行功能性的划分。

class是类似功能的device的容器。



#以一个platform设备来分析kobject

先看sys下的bus和devices。

bus的初始化在drivers/base/bus.c里。

```
buses_init
	kset_create_and_add("bus", &bus_uevent_ops, NULL); //创建一个kset容器。注意parent_kobj是NULL
		kset_create//先创建。
			1、kzalloc一块内存，
			2、kobject_set_name，name是"bus"。
			
		kset_register//再注册。
```

执行完之后，结构体的关系是这样的：



现在看devices。在/drivers/base/core.c。

```
devices_init
	devices_kset = kset_create_and_add("devices", &device_uevent_ops, NULL)
	
```

过程跟bus的类似。

然后看platform的注册。这个分为2个部分，一部分是注册到devices里，一部分是注册到bus里。

代码在drivers/base/platform.c里。

```
platform_bus_init
	device_register（&platform_bus）这个是一个device，全局变量，里面就一个成员赋值了，name叫“platform”。
		1、device_initialize
			dev->kobj.kset = devices_kset;这就是我们上面得到的devices_kset。这个相当于创建了
				/sys/devices/platform目录。
				
		2、device_add。
			这里面进行了一系列的sys下面的文件创建。
	bus_register。
	
```

到这里，bus、devices、platform的基础模型就建立好了。现在就等设备来注册了。

```
struct platform_device test_device = {
  .name = "test_platform",
  .id = -1,
};
struct platform_driver test_driver = {
  .probe = test_probe,
  .remove = test_remove,
  .driver = {
    .name = "test_platform",
    .owner = THIS_MODULE,
  },
};
static int test_init(void)
{
  platform_device_register(&test_device);
  platform_driver_register(&test_driver);
}
```

从platform_device_register开始看。

```
platform_device_register
	device_initialize
	platform_device_add
```



# 设备模型的用途

1、一个重要用途就是设备的热插拔的支持。