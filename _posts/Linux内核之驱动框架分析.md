---
title: Linux内核之驱动框架分析
date: 2021-02-20 14:23:30
tags:
- Linux
---

--

# 字符设备

Linux一切皆文件，

那么作为一个设备文件，

它的操作方法接口封装在`struct file_operations`，

当我们写一个驱动的时候，一定要实现相应的接口，这样才能使这个驱动可用，

Linux的内核中大量使用**"注册+回调"机制**进行驱动程序的编写，

所谓注册回调，

简单的理解，

就是当我们open一个设备文件的时候，

其实是通过VFS找到相应的inode，

并执行此前创建这个设备文件时注册在inode中的open函数，

其他函数也是如此，

所以，为了让我们写的驱动能够正常的被应用程序操作，

首先要做的就是实现相应的方法，**然后再创建相应的设备文件。**

罗嗦一句，如果使用静态申请设备号，那么最大的问题就是不要与已知的设备号相冲突，

内核在文档**"Documentation/devices.txt"**中已经注明了哪些主设备号被使用了，

从中可以看出，在`2^12`个主设备号中，我们能够使用的范围是`240到255以及261到2^（12-1）`这个范围内的部分，

这也可以解释为什么我们动态申请的时候，设备号经常是250的原因。

此外，通过这个文件，我们也可以看出，"主设备号表征一类设备"，

但是字符/块设备本身就可以被分为好多类，所以内核给他们每一类都分配了主设备号。



Linux下各个进程都有自己独立的进程空间，

即使是将内核的数据映射到用户进程，

该数据的PID也会自动转变为该用户进程的PID，

由于这种机制的存在，我们不能直接将数据从内核空间和用户空间进行拷贝，而需要专门的拷贝数据函数/宏



ioctl是Linux专门为用户层控制设备设计的系统调用接口，

这个接口具有极大的灵活性，

我们的设备打算让用户通过哪些命令实现哪些功能，都可以通过它来实现

```
设备类型    序列号  	方向    	数据尺寸
8bit        8bit    2bit    13/14bit
```

**设备类型**字段为一个幻数，

可以是0~0xff之间的数，

内核中的"**ioctl-number.txt**"给出了一个推荐的和已经被使用的幻数(但是已经好久没人维护了)，

新设备驱动定义幻数的时候要避免与其冲突。

**序列号**字段表示当前命令是整个ioctl命令中的第几个，从1开始计数。

**方向**字段为2bit，表示数据的传输方向，可能的值是：

**_IOC_NONE**，**_IOC_READ**，**_IOC_WRITE**和**_IOC_READ|_IOC_WRITE**。
**数据尺寸**

字段表示涉及的用户数据的大小，这个成员的宽度依赖于体系结构，通常是13或14位。



创建设备文件的方法有两种，**手动创建**或**自动创建**，

**手动创建设备文件**就是使用**mknod /dev/xxx 设备类型 主设备号 次设备号**的命令创建，

所以首先需要使用**cat /proc/devices**查看设备的主设备号并通过源码找到设备的次设备号，

需要注意的是，**理论上设备文件可以放置在任何文件加夹**，但是放到**"/dev"**才符合Linux的设备管理机制，

这里面的devtmpfs是专门设计用来管理设备文件的文件系统。

设备文件创建好之后就会和创建时指定的设备绑定，即使设备已经被卸载了，

<u>如要删除设备文件，只需要像删除普通文件一样**rm**即可。</u>

理论上模块名(lsmod),设备名(/proc/devices)，设备文件名(/dev)并没有什么关系，完全可以不一样，

但是原则上还是建议将三者进行统一，便于管理。



除了使用蹩脚的手动创建设备节点的方式，

我们还可以在设备源码中使用相应的措施使设备一旦被加载就**自动创建设备文件**，

自动创建设备文件需要我们在编译内核的时候或制作根文件系统的时候就好相应的配置:

# 平台设备

我在Linux字符设备驱动框架一文中简单介绍了Linux字符设备编程模型，

在那个模型中，只要应用程序open()了相应的设备文件，

就可以使用ioctl通过驱动程序来控制我们的硬件，这种模型直观，

**但是从软件设计的角度看，却是一种十分糟糕的方式，**

它有一个致命的问题，

就是设备信息和驱动代码冗余在一起，

一旦硬件信息发生改变甚至设备已经不在了，就必须要修改驱动源码，非常的麻烦，

为了解决这种驱动代码和设备信息耦合的问题，

Linux提出了platform bus(平台总线)的概念，

**即使用虚拟总线将设备信息和驱动程序进行分离，**

**设备树的提出就是进一步深化这种思想，**

将设备信息进行更好的整理。

**平台总线会维护两条链表，分别管理设备和驱动，**

当一个设备被注册到总线上的时候，

总线会根据其名字搜索对应的驱动，

如果找到就将设备信息导入驱动程序并执行驱动；

当一个驱动被注册到平台总线的时候，总线也会搜索设备。

总之，平台总线负责将设备信息和驱动代码匹配，

**这样就可以做到驱动和设备信息的分离。**

![img](../images/playopenwrt_pic/1022162-20170205104332511-1610594098.png)

简而言之，平台驱动、设备树这些东西的引入，都是为了达到一个目的，可变数据和代码的分离，增强内聚性和可维护性。

在设备树出现之前，设备信息只能使用C语言的方式进行编写，

在3.0之后，设备信息就开始同时支持两种编写方式——设备树、C语言，

如果用设备树，手动将设备信息写到设备树中之后，

内核就可以自动从设备树中提取相应的设备信息

并将其封装成相应的platform_device对象，i2c_device对象并注册到相应的总线中，

如果使用设备树，我们就不需要对设备信息再进行编码。

如果使用C语言，显然，我们需要将使用内核提供的结构将设备信息进行手动封装，

这种封装又分为两种形式，

一种是使用平台文件(静态)，将整个板子的所有设备都写在一个文件中并编译进内核。

另一种是使用模块(动态)，将我们需要的设备信息编译成模块在insmod进内核。

对于ARM平台，使用设备树封装设备信息是将来的趋势，

但是由于历史原因，当下的内核中这三种方式并存。

封装好后再创建相应的xxx_device实例最后注册到总线中。

针对平台总线的设备信息，我在Linux设备树语法详解一文中已经讨论了设备树的写法，

所以，本文主要讨论4个问题：

1. 如何使用C语言封装设备信息?
2. 设备树的设备信息和C语言的设备信息如何转换？
3. 如何将C语言设备信息封装到platform_device结构中?
4. 如何将封装好的platform_device结构注册到平台总线中?



所谓的设备信息，主要分为两种：

硬件信息、软件信息，

硬件信息主要包括xxx控制器在xxx地址上，xxx设备占用了xxx中断号，即**地址资源**，**中断资源**等。

内核提供了struct resource来对这些资源进行封装。

软件信息的种类就比较多样，

比如网卡设备中的MAC地址等等，

这些信息需要我们以私有数据的形式封装的设备对象

这部分信息就需要我们自定义结构进行封装。



有了这几个属性，就可以完整的描述一个资源，

但如果每个资源都需要单独管理而不是组成某种数据结构，显然是一种非常愚蠢的做法，

所以内核的resource结构还提供了三个指针：**parent,sibling,child(24)**，

分别用来表示资源的父资源，兄弟资源，子资源，

这样内核就可以使用树结构来高效的管理大量的系统资源，

linux内核有两种树结构：

iomem_resource,ioport_resource，

进行板级开发的时候，通常将主板上的ROM资源放入iomem_resource树的一个节点，

而将系统固有的I/O资源挂到ioport_resource树上。



这个对象就是我们最终要注册到平台总线上的设备信息对象，

对设备信息进行编码，其实就是创建一个platform_device对象，

可以看出，platform_device和其他设备一样，都是device的子类



准备好了platform_device对象，接下来就可以将其注册进内核，

显然内核已经为我们准备好了相关的函数



Linux中几乎所有的"设备"都是"device"的子类，

无论是平台设备还是i2c设备还是网络设备，

但唯独字符设备不是，

从"Linux字符设备驱动框架"一文中我们可以看出cdev并不是继承自device，



从"Linux设备管理（二）从cdev_add说起"一文中我们可以看出

注册一个cdev对象到内核，

其实只是将它放到cdev_map中，

直到"Linux设备管理（四）从sysfs回到ktype"一文中对device_create的分析

才知道此时才创建device结构并将kobj挂接到相应的链表，，





**所以，基于历史原因，当下cdev更合适的一种理解是一种接口(使用mknod时可以当作设备)，**

**而不是而一个具体的设备，和platform_device,i2c_device有着本质的区别**



写驱动也有一段时间了，可以发现，

其实驱动本质上只做了两件事：

**向上提供接口，向下控制硬件**，

当然，这里的**向上**并不是直接提供接口到应用层，

而是提供接口给内核再由内核间接的将我们的接口提供给应用层。

而写驱动也是有一些套路可寻的，

拿到一个硬件，我们大体可以按照下面的流程写一个驱动：

1. **确定驱动架构**：根据硬件连接方式结合分层/分离思想设计驱动的基本结构
2. **确定驱动对象**：内核中的一个驱动/设备就是一个对象，1.定义，2.初始化，3.注册，4.注销
3. **向上提供接口**：根据业务需要确定提供cdev/proc/sysfs哪种接口
4. **向下控制硬件**：1.查看原理图确定引脚和控制逻辑，2.查看芯片手册确定寄存器配置方式，3.进行内存映射，4.实现控制逻辑



设备信息有三种表达方式，

而一个驱动是可以匹配多个设备的，

平台总线中的驱动要具有三种匹配信息的能力，

基于这种需求，platform_driver中使用不同的成员来进行相应的匹配。

of_match_table

对于使用设备树编码的设备信息，我们使用其父类device_driver中的of_match_table就是用来匹配

id_table

对于使用C语言编码的设备信息，我们用platform_driver对象中的id_table就是用来匹配。

我们使用struct platform_device_id ids[]来实现一个驱动匹配多个C语言编码的设备信息。

name

如果platform_driver和C语言编码的platform_device是一一匹配的，

我们还可以使用device_driver中的name来进行匹配

填充完platform_driver结构之后，我们应该将其中用到的设备表注册到内核，

虽然不注册也可以工作，但是注册可以将我们表加入到相关文件中，便于内核管理设备。

从中不难看出，这几中形式的匹配是有优先级的：**of_match_table>id_table>name**，了解到这点，我们甚至可以构造出同时适应两种设备信息的平台驱动：

```
static struct platform_driver drv = {
	.probe	= demo_probe,
	.remove	= demo_remove,

	.driver = {
		.name = "demo",
#ifdef CONFIG_OF
		.of_match_table = of_tbl,
#endif
	},

	.id_table = tbl,
};
```

此外，如果你追一下of_driver_match_device()，

就会发现**平台总线的最终的匹配是compatible，name,type三个成员，其中一个为NULL或""时表示任意，所以我们使用平台总线时总是使用compatile匹配设备树，而不是节点路径或节点名**。

## probe()

probe即探测函数，

如果驱动匹配到了目标设备，

总线会自动回调probe函数，

下面详细讨论。

并把匹配到的设备信息封装策划platform_device对象传入，

里面主要完成下面三个工作

1. **申请资源**
2. **初始化**
3. **提供接口(cdev/sysfs/proc)**

显然，remove主要完成与probe相反的操作，

这两个接口都是我们必须实现的。

在probe的工作中，

最常见的就是提取设备信息，

虽然总线会将设备信息封装成一个platform_device对象并传入probe函数，

我们可以很容易的得到关于这个设备的所有信息，

但是更好的方法就是直接使用内核API中相关的函数



# cdev+platform

平台总线是一种实现设备信息与驱动方法相分离的方法，

利用这种方法，

我们可以写出一个更像样一点的字符设备驱动，

即

**使用cdev作为接口，平台总线作为分离方式:**

```
xjkeydrv_init()：模块加载函数
└──platform_driver_register()将驱动对象模块注册到平台总线
        └──platform_driver.probe()探测函数，提取相应的信息
                └──xjkey_init()：初始化cdev对象，创建设备文件等关于cdev接口创建的工作
                        └──cdev_init():将cdev结构与fops绑定到一起，在fops实现操作接口与控制硬件的逻辑
```

写一个xxkey的例子。

对我的，platform的probe接口。

在probe里调用xxkey_init。

xxkey_init里调用cdev的接口。还调用classs_create、device_create



没有cdev也可以的。直接对sysfs的文件进行读写。是attribute的read、write。

at24.c就是这样的。

```
	at24->bin.read = at24_bin_read;
```



# 参考资料

1、Linux Platform驱动模型(一) _设备信息

这个分析很好。

https://www.cnblogs.com/xiaojiang1025/p/6367061.html

2、What is the difference between a Linux platform driver and normal device driver?

https://stackoverflow.com/questions/15610570/what-is-the-difference-between-a-linux-platform-driver-and-normal-device-driver