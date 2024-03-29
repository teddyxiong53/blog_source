---
title: bget内存管理
date: 2023-09-29 11:21:11
tags:
	- 内存
---

--

官方文档在这：

https://www.fourmilab.ch/bget/

BGET 是一个全面的内存分配包，可以轻松配置以满足应用程序的需求。BGET 在分配和释放缓冲区所需的时间以及缓冲池管理所需的内存开销方面都很高效。

**它会自动合并连续空间以最大限度地减少碎片。**

BGET由编译时定义配置，主要选项包括：

- 内置测试程序，用于练习 BGET 并演示如何使用各种功能。
- 通过“首次适应”或“最佳适应”方法进行分配。
- 在释放时擦除缓冲区以捕获引用先前释放的存储的代码。
- 用于转储单个缓冲区或整个缓冲池的内置例程。
- 检索分配和池大小统计信息。
- 将缓冲区大小量化为 2 的幂以满足硬件对齐约束。
- 通过回调用户定义的函数自动池压缩、增长和收缩。

BGET 的应用范围

从基于 ROM 的嵌入式程序中的存储管理

到提供构建包含垃圾收集的多任务系统的框架。

BGET 使用该机制结合了广泛的内部一致性检查 `<assert.h>`；

所有这些检查都可以通过使用定义的编译来关闭`NDEBUG`，从而产生具有最小尺寸和最大速度的 BGET 版本。



BGET底层的基本算法经受住了时间的考验；

自该守则首次实施以来，已经过去五十多年了。

然而，它比许多操作系统的本机分配方案要高效得多：

例如 Macintosh 和 Microsoft Windows，通过将 BGET 作为底层系统之上的应用程序级内存管理器分层，

程序在这些操作系统上获得了显着的加速。

BGET 已[在最大的大型机](https://www.fourmilab.ch/bget/bget1972.html) 和最低的微处理器上实现。

它已成为多任务操作系统、多线程应用程序、数据网络交换处理器中的嵌入式软件以及大量 C 程序的核心。

尽管多年来它的灵活性和附加选项不断增加，但它仍然保持快速、内存高效、便携且易于集成到您的程序中。



BGET 是用尽可能可移植的 C 方言编写的。

关于底层硬件架构的唯一基本假设是分配的内存是一个线性数组，

可以作为 C 的向量进行寻址`char`对象。

在分段地址空间体系结构上，

这通常意味着应该使用 BGET 在单个段内分配存储（尽管某些编译器在分段体系结构上模拟线性地址空间）。

那么，在分段架构上，BGET 缓冲池可能不会大于段，但由于 BGET 允许任意数量的单独缓冲池，因此对可管理的总存储没有限制，仅对可管理的最大单个对象进行限制。分配。

具有线性地址架构的机器，例如本机模式下的 VAX、680x0、SPARC、MIPS 或 Intel 80386 及更高版本，可以不受限制地使用 BGET。



------

BGET 是一个全面的内存分配包，可以轻松配置以满足应用程序的需求。BGET 在分配和释放缓冲区所需的时间以及缓冲池管理所需的内存开销方面都很高效。它会自动合并连续空间以最大限度地减少碎片。BGET由编译时定义配置，主要选项包括：

- 内置测试程序，用于练习 BGET 并演示如何使用各种功能。
- 通过“首次适应”或“最佳适应”方法进行分配。
- 在释放时擦除缓冲区以捕获引用先前释放的存储的代码。
- 用于转储单个缓冲区或整个缓冲池的内置例程。
- 检索分配和池大小统计信息。
- 将缓冲区大小量化为 2 的幂以满足硬件对齐约束。
- 通过回调用户定义的函数自动池压缩、增长和收缩。

BGET 的应用范围从基于 ROM 的嵌入式程序中的存储管理到提供构建包含垃圾收集的多任务系统的框架。BGET 使用该机制结合了广泛的内部一致性检查 `<assert.h>`；所有这些检查都可以通过使用定义的编译来关闭`NDEBUG`，从而产生具有最小尺寸和最大速度的 BGET 版本。

BGET底层的基本算法经受住了时间的考验；自该守则首次实施以来，已经过去五十多年了。然而，它比许多操作系统的本机分配方案要高效得多：例如 Macintosh 和 Microsoft Windows，通过将 BGET 作为底层系统之上的应用程序级内存管理器分层，程序在这些操作系统上获得了显着的加速。

BGET 已[在最大的大型机](https://www.fourmilab.ch/bget/bget1972.html) 和最低的微处理器上实现。它已成为多任务操作系统、多线程应用程序、数据网络交换处理器中的嵌入式软件以及大量 C 程序的核心。尽管多年来它的灵活性和附加选项不断增加，但它仍然保持快速、内存高效、便携且易于集成到您的程序中。



## BGET 入门

尽管 BGET 可以通过多种方式进行配置，

但使用 BGET 的基本方式有三种。

下面提到的功能记录在以下部分中。

请原谅前向引用，这些引用是为了提供路线图来指导您使用可能需要的 BGET 功能。

### 嵌入式应用

嵌入式应用程序通常具有专用于缓冲区分配的固定内存区域（通常位于与包含可执行代码的 ROM 不同的单独 RAM 地址空间中）。

要在这样的环境中使用 BGET，只需调用`bpool()`RAM 中缓冲池区域的起始地址和长度，

然后用 分配缓冲区`bget()`并用 释放它们 `brel()`。

RAM 非常有限但 CPU 速度充足的嵌入式应用程序可能会通过配置 BGET 进行分配而受益 `BestFit`（这在其他环境中通常不值得）。

### `malloc()`仿真

如果 C 库`malloc()`函数太慢，不存在于您的开发环境中（例如，本机 Windows 或 Macintosh 程序），或者不合适，

您可以用 BGET 替换它。

最初定义适当大小的缓冲池`bpool()`— 通常通过调用操作系统的低级内存分配器来获得。

然后使用`bget()`、`bgetz()`和 分配缓冲区`bgetr()`（最后两个允许分配初始化为零的缓冲区和[低效]重新分配现有缓冲区以与 C 库函数兼容）。通过调用释放缓冲区`brel()`。如果缓冲区分配请求失败，则从底层操作系统获取更多存储，通过再次调用将其添加到缓冲池中`bpool()`，然后继续执行。

### 自动存储管理

您可以使用 BGET 作为应用程序的本机内存管理器，并通过使用定义的变量编译 BGET，然后调用和提供用于存储压缩、`BECtl`获取 `bectl()`和释放的函数来实现自动存储池扩展、收缩以及可选的特定于应用程序的内存压缩作为标准池扩展增量。

所有这些函数都是可选的（尽管提供释放函数而不提供获取函数没有多大意义，不是吗？）。一旦用 定义了回调函数`bectl()`，您只需像以前一样使用`bget()`和 `brel()`来分配和释放存储。您可以提供初始缓冲池`bpool()`或依靠自动分配来获取整个池。当有来电时 `bget()`如果不能满足，BGET 首先检查是否已经提供了压缩函数。如果是，则调用它（使用满足分配请求所需的空间和允许连续调用压缩例程而无需循环的序列号）。如果压缩函数能够释放任何存储（它不需要知道它释放的存储是否足够），它应该返回一个非零值，随后 BGET 将重试分配请求，如果再次失败，则再次调用压缩函数与下一个更高的序列号。

## BGET 函数说明

BGET 实现的功能（某些功能通过以下某些可选设置启用）：

```
typedef long bufsize;
void bpool(void *buffer, bufsize len);
void *bget(bufsize size);
void *bgetz(bufsize size);
void *bgetr(void *buffer, bufsize newsize);
void brel(void *buf);
void bectl(int (*compact)(bufsize sizereq, int sequence), void *(*acquire)(bufsize size), void (*release)(void *buf), bufsize pool_incr);
void bstats(bufsize *curalloc, bufsize *totfree, bufsize *maxfree, unsigned long  *nget, unsigned long *nrel);
void bstatse(bufsize *pool_incr, long *npool, unsigned long *npget, unsigned long *nprel, unsigned long *ndget, unsigned long *ndrel);
void bufdump(void *buf);
void bpoold(void *pool, int dumpalloc, int dumpfree);
int bpoolv(void *pool);
bufsize bstatsmaxget(void);
```



# BGET配置

以下变量在 顶部定义bget.c，允许您配置 BGET 的各种功能和操作模式。

```

#define TestProg 20000 /* 生成内置测试程序
                              如果定义的话。该值指定
                              尝试多少次缓冲区分配
                              测试程序应该使。*/

#define SizeQuant 4 /* 缓冲区分配大小量程：
                              所有分配的缓冲区都是
                              该大小的倍数。这
                              必须是 2 的幂。*/

#define BufDump 1 /* 定义该符号以启用
                              bpoold() 函数转储
                              缓冲池中的缓冲区。*/

#define BufValid 1 /* 定义该符号以启用
                              bpoolv() 函数用于验证
                              缓冲池。*/

#define DumpData 1 /* 定义该符号以启用
                              bufdump() 函数允许
                              转储已分配的内容
                              或空闲缓冲区。*/

#define BufStats 1 /* 定义该符号以启用
                              bstats() 函数计算
                              缓冲区中的总可用空间
                              池，最大的可用
                              缓冲区和总空间
                              目前已分配。*/

#define FreeWipe 1 /* 将可用缓冲区擦除到保证的值
                              垃圾绊倒的模式
                              试图使用的不法分子
                              指向已释放缓冲区的指针。*/

#define BestFit 1 /* 使用最佳拟合算法
                              寻找空间
                              分配请求。这使用
                              记忆效率更高，但是
                              分配会慢很多。*/

#define BECtl 1 /* 定义该符号以启用
                              bectl() 函数用于自动
                              池空间控制。*/
```

