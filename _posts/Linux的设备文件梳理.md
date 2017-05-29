---
title: Linux的设备文件梳理
date: 2017-05-27 21:15:35
tags:

	- Linux

	- 设备文件

---

Linux下存在各种各样的设备文件，它们的规律是怎么样的？

# 1. 先看字符设备

## 主设备号为0

0：为空设备号预留。

## 主设备号为1

代表了char内存设备

1=mem：直接存取物理内存。

2=kmem：存取经过内核虚拟之后的内存。

3=null：null设备。

4=port：存取io。

5=zero：zero设备。

6：没有。

7=full：full设备。

8=random：随机数设备。

9=urandom：更快的随机数，但是不够安全。

10=aio：异步io通知接口。

11=kmsg。对这个设备的写入都作为printk输出。

## 主设备号为4

代表的是tty设备。

0到63分别代表tty0到tty63 。

## 主设备号为5

代表的是其他的tty设备。

0=tty：当前tty设备。

1=console：控制台设备。

2=ptmx：所有PTY master的复用器。

## 主设备号为7

代表的是虚拟控制台捕捉设备，这些设备可读可写。

0=/dev/vcs：当前虚拟控制台的文本内容。

1=vcs1：tty1的文本内容。

...

63=vcs63：tty63的文本内容。

128=vcsa：当前虚拟控制台的文本/属性内容。

...

##  主设备号为10

代表的是misc设备。

1=psaux：ps/2鼠标。

## 主设备号为13

代表了核心输入设备。

32=/dev/input/mouse0：第1个鼠标。

33=/dev/input/mouse1

...

62=/dev/input/mouse30：第31个鼠标。

63=/dev/input/mice：所有鼠标的统一。

64=/dev/input/event0：第一个事件队列。

## 主设备号为21

代表通用SCSI设备，通常是SCSI光驱。

## 主设备号为29

代表fb设备。

0到31共32个fb设备。

## 主设备号为89

代表I2C设备。



# 2. 再看块设备

## 主设备号为1

代表ramdisk设备。

##  主设备号为4

0=/dev/root：如果rootfs是以只读方式挂载的，那么就不可能创建真正的设备节点，这个时候就用/dev/root这个设备来作为动态分配的主设备的别名。

## 主设备号为7

代表loop设备。

## 主设备号为8

代表了SCSI磁盘。

## 主设备号为9

代表了metadisk设备，也就是RAID了。

0=/dev/md0：第一组metadisk

## 主设备号为11

代表了SCSI的CD-ROM设备。

0=/dev/scd0

## 主设备号为180

代表usb块设备，例如U盘。





