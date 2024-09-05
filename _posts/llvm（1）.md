---
title: llvm（1）
date: 2023-06-06 15:48:11
tags:
	- 编译
---

--

# 资源收集

Getting Started with LLVM Core Libraries

https://getting-started-with-llvm-core-libraries-zh-cn.readthedocs.io/zh-cn/latest/index.html

# llvm发展历史

LLVM（Low Level Virtual Machine）是一个开源的编译器基础设施项目，它提供了一组用于构建编译器和相关工具的库和工具链。以下是LLVM的发展历史的主要里程碑：

1. 2000年：LLVM项目的起源可以追溯到2000年，由Chris Lattner在伊利诺伊大学香槟分校开始开发。最初的目标是为了实现一种新型的编译器架构，以提供更高的优化能力和灵活性。

2. 2003年：LLVM发布了第一个公开版本，也成为LLVM 1.0版。

3. 2005年：LLVM逐渐发展成为一个完整的编译器基础设施项目，支持多种编程语言和目标平台。

4. 2011年：LLVM开始引入Just-in-Time（JIT）编译技术，使得动态编程语言如Python和Ruby能够在运行时进行即时编译，提高执行速度。

5. 2012年：LLVM发布了3.1版，引入了对C++11标准的支持。

6. 2015年：LLVM 3.6版发布，引入了对C++14标准的支持，并继续改进编译器优化和工具链。

7. 2016年：LLVM 3.9版发布，引入了对C++17标准的支持，并提供了新的性能分析和调试工具。

8. 2017年：LLVM 5.0版发布，引入了对WebAssembly的支持，使得LLVM能够编译为Web平台的目标代码。

9. 2019年：LLVM 9.0版发布，引入了对RISC-V架构的支持，成为了一个广泛使用的编译器基础设施。

10. 2020年：LLVM 11.0版发布，继续改进编译器优化和工具链，并增加对新的硬件架构和编程语言的支持。

LLVM项目的持续发展和广泛应用使得它成为了一个重要的编译器基础设施，被许多编程语言和工具所采用，包括Clang、Rust、Swift等。

# 哪些编译器是基于llvm的？

LLVM作为一个开源的编译器基础设施项目，许多编译器和工具都是基于LLVM构建的。以下是一些基于LLVM的知名编译器和工具的示例：

1. Clang：Clang是一个C、C++和Objective-C编译器，它是LLVM项目的一部分。Clang具有高度可扩展性、快速编译速度和精确的错误报告，被广泛用作代替传统的GCC编译器套件的选择。

2. Rust编译器：Rust是一种现代的系统编程语言，其默认编译器也是基于LLVM构建的。LLVM提供了Rust语言的优化和代码生成能力。

3. Swift编译器：Swift是一种由苹果公司开发的现代编程语言，其编译器也是基于LLVM构建的。LLVM提供了Swift语言的代码生成和优化能力。

4. Julia编程语言：Julia是一种高性能的动态编程语言，其编译器部分是基于LLVM实现的。LLVM为Julia提供了即时编译（JIT）能力，使得代码可以在运行时进行优化和执行。

5. Emscripten：Emscripten是一个将C/C++代码编译为WebAssembly（Wasm）的工具链。它使用LLVM作为核心，通过将C/C++代码转换为LLVM IR，然后再编译为Wasm代码。

除上述之外，还有许多其他编译器和工具，如Crystal编译器、Haskell的GHC编译器的LLVM后端等，都是基于LLVM构建的。LLVM的灵活性和可扩展性使得它成为许多编程语言和工具的首选编译器基础设施。

# llvm和gcc比较

LLVM（Low Level Virtual Machine）和GCC（GNU Compiler Collection）是两个广泛使用的编译器基础设施，它们在编译器领域有一些不同之处，以下是它们的比较：

1. 架构和设计：LLVM和GCC在架构和设计上有所区别。LLVM采用了基于中间表示（Intermediate Representation，IR）的设计，其中编译过程包括将源代码转换为LLVM IR、优化IR并将其转换为机器码。GCC则使用了一系列传统的编译阶段，如预处理、编译、汇编和链接。

2. 语言支持：GCC是一个多语言编译器，可以编译C、C++、Fortran、Ada等多种语言。LLVM也支持多种语言，但它的设计更加灵活，易于扩展和添加新的语言前端。

3. 编译速度：在编译速度方面，一般情况下，GCC的编译速度比LLVM快。LLVM的设计注重优化和生成高质量的代码，这可能会导致编译时间较长。但是，LLVM的优化能力可以产生更高效的代码。

4. 优化能力：LLVM在优化方面具有强大的能力，它提供了许多高级优化技术，如逃逸分析、自动向量化等。GCC也提供了一些优化选项，但相对来说LLVM的优化能力更强。

5. 可移植性：GCC在多个平台上都有广泛的支持，包括各种操作系统和处理器架构。LLVM也具有较好的可移植性，并且正在积极扩展其支持的平台范围。

6. 社区和生态系统：GCC拥有庞大的社区和生态系统，有很多年的发展历史，并且许多开源项目和商业软件都在使用GCC。LLVM的社区也在不断增长，并且有许多基于LLVM的工具和项目。

总体而言，LLVM和GCC都是强大的编译器基础设施，它们在设计、性能、优化等方面有所差异。选择使用哪个编译器取决于具体的需求和项目要求。

# llvm-project

https://github.com/espressif/llvm-project

该存储库包含 LLVM 的源代码，LLVM 是一个用于构建高度优化的编译器、优化器和运行时环境的工具包。

LLVM 项目有多个组件。该项目的核心本身称为“LLVM”。其中包含处理中间表示并将其转换为目标文件所需的所有工具、库和头文件。工具包括汇编器、反汇编器、位码分析器和位码优化器。

类 C 语言使用 Clang 前端。该组件使用 LLVM 将 C、C++、Objective-C 和 Objective-C++ 代码编译成 LLVM 位码，并从那里编译成目标文件。

其他组件包括：libc++ C++ 标准库、LLD 链接器等。