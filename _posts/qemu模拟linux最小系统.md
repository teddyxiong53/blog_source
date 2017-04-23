---
title: qemu模拟linux最小系统
date: 2016-12-09 22:30:24
tags:
	- qemu
	- linux
---
为了更好地学习理解linux的启动过程，在Ubuntu下用qemu模拟制作一个linux最小系统。
嵌入式主要是针对arm平台。我的实验就针对arm平台来做。

# 1. 下载代码，准备环境
下载linux内核源代码和busybox的源代码。网上很好找，就不给链接了。
我的实验电脑环境是Ubuntu15.04 。
安装qemu。
```
sudo apt-get install qemu
```
下载交叉编译工具链。我当前用树莓派的官方的工具链，是现成的，就不用重新下载了。请参考我的树莓派相关文章。
我的kernel代码也是树莓派的版本。版本是`linux-rpi-4.4.y`。
到这里，基本环境就准备好了。
# 2. 编译kernel
编译kernel先要进行合理的配置，我们当前是在qemu上模拟运行，并没有真正的硬件设备，所以配置要选择为qemu支持的。一般用的是`versatile_deconfig`这个配置。versatile是万能的意思。
```
teddy@teddy-ubuntu:~/work/qemu/linux-rpi-4.4.y$ make versatile_defconfig ARCH=arm
```
这样就配置好了。
接下来编译。用12个线程来编译，几分钟就编译好了。
```
make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-
```
编译好之后，在`arch/arm/boot`目录下生产kernel镜像文件。
```
teddy@teddy-ubuntu:~/work/qemu/linux-rpi-4.4.y/arch/arm/boot$ ls
bootp  compressed  dts  Image  install.sh  Makefile  zImage
teddy@teddy-ubuntu:~/work/qemu/linux-rpi-4.4.y/arch/arm/boot$ 
```
现在尝试用qemu运行一下试试。
```
qemu-system-arm -M versatilepb -kernel arch/arm/boot/zImage -nographic
```
然后你会发现你的shell卡住了，没有反应。其实是qemu运行又问题。这时候要先按Ctrl+A，再按一下x，就可以退出qemu。
现在明显运行不正常。说明我们的kernel完全用默认配置还不行。
打开linux-rpi-4.4.y目录下的.config文件。找到`CONFIG_CMDLINE`，改为如下语句：
```
CONFIG_CMDLINE="console=ttyAMA0 root=/dev/ram0"
```
保存退出，重新编译kernel。用`qemu-system-arm -M versatilepb -kernel arch/arm/boot/zImage -nographic`在运行看看。这次又反应了。但是最后出现panic，说找不到根文件系统。这个很正常，因为到目前我们还没有生成根文件系统并传递给qemu呢。

# 3. 用busybox制作initramfs镜像
我们要生成一个ramfs根文件系统，并且在执行init程序的时候，调用其中的shell，这样就可以用这个shell来进行交互了。
当前我们的原则是要最简单的方案，所以把busybox静态编译，就不用考虑动态库的事情了。
使用默认配置：
`make defconfig ARCH=arm`
修改为静态编译：
`make menuconfig`。到界面里选择静态编译，保存退出。
开始编译：
`make -j12 ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf-`
编译成功后，会在busybox目录下得到一个名字为busybox的静态执行文件。
我在编译过程中遇到了头文件的问题。可以把Ubuntu系统的`/usr/include/`下的文件拷贝到busybox的include文件里来解决。

接下来我们要写一个init程序，这个程序是kernel执行的第一个用户态程序，我们要考这个程序来产生可以进行交互的shell。busybox里有自带一个init程序，但是我们可以自己写。
自己写可以用C语言来写，也可以用bash脚本来写。现在简单起见，我们用bash脚本来写。
脚本内容如下：
```
#!/bin/sh
echo
echo "###########################################################"
echo "## THis is a init script for initrd/initramfs            ##"
echo "###########################################################"
echo
PATH="/bin:/sbin:/usr/bin:/usr/sbin"
if [ ! -f "/bin/busybox" ];then
  echo "cat not find busybox in /bin dir, exit"
  exit 1
fi
BUSYBOX="/bin/busybox"
echo "build root filesystem..."
$BUSYBOX --install -s
if [ ! -d /proc ];then
  echo "/proc dir not exist, create it..."
  $BUSYBOX mkdir /proc
fi
echo "mount proc fs..."
$BUSYBOX mount -t proc proc /proc
if [ ! -d /dev ];then
  echo "/dev dir not exist, create it..."
  $BUSYBOX mkdir /dev
fi
# echo "mount tmpfs in /dev..."
# $BUSYBOX mount -t tmpfs dev /dev
$BUSYBOX mkdir -p /dev/pts
echo "mount devpts..."
$BUSYBOX mount -t devpts devpts /dev/pts
if [ ! -d /sys ];then
  echo "/sys dir not exist, create it..."
  $BUSYBOX mkdir /sys
fi
echo "mount sys fs..."
$BUSYBOX mount -t sysfs sys /sys
echo "/sbin/mdev" > /proc/sys/kernel/hotplug
echo "populate the dev dir..."
$BUSYBOX mdev -s
echo "drop to shell..."
$BUSYBOX sh
exit 0
```
有了init程序之后，我们要开始制作根文件系统的目录结构。
我当前的工作目录如下：
```
teddy@teddy-ubuntu:~/work/qemu$ tree -d -L 2
.
├── busybox
│   └── busybox-1.25.1
├── linux-rpi-4.4.y
│   ├── arch
│   ├── block
│   ├── certs
│   ├── crypto
│   ├── Documentation
│   ├── drivers
│   ├── firmware
│   ├── fs
│   ├── include
│   ├── init
│   ├── ipc
│   ├── kernel
│   ├── lib
│   ├── mm
│   ├── net
│   ├── samples
│   ├── scripts
│   ├── security
│   ├── sound
│   ├── tools
│   ├── usr
│   └── virt
└── ramfs
    ├── bin
    ├── dev
    ├── etc
    ├── sbin
    └── usr
```
生成根文件系统目录的命令如下：
```
cd ~/work/qemu/ramfs
mkdir -pv bin dev etc/init.d sbin usr/{bin,sbin}
cp ~/work/qemu/busybox/busybox-1.25.1/busybox bin/
ln -s busybox bin/sh
mknod -m 644 dev/console c 5 1
cp ~/work/qemu/init .
touch etc/init.d/rcS
chmod +x bin/busybox etc/init.d/rcS init
```
最后得到的ramfs的目录结构如下：
```
teddy@teddy-ubuntu:~/work/qemu/ramfs$ tree
.
├── bin
│   ├── busybox
│   └── sh -> busybox
├── dev
│   └── console
├── etc
│   └── init.d
│       └── rcS
├── init
├── sbin
└── usr
    ├── bin
    └── sbin
```
现在目录结构有了，接下来就是把这个目录制作成一个文件系统镜像。
用下面这个命令就可以了。会在当前目录生成一个ramfs.gz的文件。
```
teddy@teddy-ubuntu:~/work/qemu/linux-rpi-4.4.y$ ./scripts/gen_initramfs_list.sh -o ramfs.gz ../ramfs/  
```
这一步，我碰到了问题，总是说local variable不对。仔细一看，发现Ubuntu默认是dash而不是bash。
用这个命令吧默认的shell程序改一下：
`sudo dpkg-reconfigure dash`在弹出来的界面里，选择No就好了。
现在在运行测试一下看看：
```
teddy@teddy-ubuntu:~/work/qemu/linux-rpi-4.4.y$ qemu-system-arm -M versatilepb -kernel arch/arm/boot/zImage -nographic -initrd ramfs.gz
```
这次运行起来了，得到shell，可以进行基本的操作。到这里，一个最简单的linux系统就已经搭建好了。



# 4. 使用这个简单Linux
启动过程打印：
```
Uncompressing Linux... done, booting the kernel.
Booting Linux on physical CPU 0x0
Linux version 4.4.34 (teddy@teddy-ubuntu) (gcc version 4.7.2 (crosstool-NG 1.17.0) ) #6 Mon Dec 19 20:32:31 CST 2016
CPU: ARM926EJ-S [41069265] revision 5 (ARMv5TEJ), cr=00093177
CPU: VIVT data cache, VIVT instruction cache
Machine: ARM-Versatile PB
Memory policy: Data cache writeback
sched_clock: 32 bits at 24MHz, resolution 41ns, wraps every 89478484971ns
Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 32512
Kernel command line: root=/dev/ram console=ttyAMA0
PID hash table entries: 512 (order: -1, 2048 bytes)
Dentry cache hash table entries: 16384 (order: 4, 65536 bytes)
Inode-cache hash table entries: 8192 (order: 3, 32768 bytes)
Memory: 124468K/131072K available (3128K kernel code, 143K rwdata, 828K rodata, 136K init, 124K bss, 6604K reserved, 0K cma-reserved)
Virtual kernel memory layout:
    vector  : 0xffff0000 - 0xffff1000   (   4 kB)
    fixmap  : 0xffc00000 - 0xfff00000   (3072 kB)
    vmalloc : 0xc8800000 - 0xff800000   ( 880 MB)
    lowmem  : 0xc0000000 - 0xc8000000   ( 128 MB)
    modules : 0xbf000000 - 0xc0000000   (  16 MB)
      .text : 0xc0008000 - 0xc03e5644   (3958 kB)
      .init : 0xc03e6000 - 0xc0408000   ( 136 kB)
      .data : 0xc0408000 - 0xc042be80   ( 144 kB)
       .bss : 0xc042be80 - 0xc044afc0   ( 125 kB)
NR_IRQS:224
VIC @f1140000: id 0x00041190, vendor 0x41
FPGA IRQ chip 0 "SIC" @ f1003000, 13 irqs, parent IRQ: 63
clocksource: timer3: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 1911260446275 ns
Console: colour dummy device 80x30
Calibrating delay loop... 686.48 BogoMIPS (lpj=3432448)
pid_max: default: 32768 minimum: 301
Mount-cache hash table entries: 1024 (order: 0, 4096 bytes)
Mountpoint-cache hash table entries: 1024 (order: 0, 4096 bytes)
CPU: Testing write buffer coherency: ok
Setting up static identity map for 0x8400 - 0x8458
VFP support v0.3: implementor 41 architecture 1 part 10 variant 9 rev 0
clocksource: jiffies: mask: 0xffffffff max_cycles: 0xffffffff, max_idle_ns: 19112604462750000 ns
NET: Registered protocol family 16
DMA: preallocated 256 KiB pool for atomic coherent allocations
Serial: AMBA PL011 UART driver
dev:f1: ttyAMA0 at MMIO 0x101f1000 (irq = 44, base_baud = 0) is a PL011 rev1
console [ttyAMA0] enabled
dev:f2: ttyAMA1 at MMIO 0x101f2000 (irq = 45, base_baud = 0) is a PL011 rev1
dev:f3: ttyAMA2 at MMIO 0x101f3000 (irq = 46, base_baud = 0) is a PL011 rev1
fpga:09: ttyAMA3 at MMIO 0x10009000 (irq = 70, base_baud = 0) is a PL011 rev1
clocksource: Switched to clocksource timer3
NET: Registered protocol family 2
TCP established hash table entries: 1024 (order: 0, 4096 bytes)
TCP bind hash table entries: 1024 (order: 0, 4096 bytes)
TCP: Hash tables configured (established 1024 bind 1024)
UDP hash table entries: 256 (order: 0, 4096 bytes)
UDP-Lite hash table entries: 256 (order: 0, 4096 bytes)
NET: Registered protocol family 1
RPC: Registered named UNIX socket transport module.
RPC: Registered udp transport module.
RPC: Registered tcp transport module.
RPC: Registered tcp NFSv4.1 backchannel transport module.
Trying to unpack rootfs image as initramfs...
Freeing initrd memory: 1040K (c4000000 - c4104000)
NetWinder Floating Point Emulator V0.97 (double precision)
futex hash table entries: 256 (order: -1, 3072 bytes)
Installing knfsd (copyright (C) 1996 okir@monad.swb.de).
jffs2: version 2.2. (NAND) © 2001-2006 Red Hat, Inc.
romfs: ROMFS MTD (C) 2007 Red Hat, Inc.
Block layer SCSI generic (bsg) driver version 0.4 loaded (major 254)
io scheduler noop registered
io scheduler deadline registered
io scheduler cfq registered (default)
pl061_gpio dev:e4: PL061 GPIO chip @0x101e4000 registered
pl061_gpio dev:e5: PL061 GPIO chip @0x101e5000 registered
pl061_gpio dev:e6: PL061 GPIO chip @0x101e6000 registered
pl061_gpio dev:e7: PL061 GPIO chip @0x101e7000 registered
clcd-pl11x dev:20: PL110 rev0 at 0x10120000
clcd-pl11x dev:20: Versatile hardware, VGA display
Console: switching to colour frame buffer device 80x60
brd: module loaded
physmap platform flash device: 04000000 at 34000000
physmap-flash.0: Found 1 x32 devices at 0x0 in 32-bit bank. Manufacturer ID 0x000000 Chip ID 0x000000
Intel/Sharp Extended Query Table at 0x0031
Using buffer write method
smc91x.c: v1.1, sep 22 2004 by Nicolas Pitre <nico@fluxnic.net>
smc91x smc91x.0 eth0: SMC91C11xFD (rev 1) at c8a58000 IRQ 57
 [nowait]
smc91x smc91x.0 eth0: Ethernet addr: 52:54:00:12:34:56
mousedev: PS/2 mouse device common for all mice
ledtrig-cpu: registered to indicate activity on CPUs
NET: Registered protocol family 17
Freeing unused kernel memory: 136K (c03e6000 - c0408000)

###########################################################
## THis is a init script for initrd/initramfs            ##
## Author: wengpingbo@gmail.com                          ##
## Date: 2016-12-19 22:34:33 CST                         ##
###########################################################

build root filesystem...
input: AT Raw Set 2 keyboard as /devices/fpga:06/serio0/input/input0
/proc dir not exist, create it...
mount proc fs...
mount devpts...
/sys dir not exist, create it...
mount sys fs...
populate the dev dir...
drop to shell...
sh: can't access tty; job control turned off
/ # input: ImExPS/2 Generic Explorer Mouse as /devices/fpga:07/serio1/input/input2

/ # 
```
查看系统信息。可以看到只有一个核心。一个64M的flash。
```
/ # cat /proc/cpuinfo 
processor       : 0
model name      : ARM926EJ-S rev 5 (v5l)
BogoMIPS        : 686.48
Features        : swp half thumb fastmult vfp edsp java 
CPU implementer : 0x41
CPU architecture: 5TEJ
CPU variant     : 0x0
CPU part        : 0x926
CPU revision    : 5

Hardware        : ARM-Versatile PB
Revision        : 0000
Serial          : 0000000000000000
/ # cat /proc/mtd 
dev:    size   erasesize  name
mtd0: 04000000 00040000 "physmap-flash.0"

/ # mount
rootfs on / type rootfs (rw)
proc on /proc type proc (rw,relatime)
devpts on /dev/pts type devpts (rw,relatime,mode=600)
sys on /sys type sysfs (rw,relatime)
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/ # 
/proc # ps
PID   USER     TIME   COMMAND
    1 0          0:00 {init} /bin/sh /init
    2 0          0:00 [kthreadd]
    3 0          0:00 [ksoftirqd/0]
    5 0          0:00 [kworker/0:0H]
    7 0          0:00 [netns]
    8 0          0:00 [writeback]
    9 0          0:00 [crypto]
   10 0          0:00 [bioset]
   11 0          0:00 [kblockd]
   12 0          0:00 [rpciod]
   13 0          0:00 [kworker/0:1]
   14 0          0:00 [kswapd0]
   15 0          0:00 [fsnotify_mark]
   16 0          0:00 [nfsiod]
   22 0          0:00 [bioset]
   23 0          0:00 [bioset]
   24 0          0:00 [bioset]
   25 0          0:00 [bioset]
   26 0          0:00 [bioset]
   27 0          0:00 [bioset]
   28 0          0:00 [bioset]
   29 0          0:00 [bioset]
   30 0          0:00 [bioset]
   31 0          0:00 [bioset]
   32 0          0:00 [bioset]
   33 0          0:00 [bioset]
   34 0          0:00 [bioset]
   35 0          0:00 [bioset]
   36 0          0:00 [bioset]
   37 0          0:00 [bioset]
   38 0          0:00 [kworker/u2:1]
   41 0          0:00 [bioset]
   42 0          0:00 [kpsmoused]
   43 0          0:00 [deferwq]
   53 0          0:00 /bin/busybox sh
   55 0          0:00 [kworker/u2:2]
   67 0          0:00 [kworker/0:0]
   72 0          0:00 ps
/proc # cat devices 
Character devices:
  1 mem
  2 pty
  3 ttyp
  4 /dev/vc/0
  4 tty
  5 /dev/tty
  5 /dev/console
  5 /dev/ptmx
  7 vcs
 10 misc
 13 input
 14 sound
 29 fb
 90 mtd
128 ptm
136 pts
204 ttyAMA
254 bsg

Block devices:
  1 ramdisk
259 blkext
 31 mtdblock
179 mmc

/proc # cat iomem 
00000000-07ffffff : System RAM
  00008000-003e5643 : Kernel code
  00408000-0044afbf : Kernel data
10000008-1000000c : versatile-leds
  10000008-1000000c : versatile-leds
10002000-10002fff : versatile-i2c.0
10004000-10004fff : fpga:04
10005000-10005fff : fpga:05
10006000-10006fff : fpga:06
  10006000-10006fff : kmi-pl050
10007000-10007fff : fpga:07
  10007000-10007fff : kmi-pl050
10008000-10008fff : arm-charlcd
10009000-10009fff : fpga:09
  10009000-10009fff : fpga:09
1000b000-1000bfff : fpga:0b
10010000-1001ffff : smc91x.0
  10010000-1001000f : smc91x
10120000-10120fff : dev:20
  10120000-10120fff : clcd-pl11x
10130000-10130fff : dev:30
101e4000-101e4fff : dev:e4
  101e4000-101e4fff : dev:e4
101e5000-101e5fff : dev:e5
  101e5000-101e5fff : dev:e5
101e6000-101e6fff : dev:e6
  101e6000-101e6fff : dev:e6
101e7000-101e7fff : dev:e7
  101e7000-101e7fff : dev:e7
101e8000-101e8fff : dev:e8
101f1000-101f1fff : dev:f1
  101f1000-101f1fff : dev:f1
101f2000-101f2fff : dev:f2
  101f2000-101f2fff : dev:f2
101f3000-101f3fff : dev:f3
  101f3000-101f3fff : dev:f3
34000000-37ffffff : physmap-flash.0
  34000000-37ffffff : physmap-flash.0
/proc # cat filesystems 
nodev   sysfs
nodev   rootfs
nodev   ramfs
nodev   bdev
nodev   proc
nodev   tmpfs
nodev   sockfs
nodev   pipefs
nodev   rpc_pipefs
nodev   devpts
        ext2
        cramfs
        minix
nodev   nfs
nodev   nfsd
nodev   jffs2
        romfs
/proc # cat partitions 
major minor  #blocks  name

   1        0       4096 ram0
   1        1       4096 ram1
   1        2       4096 ram2
   1        3       4096 ram3
   1        4       4096 ram4
   1        5       4096 ram5
   1        6       4096 ram6
   1        7       4096 ram7
   1        8       4096 ram8
   1        9       4096 ram9
   1       10       4096 ram10
   1       11       4096 ram11
   1       12       4096 ram12
   1       13       4096 ram13
   1       14       4096 ram14
   1       15       4096 ram15
  31        0      65536 mtdblock0
```

