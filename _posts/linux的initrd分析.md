---
title: linux的initrd分析
date: 2016-12-13 19:44:12
tags:
	- linux
	- initrd
---
1

为什么需要initrd？

内核里没有编译根文件系统所在的介质的驱动，例如cd-rom。

就需要先用initrd，执行initrd的init进程，然后insmod cd-rom的驱动。挂载cd-rom。

然后切换到cd-rom上的真正文件系统的init上。



主要作用：

1、Linux发行版必备。

因为发行版需要适应各种不同的硬件，把所有的驱动都编译进内核是不现实的。

2、livecd必备。

3、制作Linux usb启动盘必须使用initrd。



**从本质上来说，就是为了应对存储介质的多样性和不确定性。**



initramfs从内核2.5版本才出现。比initrd要晚。

所以initramfs技术上肯定是有所进步的，不然它的出现就没有意义了。

**initramfs的根本上的不同，就是它跟内核被打包成一个文件了。**

该cpio格式的文件被链接进了内核中特殊的数据段.init.ramfs上，其中全局变量`__initramfs_start和__initramfs_end`分别指向这个数据段的起始地址和结束地址。内核启动时会对.init.ramfs段中的数据进行解压，然后使用它作为临时的根文件系统。



**linux对所有文件的读写都会在内存里做缓存，这样效率会高很多。**
ramfs直接利用了linux内核的高速缓存机制，做成一个大小可以动态变化的基于内存的文件系统。ramfs工作在vfs层，不能被格式化，可以创建多个，默认情况下，ramfs最多用到系统内存的一半。可以在编译内核的时候修改。

rootfs是一个特定的ramfs实例，始终存在于系统中，是系统的根。

initrd是一个被压缩过的小型根目录。系统启动时，initrd文件被载入到内存，内核然后把解压后的initrd挂载为根目录。然后执行/init脚本。在/init脚本里，再去挂载真正的根文件系统。
看内核里的代码，大概的流程是这样的。

```
start_kernel-->
	rest_init-->
		kernel_init-->
			kernel_init_freeable
				打开console设备。得到0/1/2这3个fd
				ramdisk_execute_command = "/init";
			执行ramdisk_execute_command
```



我们要得到initramfs的镜像文件，内核目录下的脚本可以完成：

```
./scripts/gen_initramfs_list.sh -o ramfs.gz ../ramfs/  
```

#initrd和initramfs

##区别

1、原理不同。

initrd利用ramdisk技术，把内存的一部分实现为/dev/ram设备。然后把根目录挂载到/dev/ram上。从原理上讲，是一个真正的rootfs。需要指定在uboot参数里指定root=/dev/ram这样。



2、文件系统上的差异。

**initrd，用ext2格式的文件系统。**

initramfs，使用kernel直接支持的rootfs格式（有这种格式？）的文件系统。

3、initrd从内核2.4版本支持，initramfs从2.6版本开始支持。

## 优缺点

1、initramfs省去了创建/dev/ram、mount文件系统、切换根目录的过程。启动速度会更快。

initramfs处理也更加简单。

2、initramfs使用的是cpio包，会比较大。

# initramfs分类

1、独立文件。

例如我在/boot下可以看到：

```
-rw-r--r-- 1 root root  36M 1月  18 23:16 initrd.img-4.4.0-79-generic
```

2、集成到kernel image里。

靠全局变量`__initramfs_start`来找到。

内核配置需要指定这个：

```
CONFIG_INITRAMFS_SOURCE="/path/to/rootfs/"
```





```
#define INITRD_MINOR 250
```

```
CONFIG_BLK_DEV_INITRD=y
CONFIG_INITRAMFS_SOURCE=""
CONFIG_RD_GZIP=y
```

```
obj-$(CONFIG_BLK_DEV_INITRD)   += initramfs.o
obj-y                          += noinitramfs.o //这个里面就一个函数default_rootfs
```



boot分区自带recovery mode的ramdisk;

system分区包含了Android系统的rootfs;

启动中，如何选择加载boot分区的ramdisk还是system分区的rootfs呢？
答案是由kernel的命令行参数skip_initramfs来决定。

正常启动的时候，skip_initramfs这个是设置了的。

linux调用populate_rootf**s默认会并加载boot分区自带的ramdisk**（recovery），

但如果do_skip_initramfs被设置为1，则会调用default_rootfs生成一个极小的rootfs：

```
static int __init populate_rootfs(void)
{
	char *err;

	if (do_skip_initramfs) {
		if (initrd_start)
			free_initrd();
		return default_rootfs();//生成一个很小的rootfs。
	}
```

default_rootfs 这个函数很简单，就是做了三件事情：

```
1、创建目录/dev。权限755
2、创建节点/dev/console。
3、创建目录/root。权限700
```



参考资料

1、《Linux启动过程分析》之区别Initramfs与initrd

https://blog.csdn.net/tankai19880619/article/details/16885615

2、安卓8 Android O 进入recovery判断流程

https://blog.csdn.net/shangyexin/article/details/86565711