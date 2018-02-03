---
title: rt-thread（七）调度代码分析
date: 2018-02-03 14:09:24
tags:
	- rt-thread

---



以qemu的vexpress板子为分析对象。gcc工具链。

我就最高优先级为32为例，简化分析。

1、入口函数是：rt_system_scheduler_init。

```
1、初始化线程优先级表。
2、当前优先级设为31，当前线程设置为null。
3、ready group设置为0 。这个int型，32个bit，1个位表示一个优先级有就绪的任务。这样相当于都没有就绪。
```

这一步执行后的效果是：

```
thread priority table
[0] -o - o -
[1] -o - o
...
[31] -o -o - 这些o代表的就是线程。
同一个优先级的线程串成一个链表。当然目前链表都是空的。
```

2、其他模块创建线程。调用是这样的：

```
app_init
	tid = rt_thread_create("led")
	rt_thread_startup(tid)
		rt_thread_resume
			rt_thread_insert_thread
				这个函数就把对应优先级给ready group对应的位置位了，标志是就绪状态了。
```

这个时候，调度器还没有启动呢。

3、rt_system_scheduler_start。

在os启动的最后，把调度器启动了。启动了马上就去找ready group里最低的为1的位。这个对应的就是目前就绪的最高优先级线程。取得对应的线程结构体。

调用rt_hw_context_switch_to，切换到这个线程运行。

这样第一个线程就正常运行起来了。

4、我们看线程切换的过程。

假如我们加的那个led任务，现在sleep了。另外一个key检测线程就绪了。

看看如何切换的。

我们先看rt_thread_sleep做了些什么：

```
1、取得当前线程的结构体。就是led线程了。
2、调用rt_thread_suspend挂起。
	rt_schedule_remvoe_thread
		从线程链表里移除掉。如果这个优先级的链表都空了，就把ready group也清零。
3、执行调度。rt_scheduler。
	找到最高优先级的就绪任务，跟当前的比较，不是同一个，就是执行切换任务。
```

到这里，切换过程就完成了。



# 线程结构体

结构体内容分为这么几部分：

1、所有rt-thread对象都有的4个成员：name、type、flag、module_id。总共14字节。

2、list和tlist。list是所有对象都有的，tlist是线程链表。

3、堆栈相关的。5个成员。sp、entry、param、stack addr和size。

4、状态和错误码。

5、优先级相关。

6、event相关的。

7、tick相关。

8、私有数据。



然后我们看初始化的时候，如何处理的。尤其是堆栈的填充这里。

1、把堆栈里都填上#这个字符。

2、rt_hw_stack_init。这个是重点。

```
堆栈从上往下增长的。这个跟linux的统一的。很好记忆。
内容依次是：
1、entry函数指针
2、rt_thread_exit函数指针。代表lr。？？
3、然后是r12到r0
然后把当前的栈顶指针返回。放到thread->sp里保存起来。
```





