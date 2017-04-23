---
title: Linux开机时间优化
date: 2017-04-23 14:13:30
tags:
	- Linux
---
启动时间优化涉及到时间测量、分析、人为因素、初始化技术和简化技术这些方面。开机启动时间会影响用户体验。
设备启动过程包括多个步骤，为了便于分析交流，启动时间工作组（Bootup Time Working Group of the CE Linux）定义了一组术语，这些术语也被广泛接受。术语的定义在这里：`http://elinux.org/Boot-up_Time_Definition_Of_Terms`。

# 1. 时间测量
## 1.1 printk times
printk times是一个简单的用来测量Linux启动时间的方法，它是通过网printk上添加时间打印来实现的。
Linux要支持这个功能，需要打一个补丁，需要一个工具软件。不过，从kernel2.6.11开始，这个功能就已经合入到内核的主线版本了。工具软件的作用是显示显示两次打印之间的间隔的。工具软件是Linux源代码目录下`script/show_delta`这个shell脚本。
用这种方式测量的好处是：不需要太多的额外的东西，简单易用。坏处是：printk打印本身就是一个比较耗时的操作，而且你只能看到有printk的地方的时间，要看其他的地方，你得加打印，重新编译运行。
要使用这个特点，你需要指定bootargs的时候，加上`printk.time=1`这一项。
如果你想要一直把这个打开，或者你想要看Linux启动更加靠前的时间打印，你可以在配置内核的时候，把对应的项目勾选上。
你可以在运行时动态改变printk是否带上时间打印，方法是：
```
# echo 1> /sys/module/printk/parameters/time
# echo "hello printk time" > /dev/kmsg
这样就可以测试一下这个行为了。
```

##　1.2 kernel function trace
简写为KFT。

还有一些其他的方法用于测量时间，后面补充。

# 2. 优化启动时间的手段

## 2.1 bootloader加速
kernel XIP：允许kernel在flash片内执行。
dma拷贝。
内核压缩解压。

## 2.2 kernel加速
禁用console，在启动期间。
禁用打印。
预设lpj。

## 2.3 文件系统相关

## 2.4 应用相关


