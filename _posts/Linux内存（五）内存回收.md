---
title: Linux内存（五）内存回收
date: 2018-03-28 20:51:20
tags:
	- Linux内存

---



页面回收的方式有：

1、页回写。

2、页交换。

3、页丢弃。



回收的时机有：

1、内存紧缺回收。

2、周期性回收。kswapd在后台。

3、用户触发回收。drop_caches。





换出策略有哪些？

fifo策略。不太好，会导致频繁的换入换出。

lru策略。

其他。



内存回收的对象主要是对匿名页和文件页。

对于匿名页，内核会筛选出不常用的匿名页，写入到swap分区。**然后空闲的页框就释放到伙伴系统。**

对于文件页，内核也会筛选出不常用的文件页，如果文件页跟磁盘的内容一致，就认为是干净的页，就直接释放。否则就是脏页，需要先把内容写到磁盘再释放。

这样回收的一个不好的地方就是，对io的压力加大了。所以，内核一般会设置一条水线，来看是不是要释放。

不到水线值，就不会触发回收内存的。

**所以，我们经常会看到cache占据了大量的内存。**

这个水线值在/proc/zoneinfo里可以看到。

```
  ~ # cat /proc/zoneinfo 
Node 0, zone   Normal
  per-node stats
  pages free     27279
        min      345
        low      431
        high     517
```

可以看出，这个值是很小的，所以一般是不会触发内存回收的。



怎样判断一个页是否可以被回收？

就是page结构体里的count值等于0的。这个count是引用计数。

count为-1的时候，页是空闲的。这个就还在伙伴系统里。

如果有一个进程映射了这个页，count会加一。

当一个页被10个进程映射了，它的count肯定大于10 。（因为可能还要驱动等映射了这个页）。

但是，如果是count为0，根本就不需要什么算法来进行释放。

内存回收，就希望把那个count不是0的，想办法减到0 。然后释放掉。



page结构体。有个uint的flag。

取值是枚举值。

```
enum pageflags {
	PG_locked,		/* Page is locked. Don't touch. */
	PG_error,
	PG_referenced,
	PG_uptodate,
```





我看这些换出，都是换出到硬盘。对于嵌入式应该是不存在这种的，flash那么小，速度又那么慢。

不可能把内存换出到flash上的。





# 参考资料

1、linux kernel内存回收机制

http://www.embeddedlinux.org.cn/emb-linux/kernel-driver/201707/14-6973.html

2、linux内存源码分析 - 内存回收(整体流程)

这篇写得很好。很具体。

https://blog.csdn.net/zdy0_2004/article/details/51303568