---
title: Linux之configfs
date: 2020-03-25 13:31:11
tags:
	- Linux

---

1

看rk3308的启动脚本，S50usbdevice。里面的内容：

```
mount -t configfs none /sys/kernel/config
```

configfs的作用是：在用户空间配置内核对象。

configfs vs ioctl

configfs可以直接查看。适用于内核对象很复杂的配置。

configfs vs sysfs

**configfs可以在用户态创建和删除内核对象。**



什么时候可以使用configfs？

1、配置项很多的时候。

2、**需要动态创建内核对象。**

3、不想写ioctl，直接用脚本就可以配置。



configfs默认挂载在/sys/kernel/config目录。



看kernel下的文档。



# 参考资料

1、linux之configfs简介和编程入门

https://blog.csdn.net/u014135607/article/details/79949571

2、

https://blog.csdn.net/t1506376703/article/details/109381212