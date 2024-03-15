---
title: elf文件分析
date: 2017-04-29 21:31:20
tags:
---
--

# 基础知识

elf是Linux下可执行或者可链接格式的文件。分为以下3种：
1. 可重定向文件。包括a文件和o文件。
2. 可执行文件。就是我们链接得到的可执行文件。
3. 共享文件。就是so文件。

elf文件里一般包括3个索引表：
1. elf header。放在文件开头处。描述了文件的组织结构。
2. Program header。用来告诉系统如何创建进程。可重定向文件不需要这个。
3. section header。



一个elf文件的结构是这样：

```
elf header
program headers talbe
section1
section2
...
section headers table
```



# elf header的数据结构
在elf.h里。
```
typedef struct elf32_hdr{
  unsigned char	e_ident[EI_NIDENT];
  Elf32_Half	e_type;
  Elf32_Half	e_machine;
  Elf32_Word	e_version;
  Elf32_Addr	e_entry;  /* Entry point */
  Elf32_Off	e_phoff;
  Elf32_Off	e_shoff;
  Elf32_Word	e_flags;
  Elf32_Half	e_ehsize;
  Elf32_Half	e_phentsize;
  Elf32_Half	e_phnum;
  Elf32_Half	e_shentsize;
  Elf32_Half	e_shnum;
  Elf32_Half	e_shstrndx;
} Elf32_Ehdr;
```
写一个helloword程序，编译了。

## 2.1 x86上

看elf header。

```
teddy@teddy-ubuntu:~/test/c-test$ readelf -h a.out 
ELF 头：
  Magic：   7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (可执行文件)
  Machine:                           Intel 80386
  Version:                           0x1
  入口点地址：               0x8048320
  程序头起点：          52 (bytes into file)
  Start of section headers:          6136 (bytes into file)
  标志：             0x0
  本头的大小：       52 (字节)
  程序头大小：       32 (字节)
  Number of program headers:         9
  节头大小：         40 (字节)
  节头数量：         30
  字符串表索引节头： 27
teddy@teddy-ubuntu:~/test/c-test$ 
```
看program header。
```
teddy@teddy-ubuntu:~/test/c-test$ readelf -l a.out 

Elf 文件类型为 EXEC (可执行文件)
入口点 0x8048320
共有 9 个程序头，开始于偏移量 52

程序头：
  Type           Offset   VirtAddr   PhysAddr   FileSiz MemSiz  Flg Align
  PHDR           0x000034 0x08048034 0x08048034 0x00120 0x00120 R E 0x4
  INTERP         0x000154 0x08048154 0x08048154 0x00013 0x00013 R   0x1
      [Requesting program interpreter: /lib/ld-linux.so.2]
  LOAD           0x000000 0x08048000 0x08048000 0x005d4 0x005d4 R E 0x1000
  LOAD           0x000f08 0x08049f08 0x08049f08 0x00118 0x0011c RW  0x1000
  DYNAMIC        0x000f14 0x08049f14 0x08049f14 0x000e8 0x000e8 RW  0x4
  NOTE           0x000168 0x08048168 0x08048168 0x00044 0x00044 R   0x4
  GNU_EH_FRAME   0x0004dc 0x080484dc 0x080484dc 0x0002c 0x0002c R   0x4
  GNU_STACK      0x000000 0x00000000 0x00000000 0x00000 0x00000 RW  0x10
  GNU_RELRO      0x000f08 0x08049f08 0x08049f08 0x000f8 0x000f8 R   0x1

 Section to Segment mapping:
  段节...
   00     
   01     .interp 
   02     .interp .note.ABI-tag .note.gnu.build-id .gnu.hash .dynsym .dynstr .gnu.version .gnu.version_r .rel.dyn .rel.plt .init .plt .text .fini .rodata .eh_frame_hdr .eh_frame 
   03     .init_array .fini_array .jcr .dynamic .got .got.plt .data .bss 
   04     .dynamic 
   05     .note.ABI-tag .note.gnu.build-id 
   06     .eh_frame_hdr 
   07     
   08     .init_array .fini_array .jcr .dynamic .got 
```
看section header。
```
teddy@teddy-ubuntu:~/test/c-test$ readelf -S a.out 
共有 30 个节头，从偏移量 0x17f8 开始：

节头：
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  [ 0]                   NULL            00000000 000000 000000 00      0   0  0
  [ 1] .interp           PROGBITS        08048154 000154 000013 00   A  0   0  1
  [ 2] .note.ABI-tag     NOTE            08048168 000168 000020 00   A  0   0  4
  [ 3] .note.gnu.build-i NOTE            08048188 000188 000024 00   A  0   0  4
  [ 4] .gnu.hash         GNU_HASH        080481ac 0001ac 000020 04   A  5   0  4
  [ 5] .dynsym           DYNSYM          080481cc 0001cc 000050 10   A  6   1  4
  [ 6] .dynstr           STRTAB          0804821c 00021c 00004a 00   A  0   0  1
  [ 7] .gnu.version      VERSYM          08048266 000266 00000a 02   A  5   0  2
  [ 8] .gnu.version_r    VERNEED         08048270 000270 000020 00   A  6   1  4
  [ 9] .rel.dyn          REL             08048290 000290 000008 08   A  5   0  4
  [10] .rel.plt          REL             08048298 000298 000018 08  AI  5  12  4
  [11] .init             PROGBITS        080482b0 0002b0 000023 00  AX  0   0  4
  [12] .plt              PROGBITS        080482e0 0002e0 000040 04  AX  0   0 16
  [13] .text             PROGBITS        08048320 000320 000192 00  AX  0   0 16
  [14] .fini             PROGBITS        080484b4 0004b4 000014 00  AX  0   0  4
  [15] .rodata           PROGBITS        080484c8 0004c8 000013 00   A  0   0  4
  [16] .eh_frame_hdr     PROGBITS        080484dc 0004dc 00002c 00   A  0   0  4
  [17] .eh_frame         PROGBITS        08048508 000508 0000cc 00   A  0   0  4
  [18] .init_array       INIT_ARRAY      08049f08 000f08 000004 00  WA  0   0  4
  [19] .fini_array       FINI_ARRAY      08049f0c 000f0c 000004 00  WA  0   0  4
  [20] .jcr              PROGBITS        08049f10 000f10 000004 00  WA  0   0  4
  [21] .dynamic          DYNAMIC         08049f14 000f14 0000e8 08  WA  6   0  4
  [22] .got              PROGBITS        08049ffc 000ffc 000004 04  WA  0   0  4
  [23] .got.plt          PROGBITS        0804a000 001000 000018 04  WA  0   0  4
  [24] .data             PROGBITS        0804a018 001018 000008 00  WA  0   0  4
  [25] .bss              NOBITS          0804a020 001020 000004 00  WA  0   0  1
  [26] .comment          PROGBITS        00000000 001020 000052 01  MS  0   0  1
  [27] .shstrtab         STRTAB          00000000 001072 000106 00      0   0  1
  [28] .symtab           SYMTAB          00000000 001178 000430 10     29  45  4
  [29] .strtab           STRTAB          00000000 0015a8 00024f 00      0   0  1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings)
  I (info), L (link order), G (group), T (TLS), E (exclude), x (unknown)
  O (extra OS processing required) o (OS specific), p (processor specific)
```
我们现在来分析一下上面得到的信息。
elf header的长度是52字节。
用hexdump查看a.out的前面52个字节。

```
teddy@teddy-ubuntu:~/test/c-test$ hexdump -C -n 52 a.out 
00000000  7f 45 4c 46 01 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|
00000010  02 00 03 00 01 00 00 00  20 83 04 08 34 00 00 00  |........ ...4...|
00000020  f8 17 00 00 00 00 00 00  34 00 20 00 09 00 28 00  |........4. ...(.|
00000030  1e 00 1b 00                                       |....|
00000034
```
我们先分析前面16个字节。0x7F开头是固定的。45 4c 46是elf的ASCII码值。
接下来的3个01分别是：第一个表示这是32位的，第二个01表示是小端，第三个01表示版本。
其余都是预留的。
再看第二个16字节。
前面2个字节0002表示是可执行文件。再2个字节是0003，表示cpu是x86的。
再一个00000001表示当前版本。再08048320是entry地址。
后面的不细看了，可以参照结构体的内容看。

## 2.2 arm上



```
pi@raspberrypi:~/work/test/gcc$ readelf -h a.out 
ELF Header:
  Magic:   7f 45 4c 46 01 01 01 00 00 00 00 00 00 00 00 00 
  Class:                             ELF32
  Data:                              2's complement, little endian
  Version:                           1 (current)
  OS/ABI:                            UNIX - System V
  ABI Version:                       0
  Type:                              EXEC (Executable file)
  Machine:                           ARM
  Version:                           0x1
  Entry point address:               0x102f4
  Start of program headers:          52 (bytes into file)
  Start of section headers:          4496 (bytes into file)
  Flags:                             0x5000402, has entry point, Version5 EABI, hard-float ABI
  Size of this header:               52 (bytes)
  Size of program headers:           32 (bytes)
  Number of program headers:         8
  Size of section headers:           40 (bytes)
  Number of section headers:         30
  Section header string table index: 27
```

# SimpleSection分析

SimpleSection.c

```
int printf(const char* format,...);

int global_init_var = 84;
int global_uninit_var;

void func1(int i)
{
	printf("%d\n",i);
}

int main(void)
{
	static int static_var = 85;
	static int static_var2;

	int a=1;
	int b;

	func1(static_var + static_var2 + a + b);

	return a;
}
```

编译

```
gcc SimpleSection.c -o SimpleSection.o
```

关于段的几个重要属性：

Size 表示段的长度，

File off 表示段的位置，

每个段的第2行中的 “CONTENTS” 表示该段在文件中存在。

在 bss 段中没有 “CONTENTS” ，表示该段在目标文件中不存在。

.note.GNU-stack 堆栈段的长度为0，在这里忽略掉它，认为它也不存在。



用 size 命令可以查看 ELF 文件的代码段、数据段和 bss 段的长度（dec 表示3个段长度的和的十进制，hex表示长度和的十六进制） 如下。

```
 size SimpleSection.o
   text    data     bss     dec     hex filename
   1663     608      16    2287     8ef SimpleSection.o
```



为什么 size 和 objdump 查看目标文件的 .text 段的大小不一样呢？

因为size默认是运行在"Berkeley compatibility mode"下。

在这种模式下，会将不可执行的拥有"ALLOC"属性的只读段归到.text段下，很典型的就是.rodata段。

而在我们这个例子中，使用 size 命令得到的 text 段长度 = .text + .rodata + .note.gnu.property + .eh_frame 。

如果你使用"size -A obj.o"，那么size会运行在"System V compatibility mode"，

此时，用objdump -h和size显示的.text段大小就差不多了，如下图。

## 代码段 .text

 程序源代码编译之后的机器指令经常被放在代码段中。

通过使用 -s -d 参数的 objdump 命令将所有段以十六进制的形式打印出来（-s），并将所有包含指令的段反汇编（-d）。

## 数据段 .data和只读数据段 .rodata

.data 段保存的是那些已经初始化了的全局静态变量和局部静态变量。

在我们这个例子 SimpleSection.c 中，

global_init_var 和 static_var 是已经初始化过的，每个变量 4 个字节，一共 8 个字节被存储到 .data 段中。

在这里采用小端法来存储，

.data 段中前四个字节为 5400 0000 ，转换为十进制为 84；

后四个字节为 5500 0000 ，转换为十进制为 85。

分别与这两个变量的值一一对应。

      .rodata 段中存放的是只读数据，一般是程序中的只读变量（如 const 修饰的变量）和字符串常量。在 SimpleSection.c 中调用 printf 时，用到了一个字符串常量 “%d\n”，它是一种只读数据，被存储到 .rodata 段中。.rodata 段中的四个字节 2564 0a00 分别对应的是字符 ‘%’、‘d’、’\n’ 和 ‘\0’ 。
    
      有时候编译器也会将字符串常量放在 .data 段中。
## .bss段

.bss 段中存放的是未初始化的全局变量和局部静态变量，

在上述代码中，global_uninit_var 和 static_var2 是未被初始化过的，它们被存放在 .bss 段中，

更准确的来讲，是在 .bss 段为它们预留空间。

可以认为未初始化过的变量值为0，而存储 0 是没有必要的。

.bss 段没有实际内容，所以它在可执行文件中也不占据空间。

 上面得到的 .bss 段大小为 4 个字节，与变量 global_uninit_var 和 static_var2 的大小之和 8 个字节不符。

实际上通过符号表（Symbol Table）能够看到，

只有 static_var2 被放在了 .bss 段中，

而 global_uninit_var 未被放在任何段，

只是一个未定义的 “COMMON 符号”。

**这和不同的语言不同的编译器有关，**

有的编译器会将 全局未初始化变量 存放在目标文件 .bss 段中，

有些则不存放，只是预留一个 未定义的全局变量符号，

等到最终链接为可执行文件时再在 .bss 段中分配空间。

原则上来讲，可以简单的认为全局未初始化变量被存放在 .bss 段中。

但是未初始化的静态变量（编译单元内部可见）的确是存放在 .bss 段中的。

## 其他段

   .comment 段中存放的是编译器版本信息。.其余两个段 .note.gnu.property 和 .eh_frame 在此不做说明。

# 简介

ELF（Executable and Linkable Format）是一种用于可执行文件、共享库和目标文件的标准文件格式。它是一种可移植和可扩展的文件格式，广泛用于类Unix系统中，如Linux和BSD。

ELF文件格式定义了目标文件的结构、布局和元信息，使操作系统和链接器能够正确加载和执行程序。下面是ELF文件的主要组成部分：

1. **ELF文件头（ELF Header）：** ELF文件的第一个部分是文件头，包含了描述文件本身的元信息，如文件类型、目标体系结构、入口点地址等。文件头也包含了指向其他重要部分的偏移量和大小。

2. **程序头表（Program Header Table）：** 程序头表包含了描述可执行文件或共享库中各个段（Segment）的信息，如代码段、数据段等。每个段描述了在内存中加载的位置、大小、访问权限等。

3. **节头表（Section Header Table）：** 节头表描述了目标文件中各个节（Section）的信息，例如代码节、数据节、符号表节等。每个节描述了其在文件中的位置、大小、属性等。

4. **节区（Section）：** 节区是ELF文件的基本组成单元，每个节区包含了特定类型的数据，如代码、数据、符号表、字符串表等。节区可以被链接器用于合并、重定位和优化目标文件。

5. **符号表（Symbol Table）：** 符号表包含了目标文件或共享库中定义和引用的符号信息，如函数、变量、类等。符号表记录了每个符号的名称、类型、大小、绑定属性等。

6. **重定位表（Relocation Table）：** 重定位表包含了需要在加载时进行地址重定位的位置和信息。链接器使用重定位表来解析和修正目标文件中的符号引用，以便正确地连接和执行程序。

ELF文件格式的优点包括可移植性、灵活性和可扩展性。它支持多种体系结构和操作系统，并提供了丰富的元信息和功能，使得程序能够在不同的环境中正确加载和执行。

请注意，ELF文件格式非常复杂，上述介绍只是对其主要组成部分的概述。要深入了解ELF文件格式的详细规范和细节，可以参考相关文档和标准，如《System V ABI》和《ELF标准规范》。

# elf格式发展历史

ELF格式的发展历史可以追溯到==1980年代末==和1990年代初，当时UNIX操作系统和UNIX-like操作系统的普及使得对==一个通用的二进制文件格式==的需求变得迫切。在这之前，==不同的UNIX系统使用了各种不同的二进制格式==，这导致了软件移植的困难。

以下是ELF格式的一些主要发展历程：

1. **a.out格式**：在早期的UNIX系统中，通常使用的是==a.out格式==（Assembler Output）。这是一种简单的二进制文件格式，==用于存储可执行文件和可链接文件==。然而，**a.out格式缺乏扩展性**，不适用于多种体系结构和复杂的应用场景。

2. **COFF格式**：随着UNIX操作系统的发展，一些系统开始采用COFF格式（Common Object File Format）。COFF格式相对于a.out格式来说更为灵活，支持更多的特性，如更好的调试信息支持等。但COFF格式仍然存在一些局限性，无法完全满足需求。

3. **ELF格式的提出**：在这种情况下，UNIX系统厂商和开发者开始致力于设计一种新的二进制文件格式，==既能够满足当前的需求，又具有足够的灵活性和扩展性==。1990年代初，System V Release 4（SVR4）操作系统引入了ELF格式作为默认的二进制文件格式。ELF格式在设计上更为灵活和通用，支持多种体系结构，同时也更易于扩展和维护。

4. **广泛应用**：随着UNIX和Linux操作系统的普及，ELF格式逐渐成为主流的二进制文件格式。现在，几乎所有的UNIX-like系统都使用ELF格式来存储可执行文件和可链接文件。

5. **持续发展**：ELF格式在其发展历史中持续得到改进和扩展。随着硬件和软件技术的不断进步，ELF格式也在不断地演变，以适应新的需求和挑战。例如，近年来针对安全性、性能优化等方面的改进都在不断进行。

总的来说，ELF格式的发展历史反映了操作系统和软件开发领域对一个通用、灵活、可扩展的二进制文件格式的追求，它为多种体系结构和应用场景提供了统一的解决方案。

# windows对elf格式支持吗

Windows操作系统本身并不直接支持ELF格式。Windows主要使用PE（Portable Executable）格式作为其默认的可执行文件和可链接文件格式。

==PE格式与ELF格式有一些显著的区别，包括文件头部、节表、重定位机制等。==因此，Windows操作系统无法直接执行或加载ELF格式的文件。

然而，有一些第三方工具和软件可以实现在Windows上处理ELF格式文件的功能。

例如，某些开发环境和交叉编译工具链可能支持将ELF格式的程序编译为Windows可执行文件，或者允许在Windows上调试和分析ELF格式的程序。

但是，这种支持通常是通过额外的软件或工具实现的，而不是Windows本身提供的功能。

总的来说，虽然Windows操作系统本身不直接支持ELF格式，但通过第三方工具和软件，可以在一定程度上在Windows平台上处理ELF格式的文件。

# pe格式和elf格式比较

PE（Portable Executable）和ELF（Executable and Linkable Format）是两种不同操作系统下常见的可执行文件格式，它们各自在不同的操作系统中扮演着类似的角色。以下是它们之间的比较：

1. **所属操作系统**：
   - PE格式主要用于Windows操作系统，包括Windows 32位和64位系统。
   - ELF格式主要用于UNIX和类UNIX操作系统，如Linux、BSD等，也在其他系统中有应用。

2. **文件结构**：
   - PE格式使用一种层次化的结构，由文件头、可选的头部表、节表、数据目录和节数据等组成。
   - ELF格式也使用层次化结构，由头部、节表、段表、重定位表等组成。

3. **可移植性**：
   - ELF格式通常被认为更加可移植，因为它在多个UNIX-like系统中被广泛使用，而且可以轻松移植到新的体系结构上。
   - PE格式则主要用于Windows系统，因此其可移植性相对较低。

4. **功能特性**：
   - PE格式在Windows系统中提供了丰富的功能特性，如资源管理、调试信息等，这些功能在Windows开发中经常被使用。
   - ELF格式也提供了类似的功能特性，如动态链接、重定位、符号表等，但在不同的UNIX系统中可能会有一些差异。

5. **工具支持**：
   - 在Windows平台上，开发人员通常会使用Visual Studio等工具来创建、编译和调试PE格式的文件。
   - 在UNIX和类UNIX系统上，开发人员通常会使用GCC、LLVM等工具来创建、编译和调试ELF格式的文件。

6. **安全性**：
   - PE格式和ELF格式在安全性方面都有相关的机制，如ASLR（Address Space Layout Randomization）、DEP（Data Execution Prevention）等。这些机制有助于防止恶意软件的攻击。

总的来说，PE格式和ELF格式都是现代操作系统中常见的可执行文件格式，它们在不同的操作系统中扮演着类似的角色，但在结构、特性和工具支持等方面有一些区别。

# 掌握elf格式知识可以有哪些好处

掌握ELF格式知识可以带来许多好处，特别是对于那些从事系统编程、应用程序开发和安全领域的人员。以下是一些掌握ELF格式知识的好处：

1. **理解系统内部工作原理**：ELF格式是操作系统中可执行文件的基础，掌握ELF格式知识可以帮助开发人员更好地理解系统内部的工作原理，包括可执行文件的加载、链接、执行过程等。

2. **调试和分析能力**：ELF格式提供了丰富的调试和分析信息，包括符号表、调试信息、重定位表等，掌握ELF格式知识可以帮助开发人员更好地进行程序调试和性能分析。

3. **软件逆向工程**：在软件逆向工程领域，掌握ELF格式知识可以帮助分析和理解已编译程序的内部结构，包括函数、数据、控制流等，从而进行逆向工程和漏洞分析。

4. **系统优化和性能调优**：ELF格式提供了一些优化和性能调优的机制，如重定位、共享库等，掌握ELF格式知识可以帮助开发人员更好地进行系统优化和性能调优。

5. **开发工具和编译器开发**：掌握ELF格式知识可以帮助开发人员更好地开发和维护编译器、链接器和其他开发工具，从而提高软件开发效率和质量。

6. **安全研究和漏洞分析**：ELF格式是安全研究和漏洞分析的重要基础，掌握ELF格式知识可以帮助安全研究人员更好地理解和分析已编译程序的内部结构，从而发现和修复潜在的安全漏洞。

总的来说，掌握ELF格式知识可以帮助开发人员更好地理解系统内部工作原理，提高调试和分析能力，支持软件逆向工程和安全研究等领域的工作。

# 请从helloworld开始，告诉我怎么一步步学习elf的知识，并进行应用

学习ELF格式知识并进行应用可以从编写一个简单的Hello World程序开始，然后逐步深入学习和理解ELF格式的各个方面。下面是一个逐步学习ELF知识并进行应用的建议步骤：

1. **编写Hello World程序**：首先，编写一个简单的Hello World程序，可以使用C或者其他编程语言。确保程序能够正确编译和运行。

2. **编译程序为可执行文件**：使用编译器将Hello World程序编译为可执行文件。例如，使用GCC编译器可以执行以下命令：

   ```bash
   gcc -o hello hello.c
   ```

3. **查看可执行文件的内容**：使用工具查看可执行文件的内容，了解其结构。可以使用`readelf`工具查看ELF文件的结构和相关信息。例如，可以执行以下命令：

   ```bash
   readelf -h hello   # 查看文件头信息
   readelf -S hello   # 查看节表信息
   readelf -l hello   # 查看段表信息
   ```

   这些命令将会显示可执行文件的头部、节表和段表等信息，帮助你理解ELF文件的结构。

4. **理解ELF文件的结构**：深入学习和理解ELF文件的结构，包括文件头部、节表、段表、重定位表等各个部分的作用和组成。可以参考相关资料和文档，如ELF格式规范等。

5. **修改和扩展程序**：尝试修改和扩展Hello World程序，并观察其对应的ELF文件的变化。可以添加新的函数、数据等，然后重新编译并查看生成的ELF文件的变化。

6. **应用到实际项目中**：将所学到的ELF知识应用到实际项目中，例如优化代码、调试程序、分析性能等。通过实际项目的应用，加深对ELF格式的理解和掌握。

7. **进一步学习和探索**：深入学习ELF格式的更多细节和特性，如动态链接、共享库、重定位等。可以阅读相关的书籍、论文和文档，以及参与相关的课程和培训。

通过以上步骤，你可以逐步学习和掌握ELF格式的知识，并将其应用到实际项目中，从而更好地理解和利用这一重要的二进制文件格式。

# linux的模块是elf格式的吗

在 Linux 中，内核模块不是 ELF 格式的，而是专门的一种称为核心对象文件（Core Object Files）的格式。核心对象文件格式与 ELF 格式有一些相似之处，但也有一些重要的区别。

核心对象文件（.ko 文件）包含了编译后的内核模块代码，以及模块的元数据，如模块的参数、版本信息等。这些信息用于在运行时加载和管理内核模块。

尽管核心对象文件不是 ELF 格式，但在某种程度上，它们也可以视为一种特定于 Linux 内核的二进制格式。因此，在处理核心对象文件时，需要使用特定于 Linux 内核的工具和接口，如 `insmod` 和 `rmmod` 等命令来加载和卸载模块。

总的来说，尽管 Linux 内核模块不是 ELF 格式的，但它们也是一种特定于 Linux 内核的二进制格式，用于在运行时扩展和修改 Linux 内核的功能。

# 参考资料

1、

https://blog.csdn.net/Little_ant_/article/details/119214033