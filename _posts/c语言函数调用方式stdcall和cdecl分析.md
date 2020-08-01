---
title: c语言函数调用方式stdcall和cdecl分析
date: 2017-02-18 13:07:42
tags:
	- 调用
---
1

`__stdcall`和`__cdecl`都是函数调用的约定关键字。

都是从右向左把参数压入到堆栈，区别在于：

stdcall方式由实现函数来清理堆栈，而cdecl由调用者来负责清理堆栈。



**默认都是cdecl的方式的。**

**参数的传递和函数返回值**这个课题在C和汇编混合编程的时候非常关键。

在bootloader编程及内核移植等工作需要这个知识。

arm属于risc指令集，x86属于cisc指令集，都是各自架构的典型代表。

**总的来说，risc倾向于通过寄存器来传递参数，而cisc倾向于通过堆栈传递参数。**

**返回值都是通过效率最高的寄存器来完成，arm里用R0，x86里用EAX。**

下面重点看arm的。

arm在参数个数4个寄存器放不下的时候，也只能选择通过堆栈来传递。



stdcall是Pascal方式方式压栈。

函数采用从右到左的方式压栈。

自己在退出的时候清空堆栈。

这个需要是windows在用。



cdecl

这个词是：C DEfault Calling convention。C语言默认调用约定。

也是把参数从右往左入栈。

跟stdcall的不同在于，它是要调用者来负责清理堆栈。

这样汇编代码就多了不少。所以编译出来的体积比stdcall方式的要大。



还有一种fastcall方式。

从名字上看就知道，它的特点是fast。

因为它是优先通过寄存器来传递参数。

这个是uboot这些对性能要求较高的场合使用。



参考资料

1、

https://blog.csdn.net/sunriver2000/article/details/84913380