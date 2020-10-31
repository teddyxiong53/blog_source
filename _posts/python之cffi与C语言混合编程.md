---
title: python之cffi与C语言混合编程
date: 2020-10-31 10:19:30
tags:
	- python
---

1

看easyhid里，用了cffi。是用来在python里调用C函数的。看起来比ctypes简单易用。

所以学习一下。

cffi为c语言的外部接口，在Python中使用该接口可以实现在Python中使用外部c文件的数据结构及函数。

所了解的使用方式有以下几种：

1）直接在Python文件中通过cffi调用库函数或自定义函数。

2）在一个Python文件中进行函数的定义，生成扩展模块后在其他Python中使用定义的函数。

3）使用cffi在Python中调用已定义好的函数库中的c文件。



# 直接在python里调用C函数

这种方式也叫在线API方式。

主要依赖函数verify。

```
import cffi

ffi = cffi.FFI()
ffi.cdef("""
    int printf(const char *format, ...);
""")
C = ffi.dlopen(None)
arg = ffi.new("char[]", b"world")
C.printf(b"hello %s\n", arg)
```

上面这个代码在windows上跑不起来。

```
    raise OSError("dlopen(None) cannot work on Windows for Python 3 "
OSError: dlopen(None) cannot work on Windows for Python 3 (see http://bugs.python.org/issue23606)
```

在Linux上正常运行。打印hello world。



定义结构体变量。

```
import cffi

ffi = cffi.FFI()
ffi.cdef("""
	typedef struct {
		int x;
		int y;
	} Point;
""")
# 赋值方法一
p1 = ffi.new("Point *", [1,2])
# 赋值方法二
p2 = ffi.new("Point *", {'x':1, 'y':2})
```

定义函数并调用

```
import cffi

ffi = cffi.FFI()
ffi.cdef("""
    int add(int a, int b);
    int sub(int a, int b);
""")
lib = ffi.verify("""
    int add(int a, int b)
    {
        return a+b;
    }
    int sub(int a, int b)
    {
        return a-b;
    }
""")
print(lib.add(10,2))
print(lib.sub(10,2))
```

这个在windows上运行报错。

```
LINK : fatal error LNK1158: cannot run 'rc.exe'
```

搜索rc.exe。是在C:\Program Files (x86)\Windows Kits\8.1\bin\x86\rc.exe

把路径添加到PATH。

然后windows下就可以正常运行上面的代码了。

还可以把函数定义放在单独的c文件里。

然后这样引用。

```
lib = ffi.verity(sources=['test.c'])
```

# 生成扩展模块给其他python程序调用

这种方式也叫离线API方式。

主要依赖函数compile。



参考资料

1、

https://www.cnblogs.com/ccxikka/p/9637545.html

2、

https://stackoverflow.com/questions/14372706/visual-studio-cant-build-due-to-rc-exe