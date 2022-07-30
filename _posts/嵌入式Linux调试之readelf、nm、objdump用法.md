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