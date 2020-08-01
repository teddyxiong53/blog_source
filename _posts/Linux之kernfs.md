---
title: Linux之kernfs
date: 2018-03-04 22:10:47
tags:
	- Linux

---



kernfs是一组函数，包含创建伪文件系统的，这些伪文件系统是被内核子系统使用的。

**是从sysfs里剥离一部分出来**，用来输出一组虚拟文件，包含了硬件设备信息和相关驱动信息。

**这样内核子系统就可以很容易地实现自己的伪文件系统。**

是从3.14版本开始合入到内核的。在2014年3月30号发布的。

kernfs的主要用户之一是cgroups内部使用的伪文件系统。

kernfs_node表示kernfs层次的构成部分(building block)，每个kernfs节点由单个kernfs_node表示。大多数字段都是kernfs专用的，不应该由kernfs用户直接访问。

节点有三种：目录、文件、链接。

```
enum kernfs_node_type {
	KERNFS_DIR		= 0x0001,
	KERNFS_FILE		= 0x0002,
	KERNFS_LINK		= 0x0004,
};
```



参考资料

1、kernfs_node、kobject和kset

https://blog.csdn.net/zhoudawei/article/details/86669868



