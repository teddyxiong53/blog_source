---
title: Linux开机时间优化
date: 2017-04-23 14:13:30
tags:
	- Linux
---


启动时间优化涉及到时间测量、分析、人为因素、初始化技术和简化技术这些方面。开机启动时间会影响用户体验。
设备启动过程包括多个步骤，为了便于分析交流，启动时间工作组（Bootup Time Working Group of the CE Linux）定义了一组术语，这些术语也被广泛接受。术语的定义在这里：`http://elinux.org/Boot-up_Time_Definition_Of_Terms`。

# 术语分析

1、boot up。

这个是指从上电到到init进程。

2、busy wait。

忙等待。就是delay这种延时。

3、cold start。

冷启动。

4、Deferred。

5、De-serialized。

去序列化。默认是串行的，我可以通过改成并行的方式来提高速度。

6、Disk spinup。

磁盘可用。

7、Firmware。

就是bios这些了。

8、First Available Use。

9、Hibernate。

10、Power lost。



# 时间测量
## printk times
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

##　kernel function trace
简写为KFT。

还有一些其他的方法用于测量时间，后面补充。

# 减小内核的size

 `make tinyconfig`

从Linux 3.17-rc1开始，加入了这个选项来产生一个最小的内核。

把slub分配器改成slob。

内核压缩方法有gzip改成xz。

禁用high mem。

打开内核的size优化配置项。

内核的size，涉及到3个方面：

1、内核被load到ram里需要占用的空间（这个是解压后）

2、内核用的动态内存。

3、内核镜像在flash占用的空间。

使用size命令来查看vmlinux的大小。

```
size */built-in.o  
这个可以查看所有的子模块的大小情况。
```



# 优化启动时间的手段

## bootloader加速
kernel XIP：允许kernel在flash片内执行。
dma拷贝。从flash拷贝到ram。

内核压缩解压。

##  kernel加速
禁用console，在启动期间。
禁用打印。
预设lpj。这个先不设置，看看打印出来是多少。然后在bootargs里设置上就好了。



## 文件系统相关

常用的flash文件系统对比。

| 指标/文件系统  | jffs2 | yaffs2 | logfs | ubifs |
| -------- | ----- | ------ | ----- | ----- |
| 启动时间     | 慢     | 快      | 极快    | 快     |
| io性能     | 好     | 好      | 一般    | 极好    |
| 资源占用     | 一般    | 极好     | 好     | 一般    |
| nand设备寿命 | 好     | 一般     | NA    | 极好    |
| 异常掉电容忍   | 好     | 好      | 差     | 好     |
| 内核集成     | 是     | 否      | 否     | 是     |



jffs2为什么挂载慢？

因为jffs2挂载的时候，要把flash全部扫描一遍。这个扫描是很慢的。挂载16M的jffs2文件系统需要30秒这种量级的时间。那么为什么要扫描一遍呢？是要找出所有的日志节点，建立文件结构。

ubifs则可以极大地改善这种情况。





## 应用相关



# 参考资料

1、嵌入式: jffs2,yaffs2,logfs,ubifs文件系统性能分析

https://blog.csdn.net/iceiilin/article/details/22721029

2、嵌入式 Linux 系统裁剪

https://tinylab.org/embedded-linux-system-size-optimization/