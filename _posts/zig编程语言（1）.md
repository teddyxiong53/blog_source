---
title: zig编程语言（1）
date: 2023-05-25 11:27:11
tags:
	- zig
---

--

# 资源收集

https://lupyuen.github.io/articles/zig

microzig

https://github.com/ZigEmbeddedGroup/microzig

https://github.com/ZigEmbeddedGroup/raspberrypi-rp2040

avr模拟器，zig写的

https://github.com/ZigEmbeddedGroup/aviron

# 简介

Zig 是一门现代的系统编程语言，旨在提供可靠性、性能和可读性的平衡。它的设计目标包括以下几点：

1. **可靠性：** Zig 强调代码的可靠性，尽可能避免未定义行为和隐患。它具有内存安全性、线程安全性和类型安全性的特性。

2. **性能：** Zig 旨在提供与 C 语言相媲美的性能。它具有直接的内存控制和低级别的编程能力，使程序员能够精细地控制代码的性能。

3. **可读性：** Zig 的语法和设计力求简洁和清晰，以减少代码的复杂性。这有助于编写易于维护的代码。

4. **交互性：** Zig 支持编译时和运行时的代码生成，使开发者能够更灵活地构建应用程序。

以下是一些关键特性和概念，有助于快速理解 Zig：

- **零开销抽象：** Zig 允许你在不引入运行时开销的情况下抽象控制流、数据结构和内存管理。这使得你可以编写高性能的代码，同时保持代码的可读性。

- **内存安全性：** Zig 强调内存安全性，使用严格的借用规则来防止常见的内存错误，如空指针引用和数据竞争。

- **编译时计算：** Zig 支持在编译时执行一些计算，这使得你可以将一些运行时工作转移到编译时，提高了性能和安全性。

- **自动化测试：** Zig 内置了测试框架，可以方便地编写和运行单元测试和集成测试。

- **模块化：** Zig 支持模块化编程，你可以将代码组织成模块以便重用，并且没有复杂的头文件或外部依赖。

- **跨平台支持：** Zig 被设计为跨平台语言，可以轻松地编写可在多种操作系统上运行的代码。

- **嵌入式编程：** Zig 也可以用于嵌入式系统编程，具有对硬件的低级别访问能力。

如果你想深入了解 Zig，我建议你访问 Zig 的官方网站（https://ziglang.org/），那里有详细的文档、教程和示例代码，可以帮助你更系统地学习这门语言。如果你有特定的问题或需要进一步的帮助，也请随时提问。

# 官网

https://ziglang.org/



# Zig有什么与众不同的

Zig 允许在编译期执行代码，这有什么意义？  

编程语言专家曾对 Zig 编程语言的创造者 Andrew Kelley 说，在编译时运行代码是个蠢主意。

尽管如此，Kelley 还是去实现了这个想法，

而多年以后，这个蠢主意已经成为了 Zig 的招牌。

这一特征在 Zig 中用关键字 comptime 标识，

代表需要在编译时运行的代码或者是需要的变量。

**Zig 可以在编译时运行代码的能力让开发者们可以在不明确任何泛型或模板支撑的情况下，**

编写通用代码或是进行元编程。

让我们来通过代码例子更直观地了解编译时运行是什么意思，以及其为什么重要。

以这段简单的函数为例，在 a 和 b 两个数之间取最大值。

不使用泛型或 comptime 代码的话，我们就需要将这个函数的具体变量类型写死，比如这里用的 Zig 中 32 位整数 i32 。

==Andrew Kelley 为避免依赖 C 的宏，专门设计了 Zig。可以说，Zig 存在的原因本质上就是 Andrew 想用 C 编程，但又不想折腾宏这类烦人的东西。comptime 的诞生的意义完全就是为了取代 C 的宏。==



虽然在编译时确定输入参数的类型不是不行，但这么一来变量和返回类型就难处理了。

anytype 不能用作是返回类型，

因为我们不能在函数调用处再确定变量的具体类型。

因此，我们需要用编译器内联函数 @TypeOf 在编译时生成返回类型，

比如用 @TypeOf(a) 在编译时确定参数 a 的类型，或者是用来指定返回变量 result 的类型：



用编译时的代码实现泛型

Zig 中 comptime 的强大可以通过对泛型的实现来证明。

在下面的例子中的 minimum 函数对习惯于泛型或基于模板编程的开发者来说很是熟悉。

其中的关键区别在于，类型参数 T 是作为一般参数输入的。

对于 C++、Java 和 C# 的开发者来说，这个函数一般会以 minimum(x, y) 的形式调用，

但对于 Zig 开发者来说，minimum(i8, x, y) 足矣。



语言特性

**Zig的语法类似于C语言，但在类型安全和错误检测方面更加强大。**

它支持静态类型检查、模块化编程、自动内存管理和编译时错误检测等特性。

**Zig鼓励显式编程，强调代码的可读性和可维护性。**

它还提供了对内存布局和控制流的细粒度控制，使开发者能够精确地管理资源和优化性能。



Zig的应用领域

Zig适用于各种系统级开发任务，

包括操作系统、驱动程序、编译器、嵌入式系统和网络协议栈等。

其高级的类型系统和错误检测功能使得开发者能够更轻松地编写安全可靠的底层软件。

此外，Zig还可用于性能优化、跨平台开发和工具开发等领域，为开发者提供了广阔的应用空间。



https://blog.51cto.com/u_15746412/7004842

连 1.0 版本都没有，Uber 为什么会采用这样一项新技术？

https://www.infoq.cn/article/q016nwr7ojhvoj3rkzc0

# zig cc  一种zig的使用方法

综观 Andrew 的文章，`zig cc`有以下优势：



- 完全封闭的 C/C++编译器，压缩包只有大约 40MB。这比 Clang 的标准发行版要小一个数量级。
- 可以链接到通过命令行参数提供的 glibc 版本（例如，`-target x86_64-linux-gnu.2.28`将以 x86_64 Linux 为编译目标并链接到 glibc 2.28）。
- 主机和目标平台是解耦的。不管是什么主机，针对目标平台`linux-aarch64`和`darwin-x86_64`的设置都是一样的。
- 与 musl 链接“只是一个不同的 libc 版本”：`-target x86_64-linux-musl`。我开始摆弄`zig cc`。我随便编译了一些程序，报告了一些问题。我想过把它做成一个[bazel工具链](https://bazel.build/docs/toolchains?accessToken=eyJhbGciOiJIUzI1NiIsImtpZCI6ImRlZmF1bHQiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiJhY2Nlc3NfcmVzb3VyY2UiLCJleHAiOjE2NTQ0ODM1MjcsImZpbGVHVUlEIjoiTXYxVVJmSFh5czBxWWdYeCIsImlhdCI6MTY1NDQ4MzIyNywidXNlcklkIjoyNzc5OTMxNX0.MqLRGB9Grs957ke2oHCqY9yw4AHgzhEanjZuK53mzzQ)，但有很多拦路的 bug 或缺失的功能。其中之一就是缺少 Bazel 所依赖的`zig ar`。



## Andrew Kelley 介绍

截止到我知识截止日期（2021年9月），Andrew Kelley 是 Zig 编程语言的创始人和主要开发者之一。他是该项目的核心推动力，负责领导 Zig 的开发和推广。以下是一些关于 Andrew Kelley 的基本信息：

- **Zig 创始人：** Andrew Kelley 是 Zig 编程语言的创建者，他于2016年启动了这个项目，并在其早期阶段开始了语言的设计和开发工作。

- **开发者和社区推动者：** 除了是 Zig 的创始人之外，Andrew Kelley 也是该项目的主要开发者之一。他积极参与了 Zig 的代码编写和维护工作，同时也是社区的推动者，鼓励其他开发者参与该项目。

- **Zig 的愿景：** 在创建 Zig 时，Andrew Kelley 的愿景之一是提供一门现代、可靠且高性能的系统编程语言。他关注的重点包括语言的可读性、内存安全性和性能。

- **开源贡献：** 除了 Zig 之外，Andrew Kelley 也积极参与其他开源项目，为开源社区做出了贡献。

请注意，自2021年9月以来，Andrew Kelley 和 Zig 项目的发展可能已经有了新的进展。如果你对他或 Zig 项目的最新信息感兴趣，建议查看 Zig 的官方网站以及与 Zig 相关的社交媒体渠道。

他的个人网站：

https://andrewkelley.me/

https://github.com/andrewrk

# linux下搭建环境

到这里下载安装包：

https://ziglang.org/download/

解压后就可以用：

```
./zig version
0.12.0-dev.374+742030a8f
```

把解压后的目录加入到PATH里。

解压后的目录有很多的文件。

```
const std = @import("std");

pub fn main() void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, Zig!\n");
}
```

上面这个HelloWorld已经不能正常运行了。

下面这样才行。

```
const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s}!\n", .{"world"});
}
```

编译：

```
zig build-exe hello.zig
```



所以还是要按照官网的教程来。

# zig标准库

https://ziglang.org/documentation/master/std/

std这个名字是顶层的namespace。

下面有io、os等包。

# zig的命名规律

Zig 编程语言遵循一种一致的命名规范，这有助于提高代码的可读性和可维护性。以下是 Zig 命名规范的一些关键点：

1. **驼峰命名法：** Zig 喜欢使用驼峰命名法（CamelCase）来命名标识符。这意味着变量名、函数名、类型名等使用驼峰命名，单词之间没有下划线或其他分隔符，每个单词的首字母大写，如 `myVariableName`。

2. **模块和命名空间：** Zig 支持模块化编程，而模块的名称也遵循驼峰命名法。例如，`std.io` 表示标准库中的 `io` 模块。

3. **常量和枚举：** 常量和枚举的名称通常使用大写字母和下划线来分隔单词，如 `const MY_CONSTANT = 42` 或 `const LogLevel = enum { Debug, Info, Warning, Error }`。

4. **函数和方法：** 函数和方法的名称也使用驼峰命名法。函数名通常描述其功能，如 `fn calculateSum(a: i32, b: i32) i32`。方法名与函数名相似，但在方法调用时需要指定接收者对象，如 `myObject.calculateSum(a, b)`。

5. **结构体和类型：** 类型和结构体的名称通常使用驼峰命名法，首字母大写。例如，`struct Person` 或 `pub const MyEnum`。

6. **变量和参数：** 变量和参数的名称同样使用驼峰命名法，描述其用途或数据类型。例如，`let firstName: string` 或 `fn printMessage(message: string)`。

7. **属性和字段：** 结构体和对象的属性或字段名称也使用驼峰命名法，以表示它们的用途或数据类型。例如，`pub var name: string`。

8. **模块级别：** 在 Zig 中，有一些特殊的模块级别标识符，如 `pub` 用于公开模块的内容，以及 `const`、`var`、`fn` 用于定义常量、变量和函数。

9. **函数命名约定：** Zig 通常使用 `snake_case` 命名约定来命名标准库中的函数，但在用户自定义代码中使用驼峰命名法更为常见。

请注意，虽然 Zig 有一套通用的命名规范，但编程社区中可能存在一些团队或项目特定的命名约定。因此，在编写代码时，请始终尊重项目的约定，以确保一致性。

# 语法速通

https://ziglang.org/zh/learn/