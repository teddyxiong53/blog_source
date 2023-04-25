---
title: arm汇编（一）整体规划
date: 2018-02-02 09:42:09
tags:
	- arm

---



现在开始把arm汇编知识进行系统性的学习。

目的：可以解决uboot和kernel移植中的汇编问题。

先上网找一下学习的建议。

网上说目前还没有系统化的讲解arm汇编的书籍，最权威的学习材料是arm的官方文档。

arm是精简指令集，使用的命令格式比x86 的简单很多，首先不要有畏惧心理。

到arm官网上下载指令文档，就可以开始学习了。



针对C++语言的CPPABI

运行时ABI: RTABI

子程序调用标准：aapcs

文件格式：elf

《ARM Architecture Reference Manual.pdf》这个是arm官方手册。文档长达5000页。只需要知道各部分的位置，以查阅为主。

文档按字母顺序进行编排。

Part A是架构的概述。

Part B是App层的程序模型和内存模型。可以了解到arm的寄存器、字节序、缓存、内存对齐等知识。

Part C是AArch64的指令集。

Part D是AArch64的系统级架构，只需要了解即可。

**Part E是32位ARM的应用层架构，重要。**

**Part F是32位的arm指令集格式讲解与分类。重要。**

Part E和Part F是我需要重点关注的。



如何巩固学习成果。

编写基于ARM汇编的汇编引擎和反汇编引擎，编写ARM hook工具。

这些有东西可以参考，llvm的arm反汇编处理模块。



# 下载文档查看

我下载了一份，但是看时间似乎有点早。文档也只有1100页。先看看怎么样。如果可以，先用着。

上面copyright信息只写到2005年，那估计就是2005年的文档了。

看里面指令集讲到了armv6，这个也不是很老。不算过时。

S3C2440的是armv4的指令集。ARM9系列都是是v4或者v5指令集的。

这份文档可以读。内容结构跟上面描述的不同。



# 文档内容架构

## Part A

这部分讲cpu的架构。

1、概述arm架构和指令集。

2、arm指令集操作的数据类型。通用寄存器。程序状态寄存器。处理中断的方式。大小端。对齐。

3、指令集概述。

4、指令集。

5、寻址方式。

6、thumb指令集概述。

7、thumb指令集。

## Part B

内存和系统架构。

1、概述。

2、内存模型。

3、System Control协处理器概述。

4、虚拟内存相关。MMU

5、保护内存相关。PMU。单片机用这种。

6、cache和buffer。

7、其他

## Part C

浮点相关。不看了。

## Part D

debug相关。不看了。



# gnu as手册

有了arm的这份手册，离arm编程还有距离。中断还隔着汇编器。

要选一个汇编器。还有它的手册。

我当然选择gnu的汇编器。

gnu assembler就是gcc工具链里的那个as。

```
AS - the portable GNU assembler.
```

找到文档，大概400页。版权信息写到2015年，是比较新的。文档版本是Version2.26。

《as.pdf》文档目录。

## 1. 概述

1、文档结构。

2、gun assembler。

3、o文件格式。

4、命令行。

5、输入文件。

6、输出文件。

7、错误和警告。

## 2.命令行选项

不看。

## 3. 语法

1、预处理。

2、空白。

3、注释。

4、符号。

5、指令。

6、常量。

## 4. section和relocation

1、背景。

2、link 选项。

3、汇编器内部section。

4、子section。

5、bss 段。

## 5.符号symbol 

1、label

2、赋值

3、符号名字。

4、特殊的`.`这个符号

5、符号属性。

## 6.表达式expression

1、空表达式

2、整数表达式

## 7. 汇编伪指令

1、.abort

2、.ABORT

3、.align

4、.altmacro

5、.ascii string

6、.asciz string

7、.balign

8、bundle

9、.byte

10、cfi指令

累计有100条左右。不一一看了。

## 8. o文件属性

## 9. 机器相关属性

内容也比较多。



重点看前面8章的。

# 其他资料

除了上面的两份手册，我就重点根据泰晓科技的相关文档来学习。

http://tinylab.org/linux-assembly-language-quick-start/



# 环境搭建

1、win7 pc上安装VMware。

2、VMware里安装Ubuntu，Ubuntu里安装qemu和arm工具链。

3、就采用qemu-arm来运行。

先跑一个程序试试，验证环境是ok的。

```
.data
msg:
    .ascii      "Hello, ARM!\n"
len = . - msg
.text
.globl _start
_start:
    /* syscall write(int fd, const void *buf, size_t count) */
    mov     %r0, $1     /* fd -> stdout */
    ldr     %r1, =msg   /* buf -> msg */
    ldr     %r2, =len   /* count -> len(msg) */
    mov     %r7, $4     /* write is syscall #4 */
    swi     $0          /* invoke syscall */
    /* syscall exit(int status) */
    mov     %r0, $0     /* status -> 0 */
    mov     %r7, $1     /* exit is syscall #1 */
    swi     $0          /* invoke syscall */
```

运行效果：

```
teddy@teddy-ubuntu:~/work/test/asm$ qemu-arm ./arm-hello
Hello, ARM!
```



我简单调试一下这个程序。

1、`.global _start`这一行，不加的话，也可以运行。编译的时候，会警告一下。

```
arm-none-eabi-ld: warning: cannot find entry symbol _start; defaulting to 0000000000008000
```

但是实际上用readelf读出来是一样的布局。

2、`$` `#`是一样的作用，都是表示立即数。

3、寄存器前面的`%`也可以没有。

所以这样也是可以的。我是更加习惯这种风格的。

```
.data
msg:
	.ascii "hello, arm!\n"
	
len = . - msg
.text
.global _start

_start:
	mov r0, #1
	ldr r1, =msg
	ldr r2, =len
	mov r7, #4
	swi #0
	mov r0, #0
	mov r7, #1
	swi #0
```

 这里出现了一个很重要的知识点。就是调用号。

为什么write是4号syscall？这些调用谁来规定，怎么保证一直不变，如果变了，对于开发人员的影响岂不是很大？

这里有描述：http://www.linfo.org/system_call_number.html

但是我从unistd.h里看到，和这个网页上看到的不同。

```
#define __NR3264_lseek 62
__SC_3264(__NR3264_lseek, sys_llseek, sys_lseek)
#define __NR_read 63
__SYSCALL(__NR_read, sys_read)
#define __NR_write 64
__SYSCALL(__NR_write, sys_write)
#define __NR_readv 65
```

这个write是64号了。那怎么用4还可以呢？

但是在这个文件/usr/src/linux-headers-4.4.0-112-generic/arch/x86/include/generated/uapi/asm/unistd_32.h里。却是这样的：

```
#define __NR_restart_syscall 0
#define __NR_exit 1
#define __NR_fork 2
#define __NR_read 3
#define __NR_write 4
#define __NR_open 5
#define __NR_close 6
```

以下面这个为准吧。暂时不深究了。



我们现在把学习的条件都准备好了。开始进行学习。

