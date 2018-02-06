---
title: rt-thread（十四）pthread实现分析
date: 2018-02-06 11:30:49
tags:
	- rt-thread
	- pthread

---



rt-thread实现了pthread的相关接口，我们看看是如何实现的。



# 目录分析

所有代码都在components/libc/pthreads目录下。

```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/libc/pthreads$ tree
.
├── mqueue.c
├── mqueue.h
├── posix_types.h
├── pthread_attr.c
├── pthread_barrier.c
├── pthread.c
├── pthread_cond.c
├── pthread.h
├── pthread_internal.h
├── pthread_mutex.c
├── pthread_rwlock.c
├── pthread_spin.c
├── pthread_tls.c
├── sched.c
├── sched.h
├── SConscript
├── semaphore.c
└── semaphore.h
```

pthread.c和pthread.h是统领全局的。

# pthread.h

1、定义宏。

2、定义类型。

pthread_t就是struct rt_thread *类型。

线程通信属性那些类型都是long或者int。例如pthread_condattr_t。

3、定义attr结构体。

4、函数声明。

# pthread_internal.h

这个里面有个结构体，很重要。对于attr、cancel、join、detach很重要。

```
struct _pthread_data
{
	u32 magic;
	pthread_attr_t attr;
	rt_thread_t tid;
	void *(*thread_entry)(void *param);
	void *thread_param;
	void *return_value;
	rt_sem_t joinable_sem;//join就是靠这个。
	u8 cancel_state;
	volatile u8 canceltype, canceled;
	//...
};
```

因为pthread_t就是rt_thread_t。这个结构体，通过userdata这个指针，挂进去的。

# pthread.c

就定义了pthread_xxx函数。

1、增。

create。

once。

2、删。

kill。需要支持signal。

cancel。

exit。

3、改。

detach。

join。

setcanceltype、setcancelstate。

4、查。

pthread_testcancel。

总共是2+3+4+1 = 10个接口。

我们现在看看pthread_create的实现。

