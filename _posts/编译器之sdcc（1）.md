---
title: 编译器之sdcc（1）
date: 2023-06-01 21:48:11
tags:
	- 编译器
---

--

# 什么是sdcc

sdcc是small device C compiler的意思。

SDCC 是一个可重定向、优化的标准 C（ANSI C89、ISO C99、ISO C11）编译器套件，

其目标是

基于 Intel MCS51 的微处理器（8031、8032、8051、8052 等）、

Maxim（以前的 Dallas）DS80C390 变体、

Freescale（前身为摩托罗拉）基于 HC08（hc08、s08）、

基于 Zilog Z80 的 MCU（Z80、Z180、SM83、Rabbit 2000、2000A、3000A、TLCS-90）、

Padauk（pdk14、pdk15）

和 STMicroelectronics STM8。

支持 Padauk pdk13 和 MOS 6502 目标的工作正在进行中； 

Microchip PIC16 和 PIC18 目标未维护。

 SDCC 可以重定向到其他微处理器。



SDCC 套件是几个组件的集合，这些组件来自具有不同 FOSS 许可证的不同来源。 

SDCC 编译器套件包括：

sdas 和 sdld，

一个可重定向的汇编器和链接器，基于 ASXXXX，由 Alan Baldwin 编写； （通用公共许可证）。

sdcpp 预处理器，

基于 GCC cpp； （通用公共许可证）。

ucsim 模拟器，

最初由 Daniel Drotos 编写； （通用公共许可证）。

sdcdb 源代码级调试器，

最初由 Sandeep Dutta 编写； （通用公共许可证）。

sdbinutils 库归档实用程序，

包括 sdar、sdranlib 和 sdnm，源自 GNU Binutils； (通用公共许可证)

SDCC 运行时库； (GPL+LE)。 

Pic 器件库和头文件源自 Microchip 头文件 (.inc) 和链接器脚本 (.lkr) 文件。

 Microchip 要求“头文件应说明它们只能与真正的 Microchip 设备一起使用”，这使得它们与 GPL 不兼容。

gcc-test 回归测试，源自 gcc-testsuite； （没有明确指定的许可，但由于它是 GCC 的一部分，可能是 GPL 许可的）

**packihx**; （公共区域）

**makebin**； (zlib/libpng 许可证)

sdcc C 编译器，最初由 Sandeep Dutta 编写； （通用公共许可证）。

一些功能包括：

广泛的 MCU 特定语言扩展，允许有效使用底层硬件。

大量标准优化，例如全局子表达式消除、循环优化（循环不变性、归纳变量强度降低和循环反转）、常量折叠和传播、复制传播、死代码消除和“switch”语句的跳转表。

MCU 特定优化，包括全局寄存器分配器。

适应性强的 MCU 特定后端，应该非常适合其他 8 位 MCU
基于独立规则的窥视孔优化器。

齐全的数据类型：char（8位，1字节），short（16位，2字节），int（16位，2字节），long（32位，4字节），long long（64位，8字节）字节）、浮点数（4 字节 IEEE）和 _Bool/bool。

在函数中的任何位置添加内联汇编代码的能力。

能够报告函数的复杂性，以帮助决定应该在汇编器中重写什么。

一个很好的自动回归测试选择。



SDCC 最初由 Sandeep Dutta 编写，并在 GPL 许可下发布。

自首次发布以来，已进行了大量错误修复和改进。

截至 1999 年 12 月，代码已移至 SourceForge，

所有“用户转变为开发人员”都可以访问同一源代码树。 

SDCC 不断根据所有用户和开发人员的输入进行更新。



2022 年 3 月 8 日：发布 SDCC 4.2.0。

SDCC 4.2.0 New Feature List:

- C23 memset_explicit
- Support for --oldralloc has been removed from the z80, z180, tlcs90, z80n, ez80_z80, r2k, r2ka, r3ka backends.
- gbz80 port now uses more efficient block-initalization of global variables (users of a custom crt0 need to adapt theirs).
- Full support for __z88dk_callee for the z80, z180, gbz80, tlcs90, z80n, ez80_z80, r2k, r2ka, r3ka, stm8 backends.
- Support for __raisonance, __iar and __cosmic calling conventions for stm8.
- Support for a new __sdcccall(1) calling convention in the stm8 port AS NEW DEFAULT.
- Support for a new __sdcccall(1) calling convention in the gbz80 port AS NEW DEFAULT.
- Support for a new __sdcccall(1) calling convention in the z80, z80n and z180 ports AS NEW DEFAULT.
- Support for a new __sdcccall(1) calling convention in the r2k, r2ka, r3k, tlcs90 and ez80_z80 ports.
- Removed support for --profile for gbz80, z80, z180, tlcs90, z80n, ez80_z80, r2k, r2ka, r3ka backends.
- The z80n port Z80N Core minimum version has been raised from 1.0 to 2.0.
- Improved rematerialization support in the stm8, gbz80, z80, z180, tlcs90, z80n, ez80_z80, r2k, r2ka, r3ka backends.
- The gbz80 port was renamed to sm83.
- New in-development mos6502 port.

# 环境搭建

原版的代码是放在source forge上。但是github有人建立了mirror。

下载代码：

```
 git clone https://github.com/darconeous/sdccsdcc
```

编译：

```
./configure
```

如果有错误提示，根据提示禁用一些配置即可。

```
make 
sudo make install
```

然后编译一下里面自带的ucsim

```
cd sim/ucsim
./configure
make 
sudo make install
```

得到的mcs51的模拟器是s51这个命令。

```
# 输入这个命令就可以进入到模拟器里
s51 
```

**MCS51** family is simulated by**s51**.
**AVR** family is simulated by **savr**.
**Z80** processor is simulated by **sz80**.

s51的文档在这里：

https://manpages.debian.org/testing/sdcc-ucsim/s51.1.en.html

ucsim的官网：

https://www.ucsim.hu/

# 开发中用到的语言的版本

## C

"SDCC uses ISO C17".

## C++

"SDCC uses the common subset of C++11 and C++23".

## Python

SDCC uses the common subset of Python 2.7 and Python 3.6.



# sdcc手册

https://sdcc.sourceforge.net/doc/sdccman.pdf

一共135页。我看的而这个版本就是2023年5月30日的版本。

所以是一直在更新的。

## 介绍

## 安装

### configure选项



## 使用

### 跟标准的兼容

iso c90和ansi c89，这个2个标准本质是一个。

```
--std-c89
--std-c95
--std-c99
--std-c11
--std-c2x

```

### 编译

#### 单文件方式

这个是最简单的情况，可以用一个文件来搞定一个项目。

会编译得到这些文件：

```
sdcc xx.c
```

```
xx.asm
	得到的汇编代码。
xx.lst
	list文件。
xx.rst
xx.sym
xx.rel
xx.map
xx.mem
xx.ihx
xx.adb
xx.cdb
xx.omf
xx.dump*
```

对hex文件的后处理：

**packihx sourcefifile.ihx >sourcefifile.hex**

###  命令行选项 

#### 处理器选择

```
-mxx
xx可以是
mcs51
ds390
s400
hc80
z80
z180

```



#### 预处理sdcpp选项

使用的选项是跟gcc的预处理一样的逻辑。

#### 优化选项

```
--nogcse
--noinvariant
--noinduction
--noloopreverse
--nolabelopt
--no-xinit-opt

```

#### 链接器选项



## 不同mcu的处理

## 调试

## tips

## 支持

## 技术参数

## compiler内部

# windows下安装使用

到这里下载最新的安装包。

https://jaist.dl.sourceforge.net/project/sdcc/sdcc-win32/4.2.0/

直接一路下一步就可以安装好。

然后怎么跟IDE进行集成呢？

```
SDCC（Small Device C Compiler）是一款针对嵌入式系统的开源C编译器。SDCC与各种集成开发环境（IDE）可以进行集成，以提供更方便的开发环境和工作流程。下面是将SDCC与IDE集成的一般步骤：

1. 安装SDCC：首先，确保你已经安装了SDCC编译器。你可以从SDCC官方网站（http://sdcc.sourceforge.net/）上下载适用于你的操作系统的最新版本。

2. 选择IDE：选择一个合适的IDE来集成SDCC。一些常见的IDE选项包括：
   - Visual Studio Code：安装C/C++扩展插件，然后在工作区中配置SDCC路径和编译器选项。
   - Eclipse：安装CDT（C/C++ Development Tools）插件，并在项目设置中配置SDCC路径和编译器选项。
   - Code::Blocks：在Code::Blocks中创建一个新的项目，并配置SDCC路径和编译器选项。

3. 配置项目：根据你选择的IDE，创建一个新项目或打开现有项目，并配置项目的构建设置。这通常包括设置SDCC的路径、编译器选项、链接器选项以及其他相关设置。

4. 创建源文件：在IDE中创建或导入你的C源代码文件。

5. 编译和构建：通过IDE的构建命令或按钮来执行编译和构建操作。IDE将使用SDCC编译器来编译你的源代码，并生成目标文件。

6. 调试和部署：一些IDE还提供调试功能，使你能够在嵌入式系统上调试代码。使用IDE提供的调试器来设置断点、单步执行和观察变量等操作。然后，使用合适的工具将生成的目标文件烧录到目标设备上。

以上步骤提供了一般性的指导，具体的步骤和设置可能因你选择的IDE和项目要求而有所不同。建议参考所使用IDE的文档和指南，以获取更详细的集成步骤和配置说明。
```

我还是选择codeblocks，毕竟这个是c++写的，而且是开源的。

虽然界面不怎么样，但是稳定可靠。

eclipse就算了。

vscode也不想集成太多功能了。

从官网下载codeblocks。打开就显示检测到sdcc了。我选择这个工具链，并且设置为默认的工具链。

在codeblocks里的编译输出：

```
sdcc.exe -mmcs51 --model-small  --debug    -I"d:\Program Files (x86)\SDCC\include" -Id:\sdcc\include -c main.c -o obj\Debug\main.rel
sdcc.exe -L"d:\Program Files (x86)\SDCC\lib" -Ld:\sdcc\lib -o bin\Debug\sdcc-c51.ihx -mmcs51 --model-small  --debug    --xram-size 4096 --iram-size 256 --code-size 65536 --out-fmt-ihx   obj\Debug\main.rel
Output file is bin\Debug\sdcc-c51.ihx with size 619.00 bytes
Running project post-build steps
cmd /c "packihx <bin\Debug\sdcc-c51.ihx >bin\Debug\sdcc-c51.hex"
packihx: read 15 lines, wrote 20: OK.
Process terminated with status 0 (0 minute(s), 1 second(s))
0 error(s), 0 warning(s) (0 minute(s), 1 second(s))

```

sdcc的安装路径不要有中文和空格，以免出现一些乱七八糟的问题。



https://bbs.21ic.com/icview-2885716-1-1.html

## 配合sdcdb进行调试

默认是gdb。而且没有办法在gui界面上修改。

参考下面这个链接，可以找到方法。

https://stackoverflow.com/questions/48015405/codeblocks-how-to-specify-ssdc-debugger-for-pic-micro-controllers

找到D:\Program Files\CodeBlocks\share\CodeBlocks\compilers\options_sdcc.xml

修改里面的DBGconfig字段的值为sdcdb.exe。

但是好像还是不行。

## 在vscode搭建环境

这个视频讲得非常好。

https://www.bilibili.com/video/BV1464y1e7iw

# 直接proteus里使用sdcc

现在的proteus集成的东西越来越多。

直接都可以随便把代码工程创建，支持的编译器里就有sdcc。

画一个跑马灯的图。然后用这个的程序来跑一下。

可以正常运行。

https://bbs.21ic.com/icview-2885716-1-1.html

# 参考资料

1、官网

https://sdcc.sourceforge.net/

2、官方wiki

https://sourceforge.net/p/sdcc/wiki/Home/