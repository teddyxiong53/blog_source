---
title: qemu之mini2440环境搭建
date: 2018-03-24 12:02:30
tags:
	- qemu

---



#编译定制的qemu

1、下载qemu源代码。

http://repo.or.cz/w/qemu/mini2440.git/snapshot/HEAD.tar.gz

这个压缩包才3M多。

2、配置。

解压后，进入到对应目录。

```
./configure --target-list=arm-softmmu
```

报了这个错误。

```
QEMU requires SDL or Cocoa for graphical output
```

这么解决：

```
sudo apt-get install sdl-dev
```

然后再配置。通过。

3、编译。

```
make -j4
```

报错：

```
/usr/bin/ld: vl.o: undefined reference to symbol 'timer_settime@@GLIBC_2.3.3'
//lib/x86_64-linux-gnu/librt.so.1: error adding symbols: DSO missing from command line
```

https://stackoverflow.com/questions/18286738/undefined-reference-to-symbol-timer-settimeglibc-2-3-3

这里有解决方法，原因是没有连接librt。改一下Makefile.target就好了。

```
LIBS+=-lz
LIBS+=-lrt  #加上这一行。
```

编译通过了。

```
teddy@teddy-ubuntu:~/work/qemu-2440/mini2440$ make -j4
make[1]: Nothing to be done for 'all'.
  LINK  arm-softmmu/qemu-system-arm
```

# 编译对应的uboot

1、下载。

http://repo.or.cz/w/u-boot-openmoko/mini2440.git/snapshot/HEAD.tar.gz

2、配置。

```
make mini2440_config
```

3、编译。

```
make ARCH=arm CROSS_COMPILE=arm-none-eabi-  -j4 V=1
```

先是报错了。说mkimage.c里用到的一个函数找不到。其实我没有必要编译这个文件的。

我的Ubuntu里安装了mkimage工具了。于是到tools/Makefile里，把对mkimage 的编译注释掉。

再编译就好了。

# 编译对应的kernel

1、下载源代码。

https://mirrors.edge.kernel.org/pub/linux/kernel/v2.6/

选择2.6.35.1 的代码。

理由是我之前看的就是这个版本的。

2、配置编译。

```
make ARCH=arm CROSS_COMPILE=arm-none-eabi- mini2440_defconfig
make ARCH=arm CROSS_COMPILE=arm-none-eabi- uImage -j4
```

报错：

```
Can't use 'defined(@array)' (Maybe you should just omit the defined()?) at kernel/timeconst.pl line 373.
/home/teddy/work/qemu-2440/kernel/linux-2.6.35.1/kernel/Makefile:138: recipe for target 'kernel/timeconst.h' failed
make[1]: *** [kernel/timeconst.h] Error 255
```

https://stackoverflow.com/questions/41980796/cant-use-definedarray-warning-in-converting-obj-to-h

好像说是perl的一个bug。我把kernel/timeconst.pl line 373.的

```
defined(@array)' 改成 @array'再看。
```

果然就可以了。



# 运行测试

现在东西其实还没有准备好，但是我们先试一下已经有的东西，能不能用。

```
./qemu/arm-softmmu/qemu-system-arm -M mini2440 -kernel  ./uboot/uboot/u-boot.bin -serial stdio
```

说不支持。

我用gdb调试qemu。

看到居然把参数解析成了这样。

```
find_machine (name=0x7fffffffe631 "mini2440 -kernel")
```

我仔细看了一下，我的"mini2440 -kernel"中间居然不是一个空格。这种情况都出现了。

改成空格。再试一下。

```
teddy@teddy-ubuntu:~/work/mini2440-lab$ ./qemu/arm-softmmu/qemu-system-arm -M mini2440 -kernel  ./uboot/uboot/u-boot 
mini2440_init: Boot mode: NAND
Segmentation fault (core dumped)
```

说要从nand启动。

我暂时不管uboot的了。看看直接启动kernel的。

```
qemu: fatal: Trying to execute code outside RAM or ROM at 0x34000000
```

在这篇文章找到解决方法。

https://blog.csdn.net/susubuhui/article/details/7414236

这个确实是有点奇怪。是需要把u-boot.bin也拷贝到qemu/mini2440目录下。

我们停一下。回头梳理一下。这个执行过程是什么。

```
cmd="$base/../arm-softmmu/qemu-system-arm \
	-M mini2440 $* \
	-serial stdio \
	-mtdblock "$name_nand" \
	-kernel "$base/uImage" \
	-show-cursor \
	-usb -usbdevice keyboard -usbdevice mouse \
	-net nic,vlan=0 \
	-net tap,vlan=0,ifname=tap0 \
	-monitor telnet::5555,server,nowait"
```

命令完全没有提到u-boot.bin。看了是c代码里估计有什么处理。默认都是从那边读取过来的。

现在用上面的这个cmd，可以启动到kernel了。

但是会挂掉。现在我们还没有做rootfs呢。

我们这里用nfs的方式来做。

我们在qemu/mini2440目录下，新建2个脚本文件。qemu-ifup、qemu-ifdown。

qemu-ifup

```
#!/bin/sh
echo "qemu if up"
ifconfig $1 192.168.1.1
```

qemu-ifdown

```
#!/bin/sh
echo "Close tap!"
sudo ifconfig $1 192.168.1.1 down
```

现在修改cmd为：

```
cmd="$base/../arm-softmmu/qemu-system-arm \
	-M mini2440 $* \
	-serial stdio \
	-mtdblock "$name_nand" \
	-kernel "$base/uImage" \
	-show-cursor \
	-usb -usbdevice keyboard -usbdevice mouse \
	-net nic,vlan=0 \
	-net tap,vlan=0,ifname=tap0,script=$base/qemu-ifup,downscript=./qemu-ifdown \
	-monitor telnet::5555,server,nowait"
```

在mini2440-lab根目录新建nfs目录。现在目录结构：

```
teddy@teddy-ubuntu:~/work/mini2440-lab$ tree -L 1
.
├── kernel
├── Makefile
├── nfs
├── qemu
└── uboot
```

我们需要把这个nfs目录加到我们Ubuntu的nfs server的配置文件里去，不然不能被使用。

```
/home/teddy/work/mini2440-lab/nfs *(rw,sync,no_subtree_check,no_root_squash)
```

配置后，把nfs访问重启。

然后启动qemu。居然黑屏了。

我的虚拟机的ip变了。

这个估计是导致网络发生变化导致的。

重启Ubuntu。

继续执行，还是出现kernel panic。是这里有个空指针。我进去看代码是一个函数是空指针。

```
Unable to handle kernel NULL pointer dereference at virtual address 00000000
pgd = c0004000
[00000000] *pgd=00000000
Internal error: Oops: 80000005 [#1]
last sysfs file: 
Modules linked in:
CPU: 0    Not tainted  (2.6.35.1 #1)
PC is at 0x0
LR is at s3c_gpio_setpull+0x58/0x74
pc : [<00000000>]    lr : [<c0034428>]    psr: 80000093
sp : c3c23f68  ip : 00000001  fp : 00000000
r10: 00000000  r9 : 00000000  r8 : 00000000
```



入口文件是arch/arm/amch-s3c2440/mach-mini2440.c里。

gpio是在mini2440_init里配置的。

暂时看不出什么。我把那个空指针的地方，先判断非空再调用。先这样看看。

这样改了，

```
static inline int s3c_gpio_do_setpull(struct s3c_gpio_chip *chip,
				      unsigned int off, s3c_gpio_pull_t pull)
{
	if(chip->config->set_pull) {
		return (chip->config->set_pull)(chip, off, pull);
	}
	return 0;
}
```

至少不会挂死了。

现在是跑到init那里了。

现在把nfs的环境变量设置上。跑起来。卡住了。在这个位置。

```
JFFS2 version 2.2. (NAND) © 2001-2006 Red Hat, Inc.
ROMFS MTD (C) 2007 Red Hat, Inc.
msgmni has been set to 118
alg: No test for stdrng (krng)
io scheduler noop registered
io scheduler deadline registered
io scheduler cfq registered (default)
```

之前uboot里的net/nfs.c里。有个超时时间是需要修改的，我还没改。

本来是2，改成这么多。

```
#define NFS_TIMEOUT 200000UL
```

重新编译uboot。

这样再试，还是卡住。

我看ifconfig，我的Ubuntu的tap0网卡地址并没有被配置为我要的ip值。

往前面看信息。

```
W: /etc/qemu-ifup: no bridge for guest interface found
```

算了，我还是不用nfs的方式了。

现在已经模拟出了一个nand。就把系统烧到nand里。

这个flashimg工具可以用来把uboot、kernel、rootfs进行烧到一个nand.bin文件里。

https://github.com/teddyxiong53/flashimg

下载编译安装好。

制作的命令是这样的。

```
flashimg -s 64M -t nand -f nand.bin -p uboot.part -w boot,u-boot.bin -w kernel,uImage -w root,rootfs.jffs2 -z 512 
```

运行的命令是这样的。

```
./qemu-system-arm -M mini2440 -serial stdio -mtdblock nand.bin -usbdevice mouse
```

现在我们还差rootfs没有制作。

我用一个之前的目录来做出rootfs.jffs2就好了。

```
mkfs.jffs2 -n -s 2048 -e 128KiB -d rootfs -o rootfs.jffs2 
```

然后用flashimg的时候，提示没有uboot.part。原来这个是一个分区指导文件。

看一下flashimg的源代码，找到格式。用上面的命令生成。

```
teddy@teddy-ubuntu:~/work/mini2440-lab/image$ tree
.
├── nand.bin
├── rootfs.jffs2
├── u-boot.bin
├── uboot.part
└── uImage
```

我的uboot.part是这么写的。

```
boot     0x100000   0x0    
kernel  0x500000   0x100000
root  0x3000000 0x600000
```

然后启动。

```
/arm-softmmu/qemu-system-arm -M mini2440 -serial stdio -mtdblock ../image/nand.bin 
```

在uboot里输入这些命令。

```
MINI2440 # nboot kernel 
MINI2440 # setenv bootargs root=/dev/mtdblock3 rootfstype=jffs2 console=ttySAC0,115200  mini2440=3tb
MINI2440 # saveenv 
MINI2440 # bootm 
```

但是我的在nboot kernel后，提示：

```
Loading from NAND 64MiB 3,3V 8-bit, offset 0x60000
** Unknown image type
```

为什么偏移量是0x60000，少了一个0呢？

这个板子的内存是0x3000 0000到0x3400 0000，总共64M。

我现在用nand read来做。载入地址是这个。

```
Load Address: 30008000
Entry Point:  30008000
```

读出来的内容是对的。说明做nand.bin没有问题。

```
MINI2440 # n
  nm nboot nand nfs
MINI2440 # nand read 0x30008000 0x100000 0x500000

NAND read: device 0 offset 0x100000, size 0x500000
 5242880 bytes read: OK
MINI2440 # md 0x30008000 0x20
30008000: 56190527 10f8dbff 5002b65a b8e31f00    '..V....Z..P....
30008010: 00800030 00800030 974f04f1 00020205    0...0.....O.....
30008020: 756e694c 2e322d78 35332e36 0000312e    Linux-2.6.35.1..
```

现在执行。

```
Starting kernel ...

qemu: fatal: Trying to execute code outside RAM or ROM at 0x00000004

R00=00000000 R01=000007cf R02=30000100 R03=30000000
R04=30008000 R05=00000000 R06=33fbe5a8 R07=33d5ffb8
R08=33d5ffdc R09=fff31250 R10=30000100 R11=00000000
R12=00000000 R13=00000000 R14=3000801c R15=00000004
```

这又是为什么啊。

知道了。我不应该把uImage直接读到0x30008000的位置，这个位置uboot正在用呢。

往后放。放到16M的位置。

```
nand read 0x31000000 0x100000 0x500000
```

现在再启动。现在可以进入到kernel了，但是还是挂了。

```
last sysfs file: 
Modules linked in:
CPU: 0    Not tainted  (2.6.35.1 #4)
PC is at kmem_cache_alloc+0x30/0x90
LR is at con_insert_unipair+0x90/0xdc
pc : [<c008a418>]    lr : [<c01a2ce8>]    psr: a0000093
sp : c3c23f18  ip : ffffffff  fp : 00000001
r10: c03e9d68  r9 : 00000012  r8 : c3d60480
r7 : a0000013  r6 : c03d239c  r5 : ffffffff  r4 : 000000d0
r3 : 00000000  r2 : c03dc8e4  r1 : 000000d0  r0 : c03d239c
Flags: NzCv  IRQs off  FIQs on  Mode SVC_32  ISA ARM  Segment kernel
Control: c0007177  Table: 30004000  DAC: 00000017
Process swapper (pid: 1, stack limit = 0xc3c22270)
```

我试着去掉了bootargs里的mini2440=3tb。现在这样来执行。

```
nand read 0x31000000 0x100000 0x500000
setenv bootargs root=/dev/mtdblock3 rootfstype=jffs2 console=ttySAC0,115200  mem=32m
bootm 0x31000000
```

还是卡在这里。

```
msgmni has been set to 118
alg: No test for stdrng (krng)
io scheduler noop registered
io scheduler deadline registered
io scheduler cfq registered (default)
```

慢慢调整为我熟悉的方式。

直接-kernel带上zImage来启动。

环境变量在qemu那里用append来指定。

或者我换一个kernel版本看看。

我用4.4的看看。

直接从kernel启动，在这个定制的qemu上还是不可能的。

那只能希望4.4的kernel可以正常启动。

4.4的kernel可以启动走下去。

可以，现在报的错是jffs2里的问题。

读到的信息。

```
at24 0-0050: 1024 byte 24c08 EEPROM, writable, 16 bytes/write
s3c24xx-nand s3c2440-nand: Tacls=1, 9ns Twrph0=3 29ns, Twrph1=2 19ns
s3c24xx-nand s3c2440-nand: NAND soft ECC
nand: device found, Manufacturer ID: 0xec, Chip ID: 0x76
nand: Samsung NAND 64MiB 3,3V 8-bit
nand: 64 MiB, SLC, erase size: 16 KiB, page size: 512, OOB size: 16
Creating 4 MTD partitions on "nand":
0x000000000000-0x000000040000 : "u-boot"
ftl_cs: FTL header not found.
0x000000040000-0x000000060000 : "u-boot-env"
ftl_cs: FTL header not found.
0x000000060000-0x000000560000 : "kernel"  我很奇怪这里。我指定的位置是1M开始的地方。
ftl_cs: FTL header not found.
0x000000560000-0x000004000000 : "root"
```

那我就按照这个来写uboot.part文件。

```
nand read 0x31000000 0x60000 0x500000
setenv bootargs root=/dev/mtdblock3 rootfstype=jffs2 console=ttySAC0,115200  mem=32m
bootm 0x31000000
```

还是一样的错误。

我把文件系统缓存yaffs2的看看。

用nfs的看看。之前不用nfs，是以为是nfs导致了卡住。



现在这样操作：



```
Freeing unused kernel memory: 164K (c055f000 - c0588000)
Kernel panic - not syncing: Attempted to kill init! exitcode=0x00000004
```

网上说这个问题的原因可能是：

1、busybox要编译为static的。我试了，还是不行。

2、eabi编译。

0004这个错误码是非法指令的意思。



我倒是非常怀疑EABI的版本跟arm核心的版本的匹配问题。

编译的busybox是EABI5的。

```
teddy@teddy-ubuntu:~/work/mini2440-lab/nfs$ file ./bin/busybox 
./bin/busybox: ELF 32-bit LSB executable, ARM, EABI5 version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=d4e01e912d3cad19a65b18f492da0c58ef690bc2, stripped
```



我看之前的编译的工具链都是带hf（硬浮点）的。我安装这个看看。

```
 sudo apt-get install gcc-5-arm-linux-gnueabi
  sudo apt-get install gcc-arm-linux-gnueabi
```



现在多试几次。居然nfs就不通了。看arp -a里，解析不到对应的mac地址的。

之前这个问题，我重启一下Ubuntu就好了。

现在重启也不好。 

现在主要目的是通。

所以就还是回到jffs这个上面来。



我先不急着往下走。在uboot里查看一些信息。

```
MINI2440 # mtdparts 

device nand0 <mini2440-nand>, # parts = 4
 #: name                        size            offset          mask_flags
 0: u-boot              0x00040000      0x00000000      0
 1: env                 0x00020000      0x00040000      0
 2: kernel              0x00500000      0x00060000      0
 3: root                0x03aa0000      0x00560000      0

active partition: nand0,0 - (u-boot) 0x00040000 @ 0x00000000

defaults:
mtdids  : nand0=mini2440-nand
mtdparts: <NULL>
```



我带上-sd参数来启动。

在uboot里，可以看到SD卡的东西。

```
MINI2440 # mmcinit 
mmc: Probing for SDHC ...
mmc: SD 2.0 or later card found
trying to detect SD Card...
Manufacturer:       0xaa, OEM "XY"
Product name:       "QEMU!", revision 0.1
Serial number:      3735928559
Manufacturing date: 2/2006
CRC:                0x0c, b0 = 1
READ_BL_LEN=15, C_SIZE_MULT=0, C_SIZE=3453
size = 0
SD Card detected RCA: 0x4567 type: SD
```

我可以尝试一下，从SD卡进行挂载文件系统。

设置对应的bootarg为：

```
mmcinit; nand read 0x31000000 0x60000 0x500000;set bootargs noinitrd root=/dev/mmcblk0 rootfstype=ext2 rootwait rw console=ttySAC0,115200;bootm 0x31000000
```

但是这样，在kernel里找不到SD卡。开在这里。

```
  No soundcards found.
Waiting for root device /dev/mmcblk0...
```

看来此路不同。

```
s3c24xx-nand s3c2440-nand: Tacls=1, 9ns Twrph0=3 29ns, Twrph1=2 19ns
s3c24xx-nand s3c2440-nand: NAND soft ECC
nand: device found, Manufacturer ID: 0xec, Chip ID: 0x76
nand: Samsung NAND 64MiB 3,3V 8-bit
nand: 64 MiB, SLC, erase size: 16 KiB, page size: 512, OOB size: 16
```

看nand的信息。擦除块大小是16K，页大小是512字节。oob是16字节。

我前面做nand.bin的时候，相关数据对吗？

```
mkfs.jffs2 -n -s 2048 -e 128KiB -d rootfs -o rootfs.jffs2 
```

改成这样：

```
mkfs.jffs2 -n -s 512 -e 16KiB -d rootfs -o rootfs.jffs2 

```

再用从nand启动的。

现在可以进入到命令行了。

但是会打印很多的这种内容。

感觉是oob的问题。

```
Hardware name: MINI2440
Workqueue: events_long delayed_wbuf_sync
[<c000f608>] (unwind_backtrace) from [<c000d250>] (show_stack+0x10/0x14)
[<c000d250>] (show_stack) from [<c001751c>] (warn_slowpath_common+0x74/0xac)
[<c001751c>] (warn_slowpath_common) from [<c00175f0>] (warn_slowpath_null+0x1c/0x24)
[<c00175f0>] (warn_slowpath_null) from [<c028d7cc>] (nand_wait+0x110/0x138)
[<c028d7cc>] (nand_wait) from [<c0289910>] (nand_write_oob_std+0x64/0x70)
[<c0289910>] (nand_write_oob_std) from [<c028ae84>] (nand_do_write_oob+0x1b4/0x218)
[<c028ae84>] (nand_do_write_oob) from [<c028bd38>] (nand_write_oob+0xa4/0xb8)
[<c028bd38>] (nand_write_oob) from [<c01a26b0>] (jffs2_write_nand_cleanmarker+0x98/0xe8)
[<c01a26b0>] (jffs2_write_nand_cleanmarker) from [<c019ee4c>] (jffs2_erase_pending_blocks+0x548/0x69c)
[<c019ee4c>] (jffs2_erase_pending_blocks) from [<c019d900>] (jffs2_garbage_collect_pass+0x1a0/0x668)
[<c019d900>] (jffs2_garbage_collect_pass) from [<c01a1c40>] (jffs2_flush_wbuf_gc+0xb4/0x13c)
[<c01a1c40>] (jffs2_flush_wbuf_gc) from [<c0029dfc>] (process_one_work+0x114/0x350)
[<c0029dfc>] (process_one_work) from [<c002a090>] (worker_thread+0x58/0x4e0)
[<c002a090>] (worker_thread) from [<c002ef54>] (kthread+0xc0/0xdc)
[<c002ef54>] (kthread) from [<c000a490>] (ret_from_fork+0x14/0x24)
---[ end trace 7fb1aae3c58a6e1e ]---
------------[ cut here ]------------
WARNING: CPU: 0 PID: 289 at drivers/mtd/nand/nand_base.c:934 nand_wait+0x110/0x138()
Modules linked in:
CPU: 0 PID: 289 Comm: kworker/0:1 Tainted: G        W       4.4.34 #2
Hardware name: MINI2440
Workqueue: events_long delayed_wbuf_sync
[<c000f608>] (unwind_backtrace) from [<c000d250>] (show_stack+0x10/0x14)
[<c000d250>] (show_stack) from [<c001751c>] (warn_slowpath_common+0x74/0xac)
[<c001751c>] (warn_slowpath_common) from [<c00175f0>] (warn_slowpath_null+0x1c/0x24)
[<c00175f0>] (warn_slowpath_null) from [<c028d7cc>] (nand_wait+0x110/0x138)
[<c028d7cc>] (nand_wait) from [<c028e99c>] (nand_erase_nand+0x1ec/0x324)
[<c028e99c>] (nand_erase_nand) from [<c0271a00>] (part_erase+0x3c/0x9c)
[<c0271a00>] (part_erase) from [<c019ec28>] (jffs2_erase_pending_blocks+0x324/0x69c)
[<c019ec28>] (jffs2_erase_pending_blocks) from [<c019d900>] (jffs2_garbage_collect_pass+0x1a0/0x668)
[<c019d900>] (jffs2_garbage_collect_pass) from [<c01a1c40>] (jffs2_flush_wbuf_gc+0xb4/0x13c)
[<c01a1c40>] (jffs2_flush_wbuf_gc) from [<c0029dfc>] (process_one_work+0x114/0x350)
[<c0029dfc>] (process_one_work) from [<c002a090>] (worker_thread+0x58/0x4e0)
[<c002a090>] (worker_thread) from [<c002ef54>] (kthread+0xc0/0xdc)
[<c002ef54>] (kthread) from [<c000a490>] (ret_from_fork+0x14/0x24)
```

是不是我需要对nand.bin文件做一些什么操作才可以 啊。

不用。

我觉得我还是改成yaffs的看看。

```
 git clone git://www.aleph1.co.uk/yaffs2
```

没想到mkfs.yaffs2的源代码都很难找到。

不是我要的东西。算了。

在nand上做的事情，至少证明了，busybox编译出来在mini2440上运行是正常 。

我现在再回到nfs上看看。

```
set bootargs noinitrd root=/dev/nfs rw nfsroot=192.168.1.1:/home/teddy/work/mini2440-lab/nfs ip=192.168.1.2:192.168.1.1::255.255.255.0 console=ttySAC0,115200 init=/init mem=32m
```

还是不通。

我参考网上文章，改成tap0网卡一直存在的方式看看。

```
$ sudo tunctl -u $USER -t tap0
$ sudo ifconfig tap0 192.168.0.1
```

然后qemu启停的时候，不要操作tap0了。

```
qemu-system-arm -M mini2440 -serial stdio -mtdblock nand.bin -kernel uImage -net nic -net tap,ifname=tap0,script=no,downscript=no
```



我在Ubuntu上绑定静态ip看看。

```
arp -s 192.168.1.2 08:08:11:18:12:27
```

还是不通。我把nfs重启也没有变化。

看网上别人写得，好像没有碰到什么问题啊。我这怎么这么多问题呢？

我另外起一套环境，重新弄看看。



我觉得没有必要用flashimg来做nand.bin。我自己dd一个出来。

但是怎么进行分区呢？

还是用flashimg。把root分区缩小到16M。

```
nand read 0x31000000 0x60000 0x500000
set bootargs noinitrd root=/dev/mtdblock3   rootfstype=jffs2 mtdparts=mtdparts=nandflash0:256k@0(boot),128k(params),5m(kernel),16m(root) console=ttySAC0,115200  
bootm 0x31000000
```

开机后，还是狂打印。不管。过了一会儿就不打印了。就可以正常操作了。

下次开机，打印就没有那么多了。

先把这套环境上传到github。



加入带界面的。这个只能在Ubuntu的图形界面下用。

1、修改启动qemu的命令。

```
boot-ui:
	$(ROOT_DIR)/qemu/arm-softmmu/qemu-system-arm  -M mini2440 -serial stdio \
	-mtdblock $(ROOT_DIR)/image/nand.bin  \
	-usb -usbdevice keyboard -usbdevice mouse -show-cursor
```

2、修改bootargs。

```
nand read 0x31000000 0x60000 0x500000
set bootargs noinitrd root=/dev/mtdblock3   rootfstype=jffs2 mtdparts=mtdparts=nandflash0:256k@0(boot),128k(params),5m(kernel),16m(root) console=ttySAC0,115200  mini2440=3tb
bootm 0x31000000
```



# 参考资料

1、

https://www.cnblogs.com/jinmu190/archive/2011/03/21/1990698.html

2、

http://bbs.51cto.com/thread-970787-1-1.html