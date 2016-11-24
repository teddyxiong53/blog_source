---
title: dmesg命令的使用
date: 2016-11-08 20:14:30
tags:
	- linux
---
dmesg是Diagnosis Message（诊断信息）的意思。是用来显示kernel ring buffer里的内容，内核会将各种消息存放在这里。你可以输入dmesg命令来查看内容。不过内容一般比较多，你可以`dmesg|less`这样来查看。
dmesg的内容是这种格式，前面方括号里面是时间，以秒为单位。你在linux开机过程中看到的打印就是这个。
```
[    0.219707] cpuidle: using governor menu
[    0.219781] Simple Boot Flag at 0x36 set to 0x1
[    0.219864] ACPI: bus type PCI registered
[    0.219866] acpiphp: ACPI Hot Plug PCI Controller Driver version: 0.5
```
主要应用：
# 1. 查看信息分析问题
例如你的网络出现问题了，就可以`dmesg|grep eth`这样来查看网络相关的诊断信息。

# 2. 查看开机打印
一般开机过程中，来不及细细查看打印，其实dmesg里也记录了开机过程的打印。

# 3. 调试驱动
在内核和驱动里，都是用printk来进行打印，printk有打印基本控制。
默认是4，即只打印WARNING和各种错误的信息。
```
KERN_EMERG  0
KERN_ALERT 1
KERN_CRIT  2
KERN_ERR   3

KERN_WARNING 4
KERN_NOTICE  5
KERN_INFO   6
KERN_DEBUG 7

```
你只需要`dmesg -n 8`，就可以把把所有的printk的打印都显示出来了。这样可以方便通过打印来查看驱动的运行。

在`/proc/sys/kernel/printk`里，分别记录了控制台日志级别、默认的消息日志级别、最低的控制台日志级别和默认的控制台日志级别。
```
teddy@teddy-ubuntu:/proc/sys/kernel$ cat printk
4       4       1       7
```
所以你实际上也可以这样来改变系统的日志级别。
```
echo 8 > /proc/sys/kernel/printk
```




