---
title: Linux的misc device驱动
date: 2017-05-18 23:20:30
tags:
	- Linux驱动

---

1

随着字符设备种类和数量的增加，设备号越来越紧张，为此Linux系统提出misc设备模型以解决此问题。

所有misc设备其主设备号都是10，不同设备使用不同的次设备号区分。另外misc设备驱动会为设备自动创建设备文件，不需要想cdev设备那样，需要自己手动创建，所以使用起来更为方便。



misc device是不能明确归类的一些设备，一般都是功能比较简单的设备。Linux给这类设备分配的主设备号是10。

直接看例子，先写一个misc设备的驱动，然后用一个测试程序来测试一下。

设备名为mymisc。

misc device的内部实现就是用字符设备来实现的。

鼠标、看门狗、温度传感器、rtc、nvram、kvm

# 为什么需要misc dev？

1、节省主设备号。

2、使用更加简单。开发人员注册一个char dev比misc dev要麻烦多了。



# drivers/misc/eeprom/at24.c

看看这个eeprom的代码。



# 内核代码分析

主要是2个文件，linux/miscdevice.h和drivers/char/misc.c。

## miscdevice.h

1、定义了从设备号。从1到255 。255表示是动态分配。

2、定义了miscdevice结构体。

miscdevice就跟cdev结构体不一样了，它包含了device结构体了。

3、对外的接口就2个misc_register和misc_unregiter。



注意这个别名机制。

```
#define MODULE_ALIAS_MISCDEV(minor)				\
	MODULE_ALIAS("char-major-" __stringify(MISC_MAJOR)	\
	"-" __stringify(minor))
```

##misc.c

1、misc_init。这个是在系统初始化的时候调用的。

```
1、proc_create("misc", 0, NULL, &misc_proc_fops);//这个是创建了/proc/misc节点。
2、misc_class = class_create(THIS_MODULE, "misc");//这个是创建了/sys/class/misc目录。
3、register_chrdev(MISC_MAJOR,"misc",&misc_fops)//注册字符设备。没有对应/dev/misc节点存在。
4、misc_class->devnode = misc_devnode;//这个暂时不清楚，但是应该比较重要。
```

2、注册和反注册。

这2个没有太多可看的。

3、看看misc_proc_fops结构体。

```
/proc # cat misc 
 59 ubi_ctrl
 60 memory_bandwidth
 61 network_throughput
 62 network_latency
 63 cpu_dma_latency
200 tun
183 hw_random
```

```
/sys/class/misc # ls
cpu_dma_latency     network_latency     ubi_ctrl
hw_random           network_throughput
memory_bandwidth    tun
```

常用的misc设备有：

```
看门狗 130
温度传感器 131
rtc 135
nvram 144

```



参考资料

1

https://blog.csdn.net/tong646591/article/details/8301925