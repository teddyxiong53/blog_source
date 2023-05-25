---
title: c和Python混合编程
date: 2017-04-16 19:49:39
tags:
	- python

---

--

使用ctypes库或者python的C API来实现混合编程。

来自chatgpt。



# 方法1: 使用ctypes库

```python
import ctypes

# 加载动态链接库
mylib = ctypes.CDLL('mylib.dll')

# 定义函数原型
myfunc = mylib.my_function
myfunc.argtypes = [ctypes.c_int, ctypes.c_int]
myfunc.restype = ctypes.c_int

# 调用函数
result = myfunc(2, 3)
print(result)  # 输出: 5
```

优点：
- 使用方便：ctypes是Python的标准库，无需安装额外的工具或扩展模块。
- 简单快速：通过加载动态链接库，即可直接在Python中调用C函数，无需编译过程。
- 跨平台支持：ctypes适用于多个操作系统，可以在不同平台上运行。

缺点：
- 类型处理相对麻烦：需要手动设置C函数的参数类型和返回值类型。
- 性能有限：由于Python和C语言之间存在数据类型转换和函数调用的开销，性能相对较低。

# 方法2: 使用C API

```c
// sample.c
#include <Python.h>

// 定义C函数
static PyObject* my_function(PyObject* self, PyObject* args)
{
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;

    int result = a + b;
    return PyLong_FromLong(result);
}

// 模块方法列表
static PyMethodDef SampleMethods[] = {
    {"my_function", my_function, METH_VARARGS, "Add two integers."},
    {NULL, NULL, 0, NULL} // 结束标志
};

// 模块定义结构体
static struct PyModuleDef samplemodule = {
    PyModuleDef_HEAD_INIT,
    "sample",   // 模块名称
    NULL,       // 模块文档
    -1,         // 模块状态
    SampleMethods // 模块方法列表
};

// 模块初始化函数
PyMODINIT_FUNC PyInit_sample(void)
{
    return PyModule_Create(&samplemodule);
}
```

```python
# sample.py
import sample

# 调用C函数
result = sample.my_function(2, 3)
print(result)  # 输出: 5
```

优点：
- 直接集成C代码：使用C API，可以直接编写C代码，并在Python中调用，提供了更高的性能。
- 充分利用C语言特性：可以利用C语言的底层系统访问能力和性能优势。
- 灵活性和扩展性：可以编写复杂的C扩展模块，与Python代码进行深度交互。

缺点：
- 编写和调试复杂：需要熟悉C语言和Python C API的使用，编写和调试过程相对复杂。
- 平台相关性：C扩展模块需要在每个平台上编译和安装，可能存在兼容性和部署问题。

综合比较：

- 使用ctypes更简单

# 方法3：使用swig

下面是一个简单的SWIG接口定义文件（example.i）的示例：

```c
/* example.i */

%module example

%{
#include "example.h"
%}

/* 将需要包装的C函数声明在接口文件中 */
int add(int a, int b);
double multiply(double a, double b);
void print_hello();

/* 将需要包装的C结构体声明在接口文件中 */
struct Point {
    double x;
    double y;
};

/* 告诉SWIG如何处理C结构体 */
%include "example.h"
```

上述示例中，`example.i` 文件定义了一个名为 `example` 的模块，其中包含三个函数和一个结构体。`add()` 函数接受两个整数参数并返回它们的和，`multiply()` 函数接受两个双精度浮点数参数并返回它们的乘积，`print_hello()` 函数用于打印 "Hello"。

`example.i` 文件还声明了一个名为 `Point` 的结构体，该结构体具有两个双精度浮点数字段 `x` 和 `y`。

`%include "example.h"` 指令告诉SWIG将与结构体相关的代码从 `example.h` 文件中包含到接口文件中。

接口定义文件中的其他部分可以包含更多的函数、结构体和其他类型的声明。

要生成与Python的接口代码，可以使用以下命令：

```
swig -python example.i
```

这将生成一个名为 `example_wrap.c` 的包装代码文件，其中包含Python与C语言之间的接口代码。

之后，可以将 `example.c` 和 `example_wrap.c` 编译为共享库，并在Python中导入和使用生成的模块。

请注意，上述示例仅为演示SWIG接口定义文件的基本结构和用法，实际的接口文件内容根据需要进行调整和扩展。

# 参考资料

1、

https://python3-cookbook.readthedocs.io/zh_CN/latest/c15/p01_access_ccode_using_ctypes.html