---
title: Linux内核之基础数据结构
date: 2018-04-04 14:46:37
tags:
	- Linux内核

---



跟其他的大型项目一样，linux内核里也实现了一些通用数据结构，并且提倡大家在开发的时候使用。

大家进来用内核提供的数据结构，不要自己去造轮子。

主要有这4种：

1、链表。hlist

2、队列。kfifo

3、映射。idr，比map要简单。够用了。

4、二叉树。



# Linux内核常用数据结构

Linux内核是一个复杂的操作系统内核，它使用各种数据结构来管理系统资源和执行各种任务。以下是一些在Linux内核中常用的数据结构：

1. **链表（List）**：Linux内核中经常使用双向链表和单向链表来组织数据。`list_head` 结构用于表示链表节点，这些链表用于管理各种数据结构，如进程列表、文件描述符列表等。

2. **散列表（Hash Table）**：散列表是一种高效的数据结构，用于快速查找和插入数据。Linux内核使用散列表来管理文件描述符、进程、内存页等。

3. **红黑树（Red-Black Tree）**：红黑树是一种自平衡的二叉搜索树，用于实现高效的查找和插入操作。Linux内核中使用红黑树来管理进程、定时器事件等。

4. **位图（Bit Map）**：位图用于跟踪位的状态，通常用于管理系统中的硬件资源，如内存页面、中断向量等。

5. **堆（Heap）**：堆是一种树状结构，用于实现动态内存分配。Linux内核的内存分配器使用伙伴系统（Buddy System）算法来管理堆内存。

6. **队列（Queue）**：队列用于实现先进先出（FIFO）的数据结构。在内核中，队列用于管理等待进程、I/O 请求等。

7. **栈（Stack）**：栈用于管理函数调用和中断处理。内核使用栈来维护函数调用的上下文。

8. **内存管理结构**：Linux内核使用数据结构来管理物理内存、虚拟内存、页表等。例如，`struct page` 用于表示物理页面。

9. **文件系统数据结构**：Linux内核中的文件系统使用各种数据结构，如超级块（super_block）、inode、目录项（dentry）等来管理文件和目录。

10. **网络数据结构**：Linux内核的网络子系统使用数据结构来表示套接字、网络接口、路由表、数据包缓冲区等。

11. **定时器（Timer）**：Linux内核使用定时器数据结构来实现定时任务和延迟执行操作。

12. **信号量（Semaphore）和自旋锁（Spin Lock）**：用于实现同步和互斥操作，以保护共享资源。

13. **进程控制块（Process Control Block，PCB）**：用于表示和管理进程的状态和属性。

这只是列举了一些在Linux内核中常见的数据结构。Linux内核的复杂性要求使用各种数据结构来管理系统资源、维护内核状态和实现各种功能。这些数据结构是Linux内核的基础构建块，使其能够高效地管理系统资源和提供广泛的功能。

# 双向链表
定义：
struct list_head {
	struct list_head *next, *prev;
};
基本宏定义：

```
#define LIST_HEAD_INIT(name) { &(name), &(name) }
#define LIST_HEAD(name) \
struct list_head name = LIST_HEAD_INIT(name)
```



基本操作：
增
	list_add(new, head);
	list_add_tail(new, head);
	
删
	list_del(entry);
	
改
	list_replace(old, new);
	list_move(list, head);//把list节点移动到另外一个链表head里去。
	list_move_tail(list, head);
	
查
	list_is_last(list, head);
	list_empty(head);
	list_is_singular(head);//看看链表是不是只有一个元素。
	
# 哈希链表hlist
哈希链表也在很多重要的地方有所使用，比如linux内核的dentry，进程查询，
文件系统等，可以说，弄明白hlist对于理解linux内核具有重要的意义。
为什么hlist_head不弄成双向链表呢，因为为了节约空间，
如果一个指针的话，一个哈希数组的空间消耗就会减半。





参考资料

1、Linux内核中的算法和数据结构

https://www.cnblogs.com/arnoldlu/p/6695451.html