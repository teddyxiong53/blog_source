---
title: Linux内核之页高速缓存（二）
date: 2018-04-03 13:57:56
tags:
	- Linux内核

---



本文是对《Linux内核设计与实现》第16章的总结。

页高速缓存，就是page cache，是内核实现磁盘缓存的机制。下面我都用page cache来称呼。

主要目的就是减少对磁盘的io操作。提高效率。也延长磁盘的使用寿命。

具体来说，就是把磁盘的数据缓存到内存里，把对磁盘的访问变成了对内存的访问。

这个机制工作的原理基于下面2个条件：

1、内存比磁盘快多了。

2、局部性原理。

# 缓存手段

page cache是由物理page组成的。

可以动态调整。可以扩展，也可以收缩来缓解内存压力。

当我们进行read操作的时候，首先会到page cache里去找，如果找到了，返回，否则去读取磁盘。

找到了的情况，用术语“命中”来表示。

## 写缓存

写缓存有几种策略：

1、不缓存。直接写入到磁盘。很少用。不仅要写磁盘，还要专门去把内存的内容置位失效。

2、写通。write through。既写内存，也写磁盘。实现最简单。

3、回写。write back。linux用的就是这种。写入到page cache，不马上写入到磁盘。而是把page标记为dirty。dirty page加入到一个链表，后台有一个线程定时往磁盘里写，然后清楚page的dirty标志。

## 缓存回收

理想的回收策略是回收哪些最不可能被使用的page。但是这个无法真正实现。

实际的策略是这些：

1、最近最少使用。

叫做LRU算法。

2、双链策略。

linux实现的是修改过的 LRU，就叫双链策略。

是指2个链表：活跃链表和非活跃链表。

活跃链表上的page是不会被换出的，非活跃链表上的是可以被换出的。

2个链表要保持平衡，如果活跃链表节点多于非活跃链表，就从活跃链表的头移除一个到非活跃链表。

# page cache

page cache里的page可能包含了多个块（硬盘的是 512字节一个块，一个page就有8个块），这些块可能不是连续的（在磁盘上就不连续了）。

所以这就带来了一个困难，如何在page cache里检查特定数据是否被缓存了？

不能用设备名称和块好来做查找索引，不然这就是最简单的定位方法。

为了维持page cache的普遍性（不应该跟物理文件或者inode结构体进绑定），linux的page cache使用了address_space结构体。

这个结构体跟vma结构体是对等的。

当一个文件可以被10个vma结构体标识（例如5个进程，每个进程mmap了这个文件2次）。

这个文件只能有一个address_space结构体。

这个表示的意思就是：文件可以有多个虚拟地址，但是在物理内存里，只能有一份。

address_space这个名字起得非常不好，应该叫page_cache_entry或者physical_pages_of_a_file。



address_space结构体内容：

```
1、struct inode *host 
2、struct radix_tree_root page_tree //包含全部page的radix树。
3、spinlock_t tree_lock //保护page_tree的锁。
4、uint i_mmap_writable //
5、struct prio_tree_root i_mmap //私有映射链表。
6、struct list_head i_mmap_nonlinear //
7、spinlock_t i_mmap_lock //保护i_mmap的锁。
8、atomic_t truncate_count 截断计数
9、ulong nrpages //页的数目。
10、pgoff_t writeback_index //回写的起始偏移。
11、struct address_space_operations *a_ops 
12、ulong flags 
13、struct backing_dev_info *backing_dev_info
14、spinlock_t private_lock 
15、struct list_head private_list
16、struct address_space *assoc_mapping
```



