---
title: swig研究
date: 2024-06-15 08:14:51
tags:
	- 编程

---



# 简介

SWIG (Simplified Wrapper and Interface Generator) 是一个用于自动生成C/C++代码与其他编程语言（如Lua和Python）之间接口的工具。它通过读取C/C++头文件，生成相应的包装代码，使得这些语言可以调用C/C++库中的函数和使用数据类型。

以下是SWIG的基本工作流程：

1. **编写接口文件**：你需要为C/C++代码编写一个接口文件，告诉SWIG哪些函数和数据类型需要暴露给目标语言。
2. **运行SWIG**：使用SWIG工具生成包装代码。
3. **编译包装代码**：编译生成的包装代码与原始C/C++代码一起，生成共享库。
4. **使用生成的绑定**：在目标语言中导入生成的绑定并调用C/C++代码。

具体步骤如下：

| 步骤            | 详细说明                                                     |
| --------------- | ------------------------------------------------------------ |
| 1. 安装SWIG     | 可以通过包管理器（如apt、brew）安装，也可以从SWIG官网下载安装包。 |
| 2. 编写接口文件 | 接口文件以`.i`为扩展名，内容包括C/C++头文件的声明和SWIG指令。 |
| 3. 运行SWIG     | 使用`swig -language -module interface_file`命令生成包装代码。 |
| 4. 编译         | 将生成的包装代码与原始C/C++代码一起编译，生成共享库（如`.so`或`.dll`文件）。 |
| 5. 使用         | 在目标语言中导入生成的共享库并调用C/C++函数。                |

例如，假设你有一个C库，包含以下函数：

```c
// example.h
int add(int a, int b);
```

你需要创建一个SWIG接口文件：

```c
// example.i
%module example
%{
#include "example.h"
%}

extern int add(int a, int b);
```

然后，运行SWIG生成Python绑定：

```sh
swig -python example.i
```

接下来，编译生成的包装代码：

```sh
gcc -fpic -c example_wrap.c example.c -I/usr/include/python3.8
gcc -shared example_wrap.o example.o -o _example.so
```

最后，在Python中使用生成的绑定：

```python
import example
print(example.add(3, 4))
```

这样，你就可以在Python中调用C函数了。生成Lua绑定的过程类似，只需将`-python`替换为`-lua`。

# 参考资料

1、

https://www.cnblogs.com/chen-cs/articles/13343893.html
