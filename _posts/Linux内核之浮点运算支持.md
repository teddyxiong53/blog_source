---
title: Linux内核之浮点运算支持
date: 2023-02-07 15:47:17
tags:
	- Linux内核

---



linux kernel如何处理浮点运算，我们就分为带FPU的处理器和不带FPU的处理器来讨论。

对于linux kernel来说，kernel本身编译默认使用了-msoft-float选项，

默认编译为软浮点程序，软浮点含义是有gcc编译器模拟浮点运算（glibc库提供），

将浮点运算代码替换为定点运算。

对于带FPU的处理器，我们可以将编译选项-msoft-float去掉，一般是在arch/xxx/Makefile中。将kernel编译为硬浮点，也就是让处理器的浮点指令计算浮点，

硬浮点运算肯定要比模拟的定点运算效率高。（kernel代码中一般不会有浮点运算，所以效率影响不大）

在内核里，有这些头文件定义了很多的宏来支持浮点运算。

include\math-emu\double.h



# 参考资料

1、浅谈linux kernel对于浮点运算的支持

https://cloud.tencent.com/developer/article/1720846

