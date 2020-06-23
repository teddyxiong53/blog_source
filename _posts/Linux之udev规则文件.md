---
title: Linux之udev规则文件
date: 2017-08-05 14:48:45
tags:
	- Linux
---

1

udev的工作是靠kernel发出的uevent来驱动的，如果是删除的uevent，就会删除对应的节点。如果是增加设备的uevent，就会增加对应的节点。

规则文件是放在/etc/udev/rules.d目录下的。下面的文件命名规则是：xx-yy.rules。xx是数字，yy是字母，后缀都是rules。

执行时，先看数字，后看字母，后执行的会覆盖先执行的。

每一行代表一个规则，由多个键值对。

一个例子

```
SUBSYSTEM=="udc",ACTION=="change",DRIVER=="configfs-gadget",RUN+="/usr/bin/usbdevice %E{DEVPATH}"
```



```
常用匹配键：
    * KERNEL     - 匹配设备在内核中的命名
    * SUBSYSTEM  - 匹配设备(在sysfs中)的subsystem名
    * DRIVER     - 匹配设备对应的驱动名
    * ATTR       - 匹配设备在sysfs中属性
    * KERNELS    - 匹配设备及其父亲在内核中的命名
    * SUBSYSTEMS - 匹配设备及其父亲(在sysfs中)的subsystem名
    * DRIVERS    - 匹配设备及其父亲对应的驱动名
    * ATTRS      - 匹配设备及其父亲在sysfs中属性
      注：父亲表示直到最上层的所有祖先

常用赋值键：
    * NAME - 设备节点名
    * SYMLINK - 指向设备节点的符号连接列表
```



参考资料

1、udev规则

http://blog.chinaunix.net/uid-26808060-id-4339831.html

2、Linux udev规则编写

https://blog.csdn.net/xiaoliu5396/article/details/46531893