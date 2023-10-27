---
title: Android之toybox分析
date: 2020-04-16 17:38:01
tags:

	- Linux

---

--

# 项目介绍

Toybox是一个适用于Linux系统的开源命令行工具集合项目，

旨在提供一个精简的替代品，

包括一些常见的UNIX工具，如ls、cat、cp、grep等。

这个项目的目标是提供一个小型、高效的工具集，以替代GNU Coreutils等更大型的工具集。

以下是一些Toybox项目的特点和信息：

1. **精简性**：Toybox的设计理念是尽可能精简，仅包含最常用的命令行工具，以减小二进制文件的大小和内存占用。

2. **POSIX兼容**：Toybox工具集的命令行选项和行为力求与POSIX标准一致，以确保与标准UNIX工具的互操作性。

3. **适用于嵌入式系统**：由于其小型和高效的特点，Toybox在嵌入式系统和嵌入式Linux中得到广泛应用。

4. **开源**：Toybox是一个开源项目，遵循自由软件许可协议，使任何人都可以查看、使用和贡献代码。

5. **不断发展**：Toybox项目在不断发展和改进，以适应不同Linux发行版的需求和要求。

Toybox的目标是提供一组轻量级的命令行工具，这些工具在资源受限的环境中非常有用，比如嵌入式系统、嵌入式Linux设备以及需要快速启动和运行的系统。虽然它可能不如某些更大型的工具集功能丰富，但在适当的环境下，它可以是一个有价值的替代品。如需详细信息或获取最新版本，您可以访问Toybox项目的官方网站或源代码仓库。



android为什么选择toybox呢？

toybox跟busybox有哪些区别？

在Android5.0之前，还有了一个toolbox。这个选择已经废弃了，被toybox替换了。

toybox是BSD协议的，busybox的GPL协议的。

toybox存在的价值就是为了规避协议问题。



bin、xbin、sbin的区别

xbin下面放的是extra的工具，例如你自己编译busybox的，就放在xbin目录下，这样就不会覆盖默认的ls、cat这些基础工具。



toybox的代码在aosp/external/toybox目录下。



为了方便分析，我在Ubuntu上编译运行toybox看看。



从这里https://github.com/landley/toybox下载代码。

```
make defconfig # 什么都不改，只是为了生成.config文件。
make -j4
```

当前不能编译过。是lsattr有问题。我把这个屏蔽掉。用make menuconfig去掉这个命令的编译。

再编译就可以了。

生成的toybox在generated/unstripped目录下。

为了方便调试。

修改Makefile里，加上：

```
CFLAGS += -g -O0
```



代码分析

入口文件是main.c。

toys.h

```
#include "generated/config.h"
	这个就是包括了CONFIG宏。
#include "lib/portability.h"
	这个就是可移植性。
	
中间是一堆posix的头文件包含。

#include "lib/lib.h"
	这个定义了一些工具函数。
#include "lib/lsm.h"
	几个函数声明。
#include "lib/toyflags.h"
	几个宏定义。
	
#define NEWTOY(name, opts, flags) void name##_main(void);
#define OLDTOY(name, oldname, flags) void oldname##_main(void);
new和old的区别是？new的有options。old的没有。
举个例子：例如arp的。这个字符串就是options。
(NEWTOY(arp, "vi:nDsdap:A:H:[+Ap][!sd]", TOYFLAG_USR|TOYFLAG_BIN))
old的举例：
(OLDTOY(., source, TOYFLAG_NOFORK))
new比old更多。因为大多数命令都是需要options的。

#include "generated/newtoys.h"
	这个就是生成的所有命令对应的函数声明。
	
#include "generated/flags.h"
	这个就是每个命令的参数。
	这个是各个命令可选的options的字符串宏定义。
#include "generated/globals.h"
	这个是每个命令的数据结构体。
	最后用一个union，把所有的结构体包起来。
	这个就跟busybox里的，用一个全局数组来存放，有异曲同工之妙。
	不过看起来更加好理解一些。
	
#include "generated/tags.h"
	选项的flag宏定义。
struct toy_context toys;
union global_union this;
	表示命令的上下文。
char toybuf[4096], libbuf[4096];
	2个大的是数组。
	
```



生成的config.h内容分析

```
有两种情况，一种是配置打开
#define CFG_BASENAME 1
#define USE_BASENAME(...) __VA_ARGS__
一种是配置关闭
#define CFG_CHSH 0
#define USE_CHSH(...)
```

这些宏会被generated/newtoys.h使用。

这样：

```
USE_SH(OLDTOY(-bash, sh, 0))
USE_SH(OLDTOY(-sh, sh, 0))
```

这里就看到新的宏：OLDTOY

整个编译的逻辑，其实跟busybox的还是比较相似的。



NEWTOY 和OLDTOY根据不同的位置，被反复多地undef和define。



所有的命令都是存放在这个数组里：

```
struct toy_list toy_list[] = {
#include "generated/newtoys.h"
};
```

每个命令的构成：

```
NEWTOY(name, opts, flags) {#name, name##_main, OPTSTR_##name, flags},
```

名字，入口函数，选项，flag。

这个是所有命令共用的context。

```
// Global context shared by all commands.

extern struct toy_context {
} toys;
```



这些generated的头文件是怎么生成的？

是从各个命令的文件头部提取注释生成的？

这个就要看make defconfig做了什么。

```
./make.sh:121:    > "$GENDIR"/newtoys.h
```



# 为什么要推出toybox

https://lwn.net/Articles/202106/

这篇文章有提到一些背景。

我是从代码的www/frq.html里找到这篇文章的地址的。

BusyBox 的维护者是 Rob Landley，他也是toybox的作者。

因此，思考 BusyBox 和 GPLv3 之间关系的任务落在了他身上。由于 BusyBox 可以在如此多的嵌入式系统中找到，它发现自己处于 GPLv3 反 DRM 辩论的核心。GPLv3 许可的 BusyBox 会给任何希望将其整合到锁定产品中的供应商带来明显的困难。

那么背景还就是gplv3的版权问题导致的。

BusyBox 不是 GNU 项目，因此自由软件基金会不拥有其版权；

相反，这些版权由原作者保留。

当 Rob 查看代码时，他发现许多贡献都使用通常的“或任何更新版本”语言，这将允许更改为 GPLv3。然而，其他人有明确的“仅版本 2”语言。其中一些由 Linus Torvalds 贡献，声明它们“可以根据 Linux 版权重新分发”。其他一些贡献带有 BSD 许可证——最初带有与 GPL 不兼容的广告条款。这完全是许可证的混合体。

就是Rob不愿意更新到GPLV3，这个跟有些人产生了冲突。所以他就从零开始写了这个项目。

# 有了busybox，为什么还要有toybox

BusyBox 和 Toybox 都是用于嵌入式系统和资源受限环境下的精简命令行工具集。它们的存在有一些历史背景和技术特点，解释了为什么有两个类似的项目。

1. **历史背景**：BusyBox 是第一个为嵌入式系统设计的精简命令行工具集。它在嵌入式领域非常流行，并且广泛使用。Toybox 则是后来出现的项目，旨在提供另一种选择，以满足不同需求的嵌入式系统和发行版。

2. **开发者和社区**：不同的开发者和社区支持这两个项目。这种多样性意味着不同的特性和优化，以及不同的方法和哲学可能被应用到这两个项目中。

3. **技术特点**：虽然 BusyBox 和 Toybox 都旨在提供相似的功能，但它们的设计和实现方法略有不同。例如，Toybox 的目标是更加精简，它的工具集相对较小，可以在一些非常受限的环境下运行。而 BusyBox 的目标是提供更多功能和工具，因此它可能相对更大。

4. **许可协议**：BusyBox 使用GPL（GNU通用公共许可证）许可，这使得它有一些要求，如必须开源整个系统。而 Toybox 使用更宽松的许可协议，可以更灵活地集成到各种系统中。

总之，BusyBox 和 Toybox 都有其特点，可以根据具体需求来选择。在嵌入式系统领域，开发者可以根据项目的资源需求和许可协议等因素来选择使用哪一个工具集，以满足其项目的特定要求。





# 参考资料

1、

https://blog.csdn.net/ly890700/article/details/72615465