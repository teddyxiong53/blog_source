---
title: Linux驱动之workqueue
date: 2018-02-28 19:55:51
tags:
	- Linux驱动

---



在内核驱动里，一般小型的任务（work）都不会自己起一个线程来处理，而是扔到workqueue里去处理。workqueue的主要工作就是用进程上下文来处理内核中大量的小任务。

所以，workqueue的主要设计思想就是：

1、要并行，多个work不要相互阻塞。

2、要节省资源，多个work尽量共享资源。

为了实现这个设计思想，workqueue的设计实现也经历了多个版本。最新的workqueue实现叫做CMWQ（Concurrency Managed Workqueue），也就是更加智能的算法来实现并行和节省。

相关概念：

1、work。最小单位。核心就是一个函数指针。

2、workqueue。work的集合。

相关使用接口：

静态创建：



工作队列是内核2.6版本引入的，工作队列使用起来更加方便。它把工作推后，交给一个内核thread去执行。这个thread总是在进程上下文执行，所以很方便持有sem，也可以允许sleep。

工作队列和tasklet，都是属于底半段机制。



内核对workqueue的处理是通过worker thread来完成的。worker thread一般处于sleep状态。