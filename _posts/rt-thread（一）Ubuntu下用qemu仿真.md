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

# 板子对应的资料

http://infocenter.arm.com/help/topic/com.arm.doc.dui0448i/DUI0448I_v2p_ca9_trm.pdf

这个是板子的硬件构成。

1GB的DDR2 SDRAM 。266MHz。

# memory map

我从0地址开始描述：

```
0到64M：可以remap的区域。
0x1000 0000 +128KB：motherboard 外设。
0x1020 0000 0x2000 0000： daughterboard私有的。
0x2000 0000到0x4000 0000:512MB，保留。
0x4000 0000到0x5c00 0000：motherboard外设，一般是memory device。
0x5c00 0000到0x6000 0000:64MB。保留。
0x6000 0000到0x8000 0000： 512M，ddr2
0x8000 0000到0x8200 0000： 64M的可remap区域。
0x8000 0000到0xa000 0000： ddr2,512M。
0xa000 0000到0xe000 0000： daughterboard私有 。

```

外设的寄存器分布：

在0x1020 0000这个位置。

```
DAP ROM
ETB
CTI
TPIU

```



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

但是每次启动都要输入这些命令，是挺烦人的，我们再当前目录新建一个gdb_cmd.txt文件。

```
file rtthread.elf 
target remote:1234
b rtthread_startup
c
```

然后执行：

```
arm-none-eabi-gdb 0<gdb_cmd.txt 
```

但这样会自动退出来。不行。

把gdb_cmd.txt改名为.gdbinit。

直接指向arm的gdb。会提示：

```
warning: File "/home/teddy/work/rt-thread/rt-thread/bsp/qemu-vexpress-a9/.gdbinit" auto-loading has been declined by your `auto-load safe-path' set to "$debugdir:$datadir/auto-load".
```

意思是路径不安全。

要解决这个问题。有2个方法。

默认是~/.gdbinit这个是默认的安全位置。放到这里就行。但是这个会影响全局。不想这么做。

简单的解决方法：

1、先启动gdb。

2、然后输入一句：source .gdbinit就好了。



# gdb跟读一下代码

1、rt_cpu_vector_set_base

这个在cpu/cp15_gcc.S里。

gdb查看汇编里的寄存器是用 `p $r0`这样来引用的。

默认打印的是十进制，如果要看十六进制，则这样：`p/x $r0`。

2、动态内存是8M。

```
#define HEAP_BEGIN      ((void*)&__bss_end)
#define HEAP_END        (void*)(0x60000000 + 8 * 1024 * 1024)
```

3、

先是board level的初始化。

rt_hw_timer_init

rt_hw_uart_init

# 看看SD卡

vexpress-a9默认配置文件系统最多2个，我改为8个。在rtconfig.h里改。gdb看到排序是这样的。

```
(gdb) p filesystem_operation_table
$2 = {0x600696d8 <_device_fs>, 0x6006960c <_romfs>, 0x600697e4 <_ramfs>, 0x600699a8 <dfs_elm>, 0x0, 0x0, 0x0, 0x0}
```

这个顺序是INIT_COMPONENT_EXPORT初始化决定的：

```
dfs_elm.c (rt-thread\components\dfs\filesystems\elmfat):INIT_COMPONENT_EXPORT(elm_init);
dfs_nfs.c (rt-thread\components\dfs\filesystems\nfs):INIT_COMPONENT_EXPORT(nfs_init);
dfs_ramfs.c (rt-thread\components\dfs\filesystems\ramfs):INIT_COMPONENT_EXPORT(dfs_ramfs_init);
dfs_romfs.c (rt-thread\components\dfs\filesystems\romfs):INIT_COMPONENT_EXPORT(dfs_romfs_init);
i2c_core.c (rt-thread\components\drivers\i2c):INIT_COMPONENT_EXPORT(rt_i2c_core_init);
module.c (rt-thread\src):INIT_COMPONENT_EXPORT(rt_system_module_init);
rtdef.h (rt-thread\include):#define INIT_COMPONENT_EXPORT(fn)       INIT_EXPORT(fn, "4")

```



另外，需要给qemu加上一个SD卡才行。

1、产生一个1G的空文件。

```
dd if=/dev/zero of=./sd0 bs=1M count=1024
```

2、格式化这个文件。

```
mkfs.vfat ./sd0
```

3、修改qemu启动命令：

```
sudo qemu-system-arm -M vexpress-a9 -net nic,model=lan9118 -net tap -kernel rt-thread/bsp/qemu-vexpress-a9//rtthread.elf -sd ./sd0 -gdb tcp::1234 -S -nographic 2>/dev/null
```

现在就 可以在系统里看到SD卡了。可以进行操作。

启动过程的打印：

```
SD card capacity 1048576 KB
probe mmcsd block device!
file system initialization done!
```



# shell操作

1、默认进来是msh。这个的操作风格跟bash的类似。

2、输入exit，就会推出到finsh。这个是函数式的输入，例如：ls()，后面要带上括号。

3、如果要再进入到msh，输入msh()就可以了。

这些是在rtconfig.h里配置的。

```
#define RT_USING_FINSH
#define FINSH_USING_MSH
#define FINSH_USING_MSH_DEFAULT
```



# 我在另外一台电脑搭建的环境

boot的命令应该写成这样才能运行。

```
sudo qemu-system-arm -M vexpress-a9  -kernel rt-thread/bsp/qemu-vexpress-a9//rtthread.elf -sd ./sd0   -nographic 
```

否则会报错。当前版本的qemu是2.5.0的。

先不管。

