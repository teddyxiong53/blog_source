---
title: rt-thread（一）Ubuntu下用qemu仿真
date: 2018-01-24 09:14:50
tags:
	- rt-thread

---



从github上下载最新的rt-thread，目前是3.0.2。有500M左右。比之前的大了很多。估计是增加了很多板子的支持导致的。

我的这一套是从泰晓科技的cloud-lab里弄出来的。

目录结构这样放。

```
teddy@teddy-ubuntu:~/work/rt-thread$ tree -L 1 -a
.
├── .gitmodules
├── Makefile
└── rt-thread
```

在rt-thread代码这一层目录加一个Makefile。

使用方法：

```
make config：打开menuconfig进行配置。现在版本的rt-thread支持menuconfig了。很好。
make build：编译。
make clean：清除。
make boot：启动。
```

启动时执行的命令是：

```
qemu-system-arm -M vexpress-a9 -net nic,model=lan9118 -net tap -kernel rt-thread/bsp/vexpress-a9/rtthread.elf
```

看看vexpress-a9的这个板子对应程序的做了一些什么事情。

发现找不到main函数了。看汇编文件，发现现在是这样做的：

```
    ldr     pc, _rtthread_startup
_rtthread_startup:
    .word rtthread_startup
```

现在入口就是rtthread_startup函数了。

打算用gdb来调试，发现没有安装arm的gcc工具链。

http://www.veryarm.com/arm-none-linux-gnueabi-gcc 到这个网站上下载。安装。

这里下载下来的是x86的，我的机器是64位的，不能用。

简单起见，用apt-get来安装：

```
sudo apt-get install binutils-arm-none-eabi
```

但是安装了这个，还是没有包含gcc的。

另外单独安装。下载大概500M的内容。

```
sudo apt install gcc-arm-none-eabi
```

然后配置bsp/qemu-vexpress-a9下面的rtconfig.py文件。改一下工具链的前缀。

然后执行make build，有错误。

到rtconfig.h里：

```
1、关闭RTGUI
2、关闭HAVE SELECT
```

编译通过。

# 使用gdb来调试rt-thread

1、在qemu命令后面加上`-gdb tcp::1234 -S`。

```
qemu-system-arm -M $(BOARD) -net nic,model=$(NET_DEV) -net tap -kernel $(BSP_DIR)/rtthread.elf -gdb tcp::1234 -S
```

2、用make boot启动。

3、另外开一个shell窗口。进入到bsp/qemu-vexpress-a9目录。执行下面的内容：

```
$ arm-none-eabi-gdb
(gdb) file rtthread.elf #这个文件就在当前目录下
(gdb) target remote:1234
(gdb) b rtthread_startup
(gdb) c

```

这样就可以进行单步调试了。





