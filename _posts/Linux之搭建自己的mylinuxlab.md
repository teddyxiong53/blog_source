---
title: Linux之搭建自己的mylinuxlab
date: 2018-03-13 19:44:05
tags:
	- Linux

---



泰晓科技的cloud-lab虽然强大，但是弄得有点复杂，而且还依赖图形界面的linux才能跑起来（需要浏览器来访问vnc）。用起来不方便。脚本也写得比较复杂，难以看清。

所以我决定自己搭建一个简单的环境。框架还是用Makefile来做。

环境：

1、kubuntu16.04.

2、qemu。

3、板子用vexpress c9a4



代码都用最新的，就从cloud-lab里拷贝出来。懒得下载了。



1、先把编译规划一下。

```
├── busybox
├── kernel
├── Makefile
├── rootfs
└── uboot
```



编译指定头文件。

弄出SD卡的fat文件系统。不行，不能建立软链接。换成ext4的。



先分开得到rootfs.img。然后烧录到pflash.img里。

先用initrd跑起来再说。

先把uImage放到pflash.img里读取出来。

bootm 可以带3个参数：

1、kernel地址 

2、initrd地址。

3、dtb地址。



cp 0x40000000 0x60003000 0x500000 ;

只是这样启动。卡住。

bootm 0x60003000

跟我编译的没有关系，换成cloud-lab里的正常的也卡住。我把dtb的也加载进来看看。



把其他东西都弄过来就至少可以跑起来。

所以，接下来就是自己做文件系统，然后挂载真正的文件系统。



dtb的编译。

make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- vexpress-v2p-ca9.dtb

没有问题。



看文件系统的制作。



cpio格式的initrd常用。



http://blog.csdn.net/htttw/article/details/7217706

```
这里插一句，我们完全可以自己写init进程，只要替换_install目录里的init就可以了～～

另外，这里多加一个小实验，模拟ramfs的挂载与卸载过程：

首先准备好一个busybox的ramdisk，我们把它作为真正的根文件系统

然后把它copy到我们自己做的ramfs的/root/下，并修改ramfs的etc/init.d/rcS如下：

#!/bin/sh
mount -a
mount /root/ramdisk /mnt
exec switch_root /mnt /sbin/init

这样最终就mount进我们的根文件系统
```



http://blog.csdn.net/androidstar_cn/article/details/53165941



```
对于ARM来讲，可以透过bootz kernel_addr initrd_address dtb_address的命令来启动内核，即dtb_address作为bootz或者bootm的最后一次参数，第一个参数为内核映像的地址，第二个参数为initrd的地址，若不存在initrd，可以用 -代替。      
```





http://blog.csdn.net/liuchp/article/details/4449256



```
Wrong Ramdisk Image Format
Ramdisk image is corrupt or invalid
```



```
用于大于2.6.1.x以后的内核：

cd initrd
find . | cpio -o -H newc | gzip -c > initrd.img
```



压缩和不压缩，都是说ramdisk格式不对。



退一步，采用initramfs来做。



uboot用的，前面多了64个自己，内容具体是什么？

https://www.denx.de/wiki/DULG/RootFileSystemOnARamdisk

这篇文章的最后有讲到。

```
$ mkimage -T ramdisk -C gzip -n 'Test Ramdisk Image' \
> -d ramdisk.img.gz uRamdisk
Image Name:   Test Ramdisk Image
Created:      Sun Jun 12 16:58:06 2005
Image Type:   PowerPC Linux RAMDisk Image (gzip compressed)
Data Size:    1618547 Bytes = 1580.61 kB = 1.54 MB
Load Address: 0x00000000
Entry Point:  0x00000000
```



```
## Loading init Ramdisk from Legacy Image at 60900000 ...
   Image Name:   Test Ramdisk Image
   Image Type:   PowerPC Linux RAMDisk Image (gzip compressed)
   Data Size:    1786938 Bytes = 1.7 MiB
   Load Address: 00000000
   Entry Point:  00000000
   Verifying Checksum ... OK
No Linux ARM Ramdisk Image
Ramdisk image is corrupt or invalid
```



这篇文章。http://linux-sunxi.org/Initial_Ramdisk

```
mkimage -A arm -T ramdisk -C none -n uInitrd -d /path/to/initrd.img /path/to/uInitrd
```



我改成不压缩的，现在至少可以启动了。

不知道跟加上-A arm有没有关系。

是因为-A arm没有指定导致的，跟压缩没有关系。压缩可以，不压缩也可以。



现在错误是找不到ram0这个设备。

```
input: ImExPS/2 Generic Explorer Mouse as /devices/platform/smb@4000000/smb@4000000:motherboard/smb@4000000:motherboard:iofpga@7,00000000/10007000.kmi/serio1/input/input2
VFS: Cannot open root device "ram0" or unknown-block(0,0): error -6
Please append a correct "root=" boot option; here are the available partitions:	
```

我的电脑上没有这个设备。树莓派上有。

```
pi@raspberrypi:~$ ls /dev/ram0 -l
brw-rw---- 1 root disk 1, 0 Mar 12 15:17 /dev/ram0
```

在文件系统里加上mknod的语句。

但是还是出错。



```
set bootargs 'route=172.17.0.3 root=/dev/ram0 rw console=ttyAMA0 rdinit=/linuxrc'; cp 0x40000000 0x60003000 0x500000 ; cp 0x40500000 0x60900000 0x400000; cp 0x40900000 0x60500000 0x100000; bootm 0x60003000 0x60900000 0x60500000
```



为什么ram0不能被打开呢？

1、节点存在。

2、权限是644 ，我改成777看看。还是不行。

3、改成/dev/ram，也是一样的错误。

4、在root=/dev/ram0 后加上rw。也不行。

错误是-6，表示没有这个设备。为什么会没有这个设备呢？不是明明有的吗？



还是要从cloud-lab里去找方案。

之前的不经过uboot的方式，是直接给qemu指定-initrd参数来做的。这个跟实际开发还是不同的。



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

指定rdinit=/linuxrc。

现在就报错。说没有这个文件。

明明放进去了的。

算了。我写一个脚本算了。

建立目录结构为这样。

```
teddy@teddy-ubuntu:~/work/mylinuxlab/rootfs_origin$ tree
.
├── bin
│   ├── busybox
│   └── sh -> busybox
├── dev
│   ├── console
│   ├── null
│   └── ram0
├── etc
│   └── inittab
└── init
```

init脚本内容如下：

```

```

但是还是不行。我看除了/dev/console之外，其他的都无法访问。

```
xhl -- func:kernel_init_freeable, line:1084 ,rd cmd:/init ,ret:0 
xhl -- func:kernel_init_freeable, line:1086 ,rd cmd:/init ,ret:-2 
xhl -- func:kernel_init_freeable, line:1088 ,rd cmd:/init ,ret:-2 
xhl -- func:kernel_init_freeable, line:1090 ,rd cmd:/init ,ret:-2 
xhl -- func:kernel_init_freeable, line:1092 ,rd cmd:/init ,ret:-2 
```

我为了方便调试，把ramdisk改成不压缩的。

```
xhl -- func:kernel_init_freeable, line:1084 ,rd cmd:/init ,ret:0 
xhl -- func:kernel_init_freeable, line:1086 ,rd cmd:/init ,ret:-2 
xhl -- func:kernel_init_freeable, line:1088 ,rd cmd:/init ,ret:-2 
xhl -- func:kernel_init_freeable, line:1090 ,rd cmd:/init ,ret:0 
xhl -- func:kernel_init_freeable, line:1092 ,rd cmd:/init ,ret:0 
xhl -- func:kernel_init_freeable, line:1097 
```

现在就有几个文件可以访问到了。真是奇怪。

现在是null和ram0访问不到。

```
Failed to execute /init (error -26)
Starting init: /bin/sh exists but couldn't execute it (error -26)
```

