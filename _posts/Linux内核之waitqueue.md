---
title: Linux等待队列
date: 2017-05-26 23:20:15
tags:
	- waitqueue

---



基于2.6.35版本分析。

涉及的代码是linux/wait.h和kernel/wait.c。

waitqueue也叫等待队列。在驱动里大量使用。

例如在i2c-s3c2410.c里。

```
init_waitqueue_head(&i2c->wait);
```

在这里，这个等待队列是用来等待发送完成的。在完成的中断里，会`wake_up(&i2c->wait);`。

在发送之后，会：

```
timeout = wait_event_timeout(i2c->wait, i2c->msg_num == 0, HZ * 5);
```

其实，这3个接口，就是等待队列使用的大概情况了。

另外还有定义的地方：

```
wait_queue_head_t	wait;
```



我们先从init_waitqueue_head开始看。

结构体的定义很简单。

```
struct __wait_queue_head {
	spinlock_t lock;
	struct list_head task_list;
};
typedef struct __wait_queue_head wait_queue_head_t;
```

就是一个spinlock和一个队列。

所以初始化，也就是初始化队列和spinlock了。

我们看看wait_event做了什么。

```
#define wait_event(wq, condition) 					\
do {									\
	if (condition)	 						\
		break;							\
	__wait_event(wq, condition);					\
} while (0)
```

这个condition注意了。如果满足条件，直接就返回的。

然后就是等待，然后调用schedule函数。

我现在越看，感觉linux跟rtos还是有很多类似之处的。





