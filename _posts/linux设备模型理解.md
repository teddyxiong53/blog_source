---
title: linux设备模型理解
tags:
	- linux驱动
---
sysfs是linux系统里内容非常庞杂的一部分，一直对它的结构和层次不太了解。现在从这个点入手，来理解linux的内核设备模型等相关知识。
sysfs主要用来向用户空间展示设备模型中各种组件的层次关系，可以由用户空间存取。组件层次关系的实现是通过kobject来达到的。
我们看树莓派里的`/sys`目录的内容。
```
pi@raspberrypi:/sys $ ls
block  bus  class  dev  devices  firmware  fs  kernel  module  power
```
linux里的platform出现的背景是，现在大多的芯片是soc，除了cpu之外，还集成了lcd接口、flash接口等等。通过引入platform机制，内核假设把这些外设都挂在platform虚拟总线上，方便统一管理。
platform在系统初始化的时候注册，通过`bus_register`注册`platform_bus_type`，在`/sys/bus`目录下生产一个新的目录platform。其结构如下：
```
pi@raspberrypi:/sys/bus/platform $ tree  -L 1  
.
├── devices
├── drivers
├── drivers_autoprobe
├── drivers_probe
└── uevent
2 directories, 3 files
```
2个目录devices和drivers，文件uevent（热拔插事件）。
内核利用device_register注册platform（作为一种设备）时，因为没有指定父设备，所以注册后将出现目录`/sys/device/platform`。




