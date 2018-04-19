---
title: Linux内核之网络子系统（三）skb
date: 2018-04-18 10:33:05
tags:
	- Linux内核

---



本文主要参考《Linux内核源码剖析 TCPIP实现》第三章。

skb主要涉及的文件有：

1、include/linux/skbuff.h。

2、net/core/skbuff.c。



# sk_buff结构体

sk_buff结构体是linux系统里最复杂的也最重要的结构体之一。

用来描述已接收或者待发送的数据报文信息。

目的是为了在网络协议栈的各层之间无缝传递，灵活处理。

其成员可以分为这几类：

1、与skb组织相关的。

2、通用的。

3、标志性变量。

4、与特性相关的成员变量。

skb在不同的网络协议层之间传递。

例如二层的mac、三层的ip、四层的tcp。

四层向三层传递，会添加一个四层的头。三层向二层传递，会添加一个三层的头。

这个过程是修改指针，不是复制数据。

通过skb_reserve来完成这个功能。

如果是从下面往上传递，也只是修改指针的值，不会把头删掉。



结构体的最前面是一个prev和next指针。

另外有一个头结点的专门的结构体。

```
struct sk_buff_head {
	/* These two members must be first. */ //注意这个注释，
	struct sk_buff	*next;
	struct sk_buff	*prev;
	__u32		qlen;
	spinlock_t	lock;
};
```

头结点的定义很简单。就长度、操作锁。

# 管理函数

在网络模块里，有很多函数都比较短小而简单。

内核用这些函数来操作skb里的变量或者skb链表。

在skbuff.c和skbuff.h里，很多函数有2个版本，名字分别是：

```
do_something()
__do_something()
```

不带下划线的是带下划线的版本基础上加上了合法性校验和锁机制的。

```
static inline do_something(para)
{
  ulong flags;
  spin_lock_irqsave(..);
  __do_something();
  spin_unlock_irqrestore(...);
}
```

我们不要用带下划线的。

1、skb_init。

这里调用kmem_cache_create。创建了skbuff_head_cache。

要分配的skb都是从这里分配的。

另外还创建了skbuff_fclone_cache。这个的用途是：

如果在分配skb的时候，就知道有可能需要被克隆。那么就从这个缓冲区里分配。这样在克隆的时候，就不需要再次分配skb了。

2、分配skb。alloc_skb。

```
static inline struct sk_buff *alloc_skb(unsigned int size,
					gfp_t priority)
{
	return __alloc_skb(size, priority, 0, -1);
}
```

dev_alloc_skb这个函数，一般是用在中断上下文里。

3、释放skb。

kfree_skb。

dev_kfree_skb。

4、数据预留和对齐

主要是这几个函数：

skb_reserver

skb_put

skb_push

skb_pull。

5、克隆和赋值skb。

skb_clone

pskb_copy

6、链表管理函数。

skb_queue_head_init。

skb_queue_head

skb_queue_tail

skb_dequeue

skb_dequeue_tail

skb_queue_purge

skb_queue_walk

7、添加或者删除尾部数据。

skb_add_data

skb_trim

pskb_trim

8、拆分数据。

skb_split。

9、重新分配skb的线性数据区。

pskb_expand_head。

10、其他函数。

