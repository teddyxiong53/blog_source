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

