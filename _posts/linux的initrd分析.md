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

# initrd和initramfs

## 区别

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



# buildroot里使用initramfs

BR2_TARGET_ROOTFS_INITRAMFS

看看rdinit和root在内核中是如何被处理的，

如果bootargs设置了rdinit和root，

那么内核在启动阶段解析并分别赋给ramdisk_execute_command和saved_root_name。

```
static int __init rdinit_setup(char *str)
{
	unsigned int i;

	ramdisk_execute_command = str;
	/* See "auto" comment in init_setup */
	for (i = 1; i < MAX_INIT_ARGS; i++)
		argv_init[i] = NULL;
	return 1;
}
__setup("rdinit=", rdinit_setup);
```

当前S400的板子上的启动命令里有这些。

```
rootfstype=ramfs 
 root=/dev/ubi0_0 rootfstype=ubifs init=/sbin/init
```

从vm[linux](https://so.csdn.net/so/search?from=pc_blog_highlight&q=linux).lds.h文件可知，

ramfs根据CONFIG_BLK_DEV_INITRD定义是否使用。

INIT_RAM_FS存放ramfs相关内容，包括.init.ramfs和.init.ramfs.info两个段。



INITRAMFS_IMAGE从哪里来？需要查看/usr/目录下Makefile。

从Makefile中可知，以CONFIG_INITRAMFS_SOURCE对应的rootfs.cpio文件作为输入，调用gen_init_cpio和gen_initramfs_list.sh生成initramfs_data.cpio.gz文件。

然后INITRAMFS_IMAGE对应，/usr/initramfs_data.cpio$(suffix_y)文件。

最终通过.incbin将INITRAMFS_IMAGE编译到initramfs_data.o文件中，即对应.init.ramfs段。

ramfs作为init数据的一部分，位于`__init_begin和__init_end的末端`，在free_initmem()中被释放。

ramfs是以压缩包的形式存放在`__initramfs_start和__initramfs_size`之间，在kernel_init()-->kernel_init_freeable()-->do_basic_setup()-->populate_rootfs()中调用unpack_to_rootfs()中解压。



rootfs其实不是一种实际的文件系统，他根据实际情况可能使用ramfs或者tmpfs。

这里分析rootfs是如何对应ramfs，并且简单介绍ramfs。

下面来看看rootfs文件系统是如何挂载的？rootfs没有自己的固定类型，或者使用ramfs或者使用tmpfs。



BR2_TARGET_ROOTFS_INITRAMFS_LIST

这个变量在./fs/cpio/cpio.mk里被使用。



内核里有这样一个配置项

```
Initial RAM filesystem and RAM disk (initramfs/initrd) support 
```

在./init/Kconfig

help信息写着：initramfs是一个ramfs，被bootloader载入，在正常的启动流程之前，作为root来挂载。

主要是用来载入必要的模块，从而可以挂载真正的rootfs。

挂载了真正的rootfs后，之前的rootfs被move到一个目录下，然后被卸载掉。

initrd主要用来保持kernel不要编译进太多不需要的驱动，而把更多的驱动放在initrd里。

使用initrd的时候，系统的流程是这样的：

```
1、bootloader载入kernel和initrd。
2、kernel把initrd转成一个ram disk，然后把initrd占用的内存释放掉。
3、如果root device不是/dev/ram0，那么就会执行一个change_root的操作（这个是过时的）
4、如果root device是/dev/ram0，那么initrd就被挂载为root
5、执行/sbin/init。这个init可以是二进制，也可以看是脚本。
6、/sbin/init里，挂载真正的root
7、init使用pivot_root来切换root
8、init执行新的rootfs里的/sbin/init来执行真正的初始化流程。
9、initrd被移除。
```

跟boot相关的bootargs有

```
initrd=path
noinitrd
root=/dev/ram0
```



文档在Documentation/initrd.txt里。

如果同时使能了BLK_DEV_RAM，那么就会使能initrd。

Documentation/early-userspace/README

这个文档也要看看。



一般的来说，使用ramdisk并不是一件好事，

系统自己会更加有效的使用可用的内存；

但是，在启动或者制作启动盘时，

使用ramdisk可以很方便的装载软盘等设备上的映象(尤其是安装程序、启动过程中)，

因为在正真使用物理磁盘之前，必须要加载一些必要的模块，

比如文件系统模块，scsi驱动等

(可以参见我的initrd-x.x.x.img文件分析－制作安装程序不支持的根文件系统)。



# noinitrd

noinitrd

(仅当内核配置了选项 CONFIG_BLK_DEV_RAM和CONFIG_BLK_DEV_INITRD)

现在的内核都可以支持initrd了，

引导进程首先装载内核和一个初始化的ramdisk，

然后内核将initrd转换成普通的ramdisk，

也就是读写模式的根文件系统设备。

然后[linux](https://so.csdn.net/so/search?from=pc_blog_highlight&q=linux)rc执行，然后装载真正的根文件系统，之后ramdisk被卸载，最后执行启动序列，比如/sbin/init。

选项noinitrd告诉内核不执行上面的步骤，

即使内核编译了initrd，

**而是把initrd的数据写到 /dev/initrd，**

只是这是一个一次性的设备。



# load_ramdisk=N

如果N＝1，就加载ramdisk；如果N＝0，就不加载ramdisk；默认值为0。

# root dev

```
enum {
	Root_NFS = MKDEV(UNNAMED_MAJOR, 255),
	Root_RAM0 = MKDEV(RAMDISK_MAJOR, 0),
	Root_RAM1 = MKDEV(RAMDISK_MAJOR, 1),
	Root_FD0 = MKDEV(FLOPPY_MAJOR, 0),
	Root_HDA1 = MKDEV(IDE0_MAJOR, 1),
	Root_HDA2 = MKDEV(IDE0_MAJOR, 2),
	Root_SDA1 = MKDEV(SCSI_DISK0_MAJOR, 1),
	Root_SDA2 = MKDEV(SCSI_DISK0_MAJOR, 2),
	Root_HDC1 = MKDEV(IDE1_MAJOR, 1),
	Root_SR0 = MKDEV(SCSI_CDROM_MAJOR, 0),
};
```



initrd-x.x.x.img首先是一个用gzip压缩的文件，

因为内核里包含解压缩的代码，

这主要是为了制作启动盘，

因为启动盘只有1.44M，这个文件的原始大小

是2.9M左右，压缩后大概3、4百K。

这个文件使用mkinitrd命令产生。



先解压，在mount到某个目录下来查看里面的内容。

还可以查看里面的linuxrc脚本的内容。



buildroot里有这样的配置，默认是选配的

 remount root filesystem read-write during boot







# prepare_namespace

从设备文件路径名到处设备标识符，调用mount_root安装根文件系统

CONFIG_AMLOGIC_MODIFY   amlogic的修改用这个宏来包裹的。

```
void __init prepare_namespace(void)
{
	int is_floppy;
#ifdef CONFIG_AMLOGIC_MODIFY
	dev_t res = 0;
	int wait = 80; /* 8s max wait*/
#endif /* CONFIG_AMLOGIC_MODIFY */
```



# uboot配置使用initramfs

使用initramfs的内核启动参数

不需要”initrd=”和”root=”参数,

但是必须在initramfs中创建/init文件或者修改内核启动最后代码(init文件是软连接，指向什么? init -> bin/busybox，否则内核启动将会失败)

```
使用 initrd的内 核启动参数:
initrd=addr,0x400000 root=/dev/ram rw
```

使用initramfs的内核配置(使用initramfs做根文件系统): 

General setup  —>
[*] Initial RAM filesystem and RAM disk (initramfs/initrd) support
(/rootfs_dir) Initramfs source file(s)  //输入根文件系统的所在目录 



当前S400上是这样的内核配置

```
CONFIG_BLK_DEV_INITRD=y
CONFIG_INITRAMFS_SOURCE=""
```

在buildroot的配置里

```
BR2_TARGET_ROOTFS_INITRAMFS_LIST="board/amlogic/common/initramfs/initramfs-49/ramfslist-32-ubi-release"
BR2_TARGET_ROOTFS_CPIO_UIMAGE=y
```

BR2_TARGET_ROOTFS_INITRAMFS_LIST 为什么没有传递给内核呢？



看一个原始的buildroot的fs/cpio里的内容。

有一个init脚本。内容是这样

```
#!/bin/sh
# devtmpfs does not get automounted for initramfs
/bin/mount -t devtmpfs devtmpfs /dev

# use the /dev/console device node from devtmpfs if possible to not
# confuse glibc's ttyname_r().
# This may fail (E.G. booted with console=), and errors from exec will
# terminate the shell, so use a subshell for the test
if (exec 0</dev/console) 2>/dev/null; then
    exec 0</dev/console
    exec 1>/dev/console
    exec 2>/dev/console
fi

exec /sbin/init "$@"
```

cpio.mk里

```
define ROOTFS_CPIO_CMD
	cd $(TARGET_DIR) && \
	find . \
	| LC_ALL=C sort \
	| cpio $(ROOTFS_CPIO_OPTS) --quiet -o -H newc \
	> $@
endef
```

那就是把target下面的都打包到cpio里去了。

而amlogic的，会有一个blacklist，去掉不需要打包进去的内容。

去掉了大部分独立的可执行文件。去掉了一些动态库。但是我看把C库都去掉了。

这个就有点奇怪了。



这个目录下，有个ramdisk目录

```
buildroot/board/amlogic/common/ota/ramdisk$ tree
.
├── etc
│   ├── hotplug
│   │   ├── insert.sh
│   │   └── remove.sh
│   ├── init.d
│   │   ├── rcS
│   │   └── S01swupdate
│   └── mdev.conf
└── init
```

如果在buildroot里要单独编译得到ramdisk，执行

```
make rootfs-cpio-rebuild
```

就可以了。

```
Image Name:   
Created:      Wed Dec 22 17:24:05 2021
Image Type:   AArch64 Linux RAMDisk Image (uncompressed)
Data Size:    2818665 Bytes = 2752.60 KiB = 2.69 MiB
Load Address: 00000000
Entry Point:  00000000
```



参考资料

1、

https://blog.csdn.net/androidstar_cn/article/details/53165941

# 参考资料

1、《Linux启动过程分析》之区别Initramfs与initrd

https://blog.csdn.net/tankai19880619/article/details/16885615

2、安卓8 Android O 进入recovery判断流程

https://blog.csdn.net/shangyexin/article/details/86565711

3、linux 内核 ramdisk,使用 RAMDISK的参数

https://blog.csdn.net/weixin_33387339/article/details/116642946

4、

https://www.cxybb.com/article/hellfly2000/1940267