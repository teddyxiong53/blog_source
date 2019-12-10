---
title: Linux等待队列
date: 2017-05-26 23:20:15
tags:
	- waitqueue

---

1

在Linux的驱动程序里，使用等待队列来实现阻塞进程的唤醒。

以队列为基础数据结构，跟进程调度机制紧密结合，实现内核的异步事件通知机制。

也可用用来同步对系统资源的访问。

（信号量在内核的实现，也是基于等待队列的）。

等待队列在Linux内核里有着举足轻重的作用。

很多的驱动都或多或少用到了等待队列。

所以等待队列是必须掌握的知识点。

它有两种数据结构：

```
1、等待队列头。wait_queue_head_t。
2、等待队列项。wait_queue_t。
```

在内核里的文件是linux/wait.h和kernel/wait.c。

相关操作：

定义并初始化队列头

```
wait_queue_head_t my_queue;
init_wait_queue_head(&my_queue);
有一个宏来简化定义和初始化
DECLARE_WAIT_QUEUE_HEAD(my_queue);
```

定义等待队列

```
DECLARE_WAITQUEUE(name, tsk);
```

添加和删除等待队列

```
void add_wait_queue(wait_queue_head_t *q, wait_queue_t *wait)
默认是设置非互斥进程。
还有一个互斥版本
void add_wait_queue_exclusive(...)

remove就只有一个。
void remove_wait_queue(q, wait);
```

等待事件，有4个版本：

```
wait_event(wq, condition)
wait_event_interruptible
wait_event_timeout
wait_event_interruptible_timeout
```

唤醒

```
wake_up_interruptible(x)

```

在等待队列上睡眠

```
sleep_on(q)
interruptible_sleep_on

```





参考资料

1、linux中的阻塞机制及等待队列

https://www.cnblogs.com/gdk-0078/p/5172941.html

