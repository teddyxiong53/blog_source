---
title: Linux之wifi驱动
date: 2020-06-13 17:57:49
tags:
	- Linux

---

1

# 一个实际的场景

有一个usb的wifi网卡。想要在Linux下使用，默认用不了。

这个时候应该怎么做？

1、先把usb插到windows电脑。windows一般是可以正常驱动的。

从设备管理器里，查看usb无线网卡的详细信息，查看硬件id。是一个类似0x3070这样的一个数字。

2、到下面这个网址，输入第一步查询的硬件id进行查询。这样就可以看内核是否已经支持这个设备。

http://linuxwireless.sipsolutions.net/en/users/Devices/USB/

3、然后在内核源代码里grep 上面查询到的id。看属于哪个驱动模块。

4、选择模块，重新编译内核。

5、把对应的wifi的firmware放入到/lib/firmware目录下。





参考资料

1、Linux环境下使用WIFI模块：WIFI驱动移植

https://blog.csdn.net/yunlong654/article/details/88635398