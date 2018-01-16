---
title: Linux之驱动模型
date: 2018-01-08 21:53:38
tags:
	- Linux
	- 驱动

---



linux设备模型的核心是Bus、Class、Device、Driver四大概念。将不同的硬件设备，以树状结构的形式进行归纳抽象，方便kernel的统一管理。

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

# uevent

uevent是kobject的一部分。

当kobject状态发生改变的时候，就会通知用户程序。用户程序收到这样的事件后，就会进行处理。

这个机制是用来处理热拔插的。例如，当插入U盘后，usb驱动程序会创建对应的device数据结构，然后通知用户程序，用户程序在/dev目录下创建对应的节点。然后可以mount到指定目录。

uevent的相关代码比较简单，在kobject.h和kobject_uevent.c里。

# sysfs



