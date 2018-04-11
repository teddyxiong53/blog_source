---
title: Linux内核之workqueue
date: 2018-04-09 10:36:38
tags:
	- Linux内核

---



我基于linux2.6.35的来看。

涉及的文件是kernel/workqueue.c。linux/workqueue.h。

入口函数是init_workqueues。在do_basic_setup里被调用。

这里面做的就是

```
keventd_wq = create_workqueue("events");
```

创建了一个叫做events的workqueue。

看看create_workqueue是怎么工作的。

```
struct workqueue_struct *__create_workqueue_key(const char *name,
						int singlethread,//0
						int freezeable,//0
						int rt,//0
						struct lock_class_key *key,//这个NULL
						const char *lock_name//这个NULL
						)
1、分配一个workqueue_struct结构体。
2、它的cpu_wq是alloc_percpu(struct cpu_workqueue_struct)
3、添加到workqueues这个全局链表里去。
4、create_workqueue_thread，最重要就是这里，创建了一个内核线程。工作者线程叫:events/n
	p = kthread_create(worker_thread, cwq, fmt, wq->name, cpu);
```



看看workqueue如何为系统服务。

所以我们要看看workqueue对外提供的接口有哪些。

驱动开发者，需要做的有：

1、定义一个work。

```
DEFINE_WORK(xx_work, xx_work_func);
```

或者直接：

```
struct work_struct xx_work;
INIT_WORK(&xx_work, xx_work_func);
```

驱动开发者需要使用的work_struct，而不是直接使用workqueue。

2、触发调度行为。一般是在中断里。

```
schedule_work(&xx_work);
```



下面我们就看看系统之后是如何进行调度的。

```
int schedule_work(struct work_struct *work)
{
	return queue_work(keventd_wq, work);
}
```

函数就是把work插入到队列里去了。keventd_wq又是如何定义和工作的呢？

定义是这样：

```
static struct workqueue_struct *keventd_wq
```

赋值在这里：

```
keventd_wq = create_workqueue("events");
```

接下来，我们要看work_thread这个内核线程了。

这里面就是阻塞的，在等。有事件来了。

```
f(work);//这个就是我们注册进来的函数。
```

