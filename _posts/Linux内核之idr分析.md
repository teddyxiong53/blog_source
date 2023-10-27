---
title: Linux内核之idr分析
date: 2019-12-09 13:58:38
tags:
	 - Linux

---

--

从本质上来说，这就是**一种将整数ID号和特定指针关联在一起的机制**。

这个机制最早是在2003年2月加入内核的，当时是作为POSIX定时器的一个补丁。现在，在内核的很多地方都可以找到idr的身影。

遇到这种清况，我们就可以采用idr机制，该机制内部采用radix树实现，**可以很方便地将整数和指针关联起来**，并且具有很高的搜索效率。

实现代码在lib/idr.c里。

```
 * Small id to pointer translation service.
 *
 * It uses a radix tree like structure as a sparse array indexed
 * by the id to obtain the pointer.  The bitmap makes allocating
 * a new id quick.
 *
 * You call it to allocate an id (an int) an associate with that id a
 * pointer or what ever, we treat it as a (void *).  You can pass this
 * id to a user for him to pass back at a later time.  You then pass
 * that id to this code and it returns your pointer.
```

入口是在start_kernel里调用idr_init_cache();

创建了一个kmem_cache

```
void __init idr_init_cache(void)
{
	idr_layer_cache = kmem_cache_create("idr_layer_cache",
				sizeof(struct idr_layer), 0, SLAB_PANIC, NULL);
}
```

# 简介

IDR（ID Register）是Linux内核中用于分配和管理整数标识符（ID）的一种机制。

它通常用于内核中管理诸如文件描述符、进程ID、定时器ID等需要唯一标识符的情况。

IDR是Linux中用于ID分配和管理的首选方法之一，因为它能够高效地处理不同类型的ID分配需求。

以下是关于IDR机制的一些关键信息：

1. **IDR数据结构**：IDR机制使用`struct idr`数据结构来管理分配的ID。这个数据结构包含一个内部的红黑树，用于高效地查找和管理ID。

2. **IDR初始化**：要使用IDR机制，您需要首先初始化一个`struct idr`对象，通常使用`idr_init()`函数。

3. **IDR分配**：使用`idr_alloc()`函数可以分配一个唯一的ID。通常，您需要传递一个指向`struct idr`的指针、希望分配的ID和一个最大的ID值。如果成功，函数将返回分配的ID。

4. **IDR释放**：使用`idr_remove()`函数可以释放分配的ID。通常，您需要传递一个指向`struct idr`的指针和要释放的ID。这将在IDR内部删除该ID，使其可供以后的分配使用。

5. **IDR遍历**：您可以使用`idr_for_each()`函数来遍历IDR中的所有ID。这在某些情况下非常有用，比如清理资源。

6. **IDR的应用**：IDR可用于各种情况，例如管理文件描述符、内核对象的引用计数、设备节点等。它提供了一种有效的方式来维护唯一的ID，而无需手动管理分配和释放。

以下是一个示例，演示如何在内核中使用IDR机制来分配和释放ID：

```c
#include <linux/idr.h>

struct idr my_idr;
idr_init(&my_idr);

int id;
int result = idr_alloc(&my_idr, NULL, 0, 0, GFP_KERNEL);
if (result < 0) {
    // 分配ID失败
} else {
    id = result;
    // 使用分配的ID
    // ...
    // 释放ID
    idr_remove(&my_idr, id);
}

// 在退出时释放IDR资源
idr_destroy(&my_idr);
```

这是一个简单的示例，展示了IDR机制的基本用法。具体的使用取决于您的内核模块或驱动程序的需求。

# 参考资料

1、浅析linux内核中的idr机制

https://blog.csdn.net/ganggexiongqi/article/details/6737389

2、linux中的IDR机制

https://blog.csdn.net/midion9/article/details/50923095