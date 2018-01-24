---
title: Android系统（三）HAL系统分析
date: 2018-01-23 14:45:07
tags:
	- Android系统

---



Android系统的HAL层在用户空间运行。

# hal出现的背景

在Android系统中，推出hal层是为了保护一些硬件厂商的知识产权，用来避开linux的GPL协议的。

谷歌的架构师的思路是吧控制硬件的动作都放到HAL层里。而Linux Driver进负责一些简单的数据交互。甚至把硬件寄存器都映射到用户控件来操作。

Android系统是基于Apache协议的，厂家可以只提供二进制的文件。所以Android只是一个开放平台，而不是一个开源平台。

也因为Android不遵守GPL，linux内核维护者就把Android驱动从linux内核里移除了。不过后面Linux又把Android接纳进来了。

GPL和硬件厂商之间的分歧很难弥合。

# hal分类

Android系统里的hal可以分为下面6类：

1、上层软件。

2、内部以太网。

3、内部通信client。

4、用户接入口。

5、虚拟驱动。

6、内部通信server。

# hal主要存放的目录

1、libhardware_legacy。之前的目录。采取了链接库模块的观念来进行架构的。

2、libhardware。新的 目录，采用HAL stub的观念来架构。

3、ril。是Radio接口层。

4、msm7k。qual平台相关的信息。

# hal的基本架构

基本层次关系是这样：

```
库、Android运行环境
---------------------
HAL层
----------------------
linux内核
```

hal层把Android框架跟linux内核隔离开了。

# 分析hal module架构

Android5.0的hal采用hal module和hal stub结合的方式来架构。

hal stub不是一个so文件。

hal module主要包括3个结构体：

```
struct hw_module_t;
struct hw_module_methods_t;
struct hw_device_t;
```

对应的so文件的命名规则是：

id.varient.so

例如：

gralloc.msm7k.so

