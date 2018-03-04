---
title: 树莓派之config.txt
date: 2018-03-03 19:57:45
tags:
	- 树莓派

---



https://elinux.org/RPiconfig

本文是对这个的总结。



树莓派没有一个传统的bios，各种系统配置参数，需要在一个叫config.txt里配置。

config.txt是被GPU读取的，这个过程在cpu启动之前。

这个文件在boot分区里，是一个可选的文件。

https://raw.github.com/Evilpaul/RPi-config/master/config.txt

这里是一个完整的示例文件。

#mem

1、disable_l2cache。默认是0。

禁止arm访问gpu的L2 Cache。

2、gpu_mem。默认64 。

把内存给64M给gpu用，其余的给arm用。

# CMA 

是动态内存划分。gpu和arm的内存在运行时动态调整大小。



# camera

1、start_x = 1 。这样就使能了camera模块。

2、disable_camera_led=1 。禁止camera模块的led灯，这样录像的时候就不会闪了。

3、gpu_mem=128。需要gpu_mem为128M才能支持camera。



# Network

smsc95xx.macaddr=XXX

设置mac地址。

# Video

这个配置项比较多。

# overclocking超频





# usb power



# device tree

1、使能i2c。

```
dtparam=i2c_arm=on
```

2、使能spi。

```
dtparam=spi=on
```

3、添加一个overlay /boot/overlays/xxx-overlay.dtb到设备树。

```
dtoverlay=xxx
```



