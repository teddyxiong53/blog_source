---
title: gcc（1）
date: 2020-05-30 11:31:38
tags:
	 - gcc

---

1

-W{all,xxx}

可以这样来加选项。



# PIC

PIC是Position Independent Code。位置无关代码。

编译Linux共享库的时候，为什么要加PIC选项。

写如下的测试代码：

```
void func()
{

}
int test()
{
    func();
    return 0;
}
```

编译：

```
all:
	gcc -o fpic-no-pic.s -S test.c
	gcc -fpic -o  fpic.s -S test.c
```

对比2个汇编文件。

可以看到只有一行不同：

![1591767934346](../images/random_name/1591767934346.png)



pic版本的，是通过PLT（Procedure Linkage Table）来调用函数。

加上pic的，效率会高一些。



# 强符号和弱符号

对于链接器来说，所有的全局符号可分为两种：强符号（Strong symbols），弱符号（Weak symbols）。**gcc**的attribute中有个`__attribute__((weak))`，就是用来声明这个符号是弱符号的。



一般来说，函数和已初始化的变量是强符号，而未初始化的变量是弱符号。

对于它们，下列三条规则适用：

1. 同名的强符号只能有一个。

2. 有一个强符号和多个同名的弱符号是可以的，但定义会选择强符号的。

3. **有多个弱符号时，链接器可以选择其中任意一个。**

这三条规则看起来很好理解，其实不然，尤其是当这些弱符号类型和强符号不同时！表面上看起来正确的程序会导致严重的错误！考虑下面这个[csapp中](http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15213-f06/www/lectures/class13.pdf)的例子：

===a.c===
int x=7;
int y=5;
p1() {}

===b.c===
double x;
p2() {}

我们把它们一起编译，并且在p2()函数中给x赋值，你会发现，y也改变了（因为double占用了8个字节，而y紧挨着x）！ 虽然x被看作是double，但其定义会取a.c中的int x，也就是说，在b.c中会把a.c中的int x当double来用！这当然是错误！之所以会这样，就是因为上面的规则2。避免这种错误的一个方法是，给**gcc**加上-**fno-common**选项。

# -fmessage-length=0

默认情况下，GNU工具链编译过程中，控制台输出的一行信息是不换行的，这样，当输出信息过长时(如编译错误时的信息)，会导致你无法看到完整的输出信息，加入-fmessage-length=0后，输出信息会根据控制台的宽度自动换行，这样就能看全输出信息了。



# -fno-exceptions

-fno-rtti 禁用运行时类型信息
-fno-exceptions 禁用异常机制

一般只有对程序运行效率及资源占用比较看重的场合才会使用, 如果要做这两个的话最好连libstdc++和其他所有的的c++库都用这两个参数重新编译一遍, 否则光是你自己的程序禁用了这两个特性, 而别的库依然开着, 效果就大打折扣了



# -ffunction-sections -fdata-sections

有时我们的程序会定义一些暂时使用不上的功能和函数，虽然我们不使用这些功能和函数，但它们往往会浪费我们的ROM和RAM的空间。这在使用静态库时，体现的更为严重。有时，我们只使用了静态库仅有的几个功能，但是系统默认会自动把整个静态库全部链接到可执行程序中，造成可执行程序的大小大大增加。



为了解决前面分析的问题，我们引入了标题中的几个参数。**GCC链接操作是以section作为最小的处理单元**，只要一个section中的某个符号被引用，该section就会被加入到可执行程序中去。因此，GCC在编译时可以使用 -ffunction-sections和 -fdata-sections 将每个函数或符号创建为一个sections，其中每个sections名与function或data名保持一致。**而在链接阶段， -Wl,–gc-sections 指示链接器去掉不用的section**（其中-wl, 表示后面的参数 -gc-sections 传递给链接器），这样就能减少最终的可执行程序的大小了。



# -fomit-frame-pointer

可以看到不加-fomit-frame-pointer选项编译出来的代码少了一些，最主要的区别是少了栈帧的切换和栈地址的保存，栈是从高地址向低地址扩展，而堆是从低地址向高地址扩展。在x86体系结构中，栈顶寄存器是esp，栈底寄存器位ebp，esp的值要小于ebp的值。函数调用时先将函数返回值、传入参数依次压入栈中，CPU访问时采用0x8(%esp)方式访问传入的参数，使用-fomit-frame-pointer会由于没有保存栈调用地址，而导致无法追踪函数调用顺序，我想gcc，vs等编译器记录函数调用顺序都是采用这种方式吧。



```
-Wall 打开所有警告
-Wextra 打印额外的信息
-w 小写，表示关闭所有警告信息。
-Wshadow 这个表示当一个局部变量覆盖另外一个局部变量或者全局变量时，给出警告。-Wall并没有打开这个。
-Wpointer-arith 当对void *指针进行数学运算时给出警告。-Wall没有打开这个。
-Wcast-qual 当强制类型转化丢掉了类型修饰符的时候，给出警告。-Wall没有打开这个。
-Waggregate-return 返回结构体的时候，给出警告。
-Winline 如果你的函数不能内联，给出警告。
-Wunreachable-code 如果代码里有永远执行不到的代码，给出警告。
-Wundef 当一个没有定义的符号出现在#if 里的时候，给出警告。
```

标准：

```
-ansi
-std=c89
-std=c99
-std=c++98
-std=gnu9x

```



参考资料

1、编译GNU/Linux共享库, 为什么要用PIC编译?( 转)

https://blog.csdn.net/chenji001/article/details/5691690

2、gcc中no-common的说明

https://blog.csdn.net/cybertan/article/details/5867191

3、gcc编译参数详解一

https://www.bbsmax.com/A/x9J2e3qjz6/

4、gcc编译参数详解概述

https://www.bbsmax.com/A/LPdoqkQGJ3/

5、C性能调优---GCC编译选项-fomit-frame-pointer

https://www.cnblogs.com/islandscape/p/3444122.html

6、GCC 参数

这个表格总结清晰。很好。

https://blog.csdn.net/orzlzro/article/details/6459665

7、MMD MP

https://blog.csdn.net/eydwyz/article/details/90296048