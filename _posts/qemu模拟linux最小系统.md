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
make -j12 ARCH=arm CROSS_COMPILE= arm-linux-gnueabihf-
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
`make -j12 ARCH=arm CROSS_COMPILE= arm-linux-gnueabihf-`
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





