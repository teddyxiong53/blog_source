---
title: Linux之recovery分区
date: 2019-05-16 17:16:11
tags:
	- Linux
---



之前做Linux系统，都没有带recovery分区，所以不是很了解。

现在看rk3308是带recovery分区。了解一下。

从编译脚本看， 是把kernel和rootfs打包成这个镜像的。recovery.img文件。

```
$TOP_DIR/kernel/scripts/mkbootimg --kernel $KERNEL_IMAGE --ramdisk $CPIO_IMG --second $KERNEL_DTB -o $TARGET_IMAGE
```

那什么时候可以进入到recovery分区呢？



rootfs要打开recoverySystem支持。

代码在buildroot/external/recovery目录下。

另外还有external/rkupdate。这个主要是解析update.img文件的。



但是这个根文件分区，也不是完整的。而是一个非常简单的。大部分工具都没有。



需要单独的recovery分区，因为这个分区一般是不进行升级的。



入口文件是recovery.c。



怎样进入到recovery分区呢？

《Rockchip recovery开发指南》

BR2_PACKAGE_RECOVERYSYSTEM 这个是选上的。

目前主系统中**实现调用升级功能**的有两套代码，recoverySystem 与 update，二者使用相同的参
数，均可实现进入 recovery 模式，进行 OTA的升级。

recoverySystem的代码在external目录下。

文件不多。

```
├── bootloader.c
├── bootloader.h
├── main.c
├── Makefile
├── recoverySystem.c
├── recoverySystem.h
├── strlcat.c
├── strlcpy.c
└── update_recv
    ├── DefineHeader.h
    ├── update_recv.c
    └── update_recv.h
```

recoverySystem工具的工作逻辑

```
命令行是这样：
recoverySystem ota /userdata/update_ota.img
可以带2个参数：
	参数1：升级类型。
		ota
		update
			都是调用rebootUpdate(0)
		factory和reset
			都是调用fastoryDataReset()
"/userdata/update.img"默认是这个升级包名字。

"/dev/block/by-name/misc"
BOOTLOADER_MESSAGE_OFFSET_IN_MISC = 16 * 1024;
struct bootloader_message {
    char command[32];      
    char status[32];       
    char recovery[768];    
    char systemFlag[256]   
};                         
是通过往misc分区里写一个消息。
uboot在启动的时候，会检查
```

打包 update.img 固件时需要注意，升级固件不一定要全分区升级，可修改 package-file 文件，

```
boot_a      Image/boot.img
boot_b      Image/boot.img
system_a    Image/rootfs.img
system_b    Image/rootfs.img
```

AB系统也只是内核的boot分区和rootfs这2个有2份而已。

AB系统的就没有recovery分区了。

package-file 中 recovery.img ，一般不升级，也可以打包进去。

但是会在升级的时候特殊处理，先在正常系统里把recovery分区升级了，再重启进入recovery分区升级其他版本。

是为了避免变砖。

misc分区不建议打包。打包也没用，反而容易导致问题。

升级包不要包含userdata.img。



misc分区了解

misc分区的概念来自于Android系统。Linux系统，一般用misc分区来作为系统升级或者恢复出厂时使用。

misc分区在下面这些情况下会被读写：

```
1、uboot会读取misc分区内容，决定是进入正常系统还是recovery。
2、recovery系统：
	读取misc的内容，决定采取什么操作。
```

recovery不同场景下的使用

```
1、第一次开机。
2、恢复出厂。
```



《Rockchip分片升级开发指南》

这个是针对小容量的设备的。靠手机app跟设备在同一个局域网内，一点点把数据发送给设备。

通过 socket 通讯， 获取设备的分区固件版本信息， 以及设置设备 misc 的一些信息， 为在进入 recovery
模式后分片升级做准备。

也可以设备作为热点，手机直接连到设备的方式。

```
正常系统下运行使用：frag_updater -g -d。
Recovery 下运行使用：frag_updater -u -d。
```

但是这个没有看到代码。



参考资料

1、Recovery代码分析之一

https://blog.csdn.net/nbalichaoq/article/details/44035223