---
title: Linux内核之调度（一）
date: 2018-03-26 13:47:29
tags:
	- Linux内核

---



Linux内核实现了调度类，来实现多个调度类的协同工作。

每个调度类里，有自己的优先级。

内核调度基础管理代码会遍历所有的调度类，选择高优先级的调度类。

内核里的调度分为这几种：

```
#define SCHED_NORMAL		0 //用于普通线程。
#define SCHED_FIFO		1 //实时线程。
#define SCHED_RR		2//实时线程。
#define SCHED_BATCH		3//不清楚
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





