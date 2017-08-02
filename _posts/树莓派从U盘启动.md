---
title: 树莓派从U盘启动
date: 2017-04-29 22:24:36
tags:
	- 树莓派
---
背景：
我手里有几个闲置的U盘，也想在树莓派上体验不同的系统。所以想把系统安装到U盘。方便进行系统的切换使用。
前提条件：
已经有SD卡，并且安装好了Raspbian系统。树莓派在SD卡上运行正常。
方便起见，直接用串口线连接到板子。

参考的文章是：https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/msd.md

# 1. 打开板子的从usb启动的配置
```
sudo apt-get update
sudo BRANCH=next rpi-update
```
上面两条命令会更新/boot目录下的start.elf和bootcode.bin这2个文件。
然后打开/boot/config.txt文件。
在这个文件的最后加上一句`program_usb_boot_mode=1`。
然后重启树莓派。
输入下面命令查看只能编程一次的寄存器的值。
```
vcgencmd otp_dump | grep 17:
```
看到的值是`17:3020000a`就是正常的。这样说明树莓派已经打开了usb模式了。
你现在可以把/boot/config.txt文件里加的那句话去掉了。

# 2. 开始U盘相关操作
把U盘插入到usb口上，查看。
```
root@raspberrypi:~# lsblk
NAME        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda           8:0    1 14.9G  0 disk 
└─sda1        8:1    1 14.9G  0 part 
mmcblk0     179:0    0 14.6G  0 disk 
├─mmcblk0p1 179:1    0   63M  0 part /boot
└─mmcblk0p2 179:2    0 14.5G  0 part /
```
现在开始对U盘进行分区操作。就用fdisk来做。分2个区，第一个区大概100M，做boot分区，第二个分区用剩下的全部空间。
然后对这2个分区进行格式化。
```
root@raspberrypi:~# mkfs.vfat -n BOOT -F 32 /dev/sda1
mkfs.fat 3.0.27 (2014-11-12)
root@raspberrypi:~# mkfs.ext4 /dev/sda2
```

# 3. 进行系统复制
我们先看一种简单场景，就是把当前SD卡上的系统复制到U盘上的这种情况，我们这么做的目的就是替代SD卡。






# 4. 直接把系统安装到U盘
这一步是在前面的基础上来做。

把U盘插入到电脑，直接用win32diskimager把镜像写入到U盘，但是要改一些boot分区的内容。不过好在boot分区是fat32的，在windows下可以识别，我们可以在windows下完成这一步。

1、修改config.txt的内容。把之前可以用的那个U盘的内容拷贝过来。

就是在最后增加这几行：

```
program_usb_boot_mode=1
enable_uart=1
start_x=0
```

2、修改cmdline.txt，还是把之前可以用的那个U盘的内容拷贝过来。

就是改成这样：

```
dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/sda2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait
```

3、把start.elf和bootcode.bin文件都替换掉。



# 5. 通过uboot来中转
从`https://github.com/gonzoua/u-boot-pi/archive/rpi.tar.gz`这个地址下载针对树莓派修改过的uboot代码。
在Ubuntu下解压，输入下面命令来编译：
```
 make rpi_b CROSS_COMPILE=arm-raspbian-linux-gnueabi- -j12
```
编译成功后得到u-boot.bin文件。我们把这个文件放到SD卡的boot分区里。
在SD卡的/boot/config.txt里最后加上一行`kernel=u-boot.bin`。
现在我们还是把安装好系统的SD卡插入到树莓派中，重新开机。发现开机开不了了。
把`kernel=u-boot.bin`去掉就好了。说明这样改动当前有问题。







