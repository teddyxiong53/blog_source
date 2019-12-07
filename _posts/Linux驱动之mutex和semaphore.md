---
title: Linux驱动之mutex和semaphore
date: 2018-03-23 17:22:29
tags:
	- Linux

---



#mutex

mutex中文叫互斥锁。mutex是一个缩写，是Mutual Exclusion。相互排斥的意思。



linux中可以用互斥信号量来表示互斥锁。

用DEFINE_MUTEX（后面被改成DEFINE_SEMAPHORE）来定义。后面因为DEFINE_MUTEX这个名字跟真正的mutex容易混淆。所以被改了。这个事情的邮件是这个。

https://lkml.org/lkml/2008/10/26/74

之前的那些反人类的init_MUTEX也被干掉了。



不过真正的mutex进入到linux内核是在2.6.16版本。

对应的头文件是`<linux/mutex.h>`。

我们先看看这个头文件。

最前面一段注释挺有用的。总结如下：

```
1、一次只能有一个task可以持有一个mutex。
2、谁lock，谁就unlock
3、多次unlock不允许。
4、递归lock不允许。
5、必须用指定的api来初始化mutex。
6、不能用memset、copy这些函数来赋值。
7、task不能不释放mutex就退出。
8、mutex不能被重复初始化
9、不能在中断里使用。也不能在软中断里（包括tasklet和timer）。
```

看看mutex结构体定义。

```
struct mutex {
  atomic_long_t owner;
  spinlock_t wait_lock;//内部是靠自旋锁。
  struct list_head wait_list;
};
```

定义其实挺简单的。



那么该怎么使用呢？

1、定义变量。

```
DEFINE_MUTEX(xxx_mutex);
```

2、加锁解锁。

```
mutex_lock
mutex_lock_interruptible
mutex_unlock
```



函数的实现是在kernel/locking/mutex.c里。

看了一下，暂时没看懂。不管。



# semaphore

semaphore的定义比mutex类似。

```
struct semaphore {
  raw_spinlock_t lock;
  uint count;
  struct list_head wait_list;
};
```



定义变量。

```
DEFINE_SEMAPHORE(xxx_sem);
```

使用；

```
up(&xxx_sem);
down(&xxx_sem);
```

看down的实现。这个不是很复杂。正好依次为切入口，分析linux是如何调度的。

```
void down(struct semaphore *sem)
{
	unsigned long flags;

	raw_spin_lock_irqsave(&sem->lock, flags);
	if (likely(sem->count > 0))
		sem->count--;
	else
		__down(sem); 
	raw_spin_unlock_irqrestore(&sem->lock, flags);
}
```





内核里mutex可以用semaphore来做。只要让semaphore只取0和1这2个值就好了。

```
#define DECLARE_MUTEX(name)	\
	struct semaphore name = __SEMAPHORE_INITIALIZER(name, 1)
```

```
#define init_MUTEX(sem)		sema_init(sem, 1)
#define init_MUTEX_LOCKED(sem)	sema_init(sem, 0)
```



