---
title: js之jerryscript
date: 2018-12-27 11:52:27
tags:
	- js
---

--

# 学习方法

看api手册

https://jerryscript.net/api-reference/

# 简介

JerryScript（或称为Jerry）是一个轻量级、快速的嵌入式 JavaScript 引擎，旨在在资源受限的嵌入式设备上运行。以下是一些关于 JerryScript 的介绍：

1. **轻量级和快速**：JerryScript 被设计成非常轻量级且具有出色的性能。它的目标是在内存和处理器资源有限的嵌入式系统上运行，因此它非常紧凑，具有快速的启动时间和低内存占用。

2. **符合 ECMAScript 5.1**：JerryScript 遵循 ECMAScript 5.1 标准，这是 JavaScript 的一种版本。它支持 JavaScript 的核心特性，包括函数、对象、原型继承、闭包等。

3. **嵌入式支持**：JerryScript 可以嵌入到嵌入式应用程序中，从而可以通过 C 或 C++ 代码与应用程序的其他部分进行交互。这使得开发者可以在嵌入式系统上使用 JavaScript 来编写应用逻辑。

4. **优化器**：JerryScript 包含一个简单但有效的即时编译器（JIT），可以在运行时优化 JavaScript 代码，提高执行速度。

5. **模块系统**：JerryScript 支持模块化编程，允许将 JavaScript 代码分解为模块，并使用 `require` 和 `exports` 来实现模块之间的依赖和导出。

6. **小巧的垃圾回收器**：JerryScript 包含一个小型的垃圾回收器，用于自动管理内存，确保不会发生内存泄漏。

7. **跨平台**：JerryScript 可以在多种操作系统和硬件平台上运行，包括 Linux、嵌入式 Linux、嵌入式操作系统（如 FreeRTOS）等。

8. **开源**：JerryScript 是一个开源项目，可以在 GitHub 上找到其源代码。它采用了MIT许可证，因此可以用于商业和开源项目。

JerryScript 在嵌入式系统领域非常有用，因为它可以使开发者在资源受限的设备上轻松编写和运行 JavaScript 代码，从而加速开发周期并简化嵌入式应用程序的开发。

# jerryscript 发展历史

JerryScript 的发展历史可以追溯到 2014 年，它是由三星开发的开源嵌入式 JavaScript 引擎。以下是 JerryScript 的主要发展历史里程碑：

1. **2014 年**：
   - JerryScript 项目首次亮相，由三星电子发布在 GitHub 上，并宣布其目标是创建一个轻巧的 JavaScript 引擎，适用于嵌入式设备。

2. **2015 年**：
   - JerryScript 受到了开发者社区的欢迎，开始积极贡献和合作。在这一年内，引擎的功能和性能得到了改进。

3. **2016 年**：
   - JerryScript 的稳定性和性能继续改进，并且开始支持更多的 ECMAScript 5.1 特性。
   - 项目宣布支持 ES2015（ECMAScript 2015，也称为 ES6）的一些特性。
   - JerryScript 在 IoT（物联网）和嵌入式系统领域受到越来越多的关注。

4. **2017 年**：
   - JerryScript 的开发团队持续改进引擎的性能和稳定性，并逐渐增加了对 ES2015 标准的支持。
   - JerryScript 开始被用于一些嵌入式系统的项目中。

5. **2018 年**：
   - JerryScript 发布了 v2.0 版本，这是一个重要的版本，引入了许多新特性和改进。
   - 引擎的性能继续改进，包括更好的垃圾回收性能和支持更多的 ES2015 特性。

6. **2019 年及以后**：
   - JerryScript 持续进行改进和维护，不断适应嵌入式系统和 IoT 设备的需求。
   - 引擎的社区不断扩大，更多开发者开始参与其中，为项目做出贡献。

总的来说，JerryScript 是一个不断发展和成熟的项目，它旨在为嵌入式系统提供一种轻量级的 JavaScript 引擎，以帮助开发者在资源受限的环境中运行 JavaScript 代码。它的发展历史反映了对嵌入式 JavaScript 解决方案的不断需求，并显示了一个积极的开发社区在推动项目前进。JerryScript 在 IoT 和嵌入式领域有着广泛的应用前景。

# 代码目录作用分析

JerryScript 的代码目录结构主要是根据项目的功能和组织原则来组织的，它包含了不同用途的目录和文件，用于实现 JavaScript 引擎的各个部分。以下是 JerryScript 代码目录的一些关键部分及其作用的分析：

1. **`jerry-core` 目录**：
   - 这是 JerryScript 引擎的核心部分，包含了解释器、字节码生成器、解析器等与 JavaScript 执行相关的代码。
   - `jerry-core` 目录下的文件负责实现 JavaScript 语言的核心功能，包括变量、函数、对象等。
   - `jerry-core` 目录中的 `jerry-api.c` 文件包含了 JerryScript 对外提供的 C/C++ API 的实现。

2. **`jerry-ext` 目录**：
   - 这个目录包含一些额外的扩展，例如 JerryScript 的模块系统、错误处理等。
   - `jerry-ext` 目录中的 `jerry_module.c` 文件包含了模块系统的实现，允许 JavaScript 代码进行模块化编程。
   - `jerry-ext` 目录中的 `jerry_error.c` 文件包含了错误处理相关的代码。

3. **`targets` 目录**：
   - 这个目录包含了 JerryScript 的目标平台配置，每个子目录对应一个不同的目标平台。
   - 每个目标平台的配置文件定义了与平台相关的特定选项和功能，以适应不同的嵌入式设备和操作系统。

4. **`tools` 目录**：
   - `tools` 目录包含了一些开发和构建工具，例如字节码生成器的工具、自动化测试工具等。

5. **`tests` 目录**：
   - 这个目录包含了 JerryScript 的测试套件，用于测试引擎的功能和性能。
   - 测试包括单元测试、性能测试、基准测试等，用于验证引擎的正确性和性能。

6. **`examples` 目录**：
   - `examples` 目录包含了一些示例代码，演示如何在 JerryScript 中运行 JavaScript 代码，并如何使用 JerryScript 的 API。

7. **`deps` 目录**：
   - 这个目录包含了 JerryScript 依赖的第三方库和组件的源代码。
   - JerryScript 使用一些外部库来支持底层功能，例如内存分配、文件操作等。

8. **`docs` 目录**：
   - `docs` 目录包含 JerryScript 的文档，包括用户手册、API 文档等，以帮助开发者使用和理解 JerryScript。

9. **`build` 目录**：
   - `build` 目录用于存储构建过程中生成的临时文件和构建输出。
   

JerryScript 的代码目录结构是为了使项目的各个部分模块化和易于维护。它提供了一种组织代码和资源的方式，以便开发者可以轻松地理解和扩展 JerryScript，以满足不同嵌入式设备和应用的需求。

## jerry-core目录

### api目录

下面有5个文件，但是主要看jerry.c文件。

这个文件有5000行以上。

主要对应的头文件是：

jerry-core\include\jerryscript-core.h

```
定义了版本号：2.4.0
init flag枚举
错误码枚举
feature枚举
基本数据类型

对外的api接口
都是jerry_xx开头的。
jerry_init
jerry_cleanup
jerry_gc
jerry_run_simple
jerry_eval
jerry_return
jerry_throw
```

它的特殊性在于它的接口只有jerry_的前缀，而其他文件的都是`jerry_xx_`这样的前缀。



# 资源收集

https://wiki.tizen.org/images/d/db/01-IoTjs_and_JerryScript_Overview.pdf

http://events17.linuxfoundation.org/sites/events/files/slides/openiot-summit-2016-iotjs.pdf

https://yodaos-project.github.io/ShadowNode/devs/Writing-New-Module.html



https://www.slideshare.net/rzrfreefr/webthingiotjs20181022rzr-120959360

**ShadowNode module 源码解析及我个人对该项目粗浅的认识**

https://cnodejs.org/topic/5d005cc51fe902120f31dea0



https://ai.nationalchip.com/docs/gx8010/skylark/Skylark+Guidelines.html

# 编译

直接从这里下载。

https://github.com/jerryscript-project/jerryscript

看readme就够了。

编译：

```
python ./tools/build.py
```

编译很快。

运行：

```
./build/bin/jerryr ./test.js
```

下面的doc目录下，有markdown的文档。

tests目录下，有测试脚本。

基本的是这样的。

```
print("hello jerry");
```



这样编译，方便用gdb进行调试跟踪代码的运行。

```
python2 tools/build.py --debug  --all-in-one ON --logging ON   --line-info ON --jerry-debugger ON  --jerry-cmdline ON  --jerry-port-default ON 
```



# 在rt-thread上使用

现在在rt-thread上使用起来了。

所以仔细研究一下这个。也作为深入学习js的一个材料。

jerryscript的主要特性：

1、对ES5的完整兼容。

2、对低内存的大量优化。

3、完全用C99编写。

4、对预编译的js字节码文件的的snapshot支持。

5、有成熟的C语言API，容易嵌入到你的程序里。

采用的apache2协议进行开源的。可以商用。



jerryscript的开发环境，官网推荐Ubuntu18.04。他们就是在这个上面进行开发。



jerryscript\tests\jerry 这个目录下有一下测试例子。可以看看。



# ENABLED宏

```
./jerry-core/config.h:#define ENABLED(FEATURE) ((FEATURE) == 1)
```

# ecmascript 的附录B是什么

ECMAScript附录B是ECMAScript规范的一个附录，其中包含了一些实现建议和规范化了的行为，旨在帮助开发者避免在编写ECMAScript代码时遇到一些常见的问题。

具体来说，附录B主要包含了一些被认为是JavaScript实现必须支持的特性、方法和对象。这些特性有时候可能不会出现在ECMAScript的正文中，但它们仍然被视为标准的一部分，因此ECMAScript的实现者们需要确保它们得到支持。

一些常见的内容包括：

1. `Array.prototype.sort`方法的行为规范。
2. `Date`对象的行为，包括日期和时间的解析和格式化。
3. `RegExp`对象的行为，包括正则表达式的语法和语义。
4. `JSON`对象的行为，包括对JSON数据的解析和序列化。

附录B对于确保不同ECMAScript实现之间的一致性非常重要，因为它定义了一些必须支持的行为。这有助于确保开发者编写的代码在不同的JavaScript环境中都能够正常工作。

# Realms

Realms（领域）是指在JavaScript中的一个概念，它描述了一个独立的执行环境和其相关的对象集合。每个领域都有自己的全局对象、内置对象和执行上下文。

在传统的浏览器环境中，通常每个标签页或每个iframe都会有一个独立的领域。这意味着它们有自己的全局对象（即`window`对象）和它们自己的JavaScript代码执行环境。

Realms的概念对于理解JavaScript中的代码隔离和沙箱执行非常重要。在一个领域中，代码执行是相互独立的，因此在一个领域中运行的代码通常无法直接访问其他领域的对象或变量。这种隔离性有助于确保代码的安全性和稳定性，同时也使得一些特定的安全措施（如跨域限制）能够得以实施。

在现代的JavaScript环境中，特别是在Node.js中，Realms概念也被广泛应用。

Node.js中的每个`vm`模块实例都可以被看作一个独立的领域，

允许在不同的执行环境中运行代码，并且可以控制它们之间的交互。

这种方式使得Node.js能够实现诸如沙箱执行、代码热重载等高级特性。

# 沙箱执行

沙箱执行是指在一种受限的环境中运行代码，以限制代码对系统资源和外部环境的访问。

这种技术通常用于确保安全性，防止恶意代码对系统造成损害，或者用于创建一种隔离的环境，以防止代码之间的相互影响。

在JavaScript中，沙箱执行通常通过创建一个隔离的执行环境来实现，

这个执行环境中的代码只能访问受限制的资源和对象。

在浏览器环境中，常见的做法是使用iframe或者Web Worker来创建一个沙箱环境，

这样的话，代码将在一个独立的上下文中执行，无法直接访问主页面的DOM或者其他敏感资源。

在Node.js环境中，可以使用vm模块来实现沙箱执行。

该模块允许在一个受控制的环境中执行JavaScript代码，可以限制代码对系统资源的访问，或者通过提供一个自定义的上下文对象来限制代码的可用变量和函数。

沙箱执行对于确保代码的安全性非常重要，尤其是当执行来自不信任的源头（如用户输入、第三方插件等）的代码时。

通过限制代码的权限和访问范围，沙箱执行可以帮助防止诸如代码注入、XSS（跨站脚本攻击）和CSRF（跨站请求伪造）等安全威胁。

# 代码热重载

代码热重载是一种软件开发技术，允许在应用程序运行时动态修改代码，并在不需要重新启动应用程序的情况下立即应用这些更改。这种技术通常用于加快开发周期、提高开发效率以及实现动态调试。

在JavaScript中，特别是在Node.js环境中，可以通过一些工具和技术来实现代码热重载。其中一种常见的方法是使用模块热替换（Hot Module Replacement，HMR）技术。使用HMR，当源代码发生变化时，只会重新加载已更改的模块，而不是整个应用程序。这使得开发人员能够立即看到他们所做的更改的影响，而无需停止和重新启动应用程序。

另一个常见的方法是使用开发服务器，如Webpack Dev Server或Parcel，这些服务器能够监视源代码文件的变化，并在文件发生变化时自动重新构建应用程序，并通知浏览器刷新页面，以便开发人员可以立即查看更新后的效果。

总的来说，代码热重载是一种提高开发效率的重要工具，可以极大地加速开发过程，并使开发人员更容易地进行实验和调试。

# 官方文档阅读

## api使用

这里说明了如何编译成库，如何在外面连接使用对应的api和库。

https://github.com/jerryscript-project/jerryscript/blob/master/docs/03.API-EXAMPLE.md

## 编码规范

https://github.com/jerryscript-project/jerryscript/blob/master/docs/08.CODING-STANDARDS.md

JerryScript中的每个指针必须是以`_p`后缀结尾的字符串。

JerryScript中的每个类型都必须是以`_t`后缀结尾的字符串。

Type usage conventions 类型使用约定



- 传递函数调用的参数数量始终为`uint32_t`
- 字符串大小/长度/位置相关操作应使用`lit_utf8_size_t`
- 扩展对象内部字段必须为`uint32_t`

# 基于jerryscript的项目

这个是手表。

https://pebble.github.io/rockyjs/