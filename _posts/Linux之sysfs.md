---
title: Linux之sysfs了解
date: 2018-01-28 18:52:43
tags:
	- Linux
	- sysfs

---



sysfs跟proc类似，都是提供了一种从shell访问内核数据的方式。但是sysfs会比proc更好一些。其中最重要的一点就是设计上更加清晰。

proc里的文件格式各不相同，用户程序读取后，可能要进行字符串解析，才能取得有效信息。

而sysfs的设计原则是：一个属性文件只做一件事情。里面只有一个值。



对于驱动开发者，如果想要把驱动跟用户程序建立连接，可以选择的方法有：

1、注册cdev设备。ioctl来设置属性。但是无法在脚本里用。

2、注册proc。

3、注册sysfs。

不过一般是这3个都做的。proc可以选择不做了。

sysfs需要增加的代码最少。可维护性也最好。

一般最少是需要cdev设备的。其他两个是补充性的。

/dev节点的缺点：

1、一般用read/write/ioctl来进行操作。

2、read/write，只能做一件事。

3、ioctl可以实现多种功能。但是无法在shell脚本里使用。还有大小端不兼容、64位兼容问题。

/proc的缺点：

1、写代码比较麻烦。

/sys节点的优点：

1、在用户层都是可见的，透明的。

2、需要增加的代码是最少的。



# sysfs的一些操作

这个需要慢慢去发现sysfs的用途。因为没有详细文档，只能在代码里去读。

## eeprom操作

```
/ # cd /sys/bus/i2c/devices/0-0050/
/sys/devices/platform/s3c2440-i2c.0/i2c-0/0-0050 # ls
driver     eeprom     modalias   name       power      subsystem  uevent
/sys/devices/platform/s3c2440-i2c.0/i2c-0/0-0050 # cat eeprom
```

这样用echo和cat，就可以进行eeprom的读写了。

## gpio的操作

使用"gpiolib"实现框架的平台可选择配置一个GPIO的sysfs用户接口，这不同于debugfs接口，因为它提供GPIO方向和值的控制，而不仅是显示gpio状态摘要，另外，它可再没有调试支持的产品级系统中使用。

可以在这里控制gpio的电平。



# 参考资料

1、

https://www.ibm.com/developerworks/cn/linux/l-cn-sysfs/index.html

