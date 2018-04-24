---
title: Linux之mkimage
date: 2018-02-11 10:17:37
tags:
	- Linux

---



mkimage的选项：

```
-A：指定ARCH
-O：指定os
-T：指定image type
-C：指定压缩type
-a：指定load addr
-e：指定entry addr
-n：指定镜像的name
-x：设置是否XIP。
-d：从哪个data文件里来数据。
#查看类的：
-l：查看当前镜像的信息。
```

举例：把zImage做成uImage。其实就是加了一个64字节的头部。头部信息就是arch、os这些信息。

```
mkimage -A arm -O linux -T kernel -C none -a 0x30008000 -e 0x30008000 -n "MyLinux" -d zImage uImage
```

-a和-e这2个地址，非常值得讨论一下。

可以有这两种组合：

1、-a等于30008000，-e等于30008040 。

这样的话，只能把uImage放到30008000这里。

对应的命令在这里：

```
./scripts/Makefile.lib:368:      cmd_uimage = $(CONFIG_SHELL) $(MKIMAGE) -A $(UIMAGE_ARCH) -O linux \
```

我们手动修改这里看看。

```
UIMAGE_LOADADDR=0x30008000
UIMAGE_ENTRYADDR=0x30008040
```

然后bootm 0x30008000可以启动。这样我觉得是最好的，没有kernel的搬移。

2、-a等于-e，等于除了30008000 之前的地址。

我当前的默认编译是这样，都是30008000 。

```
Image Name:   Linux-4.4.34
Created:      Tue Mar 27 14:35:22 2018
Image Type:   ARM Linux Kernel Image (uncompressed)
Data Size:    3013424 Bytes = 2942.80 kB = 2.87 MB
Load Address: 30008000
Entry Point:  30008000
```

这种情况之间读取到0x3000 8000上，然后bootm，不行的。



看看压缩选项。当前默认是不压缩的。

我们强制指定为压缩看看。



# linux内核镜像格式

格式有多种，包括：

1、vmlinux。这个elf文件。有100M左右。

2、Image。这个11M。

3、zImage。3.7M。默认用gzip压缩的。

4、bzImage。这个默认不是的。这个是用bzip来压缩的。

5、uImage。在zImage前面再加64字节的头。给uboot专用的。

6、xipImage。放在nor flash里用的。

7、bootpImage。

# linux内核镜像的产生过程

在嵌入式linux里，内核的启动过程，分为2个阶段。

第一阶段是在arch/arm/kernel/head.S里。跟CPU架构有关。跟板子无关。主要是初始化arm核心。

第二阶段就是start_kernel这部分了。



vmlinux先被压缩成Image，然后跟arch/arm/boot/compressed/head.S和arch/arm/boot/compressed/misc.c这2个一起打包成zImage。



所以，运行入口，还是arch/arm/boot/compressed/head.S这个文件。

这里的入口是start标签。



# 参考资料

1、bootm命令中地址参数，内核加载地址以及内核入口地址

https://blog.csdn.net/liangkaiming/article/details/5986680

2、Linux内核镜像格式

https://www.cnblogs.com/big-devil/p/7625880.html