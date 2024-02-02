---
title: glibc（1）
date: 2023-02-08 10:42:17
tags:
	- glibc

---

--

glibc是非常基础的库，值得研究一下。

查看glibc的版本：

```
ldd --version
```

例如这样：

```
ldd (Ubuntu GLIBC 2.31-0ubuntu9.7) 2.31
```

glibc的版本有什么需要注意的？



# 什么是 glibc？

GNU C 库项目为 GNU 系统和 GNU/Linux 系统以及许多其他使用 Linux 作为内核的系统提供*核心*库。

这些库提供关键 API，

包括 ISO C11、POSIX.1-2008、BSD、特定于操作系统的 API 等。

这些 API 包括诸如`open`、 `read`、`write`、`malloc`、`printf`、 `getaddrinfo`、`dlopen`、`pthread_create`、 `crypt`、`login`、`exit`等基础设施。



在20世纪90年代初，[Linux内核](https://zh.wikipedia.org/wiki/Linux内核)的开发团队[分叉](https://zh.wikipedia.org/wiki/分叉_(软件开发))了Glibc，名为“Linux libc”并单独维护。

当FSF在1997年1月发布glibc 2.0时，**由于glibc 2.0更符合POSIX标准**，内核开发者停止了Linux libc的开发。[[9\]](https://zh.wikipedia.org/zh-cn/GNU_C函式庫#cite_note-9) glibc 2.0还具有更好的[国际化](https://zh.wikipedia.org/wiki/国际化与本地化)和翻译、[IPv6](https://zh.wikipedia.org/wiki/IPv6)功能、64位数据访问、[多线程](https://zh.wikipedia.org/wiki/多线程)支持、未来版本的兼容性，而且代码更加可移植。



从2014年开始，[EGLIBC](https://zh.wikipedia.org/wiki/EGLIBC)不再开发，因为它“现在的目标是在glibc上直接解决问题”。



对于大多数系统来说，glibc的版本可以通过解析lib文件（例如，/lib/libc.so.6）获得。

glibc还提供了在开发[GNU](https://zh.wikipedia.org/wiki/GNU)时被认为有用或必要的扩展。



GNU C 库旨在成为一个向后兼容、可移植且高性能的 ISO C 库。它旨在遵循所有相关标准，



该项目大约于 1988 年开始，至今已有 30 多年的历史。

GNU C 库每 6 个月发布一次。有关详细信息，请参阅 glibc 源中的[新闻文件](https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=NEWS;hb=HEAD)。

- glibc 当前的稳定版本是 2.37，发布于 2023 年 2 月 1 日。
- glibc 当前的开发版本为 2.38，发布时间为 2023 年 8 月 1 日左右。

# glibc vs musl

musl是一个比较简单的libc。

以musl作为参照系，来看看glibc。

musl遵循POSIX 2008规格和 C99 标准，采用MIT许可证授权，使用Musl的Linux发行版和项目包括sabotage，bootstrap-linux，LightCube OS等等。



然而musl的源代码很简单, 不像glibc的代码一样乱如垃圾场, 将性能较慢的函数换掉就能取得较大的性能提升.

# glibc和libgcc是什么关系

glibc 和 libgcc 是在 Linux 系统中使用的两个不同的库，它们分别负责不同的功能：

1. **glibc (GNU C Library)**:
   - glibc 是 GNU 项目开发的 C 库，是 Linux 系统中最基本和重要的库之一。
   - 它提供了对 C 语言的标准函数和系统调用的访问，以及许多其他基本功能，如内存分配、文件操作、进程控制等。
   - glibc 包含了 C 语言标准库的实现，使得应用程序可以在 Linux 系统上运行并与操作系统进行交互。

2. **libgcc (GCC Library Support)**:
   - ==libgcc 是 GCC（GNU Compiler Collection）的一部分，提供了编译器运行时支持的一些关键功能。==
   - 它包含了编译器运行时所需的支持函数，例如用于处理整数溢出、浮点数运算、异常处理等的函数。
   - libgcc 还包含一些编译器内置的函数和辅助功能，帮助编译器生成的代码能够正确地运行。

这两个库在不同的层面提供支持，glibc 提供了对操作系统 API 的高级访问，而 libgcc 则提供了编译器所需的低级支持。在编译程序时，编译器（如 GCC）可能会依赖于这两个库来完成编译和链接过程中的各种操作。

总体而言，glibc 是面向操作系统 API 和 C 语言标准库的，而 libgcc 则提供了与编译器相关的支持函数和工具。两者都是 Linux 系统中必不可少的组件，用于确保程序正确运行并与操作系统和硬件交互。

# 辅助运行库

我们用c语言写一个程序，入口是main函数，

那么这个main函数是被谁调用了呢？

就是crt0.o的`_start`调用了main函数。

`_start`是真正的入口函数。

你可以自己写汇编文件，入口就写成`_start`。

crt是C RunTime的缩写。

之前的crt0.o包含了很多的东西，

现在已经被拆分成5个文件：crt1.o、crti.o、crtbegin.o、crtend.o、crtn.o。

前面这5个目标文件的作用分别是启动、初始化、构造、析构和结束，它们通常会被自动链接到应用程序中。



假设我们的c程序名字叫test.c，编译的o文件叫test.o。

那么连接的过程是这样的：

先链接crt1.o、crti.o、crtbegin.o。

再链接我们的test.o。

再链接crtend.o、crtn.o。

最后链接用到的库。



## -nostdlib

如果不进行标准的链接的话（编译选项-nostdlib），我们就必须指明这些必要的目标文件，

如果未指定，链接器就会提示找不到_start符号，并因此导致链接失败。



编译时加上选项(-nostdlib)

 

-nostdlib
不连接系统标准启动文件和标准库文件，只把指定的文件传递给连接器。

**这个选项常用于编译内核、bootloader等程序，它们不需要启动文件、标准库文件。**



C语言程序执行的第一条指令。并不是main函数。生成一个C程序的可执行文件时编译器通常会在我们的代码上加上几个被称为启动文件的代crt1.o,crti.o,crtend.o,crtn.o等，他们是标准库文件。这些代码设置C程序的堆栈等，然后调用main函数。他们依赖于操作系统，在裸板上无法执行，所以我们自己写一个。

**所以，我们自己写的*.S汇编文件就是一个启动文件，它设置好堆栈后调用main函数。因此，我们不需要系统自带的启动文件。**

## crt0.o的实现

可以看musl库的实现，这个比较简单。

crt\crt1.c



1、 crti.o

https://www.cnblogs.com/xpylovely/p/11412380.html

2、ARM-LINUX-GCC -NOSTDLIB

http://blog.chinaunix.net/uid-26739173-id-3154722.html



# libgcc_s

`libgcc_s` 是 GCC（GNU Compiler Collection）提供的一个共享库，

（后面跟的s这个字母就是表示共享库的意思吧）

用于支持一些编译器生成的代码和运行时支持。

它包含了一些与编译器相关的支持函数，

特别是与异常处理、线程局部存储（Thread-Local Storage，TLS）等方面有关。

以下是关于 `libgcc_s` 的一些重要信息：

1. **异常处理：** `libgcc_s` 包含用于支持 C++ 异常处理的函数。当你在程序中使用 C++ 并抛出异常时，`libgcc_s` 中的函数会负责处理异常的传播和相关操作。

2. **线程局部存储（TLS）：** 在多线程程序中，线程局部存储是一种使每个线程都有自己独立的变量的机制。 `libgcc_s` 提供了与 TLS 相关的支持函数，用于管理线程局部存储。

3. **一些特殊的编译器内建函数的实现：** GCC 在编译代码时可能会使用一些特殊的内建函数，例如 `__builtin_mul_overflow`、`__builtin_sadd_overflow` 等。这些内建函数的实现可能依赖于 `libgcc_s` 提供的功能。

4. **编译器运行时支持：** `libgcc_s` 中包含了一些编译器运行时的支持函数，用于处理一些特殊的运行时情况，例如整数溢出检测。

在使用 GCC 编译程序时，通常会自动链接 `libgcc_s`。这确保了在运行时能够调用其中的函数，以便正确处理编译器生成的代码。在链接命令中，可以看到类似 `-lgcc_s` 的选项，这表示链接器会将 `libgcc_s` 包含在最终的可执行文件中。

需要注意的是，`libgcc_s` 的具体实现可能会随着 GCC 版本的变化而有所不同。

# 参考资料

1、官网

https://www.gnu.org/software/libc/

2、维基百科

https://zh.wikipedia.org/zh-cn/GNU_C%E5%87%BD%E5%BC%8F%E5%BA%AB

3、官方手册

https://www.gnu.org/software/libc/manual/

4、glibc和musl对比

https://wiki.musl-libc.org/functional-differences-from-glibc.html

5、musl和glibc，性能区别到底有多大？

https://www.zhihu.com/question/550951106