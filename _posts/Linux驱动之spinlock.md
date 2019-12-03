---
title: Linux驱动之spinlock
date: 2018-03-23 13:49:54
tags:
	- Linux驱动

---



我的一个疑问是，自旋锁是怎么做到可以保证在smp系统上的正常运行的？

spinlock是保证访问资源的时候，只有一个线程可以访问。注意是一个线程。

对于CPU来说，调度的资源就是线程。进程是操作系统的概念。

线程既然是CPU的东西，那么这种spinlock肯定就要CPU来支持。

多核CPU，它自己肯定是有机制控制每个线程的运行的。

在smp系统上，spinlock就是真正的自旋等待，对于up系统（单cpu），spinlock只做抢占和中断操作。

没有进行真正意义上的自旋。



# 自旋锁的由来

自旋锁最初就是为了smp系统而设计的。实现在多处理器的情况下保护临界区。

所以smp下的自旋锁才是完整的。而up系统里的自旋锁是阉割的。

但是也只有smp系统里的自旋锁才需要自旋。



自旋锁用来保证自己操作的原子性，有哪些情况会导致自旋锁被干扰？

1、中断。

如果中断会影响你所希望保护的这个临界资源。就把中断屏蔽。如果中断对你的没有影响，就别关闭中断。

2、内核抢占。

我看spinlock里，都加上preempt_disable了。

3、其他处理器对同一临界资源有访问。



说到自旋锁的实现，一个简单的想法是用for循环来等待，但是这样其实是不行的。

因为有这么几个问题：

1、怎么保证其他的处理器没有在同一时间访问同一个标志呢？（也就是标志的独占）。

2、必须保证每个处理器不会去读取cache里的值，而是真正内存里的标志值。（其实编程可以做到，volatile就可以了）

要根本解决这个问题，需要在CPU底层上实现对物理地址的独占访问。

arm从v6版本开始，提供LDREX和STREX指令来实现真正的自旋等待。



# 自旋锁接口的使用

内核提供了好几种自旋锁接口，我们应该怎么区别使用呢？

1、如果你的临界资源只在进程上下文和软中断上下文访问，那么就应该用spin_lock_bh这个函数。

2、如果临界资源只在2个或者多个tasklet或者timer上下文访问。那么对共享资源的访问仅需要用spin_lock。因为tasklet只可能在一个cpu上运行。

3、如果临界资源只在一个tasklet或者timer上下文访问，那么不需要用自旋锁进行保护，即便是smp系统也不用。因为tasklet只可能在一个cpu上运行。

4、spin_lock_irq。



下面是代码分析。



```
#if defined(CONFIG_SMP) || defined(CONFIG_DEBUG_SPINLOCK)
# include <linux/spinlock_api_smp.h> #单核也可以走这个分支。
#else
# include <linux/spinlock_api_up.h>
#endif
```

spin_lock只是禁止了调度。禁止调度实际上就是一个barrier函数。我以服务器的场景进行分析。服务器其实是不怎么支持抢占的，因为抢占会影响吞吐量的。

spin_lock_bh禁止了bh。

```
static inline void __raw_spin_lock_bh(raw_spinlock_t *lock)
{
	__local_bh_disable_ip(_RET_IP_, SOFTIRQ_LOCK_OFFSET);
	spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
	LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);
}

static inline void __raw_spin_lock(raw_spinlock_t *lock)
{
	preempt_disable();
	spin_acquire(&lock->dep_map, 0, 0, _RET_IP_);
	LOCK_CONTENDED(lock, do_raw_spin_trylock, do_raw_spin_lock);
}
```



```
typedef struct spinlock {
  union {
    struct raw_spinlock lock;
  }
} spinlock_t;

typedef struct raw_spinklock {
  arch_spinlock_t rlock;
}raw_spinlock_t;

typedef struct {
  union {
    u32 slock;//这个是关键成员。
    struct __raw_tickets {
      u16 owner;
      u16 next;
    } tickets;
  };
} arch_spinlock_t; //在arch/arm/include/arm/spinlock_types.h里。
```

调用流程是：

```
__raw_spin_lock
	do_raw_spin_lock
		arch_spin_lock
```

对应代码。

```
static inline void arch_spin_lock(arch_spinlock_t *lock)
{
	unsigned long tmp;
	u32 newval;
	arch_spinlock_t lockval;

	prefetchw(&lock->slock);
	__asm__ __volatile__(
"1:	ldrex	%0, [%3]\n"  //可以看到就是用的ldrex指令。
"	add	%1, %0, %4\n"
"	strex	%2, %1, [%3]\n"
"	teq	%2, #0\n"
"	bne	1b"
	: "=&r" (lockval), "=&r" (newval), "=&r" (tmp)
	: "r" (&lock->slock), "I" (1 << TICKET_SHIFT)
	: "cc");

	while (lockval.tickets.next != lockval.tickets.owner) {
		wfe();
		lockval.tickets.owner = ACCESS_ONCE(lock->tickets.owner);
	}

	smp_mb();
}

```

# spinlock在up上的表现

up下的自旋锁。
在spinlock_api_up.h里。

```
spin_lock(spinlock_t *lock)
	raw_spin_lock(&lock->rlock);
		_raw_spin_lock(lock)
			__LOCK(lock)  //这里开始不同的。
				preempt_disable();//只有这句有用。那么就是变成了只是禁止调度了。
				__acquire(lock); 
				(void)(lock);
```



spinlock在不同情况下的表现：

1、up非抢占系统。被忽略了。

2、up抢占系统。变成了禁止调度。

3、smp抢占系统。防止多处理器并发访问临界资源。



# 参考资料

1、http://blog.chinaunix.net/uid-20543672-id-3252604.html

