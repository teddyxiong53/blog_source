---
title: Linux内核之smp
date: 2018-03-30 09:35:08
tags:
	- Linux内核
typora-root-url: ..\
---

--

smp是对称多处理器的意思。

smp起源于1950年代。开始的时候，因为单个处理器的性能不行，所以这个还是有很多公司在研究，**不过后面到了80年代，单个处理器的性能提升了，大家的研究热情就下降了。**

但是到了现在，这个又流行起来了。

有个Amdahl法则，就是核不是越多越好。管理多核的开销。

**最早的linux smp是松耦合smp系统。实际上是多台机器，通过高速以太网连接起来。**

对应的项目叫Linux Beowulf（贝奥武夫）。这个是一个集群。

这种就是架构起来容易，但是占用空间大，耗电。

紧耦合smp

这个就是一般说的smp了。是芯片级的。

![Linux内核之smp-图1](/images/Linux内核之smp-图1.png)

**Linux内核在早期，是通过大内核锁来进行串行化。所以对smp的支持非常不好。**

到了2.6版本的时候，才慢慢好起来。

![Linux内核之smp-图2](/images/Linux内核之smp-图2.png)



在smp机器里，有这几个概念：

1、BSP。也叫BP。就是启动CPU。虽然多个核心，但是启动的时候，还是由一个CPU核心来进行启动的。Bootstrap Processor。

2、AP。App Processor。

3、APIC。高级可编程中断控制器。

**4、IPI。处理器间中断。用于处理器之间的通信。**

直到smp_init的时候，其他的核心才开始运行。之前都是停用状态的。

注释里是这么写的。

```
/* Called by boot processor to activate the rest. */
void __init smp_init(void)
```

看看启动打印：

```
Booting Linux on physical CPU 0x0
```

```
smp: Bringing up secondary CPUs ...
CPU1: thread -1, cpu 1, socket 0, mpidr 80000001
CPU2: thread -1, cpu 2, socket 0, mpidr 80000002
CPU3: thread -1, cpu 3, socket 0, mpidr 80000003
smp: Brought up 1 node, 4 CPUs
SMP: Total of 4 processors activated (1738.24 BogoMIPS).
CPU: All CPU(s) started in SVC mode.
```

# smp启动过程

由于系统中存在多个CPU，这就引入一个问题，**当外部设备发生中断的时候，具体由哪个CPU进行处理呢？**

**Intel提出的解决方案是IO APIC和LOCAL APIC体系结构。**

IO APIC 链接各个外设，并且可以设置分发类型，根据设定的分发类型，把中断分发到对应CPU的LOCAL APIC上。

怎样确定哪个CPU是引导CPU呢？

**根据Intel提供的资料，系统上电后，会根据MP Initialization  Protocol随机选择一个CPU作为BP。**

只有BP会运行bios程序，其他的AP都进入到等待状态。**直到BP发送了IPI中断信息后，其他AP才能运行。**



# smp的负载均衡

每个cpu对应一个run_queue。

如果一个进程处于task_running的时候，这个进程就会进入到run_queue，以便调度程序在合适的时候安排它在对应的CPU上运行。

一个CPU对应一个run_queue这种设计，好处是：

1、一个持续处于task_running状态的进程总是趋于在一个CPU上运行，**这样便于进程的数据被缓存，提高效率。**

2、每个CPU上的调度程序之访问自己的run_queue，避免了竞争。**但这也带来了一个问题，就是一些CPU很忙，一些CPU却很闲。这个就要靠负载均衡来解决了。**

smp的负载均衡是指，在一定的时机，让进程从一个run_queue迁移到另外一个run_queue。



#smp的内核变量保护

就是per-cpu变量。

## 为什么引入per-cpu变量

**在armv6之前的架构里，用swp和swpb指令来实现对共享内存的访问。**

硬件的实现上会进行锁操作，这个就极大地造成性能的下降。

怎么解决？就是不要锁。不要锁，怎么解决变量的同步问题？就是每个核心分配一个。

就是per-cpu变量 了。

不过，armv6以后，CPU已经不推荐用swp这样的指令了。

**而是用ldrex和strex这样的指令。不会再锁总线。**

其实按照这种方式，per-cpu变量已经没有存在的必要了。但是考虑到cache的操作，per-cpu还是有一定的意义的。

## 内核里对per-cpu变量的操作

1、定义。

```
DEFINE_PER_CPU(type, name);
```

2、读和写操作。

```
get_cpu_var(var);
put_cpu_var(var);
```





per-cpu变量是2.6内核引入的。**当你创建一个per-cpu变量的时候，系统中的每个核心获得它自己的这个变量的拷贝。**

优点就是per-cpu变量几乎不用加锁。

per-cpu变量一般是用来做计数器。

**per-cpu变量使用的典型例子是在网络子系统里。**

```
DEFINE_PER_CPU(int, xmit_recursion);
```



per_cpu的原理就是一个变量在所有的CPU cache上都存一份，这样每次读写就可以避免锁开销和上下文切换这些操作。

一般来说，最好把per_cpu变量声明为CPU cache对齐的。



mini2440的L1 cache shift是5，也就是32字节。

它是把变量定义在特别的位置。

```
#define PER_CPU_BASE_SECTION ".data..percpu"
```

放在`__per_cpu_start`和`__per_cpu_end`之间。我们把这个地方就做per-cpu变量的原始变量。

但是有这个原始变量，还是不够的。

**必须为每个CPU建立一个副本。怎么建？直接定义一个NR_CPUS的数组？不行，这个NR_CPUS是系统支持的最大的CPU数量。并不是实际的CPU数量。这样定义非常浪费内存。**

per-cpu变量的内存分配，是归内存管理子系统来做。

内存子系统会根据当前系统的内存配置，为每一个CPU分配一大块的memory，对于UMA，就是位于ddr主存里。

```
#ifndef __per_cpu_offset 
extern unsigned long __per_cpu_offset[NR_CPUS];

#define per_cpu_offset(x) (__per_cpu_offset[x]) 
#endif
```



# 参考资料

1、Linux 和对称多处理

https://www.ibm.com/developerworks/cn/linux/l-linux-smp/

2、华中科技大学的PPT

https://max.book118.com/html/2015/0914/25330968.shtm

3、

https://wenku.baidu.com/view/add8a5a390c69ec3d4bb750e.html

4、per_cpu变量用法

https://blog.csdn.net/majieyue/article/details/32125767

5、8.4. 每-CPU 的变量

http://www.deansys.com/doc/ldd3/ch08s04.html

6、linux percpu机制解析

https://blog.csdn.net/wh8_2011/article/details/53138377

7、Linux内核同步机制之（二）：Per-CPU变量

https://www.cnblogs.com/dirt2/p/5616513.html

8、linux SMP 启动过程学习笔记

https://blog.csdn.net/jemmy858585/article/details/4509375

9、Linux内核SMP负载均衡浅析

https://blog.csdn.net/u010937616/article/details/47396619

