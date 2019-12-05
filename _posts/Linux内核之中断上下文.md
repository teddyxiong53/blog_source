---
title: Linux内核之中断上下文
date: 2018-03-24 09:52:58
tags:
	- Linux内核

---



上下文是软件里常见的一个概念。

#进程上下文

进程上下文是指一个进程执行的时候，CPU的所有寄存器里的值、进程的状态以及堆栈的内容。

当内核切换到另外一个进程的时候，需要把进程上下文保存起来。之前下次调度回来的是，就可以看恢复之前的状态。

# 中断上下文

当硬件信号导致内核调用中断处理函数的时候，进入到内核空间。

在这个过程中，硬件的一些参数要传递给内核。

中断上下文就是指，硬件传递过来的参数和被中断的进程的一些信息。

中断上下文和特定进程无关。

一个中断上下文，不可以被打断。所以中断上下文有这些限制：

1、不能睡眠或者放弃CPU。因为进中断的时候，内核已经关闭调度了。这样的话，系统就会卡住。

2、执行耗时的任务。

3、不能访问用户空间的虚拟地址。因为中断上下文跟进程无关，所以拿不到的。



中断上下文，是指系统当前正在处理硬中断或者软中断。

# in_interrupt()宏

in_interrupt()这个宏，就是用来判断中断上下文的。

```
/*
 * Are we doing bottom half or hardware interrupt processing?
 * Are we in a softirq context? Interrupt context?
 */
#define in_irq()		(hardirq_count())
#define in_softirq()		(softirq_count())
#define in_interrupt()		(irq_count())
```





在进程上下文里，可以用current这个宏来取得当前的进程。
中断上下文，因为没有后备进程，它不能sleep，中断里sleep，就不知道该哪个进程运行了。

内核栈的大小是2个page，就是8KB。
之前的中断处理程序，没有自己的栈，它共享了被它中断的进程的内核栈。
在内核2.6的早期版本里，增加了一个选项，可以选择把内核栈设置为1个page。
这样就减轻了系统的内存压力。
因为系统里的每个进程都需要2个page，连续而且不能被换出的内存。
如果内核栈只有一个page，那么这个空间就很紧张了。
为了应对这种情况，中断程序开始拥有自己的栈了。
每个核心对应一个，大小是一个page。



底半部就是执行跟中断有密切关系，但是中断处理器程序本身不执行的工作。

**如果是从硬件里拷贝数据到内存，这个还是要在顶半部完成的。**

**数据在内存里的处理，才适合放在底半部。**

顶半部和顶半部的划分，并没有绝对标准，下面是一些参考原则：

1、如果对时间要求很敏感，就放在顶半部。

2、和硬件相关，放在顶半部。

3、要保证不被其他中断打断，放在顶半部。

4、除了上面的，都放在底半部。



在linux的发展过程中，曾经出现了多种类似的底半部机制，而且令人困扰的是，它们的命名很相似。

有些名字词不达意。

2.3版本的内核，开始引入软中断。

对于大部分的底半部来说，用tasklet就可以了，但是对于网络这种对性能要求特别高的应用，需要使用软中断来进行处理。



假如CPU有4个核心，核心0上在处理irq0的软中断，核心1也可以处理irq0的软中断。

但是，这就带来了重入的问题了。

所以软中断不好写。加锁保护很麻烦。

不过，一般是采用per-cpu变量来处理，这样就规避了加锁。



软中断被执行的时机：

1、从顶半部返回的时候。

2、在ksoftirqd内核线程里。

3、在有显式检查和处理软中断的代码里，例如网络子系统。







软中断的使用过程：

1、注册软中断。open_softirq。

2、触发软中断。raise_softirq。



tasklet是用软中断机制来实现的一种底半部机制。

tasklet是一种特殊的软中断。软中断号是TASKLET_SOFTIRQ。

分为两种：

1、普通tasklet。HI_SOFTIRQ。

2、高优先级tasklet。TASKLET_IRQ。



tasklet的好处：

1、可以动态添加。软中断是定死的。

2、对加锁的要求不高，所以编写难度不大。

3、性能也还可以。



tasklet的state只能有3种情况：

1、0

2、TASKLET_STATE_SCHED。已经被调度，等待运行。

3、TASKLET_STATE_RUN。正在运行。

tasklet里的count变量，>0表示，tasklet被禁止。=0才能运行。



tasklet的调度：

1、检查是不是TASKLET_STATE_SCHED状态，如果是，直接返回。

2、调用__tasklet_schedule函数。

3、



tasklet的运行：

1、如果是多处理器系统，检查TASKLET_STATE_SCHED来判断这个tasklet是不是正在被别的处理器处理。

如果是，就不做任何事情。



作为一个优化措施，一个tasklet总是在调度它的核心上运行。这样可以更好地利用CPU的cache。

你要暂时禁止一个tasklet，就用tasklet_disable来做。这里面实际上就是把count成员变量加1了。



ksoftirqd

一般软中断会在顶半部返回的时候执行，这个时候的概率是最高的。

但是有时候，中断就是特别频繁，例如在大量网络数据通信的时候。

而且，有的软中断处理程序会自我触发，例如网络的。

这就会导致用户程序没有执行的时间了。

这个肯定是不行的。

怎么解决？

在大量软中断出现的时候，内核会唤醒一组内核线程来处理这些负载。

这些线程在最低的优先级上运行（nice值为19）。这样可以避免它们跟其他重要任务抢夺资源。

每一个处理器都有一个这样的线程，名字叫ksotfirqd/n（n是核心的编号）。



工作队列

工作队列，本质上跟软中断和tasklet不一样。它是在进程上下文执行。

如何进行选择呢？有这么几个原则：

1、如果需要睡眠，就选工作队列。

2、如果不需要睡眠，就选tasklet。

实际上，工作队列可以用内核线程来替换，但是内核开发者非常反对创建新的内核线程。



工作队列的实现

工作队列子系统是一个用户创建内核线程的接口，它创建的内核线程叫做worker thread。

提供了一个默认的work thread来处理要推后的工作。

默认的worker thread叫做events/n。n是核心的编号。

（我看最新的kernel里，这个已经是叫做kworker了。）

相关的结构体是：

```
struct workqueue_struct //在kernel/workqueue.c里。
struct cpu_workqueue_struct //在kernel/workqueue.c里。
struct work_struct //在include/linux/workqueue.h里。我需要关注的就是这个。上面那2个对我们不可见。
```



工作队列的使用

1、定义一个工作队列。

```
DECLARE_WORK(xxx_work, xxx_work_func, &xxx);
```

2、实现处理函数。

```
void xxx_work_func(void *data)
```

3、调度。

```
schedule_work(&xxx_work);
```

如果你不希望马上被调度，你还可以这样：

```
schedule_delayed_work(&xxx_work, delay);
```



如果默认的工作队列不能满足你的要求，你可以自己创建一个工作队列。

```
struct workqueue_struct *create_workqueue(char *name);
```



# 参考资料

1、

https://www.cnblogs.com/reality-soul/p/6377137.html

2、《Linux内核设计与实现》。中断相关章节。

