---
title: js运行时之duktape
date: 2024-03-12 19:09:17
tags:
	- js

---

--

# 资源收集

代码

https://github.com/svaarala/duktape

wiki

https://wiki.duktape.org/



# 简介

Duktape 是一个嵌入式 Javascript 引擎，注重可移植性和紧凑的占用空间。

Duktape 很容易集成到 C/C++ 项目中：将 duktape.c、duktape.h 和 duk_config.h 添加到您的构建中，并使用 Duktape API 从 C 代码调用 ECMAScript 函数，反之亦然。

主要特点：

- 嵌入式、便携式、紧凑
- 符合 ECMAScript E5/E5.1 标准，部分语义从 ES2015+ 更新
- 部分支持 ECMAScript 2015 (E6) 和 ECMAScript 2016 (E7)、Post-ES5 功能状态、
- ES2015 TypedArray 和 Node.js Buffer 绑定
- WHATWG 编码 API 生活标准
- 内置调试器
- 内置正则表达式引擎
- 内置 Unicode 支持
- 最小的平台依赖性
- 将引用计数和标记清除垃圾收集与终结相结合
- 自定义功能，例如协程
- 使用 ECMAScript ES2015 代理对象的子集进行属性虚拟化
- 用于缓存编译函数的字节码转储/加载
- Distributable 包括可选的日志框架、基于 CommonJS 的模块加载实现、CBOR 绑定等
- 自由 MIT 许可证（参见 LICENSE.txt）



# duktape发展历史

Duktape 的发展历史可以追溯到 2010 年左右。以下是关于 Duktape 发展历史的一些关键里程碑：

1. **起源**: Duktape 最初由 Finnish Institute of Occupational Health（芬兰职业健康研究所）的 Lars T. Kyllingstad 开发。他的目标是创建一个小型、高效的 JavaScript 引擎，可以嵌入到他们的设备中。

2. **首次发布**: Duktape 在 2011 年首次发布，并在开源社区中引起了一定的关注。这个版本提供了基本的 JavaScript 功能，包括解析和执行 JavaScript 代码的能力。

3. **持续改进**: 随着时间的推移，Duktape 继续得到改进和扩展，添加了许多新的特性和功能。这些改进包括对 ECMAScript 5.1 标准的更好支持，更好的性能优化，以及更多的扩展模块和功能。

4. **社区贡献**: 随着开源社区的参与和贡献，Duktape 的功能和生态系统得到了扩展。社区为项目添加了许多新的功能和改进，并提供了大量的文档和示例代码，使得开发人员更容易使用和集成 Duktape。

5. **广泛应用**: Duktape 在嵌入式系统、物联网设备、游戏开发等领域得到了广泛应用。它被用于各种产品和项目中，包括智能家居设备、工业控制系统、嵌入式传感器等。

尽管 Duktape 并没有像一些其他 JavaScript 引擎那样广为人知，但它在嵌入式系统和低资源环境中的应用场景中发挥着重要作用，并且持续受到开发者和组织的关注和使用。

# 使用duktape的项目

https://wiki.duktape.org/projectsusingduktape

## AllJoyn.js

AllJoyn，由高通公司主导的高通创新中心（Qualcomm Innovation Center）所开发的开放源代码专案，主要用于近距离无线传输，透过Wifi或蓝牙技术，进行定位与点对点档案传输。这个专案在2012年对外公开。

## AtomicGameEngine

https://github.com/AtomicGameEngine/AtomicGameEngine

Atomic 游戏引擎是强大的原生技术，具有一致的 API 和 C++、C#、Typescript 和 JavaScript 中可用的工具。 Atomic Editor 已在超过 75 个国家/地区安装，并已在多个行业的生产中达到“临界质量”。

Atomic 还可以在现有项目中用作库，并在开发中使用 C++ SDK、C# NuGet 和 JavaScript npm 包。

# helloworld

从这里下载代码：

https://duktape.org/download

解压后，编译：

```
make -f Makefile.cmdline
```

这个命令执行展开是：

```
cc    -o duk  -Os -pedantic -std=c99 -Wall -fstrict-aliasing -fomit-frame-pointer -I./examples/cmdline -I./src    -DDUK_CMDLINE_PRINTALERT_SUPPORT -I./extras/print-alert -DDUK_CMDLINE_CONSOLE_SUPPORT -I./extras/console -DDUK_CMDLINE_LOGGING_SUPPORT -I./extras/logging -DDUK_CMDLINE_MODULE_SUPPORT -I./extras/module-duktape src/duktape.c examples/cmdline/duk_cmdline.c extras/print-alert/duk_print_alert.c extras/console/duk_console.c extras/logging/duk_logging.c extras/module-duktape/duk_module_duktape.c -lm
```

Duktape 不提供文件或控制台 I/O 的内置绑定，以避免可移植性问题（例如，某些平台根本没有 I/O API）。

命令行实用程序使用 extras/print-alert 提供 print() 和alert() 绑定，以使其更易于使用。

可分发中有一些有用的“额外内容”，提供有用的（可选）绑定，例如：

print() and alert()
console object, e.g. console.log()



```
gcc -std=c99 -o hello -Isrc src/duktape.c examples/hello/hello.c -lm
```

由于 Duktape 是一个嵌入式引擎，因此您无需更改程序的基本控制流程。

基本方法是：

创建 Duktape 上下文，例如在程序初始化中（或者甚至在需要脚本时按需）。通常，您还会在初始化期间加载脚本，尽管这也可以按需完成。

确定代码中您想要使用脚本的点，并在其中插入对脚本函数的调用。

要进行脚本函数调用，首先使用 Duktape API 将调用参数推送到 Duktape 上下文的值堆栈。

然后，使用另一个 Duktape API 调用来启动实际调用。

脚本执行完成后，控制权将返回到您的程序（API 调用返回），并且返回值将保留在 Duktape 上下文的值堆栈中。

然后，C 代码可以使用 Duktape API 访问返回值。



更广泛地说，有多种方法可以将 Duktape 与本机代码结合使用；

例如：

- 在 C/C++ 代码中运行主应用程序，但调用 Duktape 来扩展基本功能（例如插件或配置）。

- 在 ECMAScript 代码中运行主应用程序，并调用 I/O、性能密集型操作等的简单 C/C++ 本机绑定。本机绑定通常保持无状态，以便状态逻辑保留在脚本代码的视图中。

- 在 ECMAScript 代码中运行主应用程序，但使用更复杂、有状态的 C/C++ 本机绑定来执行性能密集型操作。例如，图形引擎可以被实现为本机对象。

# 代码分析

duktape.c行数达到10万行。

它也是把一堆C文件合并得到的。

总的来说，这种量级的js运行时复杂度都差不多。

