---
title: meson用法
date: 2019-08-03 16:32:19
tags:
	- 编译

---

--

# 简介

Meson是一个现代的、快速的构建系统，用于管理软件项目的构建过程。

以下是一些关于Meson构建系统的基本信息：

1. **简介：** Meson是由Jussi Pakkanen创建的构建系统，旨在提供简单、快速、高效的构建解决方案。它使用Ninja构建系统来实现高性能的并行构建。

2. **特点：** Meson的一些主要特点包括易于学习的DSL（领域特定语言）、跨平台支持、自动检测依赖关系、并行构建、可扩展性和灵活性。

3. **安装：** 要开始使用Meson，您首先需要安装它。您可以通过以下命令在Linux系统上使用pip安装：

   ```
   pip install meson
   ```

   对于其他平台，请查阅Meson官方文档以获取详细的安装说明。

4. **项目配置：** Meson使用`meson.build`文件作为项目的配置文件。在这个文件中，您可以定义项目的结构、源文件、编译选项和其他构建相关的设置。

5. **构建项目：** 一旦配置文件准备好，您可以使用以下命令来构建项目：

   ```
   meson build
   ninja -C build
   ```

   这将生成构建文件并使用Ninja进行并行构建。

6. **依赖管理：** Meson支持自动检测和管理项目依赖关系。您可以使用`dependency()`函数来指定依赖项，并让Meson负责检查和配置它们。

7. **示例：** 以下是一个简单的`meson.build`文件的示例，用于构建一个C语言项目：

   ```meson
   project('my_project', 'c')

   executable('my_app', 'main.c', dependencies: ['my_dependency'])
   ```

   这定义了一个名为`my_app`的可执行文件，它依赖于名为`my_dependency`的外部依赖项。

以上只是Meson的一些基本概念和命令。如果您有特定的问题或需要更详细的信息，请随时提问。

# meson是用Python写的吗？

是的，Meson构建系统是使用Python编写的。 

Meson的主要开发者Jussi Pakkanen选择了Python作为构建系统的编写语言，

因为Python具有清晰的语法、强大的标准库和跨平台的能力，

使得Meson能够在各种操作系统上运行，并且易于理解和扩展。

Meson构建系统的核心代码以及项目配置文件（`meson.build`）都是用Python编写的。

此外，Meson提供了一个用于配置和运行构建的命令行工具，

这个工具也是用Python编写的。

这种设计选择使得Meson具有灵活性、易用性，并且能够与Python生态系统良好地集成。

# meson为什么没有流行开来？

Meson构建系统实际上在一些项目和社区中相当流行，但流行程度可能受到多种因素的影响。以下是一些可能解释为什么Meson没有在某些情况下变得更为流行的原因：

1. **历史原因：** 在构建系统领域，一些早期的构建工具如Make和CMake已经存在并得到广泛使用。对于许多项目来说，更换构建系统可能需要投入大量的时间和资源，因此人们可能更愿意继续使用他们熟悉的工具。

2. **社区认知度：** Meson相对较新，可能还没有在某些开发者社区中得到足够的认知度。在开发者选择构建系统时，社区支持和文档的丰富性通常是一个考虑因素。

3. **项目需求：** 不同的项目有不同的需求和偏好。某些项目可能对Meson提供的功能和性能优势感兴趣，而其他项目可能更愿意继续使用他们当前的构建系统。

4. **生态系统集成：** 一些构建系统的成功也与它们能够轻松集成其他工具和库有关。如果Meson在某些生态系统中的集成性不足，开发者可能会更倾向于选择其他构建系统。

5. **学习曲线：** Meson的学习曲线相对较低，但对于已经熟悉其他构建系统的开发者来说，可能需要一些时间来适应新的DSL和工作流。

尽管Meson可能没有像其他一些构建系统那样广泛流行，但它在一些项目中仍然得到了积极的评价，并且其简洁性和性能优势使其在一些场景下成为首选。随着时间的推移，Meson的流行度可能会增加，特别是如果它持续改进并吸引更多的社区支持。

# HelloWorld

现在看到不少的工程是用meson.build来做编译脚本的。

了解一下。

安装meson和ninja。

依赖python3.5版本以上和ninja 1.5版本以上。

```
git clone https://github.com/mesonbuild/meson.git
然后把目录加入到PATH环境变量里。
```

```
sudo apt install ninja-build
```



ninja是谷歌为了开发chrome而做的工具。

进行编译：

```
在有meson.build的目录下，执行meson.py build。
然后会在当前目录生成一个build目录。
进入到build目录。
ninja 
然后就会进行编译。
```

meson.build文件。

```
project('tutorial', 'c')
executable('demo', 'test.c')
```

test.c文件：

```
#include<stdio.h>

int main(int argc, char **argv) {
  printf("Hello there.\n");
  return 0;
}
```

# ninja和meson是什么关系

Ninja和Meson是两个不同的工具，分别用于构建系统和构建系统的配置。它们通常一起使用，但执行不同的任务。

1. **Ninja：** Ninja是一个用于构建软件项目的构建系统，专注于提供快速和高效的构建。它是一个轻量级的构建系统，旨在执行构建任务并生成目标文件，使得构建过程更加并行和高效。Ninja的配置文件通常是由其他构建系统生成的，Meson是其中一个例子。

2. **Meson：** Meson是一个构建系统的配置工具，它使用自己的领域特定语言（DSL）来定义项目的结构、依赖关系和构建选项。Meson生成Ninja构建系统的配置文件，然后您可以使用Ninja来实际执行构建。Meson的目标是提供一个现代、易用、高性能的构建系统，它与Ninja的结合使得构建过程更加简化和高效。

因此，Meson和Ninja通常一起使用，

==Meson负责项目的配置，生成Ninja构建文件，而Ninja执行实际的构建。==

这种组合使得开发者能够轻松地配置和管理复杂的项目，并在构建时获得高性能的优势。 

==Meson还支持其他构建系统的生成，而不仅仅是Ninja，但Ninja是其默认的后端。==



# meson.build文件分析

`meson.build` 文件是 Meson 构建系统使用的配置文件，用于描述项目的结构、依赖关系和构建规则。该文件通常位于项目的根目录下，并且是一个或多个子目录的入口点。

`meson.build` 文件使用了 Python-like 的语法，可以定义变量、函数、条件语句和循环等。它的主要目的是描述项目的构建过程，并生成相应的构建脚本。

下面是一个典型的 `meson.build` 文件的结构和内容：

1. 项目信息：`project` 函数用于定义项目的名称、版本号和许可证等信息。例如：

```python
project('myproject', 'c', version: '1.0', license: 'GPLv3')
```

2. 构建选项：`option` 函数用于定义构建选项，允许用户在构建过程中选择不同的配置。例如：

```python
option('debug', type: 'boolean', description: 'Enable debug mode', default_value: false)
```

3. 导入模块和库：`include_directories` 和 `link_directories` 函数用于指定项目中包含的头文件和库文件的路径。例如：

```python
include_directories('src/include')
link_directories('libs')
```

4. 定义目标：使用 `executable`、`library` 或 `shared_library` 函数定义项目的可执行文件、静态库或共享库。例如：

```python
executable('myapp', 'src/main.c', dependencies: ['mylib'])
library('mylib', 'src/lib.c')
```

5. 设置编译选项：使用 `add_project_arguments` 函数设置编译选项，如编译标志、宏定义等。例如：

```python
add_project_arguments('-Wall', '-DDEBUG', language: 'c')
```

6. 依赖管理：使用 `dependency` 函数指定项目所依赖的外部库或模块。例如：

```python
glib_dep = dependency('glib-2.0')
```

7. 构建配置：使用 `configure_file` 函数生成配置文件，根据模板文件和变量值生成最终的配置文件。例如：

```python
configure_file(input: 'config.h.in', output: 'config.h')
```

8. 构建脚本生成：`meson.build` 文件最后会生成一个 `build.ninja` 文件，这是实际的构建脚本，用于执行编译和链接操作。

请注意，`meson.build` 文件的具体内容和结构会根据项目的需求和复杂度而有所不同。以上只是一个简单的示例，实际项目中可能包含更多的模块、函数和条件语句。

要深入了解 `meson.build` 文件的语法和功能，你可以参考 Meson 构建系统的官方文档和示例代码。

# Meson 构建系统有什么优缺点？哪些开源项目使用了这个构建系统？

Meson 构建系统是一个快速、简洁和易于使用的构建系统，具有以下优点：

1. 简洁易用：Meson 使用简洁的语法和直观的设计理念，使得构建脚本易于编写和维护。它采用了类似 Python 的语法，使得构建逻辑更加清晰和易读。

2. 高效快速：Meson 的设计目标是提供快速的构建过程。它利用多线程和并行构建技术，以及优化的依赖管理，可以快速地进行增量构建，减少了构建时间。

3. 跨平台支持：Meson 可以在多个操作系统上运行，包括 Linux、Windows、macOS 等。它提供了对不同编译器和构建工具链的良好支持，使得跨平台构建变得更加简单和可靠。

4. 强大的功能：Meson 提供了丰富的功能和选项，如条件编译、模板生成、测试框架集成等。它还支持多种语言的构建，包括 C、C++、Rust、Python 等。

然而，Meson 也有一些缺点：

1. 学习曲线：对于初次接触 Meson 的开发者来说，学习其语法和概念可能需要一些时间和努力。相比于其他构建系统，Meson 的文档相对较少，可能对于某些高级用法的支持不够完善。

2. 生态系统和社区：相比于一些成熟的构建系统（如 CMake 和 Autotools），Meson 的生态系统和社区规模相对较小。这意味着在某些特定需求或平台的支持上可能不如其他构建系统。

一些知名的开源项目使用了 Meson 构建系统，包括但不限于：

- GNOME 桌面环境：GNOME 项目采用 Meson 作为其主要的构建系统，用于构建各个模块和组件。

- GStreamer 多媒体框架：GStreamer 使用 Meson 作为其构建系统，用于构建音视频处理和流媒体应用。

- FFmpeg 多媒体框架：FFmpeg 项目在其最新的版本中采用了 Meson 作为其构建系统，以替代传统的 Autotools。

- Kodi 媒体中心：Kodi 使用 Meson 作为其主要的构建系统，用于构建跨平台的媒体中心应用。

这只是一些使用 Meson 的开源项目的例子，还有许多其他项目也在逐渐采用 Meson 构建系统。你可以在 Meson 的官方网站（https://mesonbuild.com/users.html）上找到更多使用 Meson 的项目列表。

# 参考资料

1、使用 meson 编译代码

https://blog.csdn.net/CaspianSea/article/details/78848021

