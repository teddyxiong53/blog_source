---
title: 《Linux设备驱动》读书笔记
date: 2019-12-04 14:53:28
tags:
	- 读书笔记
---

# 2. 构造和运行模块

## 设置测试系统

## hello world模块
模块可以使用printk，是因为模块在被insmod后，模块就连接到内核了。
所以可以使用内核的公共符号。

## 核心模块与应用程序的对比

## 用户空间和内核空间

## 内核中的并发
内核的并发是非常常见的。所以写驱动的时候，一定要注意。
1、可能有多个进程在使用我们的驱动。
2、中断。
3、smp。
4、内核可抢占。

所以驱动代码必须是可重入的。

## 当前进程

## 其他细节
双下划线开头的函数，是警告程序员要注意。

## 编译和装载
单个文件：
```
obj-m := hello.o
```
多个文件：
```
hello-objs := hello1.o hello2.o
obj-m := hello.o
```
```
make -C kernel_include_dir M=`pwd` modules
```
modprobe比insmod智能一点，会帮我们把依赖的模块自动加载进去。

## 版本依赖

## 平台依赖

## 预备知识

## 初始化和关闭

## 模块装载竞争

## 模块参数

## 在用户空间编写驱动程序

# 3 字符设备驱动程序

## scull的设计
scull实现了下列设备。
scull0到scull3：
	这4个设备分别由一个全局切持久的内存区域组成。
	全局的含义是：
		如果设备被多次打开，则打开它对应的所有fd，共享这个内存区域。
		所以需要包含并发。
	持有的含义是：
		如果设备关闭后再打开，里面的数据还在。
	测试这4个设备的方法：
		echo "123" > /dev/scull
		cat /dev/scull
		cp /dev/scull /root/1.txt
		
scullpipe0到scullpipe3：
	这个4个fifo与pipe类似。先入先出。
	用来演示阻塞和非阻塞的操作。
	
scullsingle
scullpriv
sculluid
scullwuid
	这4个设备跟scull0类似。
	但是在对open的时机有约束。
	scullsingle
		只允许一个进程使用这个驱动。
	scullpriv
		对每个console是私有的。
		每个进程访问到的内存区域是不同的。
	sculluid
		可以被打开多次，但是每次只能由一个用户打开。
		如果另外一个用户锁定了这个设备，sculluid将会返回Device busy的错误。
	scullwuid
		实现了阻塞式open。
		
每个scull设备都展示了驱动程序的不同功能，也提出了不同的难点。

## 主设备号和次设备号

## 设备号的内部表示

## 分配和释放设备编号

## 动态分配主设备号

## 一些重要的数据结构
驱动程序涉及到3个重要的数据结构：
file_operations
	对文件的操作。
file
	打开的文件。
inode
	文件。
	
## 字符设备的注册

# 4 调试技术
printk
使用proc文件系统

# 5 并发和竞态

## scull的缺陷

## sem和mutex

## completion

## spinlock

## 不用锁怎么做
原子变量
位操作

# 6 高级字符驱动程序操作

## ioctl

# 7 时间以及延迟操作

