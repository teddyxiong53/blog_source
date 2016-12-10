---
title: linux驱动并发控制理解
date: 2016-11-29 23:23:53
tags:
	- linux驱动
---
linux内核中，可能产生竞争的主体可能是：
1. SMP系统的各个cpu之间。
2. 单cpu内的进程和进程之间。
3. 进程和中断之间。
4. 中断和中断之间。
上面罗列的情况中，只有SMP系统的真正的并行，其他的系统都是“宏观并行，微观串行”的。
解决竞争问题的关键在于保证对共享资源的互斥访问。
访问共享资源的代码，我们称之为临界区。
互斥机制有如下这些：
1. 中断屏蔽。
这是在单cpu系统里简单省事的一种方法。就是在进入临界区的时候，把中断关闭，出临界区之后，再把中断打开。
但是关闭中断对于linux系统影响较大，所以关闭的时间尽量短。
linux里提供的接口是`local_irq_disable`和`local_irq_enable`。这2个接口只能屏蔽本cpu的中断。对于SMP系统的竞争没用。
单独使用关闭中断的方式，是不推荐的。一般和自旋锁一起用。
关闭中断还有另外一对接口。`local_irq_save`和`local_irq_restore`。这个和前面的不同在于，它在禁止中断的时候，还保存了当前的中断位信息。

2. 原子操作
原子操作是指执行过程中不可能被打断的操作，可以放心使用。
原子操作分两种：对位和对int变量。

3. 自旋锁
对应的英文是spinlock，字面含义是原地打转的锁。一直等到锁有效为止。
一个典型的使用过程如下：
```
spinlock_t mylock;
spin_lock_init(&mylock);
spin_lock(&mylock);//or spin_trylock(&mylock)
//临界区代码。
spin_unlock(&mylock);
```
自旋锁对于SMP系统或者内核可以抢占的单cpu系统有用，其他系统的spinlock是空操作。
自旋锁的注意事项
* 自旋锁是忙等锁，会一直阻塞系统，导致系统效率低下，不宜多用。
* 可能会导致系统死锁。
* 在锁定期间不能调用会导致系统调度的函数。
自旋锁不关心临界区里导致是做什么，不管是读还是写，都是一样看待。但是实际上，对于共享资源的读可以放宽限制的。
所以就衍生了自旋锁的改进版本，读写锁rwlock。
读写锁的一般使用：
```
rwlock_t lock;
rwlock_init(&lock);

read_lock(&lock);
//
read_unlock(&lock);

write_lock_irqsave(&lock, flags);
//
write_unlock_irqrestore(&lock, flags);
```
另外还有顺序锁seqlock和rcu（读拷贝更新）。

4. 信号量
信号量使用起来跟自旋锁差不多，不同在于，在锁定时，不会原地打转，而是使得当前进程进入休眠状态。
一般的使用过程：
```
DECLEAR_MUTEX(mount_sem);
down(&mount_sem);
//
up(&mount_sem);
```
可以用来保证一个设备只能被一个进程打开。代码如下：
```
static DECLARE_MUTEX(xxx_lock);
int xxx_open(...)
{
	if(down_trylock(&xxx_lock))
	{
		return -EBUSY;
	}
	return 0;
}
int xxx_release(...)
{
	up(&xxx_lock);
	
}
```
信号量还可以用来做同步用。一个进程产生信号量，另外一个进程等待这个信号量。
信号量用来做同步作用时，有一个改进版本，叫做完成量completion。
```

```
