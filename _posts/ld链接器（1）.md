---
title: ld链接器（1）
date: 2020-06-30 09:30:51
tags:
	- Linux

---

1

关于链接，需要进行系统的学习了解。

crt1.o, crti.o, crtbegin.o, crtend.o, crtn.o 等目标文件和daemon.o（由我们自己的C程序文件产生）链接成一个执行文件。

前面这5个目标文件的作用分别是**启动、初始化、构造、析构和结束**，它们通常会被自动链接到应用程序中。

例如，应用程序的main()函数就是通过这些文件来调用的。

**如果不进行标准的链接的话（编译选项-nostdlib）**，我们就必须指明这些必要的目标文件，如果未指定，链接器就会提示找不到_start符号，并因此导致链接失败。

且，**将目标文件提供给编译器的次序也很重要**，因为GNU链接器（编译器会自动调用该链接器进行目标文件的链接）只是个单次处理链接器。



Glibc有几个辅助程序运行的运行库 (C RunTime Library)，

分别是/usr/lib/crt1.o、/usr/lib/crti.o和/usr/lib/crtn.o，

其中crt1.o中包含程序的入口函数`_start`以及两个未定义的符号`__libc_start_main`和main，由`_start`负责调用`__libc_start_main`初始化libc，然后调用我们源代码中定义的main函数；

另外，**由于类似于全局静态对象这样的代码需要在main函数之前执行，crti.o和crtn.o负责辅助启动这些代码**。

**另外，Gcc中同样也有crtbegin.o和crtend.o两个文件，这两个目标文件用于配合glibc来实现C++的全局构造和析构。**



android bionic,这个C runtime library设计并不是功能特别强大,

并且有些gnu glic中的函数没有实现,

这是移植时会碰到的问题.

而且,这个C runtime library也并没有采用crt0.o,crt1.o,crti.o crtn.o,crtbegin.o crtend.o,

而是**采用了android自己的crtbegin_dynamic.o, crtbegin_static.o 和crtend_android.o。**



crt1.o是crt0.o的后续演进版本,

crt1.o中会非常重要的.init段和.fini段以及_start函数的入口.

.init段和.fini段实际上是靠crti.o以及crtn.o来实现的

. init段是main函数之前的初始化工作代码, 

比如全局变量的构造

. fini段则负责main函数之后的清理工作

.crti.o crtn.o是负责C的初始化,

而C++则必须依赖crtbegin.o和crtend.o来帮助实现.

​        So,在标准的linux平台下,link的顺序是:ld crt1.o crti.o [user_objects] [system_libraries] crtn.o

​        而在android下,link的顺序是:arm-eabi-g++ crtbegin_dynamic.o [user_objects] [system_libraries]crtend_android.o

​        所以这就是从另一个方面说明为什么不适合codesourcery之类编译来开发android底层东西的原因了,这里不包括BSP之类.



main()也是一个函数。

这是因为在编译连接时它将会作为crt0.s汇编程序的函数被调用。

crt0.s是一个桩（stub）程序，名称中的“crt”是“C run-time”的缩写。

该程序的目标文件将被链接在每个用户执行程序的开始部分，主要用于设置一些初始化全局变量。

通常使用gcc编译链接生成文件时，gcc会自动把该文件的代码作为第一个模块链接在可执行程序中。

**在编译时使用显示详细信息选项“-v”就可以明显地看出这个链接操作过程。**

**因此在通常的编译过程中，我们无需特别指定stub模块crt0.o。**



# .ARM.extab

.ARM.extab and .ARM.exidx are related to unwinding

You don't need them if you don't care about unwinding (unwinding is useful for C++ exception and for debugging).

参考资料

1、crt0.o

https://www.cnblogs.com/xpylovely/p/11412380.html

2、

https://stackoverflow.com/questions/40532180/understanding-the-linkerscript-for-an-arm-cortex-m-microcontroller