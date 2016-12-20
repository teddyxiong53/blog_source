---
title: linux的电源管理分析
date: 2016-12-12 19:15:42
tags:
	- linux
	- 电源管理
---
linux的电源管理，有4个名词需要先了解一下：
* standby。可以理解为打盹。只是cpu冻结所有的进程而已。
* sleep。理解为睡觉。把相关内容保存到内存里。
* hibernate。理解为冬眠。把相关内容保存到硬盘里。
* wakeup。从standby、sleep、hibernate这3种状态转为正常状态，叫做唤醒。

hibernate的出现是因为用户的省电和快速开机的需求。hibernate的其中一种实现是Swap Suspend（简写为swsusp），这个实现从内核2.6版本开始引入。
swsusp是一种STD（Suspend To Disk）的实现方法，要可以达到上电后恢复现场的目的。
站在开发者的角度来看，要达到这个目的，系统至少需要保存3种信息：cpu状态、register状态、memory状态。swsusp的swap表示把memory保存到swap分区。
而对于cpu和register的状态，可以先保存到内存里，然后随着内存一起保存到swap分区。但是内核里实际用的是另外一种方法，借助于kernel的cpu suspend框架，suspend时让cpu进入到suspend状态，resume时从这个状态返回。这种方法的实质和前面一种还是一样的。

电源管理的核心内容在kernel/power目录下。用户层的使用接口有/dev/snapshot和/sys/power目录。



