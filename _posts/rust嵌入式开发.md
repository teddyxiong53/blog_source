---
title: rust嵌入式开发
date: 2024-04-15 17:08:17
tags:
	- rust

---

--

https://github.com/rust-embedded/cortex-m

以这个为切入点来学习。

# core模块

`core`模块是Rust语言的标准库中的一个模块，

它包含了许多基本的 Rust 类型、traits 以及常见的 Rust 语言功能。

与 `std` 模块相比，`core` 是一个更加轻量级的标准库，

主要用于提供基本的语言功能和不依赖于操作系统的功能，因此它也适用于嵌入式开发等场景。



在 Rust 中，`core` 模块是标准库的核心部分，包含了一些基本的数据类型、标准库中常用的功能和 trait 等。`core` 模块是所有 Rust 程序的基础，它提供了 Rust 语言的核心功能，并且在编写 Rust 代码时自动引入，不需要额外的导入语句。

下面是 `core` 模块中的一些重要部分和功能：

1. 基本数据类型：`core` 模块定义了 Rust 的基本数据类型，包括整数类型（`i8`、`i16`、`i32`、`i64` 等）、浮点数类型（`f32`、`f64`）、布尔类型（`bool`）、字符类型（`char`）等。

2. 标准库功能：`core` 模块包含了 Rust 标准库中的许多常用功能，例如：错误处理（`Result`、`Option`）、迭代器（`Iterator`、`IntoIterator`、`FromIterator` 等）、切片（`Slice`、`SliceMut`）、字符串处理（`String`、`&str`）、文件操作（`File`、`Read`、`Write`）、线程和同步（`Thread`、`Mutex`、`Arc` 等）、时间和日期（`Duration`、`Instant`、`SystemTime` 等）等。

3. Trait：`core` 模块定义了许多 Rust 中常用的 trait，例如：`Clone`、`Copy`、`Debug`、`PartialEq`、`Iterator` 等。这些 trait 提供了一种通用的接口，使得不同类型的对象可以共享相同的行为。

4. 标准库宏：`core` 模块包含了一些常用的标准库宏，例如：`println!`、`format!`、`assert!` 等。这些宏提供了一种方便的方式来进行打印、格式化、断言等操作。

总的来说，`core` 模块是 Rust 语言的核心部分，提供了许多基本的数据类型、常用的功能和通用的 trait，为 Rust 程序的编写提供了基础设施。它与标准库中的其他模块（例如 `std`）一起构成了 Rust 强大而丰富的标准库，为 Rust 开发者提供了丰富的功能和便利的工具。



核心库是最小的：它甚至不知道堆分配，也不提供并发或 I/O。这些东西需要平台集成，而这个库与平台无关。



https://doc.rust-lang.org/core/index.html

# 参考

这篇文章是对这个教程的学习总结。

https://xxchang.github.io/book/intro/tooling.html