---
title: pragma once作用
date: 2019-01-15 10:18:59
tags:
	- 编译
---



我写代码从来没有用过#pragma once这个。具体代表了什么呢？

作用跟#ifndef其实是一样的，就是用来避免同一个头文件被包含多次。

pragma是后面才出现的，老的编译器不支持。所以也推广不太好。

其格式一般为:

\#pragma Para。其中Para 为参数，下面来看一些常用的参数

# message

Message 参数能够在编译信息输出窗口中输出相应的信息，这对于源代码信息的控制是非常重要的。

```
#pragma message("hello")
```

当编译器遇到这条指令时就在编译输出窗口中将消息文本打印出来。

当我们在程序中定义了许多宏来控制源代码版本的时候，

我们自己有可能都会忘记有没有正确的设置这些宏，

此时我们可以用这条指令在编译的时候就进行检查。

假设我们希望判断自己有没有在源代码的什么地方定义了_X86这个宏可以用下面的方法

```
#ifdef _X86
#pragma message("_X86 macro activated!")
#endif
```

# code_seg

另一个使用得比较多的pragma参数是code_seg。格式如：

它能够设置程序中函数代码存放的代码段，

当我们开发驱动程序的时候就会使用到它。

```
#pragma code_seg(["section-name"[,"section-class"]])
```

# once

# hdrstop

#pragma hdrstop表示预编译头文件到此为止，

后面的头文件不进行预编译。

BCB可以预编译头文件以加快链接的速度，

但如果所有头文件都进行预编译又可能占太多磁盘空间，

所以使用这个选项排除一些头文件。

有时单元之间有依赖关系，

比如单元A依赖单元B，所以单元B要先于单元A编译。

你可以用#pragma startup指定编译优先级，

如果使用了#pragma package(smart_init) ，BCB就会根据优先级的大小先后编译。

# warning

```
#pragma warning(disable:450734;once:4385;error:164)
```

等价于

```
#pragma warning(disable:450734)//不显示4507和34号警告信息
#pragma warning(once:4385)//4385号警告信息仅报告一次
#pragma warning(error:164)//把164号警告信息作为一个错误。
```

同时这个pragma warning 也支持如下格式：

```cpp
#pragma warning(push[,n])
#pragma warning(pop)
```

# comment

\#pragma comment(…)
该指令将一个注释记录放入一个对象文件或可执行文件中。

常用的lib关键字，可以帮我们连入一个库文件。

每个编译程序可以用#pragma指令激活或终止该编译程序支持的一些编译功能。

例如，对循环优化功能：

# pack

# data_seg



# 参考资料

1、

https://blog.csdn.net/qq_38145502/article/details/107688889