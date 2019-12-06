---
title: Linux内核之调度（一）
date: 2018-03-26 13:47:29
tags:
	- Linux内核

---

1

我的一个疑问：

内核调度抢占的时机是什么？

CPU抢占分两种情况, 用户抢占, 内核抢占

其中内核抢占是在Linux2.5.4版本发布时加入, 同SMP(Symmetrical Multi-Processing, 对称多处理器), 作为内核的可选配置。



需要满足下面的条件，kernel才可以抢占一个任务的内核态：

1、没有锁。

2、code是可重入的。

内核抢占发生的时机，一般发生在：

1、中断处理返回的时候，隐式调用了schedule函数，当前任务没有主动放弃cpu使用权，而是被剥夺了cpu使用权。

2、spinlock解锁后，软中断使能后。也会产生抢占。

3、主动调用schedule主动放弃cpu使用权。

4、内核中阻塞，也会导致被抢占。



这些情况，不能被内核抢占：

1、内核正在进行中断处理。

2、内核在中断上下文的下半部里。

3、在spinlock锁内。

4、内核正在执行schedule函数。

5、内核正在对per-cpu变量进行处理的时候。







进程调度是os的核心功能。

调度器的主要工作就是在所有状态为running的进程里，选择最合适的一个进程来运行。

调度器把进程分成3类：

1、交互式进程。

```
特点是不断地处于睡眠状态，等待用户输入。
例如编辑器vi。
但是要求能够快速响应。
```

2、批处理进程。

```
1、在后台运行。
2、使用大量的资源。
3、可以容忍延迟。
4、典型应用是编译器gcc。
```

3、实时进程。



传统的linux调度器，是采取提高交互进程的优先级，保证交互进程的响应及时。





# Linux2.4的调度器

Linux2.4使用的调度器基于优先级，跟1992年Linus发布的调度没有大的区别。

使用的pick next算法是：

对runqueue里的所有进程的优先级进行比较，选择最高优先级作为下一个被调度的进程。

每个进程被创建的时候，被赋予了一个时间片。

当时间片用完了，就要等被赋予新的时间片才能有机会参与调度。

Linux2.4的调度器，只有当所有running的进程的时间片都用完了，才对所有进程重新分配时间片。

这段时间被称为epoch（新纪元）。这种设计保证了每个进程都有机会得到执行。

## 实时进程

实时进程的优先级是静态设定的，始终高于普通进程的优先级。

只有当runqueue里没有实时进程的时候，普通进程才有得到调度的机会。

实时进程采用两种调度策略：

1、FIFO。对于同一优先级的。

2、RR。

## 普通进程

普通进程的优先级由进程描述符里的counter字段来决定。

进程被创建的时候，子进程的counter值为父进程的一半，这样就可以避免进程通过不断fork来提高自己的优先级了。

## 缺点

这个版本的调度器有这些缺点：

1、可扩展性不好。

当进程数很大的时候，遍历所有进程画的时间就很长了。调度的时间复杂度是O(n)。

2、高负载的时候，调度性能低。

3、交互式进程的优化不完善。

4、对实时进程的支持不够。是非抢占的。

# Linux2.6的调度器

Linux2.6的调度器调度算法把时间复杂度优化到O(1)。不受进程数量的影响。

主要修改2个点：

1、进程优先级的计算方法。

2、pick next算法。

## 普通进程的优先级计算

普通进程的优先级的动态计算的，计算公式里引入了静态优先级的系数。

静态优先级是nice值决定的。

（nice值越大，优先级越低。好人不好做啊。）

动态优先级的计算公式是：

```
dyn_prio = max(100, min(static_prio - bonus + 5, 139))
```

bonus这个是跟进程的平均睡眠时间有关的。

睡眠越久，bonus就越大，计算出来的优先级就越高。

平均睡眠时间也被用来判断一个进程是否是交互式进程。

如果满足这个公式，就说明是交互式进程。

```
dyn_prio <= 3*static_prio/4 + 28
```

平均睡眠时间的更新分布在很多的内核函数里。

## 实时进程的优先级计算

在进程描述符里，是有一个rt_priority来表示实时优先级的。





------



Linux内核实现了调度类，来实现多个调度类的协同工作。

每个调度类里，有自己的优先级。

内核调度基础管理代码会遍历所有的调度类，选择高优先级的调度类。

内核里的调度分为这几种：

```
#define SCHED_NORMAL		0 //用于普通线程。
#define SCHED_FIFO		1 //实时线程。
#define SCHED_RR		2//实时线程。
#define SCHED_BATCH		3//批处理。优先级应该是最低的。
```

SCHED_NORMAL

在2.6之前的版本，SCHED_NORMAL根据线程的优先级（nice值）来分配时间片。

nice值等于0，分配100ms。

nice等于-20，分配5ms。

在2.6之后的版本，SCHED_NORMAL使用的是2.6.23版本引入的CFS（Complete Fair Schedule完全公平调度）。

这样线程优先级和时间片没有固定关系了。



实时线程优先级高于普通线程。

# 相关接口

1、修改nice值。

```
int nice(int incr);
int setpriority(int which, id_t who, int prio);
```

2、修改实时优先级和调度策略。

就是用pthread的那一套接口。

3、设置线程在哪个CPU上运行。

```
int pthread_setaffinity_np (pthread_t thread, size_t cpusetsize, const cpu_set_t *cpuset)
```





# 参考资料

1、Linux系统调度简介

http://www.emtronix.com/article/article20171018.html

2、Linux的任务调度机制

https://blog.csdn.net/zhongbeida_xue/article/details/51280292

3、基于Linux的实时系统

https://www.ibm.com/developerworks/cn/linux/embed/l-realtime/

4、Linux 调度器发展简述

https://www.ibm.com/developerworks/cn/linux/l-cn-scheduler/

5、linux进程调度浅析

https://blog.csdn.net/ctthuangcheng/article/details/8914309

6、Linux调度子系统

https://blog.csdn.net/u012259202/category_1774977.html

7、Linux用户抢占和内核抢占详解(概念, 实现和触发时机)--Linux进程的管理与调度(二十）

https://blog.csdn.net/gatieme/article/details/51872618