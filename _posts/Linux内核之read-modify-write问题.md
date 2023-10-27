---
title: Linux内核之read-modify-write问题
date: 2020-08-31 14:42:59
tags:
	- Linux
---

--

read-modify-write的问题本质上是一个保持对内存read和write访问的原子性的问题。

也就是说对内存的读和写的访问不能被打断。

对该问题的解决可以通过硬件、软件或者软硬件结合的方法来进行。

早期的ARM CPU给出的方案就是依赖硬件：

SWP这个汇编指令执行了一次读内存操作、一次写内存操作，

但是从程序员的角度看，SWP这条指令就是原子的，

读写之间不会被任何的异步事件打断。

具体底层的硬件是如何做的呢？

这时候，硬件会提供一个lock signal，在进行memory操作的时候设定lock信号，

告诉总线这是一个不可被中断的内存访问，

直到完成了SWP需要进行的两次内存访问之后再clear lock信号。

lock memory bus对多核系统的性能造成严重的影响（系统中其他的processor对那条被lock的memory bus的访问就被hold住了），

如何解决这个问题？

最好的锁机制就是不使用锁，

因此解决这个问题可以使用釜底抽薪的方法，

那就是不在系统中的多个processor之间共享数据，给每一个CPU分配一个不就OK了吗。

当然，随着技术的发展，在ARMv6之后的ARM CPU已经不推荐使用SWP这样的指令，

而是提供了LDREX和STREX这样的指令。

这种方法是使用软硬件结合的方法来解决原子操作问题，

看起来代码比较复杂，但是系统的性能可以得到提升。

其实，从硬件角度看，LDREX和STREX这样的指令也是采用了lock-free的做法。

**OK，由于不再lock bus，看起来Per-CPU变量存在的基础被打破了。**

**不过考虑cache的操作，实际上它还是有意义的。**



参考资料

1、读-修改-写（Read-Modify-Write）

http://blog.sina.com.cn/s/blog_66a3953f0101rsb3.html