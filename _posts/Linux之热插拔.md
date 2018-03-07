---
title: Linux之热插拔
date: 2018-03-07 09:28:54
tags:
	- Linux
typora-root-url: ..\
---



当系统被插入一个U盘，系统的usb hub就会检测到U盘的插入，并且完成设备的枚举过程（从设备上读取出相应的设备信息）。并在内核中创建对应的设备结构体。

但是usb设备千奇百怪，内核不可能预先把所有的usb设备驱动都增加到内存里来。

也就是说，系统被插入U盘的时候，内核里不一定有U盘的驱动。而是作为一个ko文件放在lib目录下。

加载驱动只能从用户态来进行。

怎么办？

直观的想法就是手动insmod。

这样太不方便，有没有办法改进？有。

就是uevent机制。

什么叫uevent机制？

就是当有设备插入的时候，发送一个消息到用户空间，用户态运行一个叫udev的进程，专门监听这个消息的。收到消息后就进行驱动加载、文件系统挂载等操作。

# uevent介绍

uevent是kobject的一部分。是系统的最底层的基础设施。

![Linux热插拔](/images/Linux热插拔.png)



uevent的代码，在内核的kobject.h和kobject_uevent.c里。

kobject.h里定义了kobject_action类型：

```
enum kobject_action {
  KOBJ_ADD,
  REMOVE,
  CHANGE,
  ONLINE,//实质是使能
  OFFLINE,
  KOBJ_MAX
};
```

kobj_uevent_env结构体。

```
1、环境变量指针数组。
2、环境变量指针数组索引。
3、buf。保存环境变量的。
4、buflen。
```

kset_uevent_ops

```
1、filter函数。
2、name函数。返回kset的名字。
3、uevent函数。
```



# 实例分析



## U盘的识别流程

1、在我的树莓派上插入一个U盘。先用dmesg -C清空之前的内核打印。然后用dmesg查看。

```
[590235.987988] usb 1-1.2: new high-speed USB device number 8 using dwc_otg
[590236.089723] usb 1-1.2: New USB device found, idVendor=090c, idProduct=1000
[590236.089737] usb 1-1.2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[590236.089744] usb 1-1.2: Product: USB Flash Disk
[590236.089750] usb 1-1.2: Manufacturer: General
[590236.089757] usb 1-1.2: SerialNumber: 0337614020002316
[590236.090367] usb-storage 1-1.2:1.0: USB Mass Storage device detected
[590236.090583] scsi host2: usb-storage 1-1.2:1.0
[590237.660685] scsi 2:0:0:0: Direct-Access     General  USB Flash Disk   1100 PQ: 0 ANSI: 4
[590237.661913] sd 2:0:0:0: Attached scsi generic sg2 type 0
[590237.662326] sd 2:0:0:0: [sdc] 15728640 512-byte logical blocks: (8.05 GB/7.50 GiB)
[590237.662867] sd 2:0:0:0: [sdc] Write Protect is off
[590237.662888] sd 2:0:0:0: [sdc] Mode Sense: 43 00 00 00
[590237.663475] sd 2:0:0:0: [sdc] No Caching mode page found
[590237.663495] sd 2:0:0:0: [sdc] Assuming drive cache: write through
[590237.669493]  sdc: sdc1
[590237.672548] sd 2:0:0:0: [sdc] Attached SCSI removable disk
```

2、然后拔掉。只有一行打印。

```
[590373.243052] usb 1-1.2: USB disconnect, device number 8
```

3、开始看代码。

usb子系统的初始化是在usb.c里的usb_init做的。调用了usb_hub_init。创建了hub_thread。

这个线程里，循环判断链表是否非空。

在hub_irq检查到设备，插入到链表里。

调用kick_hub_wq让hub_event开始工作。

usb的设备插入后的处理较多，不细看。

然后是匹配到drivers/usb/storage/usb.c。

在usb_stor_probe1会打印

```
[590236.090367] usb-storage 1-1.2:1.0: USB Mass Storage device detected
```

然后是drivers/scsi/sd.c里。注册块设备。

然后在rescan_partitions里，用kobject_uevent通知用户控件分区表的变化。



电池的电量变化。

linux下电池驱动的core文件是drivers/power/power_supply_core.c。



# udev和mdev的比较

1、udev用的是netlink机制。适合在有大量uevent的pc机上。

2、mdev用的是uevent_helper，适合在嵌入式上应用。



# 参考文章

1、Linux设备模型(3)_Uevent

http://www.wowotech.net/linux_kenrel/uevent.html