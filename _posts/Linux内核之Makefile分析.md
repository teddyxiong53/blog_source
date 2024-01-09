---
title: Linux内核之Makefile分析
date: 2023-12-27 16:36:28
tags:
	- Linux
---

--

以5.4的内核作为分析对象。

总的Makefile有2000行。

# Linux kernel Makefile文件分析

Linux内核的Makefile是一个非常庞大且复杂的文件，它负责整个内核的编译和构建过程。我可以向你介绍一些Makefile的基本结构和主要部分。

1. **顶层Makefile：** 位于Linux内核源代码的顶层目录，通常命名为`Makefile`或`Makefile`开头的文件。它负责协调整个编译过程，调用各个子目录下的Makefile。

2. **子目录Makefile：** Linux内核源代码包含许多子目录，每个子目录都有自己的Makefile。这些Makefile负责编译和构建各个子模块，然后将它们整合到最终的内核镜像中。

3. **变量定义：** Makefile包含了大量的变量定义，用于指定编译器、编译选项、源文件列表等。这些变量可以在整个Makefile中使用，通过改变这些变量的值可以修改编译的行为。

4. **目标规则：** Makefile定义了一系列的目标规则，描述了如何生成最终的内核镜像。常见的目标包括`all`（编译所有）、`clean`（清理编译产生的文件）、`install`（安装内核）、`modules`（编译模块）等。

5. **条件判断和循环：** Makefile中可以包含条件判断和循环结构，根据不同的条件执行不同的编译操作。这些条件可以基于环境变量、系统架构、编译器版本等。

6. **包含其他Makefile：** Makefile可以包含其他Makefile，通过`include`指令引入其他文件，可以使得Makefile结构更加清晰和模块化。

7. **命令规则：** 每个目标都会有对应的命令规则，描述了如何生成该目标。这些规则通常包含了编译命令、链接命令等。

对于深入理解Linux内核的Makefile，需要逐步阅读和理解其中的代码结构和逻辑。建议通过阅读Linux内核源代码及相关的文档来逐步领会其工作原理和编译流程。

# kernel的makefile target说明

Linux内核的Makefile中包含了大量的目标（targets），用于执行各种编译、清理、安装等操作。这些目标的名称和功能在不同版本的内核中可能会有所不同，但是一些常见的目标包括：

1. **all（或vmlinux）：** 编译整个内核并生成`vmlinux`文件，这是未经压缩的内核镜像。

2. **clean：** 清理编译过程中生成的临时文件，以便重新开始编译。

3. **modules：** 编译内核模块，生成`.ko`文件。

4. **install：** 将编译完成的内核安装到指定的目录，使得系统可以启动这个新的内核。

5. **mrproper（或distclean）：** 执行比`clean`更彻底的清理，包括清除配置和头文件，将内核源代码还原到初始状态。

6. **menuconfig（或config）：** 打开一个菜单式的界面，允许用户配置内核的编译选项。

7. **xconfig、gconfig、nconfig：** 类似于`menuconfig`，但使用不同的图形界面。

8. **bzImage（或vmlinuz）：** 生成一个可引导的压缩内核镜像文件，一般用于实际部署到系统中。

9. **headers_install：** 安装内核头文件，使得开发人员可以编译和构建外部内核模块。

10. **modules_install：** 安装编译好的内核模块到指定目录。

这只是一些常见的目标，实际上，Linux内核的Makefile可能包含许多其他的目标，用于执行更加细致的操作或针对特定的需求。要了解特定内核版本的所有可用目标及其功能，最好查阅该版本内核源代码中的Makefile或相关文档。

# target的分类

```
clean-targets := %clean mrproper cleandocs
no-dot-config-targets := $(clean-targets) \
			 cscope gtags TAGS tags help% %docs check% coccicheck \
			 $(version_h) headers headers_% archheaders archscripts \
			 %asm-generic kernelversion %src-pkg
no-sync-config-targets := $(no-dot-config-targets) install %install \
			   kernelrelease
single-targets := %.a %.i %.ko %.lds %.ll %.lst %.mod %.o %.s %.symtypes %/
```

clean类的

不依赖.config的

单个目标的

# Makefile 中 LINUXINCLUDE 的作用

在驱动开发的时候，我们经常会创建很多新的头文件，这些头文件大多以#include"xxx.h"的形式放在源码中。

而内核头文件则是以#include <xxx.h>的形式存在。

实际移植过程中遇到的问题是，#include"xxx.h"形式的头文件，它的路径通常会很长，代码耦合性相对更高一些。

如果能改成#include <xxx.h>的形式，那么是更好的选择。

如何将自己写的头文件添加到标准路径？

看一个Makefile的例子：

LINUXINCLUDE += -Idrivers/klsp/drivers/net/pifm/include



这其中有一个LINUXINCLUDE 就是做了相应的操作，

具体应该是在根目录下的Makefile，会将LINUXINCLUDE中的所有路径添加到标准检索中。

直接从源码的变化上看效果：

原先路径是：

#include "../../../include/pif.h"

修改Makefile之后，代码中可以改为：

#include <pif.h>

这样的一个好处就是，从代码的可维护性、可读性角度来说，这肯定是更好的一个选择！

参考资料

1、

https://blog.csdn.net/Ivan804638781/article/details/113250556

# Module.symvers

`Module.symvers` 文件是 Linux 内核模块编译过程中生成的一个重要文件。

它记录了编译生成的模块的符号版本信息。

当你编译内核模块时，模块代码中会引用一些内核提供的函数或者符号。

`Module.symvers` 文件记录了这些模块代码使用的符号及其版本信息，以便在模块加载时与内核进行匹配。

这个文件的创建过程通常是这样的：

在编译内核模块时，模块代码中使用的符号会被记录在 `Module.symvers` 中，

包括这些符号的名称、类型以及版本信息。

当模块加载到内核时，系统会检查该模块所需的符号是否与当前内核中的符号匹配，如果匹配，则允许模块加载；否则，加载会失败。

这个文件的存在确保了模块在编译和加载时使用了正确版本的符号，有助于确保模块与当前内核的兼容性。

# make HOSTCC=gcc  -isystem

这个命令看起来像是一个在 Linux 内核源代码目录下运行的 Makefile 命令。让我解释一下这个命令的不同部分：

- `make`: 这是调用 Make 工具来执行 Makefile 中定义的指令，用于构建或编译项目。

- `HOSTCC=gcc`: 这个部分设置了一个环境变量 `HOSTCC`，指定了用于主机编译器的程序。在这个命令中，`HOSTCC` 被设置为 `gcc`，表示使用 GCC 作为主机编译器。

- `-isystem`: ==这个选项通常用于告诉编译器去指定的目录中查找系统头文件==。在这个命令中，似乎被截断了，后面缺少了要添加的目录路径。正常情况下，你会在 `-isystem` 后面加上系统头文件所在的路径。

这个命令的完整形式可能是类似下面的样子：

```bash
make HOSTCC=gcc -isystem/path/to/system/headers
```

其中 `/path/to/system/headers` 是系统头文件的实际路径。这个命令告诉 Make 使用指定的 GCC 作为主机编译器，并且添加了一个系统头文件搜索路径，以确保在编译时能够正确地引用系统头文件。

# make prepare做了什么

`make prepare` 是一个针对 Linux 内核源代码的 Makefile 中定义的一个目标（target），用于准备内核构建所需的一些基本文件和配置。

当你在内核源代码目录下运行 `make prepare` 时，它通常会执行一系列操作，包括但不限于以下内容：

1. **生成 Makefile：** 确保生成了编译内核所需的 Makefile 文件，其中包含了构建内核所需的编译选项和规则。

2. **生成配置文件：** 确保生成了 `.config` 或其他类似的配置文件，这个文件包含了编译内核时所需的配置选项和参数。

3. **生成头文件或其他预处理文件：** 在某些情况下，`make prepare` 可能会生成一些预处理的头文件或其他文件，这些文件可能是构建过程中需要的。

4. **创建符号链接或目录结构：** 可能会在构建过程中创建一些符号链接或者目录结构，用于确保编译过程能够顺利进行。

总的来说，`make prepare` 是用来准备内核构建过程中所需的基本文件和配置，它确保了在编译内核之前，系统处于一个可以进行编译的状态。