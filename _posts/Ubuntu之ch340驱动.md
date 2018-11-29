---
title: Ubuntu之ch340驱动
date: 2018-11-29 20:11:07
tags:
	- Ubuntu

---



现在我需要在我的Ubuntu笔记本上做开发。

一块esp8266的板子，是ch340的usb转串口的驱动芯片。

所以，首先就是需要在linux下安装驱动。

驱动就一个c文件。

```
make
sudo make load
```

查看dmesg信息的最后部分。

```
[ 4109.309612] usbcore: registered new interface driver usbserial
[ 4109.309634] usbcore: registered new interface driver usbserial_generic
[ 4109.309652] usbserial: USB Serial support registered for generic
[ 4109.321183] usbcore: registered new interface driver ch341
[ 4109.321208] usbserial: USB Serial support registered for ch341-uart
[ 4109.321231] ch341 6-2:1.0: ch341-uart converter detected
[ 4109.333621] usb 6-2: ch341-uart converter now attached to ttyUSB0
[ 4429.061760] ch34x: module verification failed: signature and/or required key missing - tainting kernel
[ 4429.062162] usbcore: registered new interface driver ch34x
[ 4429.062184] usbserial: USB Serial support registered for ch34x
```

对应的设备节点是/dev/ttyUSB0。

这个驱动可以作为学习资料看看。







# 参考资料

1、CH340 Linux驱动使用教程

https://blog.csdn.net/JAZZSOLDIER/article/details/70170466