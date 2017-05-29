---
title: Linux驱动增加阻塞io支持
date: 2017-04-20 23:33:59
tags:

	- waitqueue

---
要实现驱动对应的设备，可以在打开的时候，指定阻塞。在驱动里，要使用一个叫wait_queue的东西来支持这种特性。
它以队列为基础数据结构，与进程调度紧密结合。
wait_queue叫做等待队列。
一般的使用步骤是：
1、定义等待队列头。
wait_queue_head_t my_queue;
2、初始化等待队列头。
init_wait_queue_head(&my_queue);
第一和第二步可以合并为这个宏：DECLARE_WAIT_QUEUE_HEAD(my_head);


等待队列头和等待队列。

wait_queue_head_t比wait_queue_t要简单，只有一个lock和一个list。


看看在globalfifo里加阻塞io的。
1、在globalfifo_dev结构体里加上两个成员变量。
wait_queue_head_t r_wait;
wait_queue_head_t w_wait;
2、在globalfifo_init里初始化：
init_wait_queue_head(&r_wait);
init_wait_queue_head(&w_wait);
3、在globalfifo_read函数里：
```
{
	DECLARE_WAITQUEUE(wait, current);//定义一个名字叫wait的等待队列。task是当前的进程。
	add_wait_queue(&r_wait, &wait);//把wait这个等待队列添加到读等待队列头里去。
	//如果没有有数据可以读，改变进程进入睡眠状态
	__set_current_state(TASK_INTERRUPTIBLE);
	schedule();//调用schedule函数
	//如果读了东西，发消息去唤醒写等待队列。
	wake_up_interruptible(&w_wait);
	//最后，移除等待队列
	remove_wait_queue(&w_wait, &wait);
	set_current_state(TASK_RUNNING);
}
```
4、在globalfifo_write函数里：
{
	与read类似。
}