---
title: meson用法
date: 2019-08-03 16:32:19
tags:
	- 编译

---

--

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

这只是一些使用 Meson 的开源项目的例子，还有许多其他项目也在逐渐采用 Meson 构建系统。你可以在 Meson 的官方网站（https://

mesonbuild.com/users.html）上找到更多使用 Meson 的项目列表。

# 参考资料

1、使用 meson 编译代码

https://blog.csdn.net/CaspianSea/article/details/78848021

