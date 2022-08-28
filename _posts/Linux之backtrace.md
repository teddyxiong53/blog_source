---
title: Linux之backtrace
date: 2020-05-27 22:28:08
tags:
	- Linux

---

--

backtrace是用来在程序崩溃的时候，把栈信息打印出来。

在Linux的C编程环境下，可以通过下面这3个函数来获取函数的调用栈。

```
#include <execinfo.h>
int backtrace(void **array, int size);
char **backtrace_symbols(void * const *array, int size);
void backtrace_symbos_fd(void *const *array, int size, int fd);
```

这3个函数是gnu的libc提供的。

使用上有这么几点需要注意的：

1、backtrace的实现依赖于栈指针（fp寄存器），在gcc编译器过程中，**加入任何非-O0的优化**，或者加入了栈指针优化参数（-fomit-frame-poiner）后，都不能得到正确的栈信息。

2、backtrace_symbols的实现需要符号名称的支持，在gcc编译过程中要加入**-rdynamic参数。**

3、inline函数没有栈帧。

4、尾调用优化，将复用当前函数栈，这也会导致栈信息不能正确获取。



程序出现异常的时候，一般会收到内核发来的一个信号。

例如常见的内存错误，就是sigsegv。

我们就可以捕获这些信号，处理的时候，进行backtrace调用。



```
=========>>>catch signal 11 (Segmentation fault) <<<=========
Dump stack start...
backtrace() returned 0 addresses
Dump stack end...
```

为什么返回0个地址呢？

The application must be compiled with `-funwind-tables` to make backtrace() work on ARM.

那就再加上这个选项。

现在

# 参考资料

1、在Linux中如何利用backtrace信息解决问题

https://blog.csdn.net/jxgz_leo/article/details/53458366

2、

https://www.cnblogs.com/muahao/p/7610645.html

3、

https://stackoverflow.com/questions/24700150/on-raspberry-pi-backtrace-returns-0-frames