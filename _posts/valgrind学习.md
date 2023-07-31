---
title: valgrind学习
date: 2017-04-15 12:55:22
tags:

	- valgrind

---

# valgrind是什么

valgrind是用来在运行时检测程序的内存问题的工具。一个常用的用途就是检测内存泄漏。

# valgrind 发展历史

Valgrind是一款用于检查C/C++程序中内存错误和性能问题的开源工具，其发展历史如下：

- 1999年：Valgrind的前身是一款名为“Vex”的二进制转换引擎，由University of California, Berkeley的一位研究人员Julian Seward开发。Vex的目标是将二进制代码转换为一种中间表示形式，以便在不同的处理器上运行。

- 2000年：Julian Seward在Vex的基础上开发出了Valgrind工具，最初只用于检测内存泄漏和非法内存访问等内存错误。

- 2002年：Valgrind发布了第一个稳定版本，支持检测内存泄漏、非法内存访问、使用未初始化的内存、重复的释放等内存错误。

- 2003年：Valgrind发布了2.0版本，支持检测多线程程序中的内存错误。

- 2004年：Valgrind发布了3.0版本，支持检测CPU缓存访问和分支预测等性能问题。

- 2005年：Valgrind发布了3.1版本，支持检测对未映射虚拟内存地址的访问。

- 2006年：Valgrind发布了3.2版本，支持检测对共享内存的访问。

- 2007年：Valgrind发布了3.3版本，支持检测对堆栈和堆的混用等内存错误。

- 2008年：Valgrind发布了3.4版本，支持检测对文件描述符和网络套接字等资源的泄漏。

- 2010年：Valgrind发布了3.6版本，支持检测对SDL、GTK+和Qt等图形界面库的内存错误。

- 2011年：Valgrind发布了3.7版本，支持检测对OpenGL和OpenCL等图形和计算库的内存错误。

- 2013年：Valgrind发布了3.9版本，支持检测对Android应用程序的内存错误。

- 2017年：Valgrind发布了3.13版本，支持检测对AVX-512指令集的内存错误。

- 2021年：Valgrind发布了3.17版本，支持检测对C++20标准的新特性的内存错误。

Valgrind工具的发展历史表明，它已经成为了C/C++程序调试和优化的重要工具之一，并不断更新、完善和扩展功能，以满足不断变化的需求。

# 基本用法

Valgrind是一个非常强大的工具，可以用于检测C/C++程序中的内存错误、线程问题、锁问题、性能问题等，以下是Valgrind的基本用法：

1. 安装Valgrind：在Linux系统下，可以使用包管理器安装Valgrind，例如：

   `````
   sudo apt-get install valgrind
   ```

2. 编译程序：使用编译器编译您的C/C++程序，需要使用-g选项生成调试信息，例如：

   ````
   gcc -g -o your_program your_program.c
   ````

3. 运行程序：使用Valgrind运行程序，例如：

   ````
   valgrind ./your_program
   ````

   这将启动Valgrind工具，并在运行程序时对其进行监视。Valgrind将检测程序中的内存错误、线程问题、锁问题等，并向您报告这些问题的详细信息。

4. 分析报告：Valgrind将在程序运行结束后生成一个报告文件，您可以使用命令行工具或者GUI工具来分析报告文件。例如，使用命令行工具查看报告文件：

   ````
   valgrind --tool=memcheck --leak-check=full ./your_program > report.txt 2>&1
   ````

   这将使用memcheck工具检测内存错误，并对报告进行完整的泄漏检查。报告将输出到report.txt文件中。

需要注意的是，Valgrind工具的运行会对程序的性能产生一定的影响，因此应该谨慎使用，只在需要检测内存错误、线程问题、锁问题和性能问题时才使用。同时，Valgrind工具只能用于检测通过C标准库中的malloc和free函数分配和释放的内存。如果程序使用了其他分配和释放内存的方式，可能会导致检测不到内存错误。