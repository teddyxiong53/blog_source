---
title: 嵌入式Linux调试之readelf、nm、objdump用法
date: 2020-05-08 09:48:08
tags:
	- Linux

---

1

发现自己对这几个工具的详细用法不是很了解，现在有个问题，是需要借助这几个工具来找思路。

所以，现在系统分析一下这几个工具的用法。

readelf的主要设计目的是什么？nm的目的又是什么？objdump的主要用途又是什么？

nm主要是查看符号。

readelf可以看section情况，也可以看符号。

objdump主要用把elf转成可烧录的bin文件，对elf进行反汇编。



# readelf

从名字上看，这个就是跟elf文件相关的。

主要是用来查看elf文件相关的信息。

Linux上，可执行文件、so文件、a文件，都是elf文件格式。

命令基本格式：

```
用法：readelf <选项> elf-文件
```

写一个HelloWorld程序。编译得到可执行文件，作为分析的对象。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ readelf -h hello
ELF 头：
  Magic：   7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00 
  类别:                              ELF64
  数据:                              2 补码，小端序 (little endian)
  版本:                              1 (current)
  OS/ABI:                            UNIX - System V
  ABI 版本:                          0
  类型:                              EXEC (可执行文件)
  系统架构:                          Advanced Micro Devices X86-64
  版本:                              0x1
  入口点地址：               0x400430
  程序头起点：          64 (bytes into file)
  Start of section headers:          6616 (bytes into file)
  标志：             0x0
  本头的大小：       64 (字节)
  程序头大小：       56 (字节)
  Number of program headers:         9
  节头大小：         64 (字节)
  节头数量：         31
  字符串表索引节头： 28
```

常用的选项：

```
-s ：查看符号。
-d ： 查看动态链接库情况。
```



# nm

基本格式：

```
用法：nm [选项] [文件]
```

常用的选项：

```
-C 这个列出来的符号可读性很好，尤其是C++代码。
```

符号类型如果是小写，符号通常是本地的；

如果是大写，符号是全局的（外部的）。

但是，有一些小写符号类型表示特殊的全局符号，例如 u、v 和 w。

```
A
该符号的值是绝对的，在以后的链接过程中，不允许进行改变。这样的符号值，常常出现在中断向量表中，例如用符号来表示各个中断向量函数在中断向量表中的位置。

b,B
该符号的值出现在非初始化数据段（BSS）中。例如，在一个文件中定义全局static int test。则该符号test的类型为b，位于bss section中。其值表示该符号在BSS段中的偏移。

C
该符号为common。common symbol是未初始化的数据。该符号没有包含在一个普通section中，只有在链接过程中才进行分配。符号的值表示该符号需要的字节数。例如在一个C文件中，定义int test，并且该符号在别的地方会被引用，则该符号类型即为C，否则其类型为B。

d,D
该符号位于初始化数据段（data section）。例如定义全局变量 int baud_table[5] = {9600, 19200, 38400, 57600, 115200}，则会被分配在初始化数据段中。

g,G
该符号也位于初始化数据段中。主要用于small object提高访问small data object的一种方式

i
这是对标准ELF符号类型集的GNU扩展。它表示一个符号如果被重定位引用，不会计算该符号的地址，而是必须在运行时计算

N
该符号是一个debugging符号。

p
该符号在stack unwind section

r,R
该符号位于只读数据段（read only data section）。例如定义全局const int test[] = {123, 123};则test就是一个只读数据段的符号。

s,S
符号位于非初始化数据区，用于small object。

t,T
该符号位于代码段（text section）。

u
符号是唯一的全局符号。这是GNU对标准ELF符号绑定集的扩展。对于这样的符号，动态链接器将确保在整个过程中只有一个使用此名称和类型的符号。

U
该符号在当前文件中是未定义的，即该符号定义在别的文件中。例如，当前文件调用另一个文件中定义的函数，这个被调用的函数在当前文件就是未定义的，但是在定义它的文件中类型是T。对于全局变量来说，在定义它的文件中，其符号类型为B或D，在使用它的文件中，其类型为U。

v,V
该符号是一个弱符号。当弱定义符号与正常定义符号链接时，使用正常定义符号时不会出错。当链接未定义的弱定义符号，弱符号的值将变为零，且没有错误。在某些系统上，大写表示已指定默认值

w,W
该符号是一个弱符号，未专门标记为弱对象符号。当弱定义符号与正常定义符号链接时，使用正常定义符号时不会出错。当链接未定义的弱未定义符号时，该符号的值将以系统特定的方式确定，且不会出错。在某些系统上，大写表示已指定默认值

-
该符号是a.out格式文件中的stabs symbol。在这种情况下，打印的下一个值是stabs other字段、stabs desc字段和stab类型。stabs符号用于保存调试信息

?
该符号类型没有定义

```







## 参考资料

1、

https://blog.csdn.net/lgfun/article/details/103600880

2、

https://www.huoban.com/news/post/19230.html

3、Linux 命令（63）—— nm 命令

https://blog.csdn.net/K346K346/article/details/89088542

# objdump

objdump是查看o文件或者exe文件的构成的工具。



基本用法：

```
用法：objdump <选项> <文件>
```

我在我的c-test目录下进行验证命令。

常用的命令有：

查看文件头信息

```
hanliang.xiong@walle01-sz:~/work/test/c-test$ objdump -f a.out 


a.out:     file format elf64-x86-64
architecture: i386:x86-64, flags 0x00000150:
HAS_SYMS, DYNAMIC, D_PAGED
start address 0x00000000000010a0
```

查看section header信息

```

```



https://www.cnblogs.com/arnoldlu/p/9649229.html#objdump



# 参考资料

1、readelf命令使用说明

https://www.cnblogs.com/lidabo/p/5702784.html

2、Linux程序分析工具:ldd和nm

https://www.cnblogs.com/xiaomanon/p/4203671.html

3、Linux objdump命令

https://www.cnblogs.com/274914765qq/p/4568084.html