---
title: elf文件分析
date: 2017-04-29 21:31:20
tags:
---
# 1. 基础知识
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



# 2. elf header的数据结构
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

##2.1 x86上

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



