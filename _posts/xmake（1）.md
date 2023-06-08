---
title: xmake（1）
date: 2023-06-06 10:41:11
tags:
	- 编译
---

--

# xmake发展历史

XMake 的发展历史如下：

1. 2011年：XMake 诞生。最初的 XMake 版本是由 hongliangpan 开发的一个简单的构建工具。它的设计目标是提供一种简单的构建方式，使开发者可以快速地构建 C/C++ 项目。

2. 2013年：引入 Lua 脚本支持。为了提供更灵活和可扩展的构建配置，XMake 引入了 Lua 脚本作为构建配置的脚本语言。开发者可以使用 Lua 脚本编写构建规则和自定义构建过程。

3. 2015年：全面重构。为了改进 XMake 的性能和可扩展性，XMake 在这一年进行了全面的重构。它引入了基于 Lua 的构建脚本和插件系统，使用户能够更好地定制和扩展构建过程。

4. 2016年：支持更多平台。XMake 进一步扩展了其跨平台能力，支持更多的操作系统，包括 Windows、MacOS、Linux 和 FreeBSD。

5. 2017年：增加包管理功能。为了方便项目的依赖管理，XMake 增加了包管理功能，支持下载和安装第三方库和工具。

6. 2018年：支持更多语言。除了 C/C++，XMake 还增加了对其他编程语言的支持，包括 Rust、Golang、Swift 等。

7. 2019年：持续改进和增强。XMake 团队在每个版本中持续改进和增强 XMake 的功能和性能，修复 bug，提供更好的用户体验。

8. 至今：XMake 继续发展。目前，XMake 仍在积极开发和改进中，持续推出新版本，并与社区合作，吸收用户反馈和贡献，以满足开发者在构建方面的需求。

总体而言，XMake 是一个持续发展和不断改进的跨平台构建工具，旨在提供简单、灵活和可扩展的构建解决方案，使开发者能够轻松地构建和管理 C/C++ 项目。



# 安装

这个本质上是编译安装的。

```
wget https://xmake.io/shget.text -O - | bash
```

安装后执行：

```
source ~/.xmake/profile
```

把这个加到.bash_profile里。命令基本语法：

```
xmake [task] [options] [target]
```

## 子命令

输入xmake，然后按tab补全提示的子目录有这些：

```
build
clean
create
format
install
macro
plugin
repo
run
show
update
check
config
doxygen
global
lua
package
project
require
service
uninstall
watch
```

# helloworld

创建 名为hello的控制台工程。

```
xmake create -l c -P ./hello
```

创建过程的打印：

```
create hello ...
  [+]: src/main.c
  [+]: xmake.lua
  [+]: .gitignore
create ok!
```

得到的目录结构：

```
.
└── hello
    ├── src
    │   └── main.c
    └── xmake.lua
```

然后在hello目录下执行：

```
xmake 
```

这样就执行了构建操作。

```
checking for platform ... linux
checking for architecture ... x86_64
[ 25%]: cache compiling.release src/main.c
[ 50%]: linking.release hello
[100%]: build ok, spent 1.357s
```

然后可以调试程序：

需要先调整到debug模式进行编译。

```
xmake config -m debug
xmake
```

然后执行debug：

```
xmake run -d hello 
```

# 目录有多层嵌套，头文件也分散在各处

如果您的工程目录结构是多层嵌套的，并且头文件分散在各个目录中，您可以在xmake.lua文件中使用递归添加目录的方式来处理。

以下是一个示例，假设您的工程目录结构如下：

```
project/
├─ src/
│  ├─ main.c
│  ├─ subdir1/
│  │  ├─ file1.c
│  │  └─ file1.h
│  └─ subdir2/
│     ├─ file2.c
│     └─ subdir3/
│        ├─ file3.c
│        └─ file3.h
└─ include/
   └─ common/
      └─ common.h
```

您可以按照以下方式在xmake.lua文件中配置：

```lua
-- 添加头文件搜索路径
add_includedirs("include")

-- 递归添加源文件
target("demo")
    set_kind("binary")
    add_files("src/*.c") -- 添加根目录下的.c文件

    -- 递归添加子目录下的.c文件
    add_files("src/subdir1/*.c", "src/subdir2/*.c", "src/subdir2/subdir3/*.c")

    -- 添加头文件
    add_includedirs("src/subdir1", "src/subdir2/subdir3", "include/common")

    -- 设置编译选项
    add_cflags("-Wall")
    add_cxxflags("-std=c++11")
```

在上面的示例中，通过使用通配符`*`来匹配不同层级的目录和文件，递归地添加了源文件和头文件的路径。您可以根据实际情况进行相应的调整。

请注意，如果您的工程目录结构非常复杂，可能需要更多的配置和匹配规则来确保正确地包含所有的源文件和头文件。

# xmake f == xmake config

这2个是等价的。

