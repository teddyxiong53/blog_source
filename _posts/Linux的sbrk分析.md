---
title: Linux的sbrk分析
date: 2017-03-02 22:20:17
tags:
	- linux
---
Linux中每个用户进程可以访问的虚拟内存空间为3G，但是一般写程序用不了这么多，所以系统默认只给程序分配了并不大的数据段空间，如果空间不够时，malloc函数内部会调用sbrk函数，再把数据段的边界移动，sbrk函数再内核的管理下，将虚拟地址空间映射到内存。
sbrk并不是系统调用，而是一个C库函数。
我们可以用sbrk(0)来查询当前程序用到的内存是多少。示例如下：
```

int main()
{
	int start ,end;
	start = sbrk(0);
	malloc(0x1);
	end = sbrk(0);
	printf("used memory:0x%x \n", end - start);
}

```

# 单片机里的sbrk

我看newrtos的代码，

https://github.com/cpq/newrtos

这个里面有这样的方法：

```
__attribute__((weak)) void *_sbrk(ptrdiff_t diff) {
  char *old = s_brk;
  if (&s_brk[diff] > s_heap_end) {
    errno = ENOMEM;
    return NULL;
  }
  s_brk += diff;
  return old;
}
```

这个没自己去实现malloc函数。就是靠_sbrk来接管标准库的malloc、free等的行为。

这个是newlib这个C库的行为。

```
// Initialise newlib malloc. It expects us to implement _sbrk() call,
// which should return a pointer to the requested memory.
// Our `rtos_heap_init` function sets up an available memory region.
//
//   s_heap_start                s_brk               s_heap_end
//      |--------------------------|----------------------|
//      |      (used memory)       |    (free memory)     |
```





`_sbrk` 函数与内存分配有关，它通常用于管理C/C++程序的堆内存。`_sbrk` 是一个系统调用，它允许程序在运行时动态地增加或减少堆内存的大小。

以下是 `_sbrk` 函数与内存分配之间的关系：

1. **堆内存管理**：堆内存是用于动态分配内存的一块区域。C/C++中的函数如 `malloc`、`calloc` 和 `realloc` 通常用于在堆上分配内存。这些函数会通过 `brk` 或 `sbrk` 系统调用来扩展或缩小堆内存的大小。

2. **sbrk 系统调用**：`_sbrk` 函数通常是一个封装了系统的 `sbrk` 系统调用的C库函数。`sbrk` 允许程序在堆的末尾增加或减少内存块的大小。当程序需要更多内存时，`sbrk` 可以增加堆的大小，使其包含新分配的内存。当程序释放内存时，`sbrk` 可以缩小堆的大小，以释放不再使用的内存。

3. **内存分配器**：通常，C/C++标准库中的内存分配函数（如 `malloc` 和 `free`）会使用 `_sbrk` 或 `sbrk` 来管理堆内存的分配和释放。这些函数会调用 `_sbrk` 来请求更多内存或释放不再需要的内存块。

4. **注意事项**：虽然 `_sbrk` 可以用于管理堆内存，但在现代操作系统中，更常见的是使用更高级别的内存分配器（如`malloc`库的分配器）来管理堆内存。这些分配器通常比直接使用 `_sbrk` 更高效且更易于使用。

总之，`_sbrk` 函数与内存分配紧密相关，它允许程序在运行时动态管理堆内存的大小。然而，在实际应用中，通常会使用更高级别的内存分配函数来更方便地进行内存管理。



从musl clib里看看这个函数是怎么做的。

没有这个。