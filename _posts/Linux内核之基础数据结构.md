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