---
title: usb（五）linux下实现U盘功能
date: 2018-04-05 21:27:57
tags:
	- usb

---



usb gadget驱动也叫usb器件驱动。主要是用在嵌入式设备上。使得设备具有普通usb设备的功能。



```
losetup /dev/loop0 vfat.img          //将镜像与loop0建立连接 
insmod gadgetfs.ko
insmod libcomposite.ko 
insmod usb_f_mass_storage.ko
mount /dev/loop0 vfat_mount_point     //挂载挂载点 
insmod g_mass_storage.ko  file=/dev/loop0 stall=0 removable=1
```

我们看这个几个ko分别对应哪些源文件。

gadgetfs.ko

```
gadgetfs-y			:= inode.o
```

对应inode.c文件。

libcomposite.ko 

```
这个很奇怪，Makefile里没有看到。但是用nm看ko文件里的内容，应该是包含了composite.c文件。
```

usb_f_mass_storage.ko

```
g_file_storage-y		:= file_storage.o
```

对应file_storage.c。

g_mass_storage.ko 

```
g_mass_storage-y		:= mass_storage.o
```

对应mass_storage.c。

一个个文件分析一下。

# inode.c

这里注册了一个文件系统。

```
static int __init init (void)
{
	int status;

	status = register_filesystem (&gadgetfs_type);
	if (status == 0)
		pr_info ("%s: %s, version " DRIVER_VERSION "\n",
			shortname, driver_desc);
	return status;
}
```





# 参考资料

1、让mini2440成为U盘之linux gadget driver

https://blog.csdn.net/luckywang1103/article/details/21546129