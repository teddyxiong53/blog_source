---
title: Linux之原子操作
date: 2018-03-08 17:56:07
tags:
	- Linux

---



现代os支持多任务并发，提高效率的同时，也带来了资源竞争的问题。

对于C语言里从count++这个语句，如果不特别处理，都会有并发问题存在。

对于单CPU系统，Intel提供了支持内存操作数的inc指令，让这个操作只有一条指令，所以就是一个原子操作。

但是对于smp系统。inc指令的实际过程是：

```
1、从内存里把count读取到CPU寄存器。
2、累加。
3、存回到内存。
```

这个还是会有问题，不过竞争的主角变成了CPU，而不是进程。

intel又想了一个招，加了一个指令前缀lock。

```
lock inc [count]
```

这下就解决了smp的原子操作问题。

这个我们可以从x86的atomic.h里看出来。

```
static __always_inline void atomic_inc(atomic_t *v)
{
    asm volatile(LOCK_PREFIX "incl %0"
             : "+m" (v->counter));
}
```

```
#ifdef CONFIG_SMP
    #define LOCK "lock ; "
#else
    #define LOCK ""
#endif
```



那么对于arm架构呢？它可没有lock指令前缀啊。

是靠ldrex和strex这2个指令。



# 参考文章

1、Linux的原子操作与同步机制

https://www.cnblogs.com/fanzhidongyzby/p/3654855.html