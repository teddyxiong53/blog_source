---
title: Linux内核之进程（一）
date: 2018-03-29 16:12:19
tags:
	- Linux内核

---



# 什么是进程

进程就是处于运行期的程序和相关资源的总和。

进程包括这些东西：

1、代码段。

2、打开的文件、挂起的信号、内核内部数据、处理器状态，内存地址空间、线程。

3、数据段。

内核调度的对象是线程，而不是进程。

传统的unix程序，一个进程只有一个线程。现在的进程一般都是多线程的。

# task_struct

task_struct结构体很大，在32位机器上，大概是1.7KB。

但是考虑这个结构体包含了内核管理一个进程所需要的全部信息，这个也是值得的。

内核通过slab分配器分配task_struct结构体。这样可以达到对象复用和缓存着色的目的。

struct thread_info，在x86架构上，是这样的

```
1、struct task_struct *task
2、struct exec_domain *exec_domain。
3、u32 flags
4、u32 status
5、u32 cpu
6、int preempt_count
7、mm_segment_t addr_limit
8、struct restart_block restart_block
9、void *sysenter_return
10、int uaccess_err
```

每个任务的thread_info结构体在它的内核栈的尾部分配。

# pid

pid_t实际上是int类型，但是为了更老版本的linux和unix兼容，这个值的范围被限制为32768 。

因为之前unix上是short类型的。

32768这个值对于普通的桌面系统肯定是够了，但是对于服务器是不够的。

这个值，你可以改。动态改。这么改。

```
echo 65536 > /proc/sys/kernel/pid_max
```

在内核里，访问任务，第一步就是要拿到对应的task_struct指针。

是通过current这个宏来拿到的。这个current宏的实现，跟CPU架构相关。

有的CPU，可以专门拿出一个寄存器来存放这个指针，这样访问就比较快。

而像x86这样的，寄存器本来就不多的，就要靠在堆栈的尾部创建thread_info结构体，通过计算偏移来得到task_struct。

# 进程状态

基本的3种状态的：

TASK_RUNNING

TASK_INTERRUPTIBLE

TASK_UNINTERRUPTIBLE

设置状态的函数：

```
set_task_state(task, state_value)
```

# 进程上下文

进程上下文里，current宏是有效的。



# 进程的家谱



# 进程的创建

在fork之后，马上exec，就不会有拷贝发生。

copy_process函数里做的事情：

```
1、调用dup_task_struct分配一个task_struct结构体。
2、检查进程有没有超过限制值。超过就跑去free掉，返回失败。
3、子进程的task_struct里的成员开始进行设置，主要是一些统计信息的初始化。大部分都是跟父进程的一样的。
4、子进程的状态被设置为TASK_UNINTERRUPTIBLE，保证它不会被投入运行。
5、调用copy_flags函数拷贝flags。
6、调用alloc_pid为新进程分配一个有效的pid。
7、根据传递给clone的flags，决定是否要拷贝一些东西。
8、收尾工作，返回一个指向子进程的指针。
```

copy_process完成后，继续回到do_fork函数，如果成功，新创建的子进程被唤醒，并且投入运行。

内核是倾向于让子进程先运行的，因为子进程一般会马上调用exec函数，这样可以避免写时拷贝的开销。

如果是父进程先运行，就有可能写入内容。导致子进程得拷贝。

但是，这一点是不能保证的。

## vfork

vfork跟fork的本质区别就是vfork不拷贝父进程的页表。

子进程作为父进程的一个线程，在父进程的空间里运行。父进程这个时候会阻塞，直到子进程退出，或者执行exec。

vfork非常不建议使用。



# 线程在linux里的实现

线程机制是现代编程技术里常用的一种抽象概念。

linux里是把线程当成共享资源的进程来实现的。每个线程也对应一个task_struct。

这个和windows的实现差别是很大的。

## 内核线程

内核经常需要在后台做一些事情。这些事情是通过内核线程（kernel thread）来完成的。

内核线程和普通进程的区别：

内核线程没有独立的地址空间，对应的mm_struct是指向NULL的。

创建是用kthread_create来做。



# 参考资料

1、《Linux内核设计与实现》第3章。





