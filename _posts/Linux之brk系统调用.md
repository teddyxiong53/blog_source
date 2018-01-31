---
title: Linux之brk系统调用
date: 2018-01-31 12:17:38
tags:
	- Linux

---



brk和sbrk的主要工作就是实现虚拟内存到物理内存的映射。

brk是系统调用。sbrk是库函数。

brk是break的缩写。



函数原型是：

```
#include <unistd.h>
int brk(void *addr);
void *sbrk(intptr_t increment);
```

在musl libc里，sbrk的实现是这样的：

```
void *sbrk(intptr_t inc)
{
	if (inc) return (void *)__syscall_ret(-ENOMEM);
	return (void *)__syscall(SYS_brk, 0);
}
```

sbrk接受整数作为参数，大于0，堆顶往上走，小于0，堆顶往下走。

如果给0，就可以得到当前的堆顶的位置，可以用来查看是否有内存泄漏。



sbrk参数是相对地址，brk参数是绝对地址。



