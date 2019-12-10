---
title: Linux内核之workqueue
date: 2018-04-09 10:36:38
tags:
	- Linux内核

---

1

在内核驱动里，一般小型的任务（work）都不会自己起一个线程来处理，而是扔到workqueue里去处理。**workqueue的主要工作就是用进程上下文来处理内核中大量的小任务。**

工作队列是内核2.6版本引入的，工作队列使用起来更加方便。它把工作推后，交给一个内核thread去执行。这个thread总是在进程上下文执行，所以很方便持有sem，也可以允许sleep。

工作队列和tasklet，都是属于底半段机制。

每个workqueue就是一个内核进程。

所以，workqueue的主要设计思想就是：

1、要并行，多个work不要相互阻塞。

2、要节省资源，多个work尽量共享资源。

工作队列workqueue**不是通过软中断实现**的，它是**通过内核进程实现**的

内核进程worker_thread做的事情很简单，死循环而已，不停的执行workqueue上的work_list.



为了实现这个设计思想，workqueue的设计实现也经历了多个版本。最新的workqueue实现叫做CMWQ（Concurrency Managed Workqueue），也就是更加智能的算法来实现并行和节省。

相关概念：

1、work。最小单位。核心就是一个函数指针。

2、workqueue。work的集合。



涉及的数据结构：

```
struct work_struct
struct cpu_workqueue_struct
struct workqueue_struct
```



workqueue系统的初始化：

```
start_kernel
	do_basic_setup
		init_workqueues
			keventd_wq = create_workqueue("events");
				create_workqueue_thread
					kthread_create(worker_thread, cwq, fmt, wq->name, cpu);
```















参考资料

1、Linux workqueue工作原理 

https://www.cnblogs.com/sky-heaven/p/5847519.html