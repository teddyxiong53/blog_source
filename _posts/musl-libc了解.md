---
title: musl libc了解
date: 2018-01-26 18:04:20
tags:
	- musl
	- libc

---



# musl简介

1、读音就跟muscle（肌肉）单词同音。

2、采用MIT协议开源。

3、可以应用到小型嵌入式设备和大型服务器。

4、需要linux2.6以后的版本。

5、所有东西都打包到一个库，就叫libc。分a和so 2个文件。所以libm就变成空的了。是否链接都没有关系。但是有个空的，可以避免其他程序链接时报错。

6、这个c库是专门针对linux系统的。

7、完全重新设计，以达到可以更有效地static link和更好的实时性。

8、符合posix 2008和C11标准。另外增加了linux系统的相关非标准c函数的实现。

9、目前alpine、OpenWRT等系统使用了这个库。

10、和uclibc、glibc比较。效率比不上glibc。但是尺寸最小，比uclibc要好。

https://www.etalabs.net/compare_libcs.html 这里有详细数据。

11、第一个版本发布于2011年1月11日。

12、作者是Rich Felker。github上关注的人不多，才20人。





# 参考手册

https://musl.libc.org/doc/1.1.24/manual.html

```mermaid
graph LR
    A[musl libc] --> B[标准合规性]
    A --> C[构建系统]
    A --> D[支持架构]
    A --> E[动态链接]
    A --> F[特性与优势]

    B --> B1[ISO C11]
    B --> B2[POSIX 2008]
    B --> B3[依赖内核: Linux 2.6.39+]
    B --> B4[依赖编译器: C99]

    C --> C1[./configure]
    C --> C2[GNU Make 3.81+]
    C --> C3[POSIX Shell]
    C --> C4[编译器: GCC/Clang]
    C --> C5[支持 -fPIC]

    D --> D1[x86/x86_64]
    D --> D2[ARM/AArch64]
    D --> D3[MIPS/PowerPC]
    D --> D4[RISC-V/Microblaze]
    D --> D5[实验性架构]

    E --> E1[ld-musl-xx.so.1]
    E --> E2[单共享库]
    E --> E3[路径配置]

    F --> F1[静态链接]
    F --> F2[动态链接优化]
    F --> F3[线程鲁棒性]
    F --> F4[低内存占用]
    F --> F5[MIT 许可证]
```

# open-std网站内容

```mermaid
graph LR
    A[open-std.org 标准文件] --> B[C 语言标准]
    A --> C[C++ 语言标准]
    A --> D[技术报告与规范]
    A --> E[工作组内部文档]
    A --> F[其他相关文档]

    B --> B1[C23 ISO/IEC 9899:2024]
    B --> B2[历史版本: C99, C11]
    B --> B3[技术规范: N3389, N3231]
    B --> B4[澄清请求: N2397]

    C --> C1[ISO/IEC 14882: 1998-2020]
    C --> C2[草案与提案]
    C --> C3[邮件列表: 2024-01 至 2024-12]
    C --> C4[库扩展: ISO/IEC TR 19768:2007]

    D --> D1[十进制浮点运算: ISO/IEC TR 24733:2011]
    D --> D2[数学特殊函数: ISO/IEC 29124:2010]
    D --> D3[安全提案: memset_explicit N2485]

    E --> E1[会议记录]
    E --> E2[问题列表: 核心/库]
    E --> E3[提案文档]
    E --> E4[成员专属文档]

    F --> F1[信息技术词汇: ISO/IEC 2382:2015]
    F --> F2[Ada Ravenscar Profile 指南]
    F --> F3[历史技术报告: C++ 性能]
```

# ubuntu下安装使用musl

```
sudo apt-get install musl musl-dev musl-tools
```

```
ls /usr/lib/x86_64-linux-musl/ -lh
total 2.3M
-rw-r--r-- 1 root root 1.2K 5月  19  2015 crt1.o
-rw-r--r-- 1 root root 1016 5月  19  2015 crti.o
-rw-r--r-- 1 root root  960 5月  19  2015 crtn.o
-rw-r--r-- 1 root root 2.3M 5月  19  2015 libc.a
-rw-r--r-- 1 root root    8 5月  19  2015 libcrypt.a
lrwxrwxrwx 1 root root   30 5月  19  2015 libc.so -> /lib/x86_64-linux-musl/libc.so
-rw-r--r-- 1 root root    8 5月  19  2015 libdl.a
-rw-r--r-- 1 root root    8 5月  19  2015 libm.a
-rw-r--r-- 1 root root    8 5月  19  2015 libpthread.a
-rw-r--r-- 1 root root    8 5月  19  2015 libresolv.a
-rw-r--r-- 1 root root    8 5月  19  2015 librt.a
-rw-r--r-- 1 root root    8 5月  19  2015 libutil.a
-rw-r--r-- 1 root root    8 5月  19  2015 libxnet.a
-rw-r--r-- 1 root root  724 5月  19  2015 musl-gcc.specs
-rw-r--r-- 1 root root 1.2K 5月  19  2015 Scrt1.o
```

检查：

```
musl-gcc --version
```

测试编译：hello.c 

```
#include <stdio.h>
int main() {
    printf("Hello, musl!\n");
    return 0;
}
```

编译：

```
musl-gcc -static -Os hello.c -o hello
./hello
```

查看ldd

```
musl-ldd ./hello
musl-ldd: ./hello: Not a valid dynamic program
~/work/tmp/0427$ ldd ./hello
        not a dynamic executable
```

hello大小只有9.3K。

这个是静态链接的。

要配置动态链接的，需要做这些：

```
sudo mkdir -p /etc/ld-musl-x86_64.d
echo "/usr/local/musl/lib" | sudo tee /etc/ld-musl-x86_64.path
```

然后编译：

```
musl-gcc -no-pie hello.c -o hello
```

-no-pie 是需要的，不然会报错。

```
musl-ldd ./hello
        /lib/ld-musl-x86_64.so.1 (0x7f00673bd000)
        libc.so => /lib/ld-musl-x86_64.so.1 (0x7f00673bd000)
```

```mermaid
graph TD
    A[musl-gcc 编译错误] --> B{错误原因}
    B --> C[PIE 与 crt1.o/crtbegin.o 不兼容]
    B --> D[musl-gcc 配置问题]
    B --> E[工具链混合]
    C --> F{解决方案}
    F --> G[方法 1: 静态链接<br>musl-gcc -static]
    F --> H[方法 2: 禁用 PIE<br>musl-gcc -no-pie]
    F --> I[方法 3: 重新编译 musl<br>CFLAGS=-fPIC]
    F --> J[方法 4: 使用 musl 交叉工具链<br>x86_64-linux-musl-gcc]
    F --> K[方法 5: 检查 musl 安装]
    G --> L[生成静态二进制]
    H --> M[生成动态二进制]
    I --> M
    J --> L
    J --> M
    K --> F
    L --> N[验证: file, ./hello]
    M --> N
```

# 版本历史



| **版本**   | **发布日期**                 | **主要功能与新特性**                                         | **主要修复**                                                 | **备注**                                      |
| ---------- | ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------------------------------- |
| **1.2.5**  | 2023-05-02                   | - 添加 qsort_r（POSIX 未来标准）。<br>- 支持 PowerPC 的 SPE FPU。<br>- 动态链接器支持 RELR 格式的紧凑相对重定位（需 musl 1.2.4+ 运行时）。 | - 修复宽字符 printf 系列函数的多个错误。<br>- 修复 strverscmp 中数字与非数字排序错误。<br>- 修复线程同步逻辑中的罕见竞争条件（线程退出、多线程 fork、pthread_detach、POSIX 信号量）。 | 最新版本，推荐使用以获取最新修复。            |
| **1.2.4**  | 未明确日期（推测 2022-2023） | - 引入 mallocng 分配器，替换原有 dlmalloc：<br> - 更细粒度释放内存。<br> - 避免灾难性碎片化。<br> - 增强错误检测（溢出、双重释放、释放后使用）。<br>- res_* API 报告 DNSSEC 状态（支持 DANE）。<br>- AArch64 优化的 memcpy 和 memset。 | - 修复多线程进程返回单线程状态后的锁跳跃错误。<br>- 修复 32 位架构的 time64 回归问题。 | 强调内存分配改进，适合高可靠性场景。          |
| **1.2.0**  | 未明确日期（推测 2020-2021） | - 所有 32 位架构升级到 64 位 time_t，解决 2038 年问题（不影响 64 位系统）。<br>- 更新字符数据到 Unicode 12.1.0。<br>- 添加 GLOB_TILDE 扩展（glob）。<br>- 实现非存根的 catgets 本地化 API。<br>- posix_spawn 支持子进程 chdir。 | - 改进数学库的正确性（复杂函数、32 位 x86 汇编）。<br>- 修复特定架构的 bug。 | 32 位用户需阅读 time64 发布说明以确保兼容性。 |
| **1.1.15** | 未明确日期（推测 2016-2017） | - 添加新 64 位 MIPS 和 PowerPC 端口。<br>- 支持 32 位 PowerPC 软浮点 ABI。<br>- 支持 MIPS ISA 第 6 版（不兼容旧 MIPS）。<br>- 添加 pthread_tryjoin_np、pthread_timedjoin_np 和 sched_getcpu 扩展函数。<br>- 支持 Linux 4.5 和 4.6 新功能。 | - 修复 memmem、ungetwc 和 putenv 的严重错误。<br>- 修复 PowerPC 线程局部存储问题（依赖编译器）。 | 修复了 1.1.13 的回归问题。                    |
| **1.1.13** | 未明确日期（推测 2015-2016） | - 引入新的 C 本地化（符合未来 POSIX 要求），支持非 UTF-8 数据处理。<br>- 支持首个 NOMMU 目标 SH-2，为未来 NOMMU 目标奠定基础。<br>- 提供 musl-clang 包装器，复用非 musl 目标的 clang。<br>- 动态链接器性能增强。<br>- ARM 系统使用 vdso 加速 clock_gettime。<br>- i386 调试器回溯改进（自动生成调用框架信息）。 | - 修复 fputs 和 puts 在零长度字符串上的失败。<br>- 修复 ARM 硬浮点在 clang 上的编译失败。<br>- 修复 SH/FDPIC 动态链接器入口点挂起。<br>- 修复 make clean/make distclean 在未配置树中的问题。 | 主要修复回归问题，增强调试和性能。            |
| **1.1.0**  | 未明确日期（推测 2014-2015） | - 完成 ISO C99 和 POSIX 2008 基本接口覆盖。<br>- 添加 Linux、BSD 和 glibc 兼容的非标准接口。 | - 未详细列出，但专注于标准符合性和兼容性。                   | 1.1 系列的起点，奠定现代 musl 基础。          |
| **1.0.0**  | 未明确日期（推测 2013-2014） | - 提供完整的 ISO C99 和 POSIX 2008 基本接口支持。<br>- 支持静态链接，生成小巧二进制文件（最小可低于 10kB）。 | - 未详细列出，重点是稳定性和标准实现。                       | 首个稳定主版本，强调轻量和高效。              |
| **0.9.0**  | 2012-05-06                   | - 早期版本，奠定 musl 基础。<br>- 支持基本 C 标准库功能。    | - 修复早期实现中的基本问题。                                 | 早期开发阶段，功能有限。                      |
| **0.5.0**  | 2011-02-12                   | - 首个公开版本，初步实现标准 C 库功能。<br>- MIT 许可证发布。 | - 初始实现，未列出具体修复。                                 | 项目起点，面向嵌入式和轻量系统。              |



# 代码简单分析

整个压缩包1.5M左右。src目录下，大概1500个文件。

先从顶层Makefile开始看。

这个文件大概200行。

1、默认目标是all。依赖ALL_LIBS和ALL_TOOLS。

2、

```
ALL_LIBS 包括：
1、CRT_LIBS
	lib/crt1.o
	lib/Scrt1.o
	lib/crti.o
	lib/crtn.o
2、STATIC_LIBS。lib/libc.a
3、SHARED_LIBS。lib/libso.a
4、EMPTY_LIBS。m、rt、pthread、crypt、util、xnet、resolv、dl这几个。
5、TOOLS_LIBBS。lib/musl-gcc.specs
```

```
ALL_TOOLS：tools/musl-gcc
```

# 先编译一下

我在alpine里进行编译。这个系统就是用的musl的。

下面的操作用普通用户身份来进行，避免不小心覆盖到系统的东西。

1、配置。

```
vm-alpine-0:~/work/musl-master$ ./configure 
checking for C compiler... gcc
checking whether C compiler works... yes
checking whether compiler is gcc... yes
checking whether to build musl-gcc wrapper... no
checking target system type... i586-alpine-linux-musl
checking whether compiler accepts -std=c99... yes
checking whether compiler accepts -nostdinc... yes
checking whether compiler accepts -ffreestanding... yes
checking whether compiler accepts -fexcess-precision=standard... yes
checking whether compiler accepts -frounding-math... yes
checking whether compiler needs attribute((may_alias)) suppression... no
checking whether compiler accepts -fno-stack-protector... yes
checking whether compiler accepts -fno-tree-loop-distribute-patterns... yes
checking for optimization settings... using defaults
checking whether compiler accepts -Os... yes
components to be optimized for speed: internal malloc string
checking whether compiler accepts -pipe... yes
checking whether compiler accepts -fomit-frame-pointer... yes
checking whether compiler accepts -fno-unwind-tables... yes
checking whether compiler accepts -fno-asynchronous-unwind-tables... yes
checking whether compiler accepts -Wa,--noexecstack... yes
checking whether linker accepts -march=i486... yes
checking whether linker accepts -mtune=generic... yes
checking whether compiler accepts -Werror=implicit-function-declaration... yes
checking whether compiler accepts -Werror=implicit-int... yes
checking whether compiler accepts -Werror=pointer-sign... yes
checking whether compiler accepts -Werror=pointer-arith... yes
checking whether global visibility preinclude works... yes
checking whether linker accepts -Wl,--hash-style=both... yes
checking whether linker accepts -Wl,-Bsymbolic-functions... yes
checking whether linker accepts -lgcc... yes
checking whether linker accepts -lgcc_eh... yes
using compiler runtime libraries: -lgcc -lgcc_eh
checking whether compiler's long double definition matches float.h... yes
creating config.mak... done
```

2、编译。1分钟就完成了。

```
make -j256
```

看生成的库文件：

```
vm-alpine-0:~/work/musl-master/lib$ ls -lh
total 2396
-rw-r--r--    1 teddy    teddy        816 Jan 28 15:30 Scrt1.o
-rw-r--r--    1 teddy    teddy        744 Jan 28 15:30 crt1.o
-rw-r--r--    1 teddy    teddy        692 Jan 28 15:30 crti.o
-rw-r--r--    1 teddy    teddy        648 Jan 28 15:30 crtn.o
-rw-r--r--    1 teddy    teddy          0 Jan 28 15:28 empty
-rw-r--r--    1 teddy    teddy       1.7M Jan 28 15:31 libc.a
-rwxr-xr-x    1 teddy    teddy     621.8K Jan 28 15:31 libc.so
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libcrypt.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libdl.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libm.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libpthread.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libresolv.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 librt.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libutil.a
-rw-r--r--    1 teddy    teddy          8 Jan 28 15:31 libxnet.a
```

看这些8个字节的空库里是什么内容。就是一个“!<arch>.”字符串。都是这样的。

```
vm-alpine-0:~/work/musl-master/lib$ hexdump  -C  libm.a
00000000  21 3c 61 72 63 68 3e 0a                           |!<arch>.|
00000008
```

编译过程中生成的o文件，就跟c文件放在一起。所以这是采取最简单的做法。

3、安装看看。

```
vm-alpine-0:~/work/musl-master$ make install
./tools/install.sh -D -m 644 lib/crt1.o /usr/local/musl/lib/crt1.o
mkdir: can't create directory '/usr/local/musl/': Permission denied
make: *** [Makefile:166: /usr/local/musl/lib/crt1.o] Error 1
```

install包括3部分：libs、headers、tools。

可以看到目标目录是：/usr/local/musl。这个是为了避免跟系统原来的冲突。我就不安装了。

# 看C代码

我们先看一个简单的stdio.h文件。

看看跟glibc的区别是怎样的。我另外打开一个树莓派。查看/usr/include/stdio.h。

glibc：

1、近1000行代码。

2、各种宏。情况处理复杂。注释详尽。

musl： 

1、200行代码。

2、几乎没有注释，代码结构简单。看起来很清晰。

看src/stdlib目录下的内容。都实现得很简单。

几乎是一个函数一个文件。很多文件都只有几行代码。

```
vm-alpine-0:~/work/musl-master/src/stdlib$ ls -lh *.c
-rw-r--r--    1 teddy    teddy         41 Jan 28 15:28 abs.c
-rw-r--r--    1 teddy    teddy         74 Jan 28 15:28 atof.c
-rw-r--r--    1 teddy    teddy        300 Jan 28 15:28 atoi.c
-rw-r--r--    1 teddy    teddy        308 Jan 28 15:28 atol.c
-rw-r--r--    1 teddy    teddy        320 Jan 28 15:28 atoll.c
-rw-r--r--    1 teddy    teddy        393 Jan 28 15:28 bsearch.c
-rw-r--r--    1 teddy    teddy         90 Jan 28 15:28 div.c
-rw-r--r--    1 teddy    teddy        358 Jan 28 15:28 ecvt.c
-rw-r--r--    1 teddy    teddy        454 Jan 28 15:28 fcvt.c
-rw-r--r--    1 teddy    teddy        139 Jan 28 15:28 gcvt.c
-rw-r--r--    1 teddy    teddy         78 Jan 28 15:28 imaxabs.c
-rw-r--r--    1 teddy    teddy        114 Jan 28 15:28 imaxdiv.c
-rw-r--r--    1 teddy    teddy         44 Jan 28 15:28 labs.c
-rw-r--r--    1 teddy    teddy         95 Jan 28 15:28 ldiv.c
-rw-r--r--    1 teddy    teddy         55 Jan 28 15:28 llabs.c
-rw-r--r--    1 teddy    teddy        108 Jan 28 15:28 lldiv.c
-rw-r--r--    1 teddy    teddy       4.7K Jan 28 15:28 qsort.c
-rw-r--r--    1 teddy    teddy        857 Jan 28 15:28 strtod.c
-rw-r--r--    1 teddy    teddy       1.5K Jan 28 15:28 strtol.c
-rw-r--r--    1 teddy    teddy       1.3K Jan 28 15:28 wcstod.c
-rw-r--r--    1 teddy    teddy       1.8K Jan 28 15:28 wcstol.c
```

所以文件虽然多。1500个文件，就是对应了1500个函数。

# 分析crt的文件

这个是链接生成C可执行文件的一些基础o文件。

主要就是crt1.c文件。

内容就这样：

```
#include <features.h>
#include "libc.h"

#define START "_start"

#include "crt_arch.h"

int main();
weak void _init();
weak void _fini();
int __libc_start_main(int (*)(), int, char **,
	void (*)(), void(*)(), void(*)());

void _start_c(long *p)
{
	int argc = p[0];
	char **argv = (void *)(p+1);
	__libc_start_main(main, argc, argv, _init, _fini, 0);
}
```

先看features.h里的内容。

这些source到底表示什么含义？

```
_ALL_SOURCE
_GNU_SOURCE
_DEFAULT_SOURCE 
_BSD_SOURCE
_POSIX_SOURCE
_POSIX_C_SOURCE
_XOPEN_SOURCE
```

就是表示你希望编译出来的libc支持哪些特性。

例如支持所有的特性。

支持gnu的特性。

支持bsd的特性。

支持posix的特性。

支持xopen的特性。



# get started

## 使用musl-gcc的wrapper

这个是为了很方便地在基于glibc的系统上测试musl的库。

但是只能用在C语言上。不能用在C++上。

在configure musl的时候，有3个重要的标志可以传递。

这个configure脚本，只是一个普通的脚本，目的就是生成一个config.mak文件。

```
--prefix=xx
	这个是配置musl的安装位置，建议放在~/musl这样的目录。
--exec-prefix=xx
	musl-gcc wrapper的安装位置。
	建议放在~/bin目录。
--syslibdir=xx
	动态linker的安装位置，默认是/lib。
	建议放在~/musl/lib目录。
```

confiugre之后，会生成一个config.mak文件。

然后make && make install就可以。

然后编译你的测试文件，用musl-gcc，而不是gcc。

```
CC="musl-gcc -static" ./configure --prefix=$HOME/musl && make
```

## 使用musl库编译交叉编译器

# musl-gcc原理

### musl-gcc 包装脚本的作用和原理

#### 作用
`musl-gcc` 是一个围绕 `gcc`（GNU 编译器集合）的包装脚本，其主要作用是方便使用 musl libc（一个轻量级 C 标准库）替代默认的 C 标准库（如 glibc）进行编译。具体作用包括：

1. **重定向库和头文件路径**：
   - `musl-gcc` 修改 `gcc` 的默认头文件和库搜索路径，使其指向 musl 的头文件（通常在 `/usr/local/musl/include`）和库文件（通常在 `/usr/local/musl/lib`），而不是系统默认的 glibc 路径。
   - 这允许开发者在不更改现有工具链的情况下，使用 musl libc 编译程序。

2. **简化 musl 的集成**：
   - 对于需要在 musl 环境中编译程序的开发者，`musl-gcc` 提供了一种便捷的方式，无需构建完整的 musl 专用交叉编译工具链。
   - 它特别适合在 glibc 主机系统上快速编译针对 musl 的程序，或在 musl 系统中重用现有 `gcc` 工具链。

3. **支持静态链接**：
   - `musl-gcc` 常用于生成完全静态链接的可执行文件（通过 `-static` 标志），生成单一、可移植的二进制文件，无需外部动态库依赖。
   - 例如，编译一个简单的 C 程序：
     ```bash
     musl-gcc -static -Os hello.c
     ```
     会生成一个静态链接的二进制文件，体积小巧（如 10kB 级别）。[](https://www.musl-libc.org/how.html)

4. **引导 musl 系统**：
   - `musl-gcc` 可用于构建新的 musl 环境（如 musl 发行版或小型嵌入式系统），通过在主机系统上编译 musl 链接的程序来引导目标系统。[](https://www.musl-libc.org/how.html)

5. **兼容性**：
   - 它允许在现有 glibc 主机系统上编译 musl 程序，无需替换系统全局的 C 库，适合开发者和嵌入式系统构建。

#### 原理
`musl-gcc` 的工作原理基于以下机制：

1. **包装脚本本质**：
   - `musl-gcc` 是一个 shell 脚本，调用底层的 `gcc` 编译器，并通过特定的命令行参数或配置文件修改其行为。
   - 它通过设置环境变量或传递参数（如 `-specs`）来覆盖 `gcc` 的默认配置。

2. **使用 specs 文件**：
   - `musl-gcc` 依赖一个特定的 specs 文件（通常位于 `/usr/lib/$ARCH-linux-musl/musl-gcc.specs`），该文件定义了 musl 的头文件和库路径。
   - 脚本通过 `-specs` 参数将此文件传递给 `gcc`，覆盖默认的 include 和 library 路径。例如：
     ```bash
     gcc -specs=/usr/lib/$ARCH-linux-musl/musl-gcc.specs "$@"
     ```
     这里的 `$@` 表示传递给 `musl-gcc` 的所有命令行参数。[](https://manpages.ubuntu.com/manpages/focal/man1/musl-gcc.1.html)[](https://manpages.ubuntu.com/manpages/jammy/man1/musl-gcc.1.html)

3. **环境变量支持**：
   - `musl-gcc` 支持通过环境变量 `REALGCC` 指定实际的 `gcc` 编译器路径，允许用户自定义底层编译器（默认为 `gcc`）。
   - 例如：
     ```bash
     export REALGCC=/usr/bin/gcc-9
     musl-gcc -static hello.c
     ```
     这会使用指定的 `gcc-9` 而不是默认的 `gcc`。[](https://www.musl-libc.org/faq.html)

4. **动态链接器配置**：
   - 对于动态链接的程序，`musl-gcc` 确保二进制文件使用 musl 的动态链接器（通常为 `/lib/ld-musl-$ARCH.so.1`）。
   - 动态链接需要配置库搜索路径（如 `/etc/ld-musl-$ARCH.path`），`musl-gcc` 通过 specs 文件自动设置正确的链接器路径。[](https://github.com/quic/musl/blob/master/INSTALL)

5. **C++ 支持的局限性**：
   - 默认情况下，`musl-gcc` 主要支持 C 程序，因为 musl 的标准安装不包含 C++ 标准库（如 libstdc++）的头文件和库。
   - 若需 C++ 支持，需额外构建 musl 专用的交叉编译工具链（如通过 musl-cross-make），以包含 libstdc++ 或 libc++。[](https://stackoverflow.com/questions/64230710/how-does-musls-gcc-wrapper-differ-from-musls-cross-compiler)[](https://www.musl-libc.org/faq.html)

6. **构建与安装**：
   - 在 musl 的构建过程中，`musl-gcc` 脚本由 `make install` 自动生成并安装到指定路径（默认 `/usr/local/bin`）。
   - 脚本内容由 `tools/musl-gcc.specs.sh` 生成，包含 musl 的安装路径（如 `includedir` 和 `libdir`）。[](https://www.openwall.com/lists/musl/2015/06/28/12)

#### 示例
以下是一个典型的 `musl-gcc` 脚本内容（简化版）：
```bash
#!/bin/sh
exec "${REALGCC:-gcc}" "$@" -specs "/usr/lib/$ARCH-linux-musl/musl-gcc.specs"
```
- 脚本调用 `gcc`，并附加 `-specs` 参数指向 musl 的 specs 文件。
- `$@` 确保所有用户提供的参数（如 `-static`、`-Os`）传递给 `gcc`。

#### 与交叉编译工具链的区别
- **musl-gcc 包装器**：
  - 依赖主机系统的 `gcc`，仅修改库和头文件路径。
  - 适合快速开发或简单项目，但对复杂项目（如需要 C++ 或多架构支持）可能不足。
  - 不支持完整的 musl 目标架构配置（如特定的 ABI 或指令集优化）。[](https://stackoverflow.com/questions/64230710/how-does-musls-gcc-wrapper-differ-from-musls-cross-compiler)
- **musl 交叉编译器**（如 `x86_64-linux-musl-gcc`）：
  - 专为 musl 构建的完整工具链，包含针对特定架构的编译器、链接器和库。
  - 支持 C++、多架构，且路径配置更独立，适合大型项目或嵌入式系统。[](https://www.openwall.com/lists/musl/2019/06/18/2)[](https://stackoverflow.com/questions/64230710/how-does-musls-gcc-wrapper-differ-from-musls-cross-compiler)

#### 局限性
1. **C++ 支持**：
   - 默认不支持 C++，需额外配置或使用交叉编译器。[](https://stackoverflow.com/questions/64230710/how-does-musls-gcc-wrapper-differ-from-musls-cross-compiler)[](https://www.openwall.com/lists/musl/2019/06/18/10)
2. **复杂依赖**：
   - 对于依赖 glibc 特定功能的库，`musl-gcc` 可能需要额外的 ABI 兼容层（如 gcompat）。[](https://en.wikipedia.org/wiki/Musl)
3. **主机依赖**：
   - 依赖主机系统的 `gcc`，可能因版本或配置差异导致兼容性问题。[](https://www.openwall.com/lists/musl/2011/09/21/4)
4. **动态链接配置**：
   - 动态链接需要手动配置库路径文件，增加了部署复杂性。[](https://github.com/quic/musl/blob/master/INSTALL)

#### Mermaid 示意图
以下是 `musl-gcc` 包装脚本的工作流程示意图：

```mermaid
graph TD
    A[用户调用 musl-gcc] --> B[Shell 脚本]
    B -->|读取 REALGCC 环境变量| C[调用底层 gcc]
    B -->|加载 specs 文件| D[musl-gcc.specs]
    D --> E[设置 musl 头文件路径: /usr/local/musl/include]
    D --> F[设置 musl 库路径: /usr/local/musl/lib]
    D --> G[设置动态链接器: /lib/ld-musl-$ARCH.so.1]
    C -->|传递用户参数| H[编译 C 程序]
    H --> I[生成可执行文件]
    I -->|静态链接| J[单一二进制文件]
    I -->|动态链接| K[依赖 musl 动态链接器]
```

#### 示意图说明
- **用户调用**：用户运行 `musl-gcc` 命令，传入参数（如 `-static`）。
- **脚本处理**：脚本读取 `REALGCC` 或默认使用 `gcc`，加载 musl 的 specs 文件。
- **路径配置**：specs 文件重定向头文件、库文件和动态链接器路径。
- **编译输出**：根据参数生成静态或动态链接的可执行文件。

#### 结论
`musl-gcc` 是一个轻量、便捷的工具，允许开发者在 glibc 主机系统上快速使用 musl libc 编译 C 程序。其核心原理是通过 specs 文件修改 `gcc` 的路径配置，支持静态链接和 musl 的动态链接器。虽然适合简单项目和系统引导，但对于需要 C++ 或复杂依赖的项目，推荐使用 musl 专用的交叉编译工具链。

如果需要更详细的配置示例或特定场景的分析，请告知！

# libc.h

```
struct __libc {
	int can_do_threads;
	int threaded;
	int secure;
	volatile int threads_minus_1;
	size_t *auxv;
	struct tls_module *tls_head;
	size_t tls_size, tls_align, tls_cnt;
	size_t page_size;
	struct __locale_struct global_locale;
};
```

```
hidden void __init_libc(char **, char *);
hidden void __init_tls(size_t *);
hidden void __init_ssp(void *);
hidden void __libc_start_init(void);
hidden void __funcs_on_exit(void);
hidden void __funcs_on_quick_exit(void);
hidden void __libc_exit_fini(void);
hidden void __fork_handler(int);
```

`src\env\__libc_start_main.c`

# musl和glibc比较

开源的libc的历史很长，这里就不说了。

大约在20余年前，有人对当时的libc5的架构不满意，

在此基础上翻新设计了架构更好、可移植更好、性能更好、不依赖特定OS的libc6。

libc6后来被GNU项目接受，被称为glibc。

不过debian发行版还是喜欢其原来的名字libc6做包名。

==而libc5如今还是广泛用于BSD等系统中。==



性能上musl比glibc差多少呢？

恐怕不会有人给你确切答案。

从感觉上说，glibc应该比musl快一些，

毕竟经过20多年的持续优化，不是其它项目一朝一夕能追上的。

但是要说快多少，恐怕也不会很明显，不会有压倒性优势。

==libc的代码相比其它上层复杂项目，==

==比如浏览器或图形系统，还是相对简单的，层次少，也不需要复杂的架构。==

已知的热点，比如memory相关模块，都是需要汇编优化，这点musl有差距，

毕竟没有公司持续投钱，用爱发电，开发效率还是低。

相比android/bionic，有公司持续投入，很快就追上来。

至于对于系统调用的封装，就这么点层次，谁也不会比谁快到哪里去。



musl相比glibc，最大的问题就是兼容性问题了。

musl号称严格遵循各种国际标准进行开发。

glibc从来就不这么宣扬自己，因为GNU自成一派。

于是在二十多年的发展中，glibc添加了很多自有的独特的特性，

相类似的，gcc也是如此，

==然后无数的开源应用软件有意无意的也使用了这些特性，==

==也就是说开源软件大多无意识地绑定了gcc/glibc，==

反正二十多年来大家都这么用，也用得挺好的。

后来者，如llvm/clang，就得为此添加不少gcc的特性，

linux也绑定不少gcc特性，

clang和linux两者要做不少修改才能编译通过。

musl同样也是有这个问题，看[https://alpinelinux.org/](https://link.zhihu.com/?target=https%3A//alpinelinux.org/)里面的软件包里的补丁，

就知道要维护一个完全符合国际标准的应用软件需要做哪些修改了。







https://www.zhihu.com/question/550951106/answer/2653996968

# 鸿蒙支持musl



https://zhuanlan.zhihu.com/p/461208555

# musl的堆利用技巧

最近比赛出的musl题型的越来越多，

不得不学习一波musl的堆利用来应对今后的比赛。

这里要讲的是musl1.22版本的利用，

因为网上可以找到很多审计源码的文章，

所以这篇文章是通过一道题目来debug去学习堆的利用技巧，

这里用到的是2021第五空间线上赛的notegame题目。



https://zhuanlan.zhihu.com/p/468332990

# musl堆代码分析

https://zhuanlan.zhihu.com/p/583188846

# lib(m|pthread|crypt).a/so 为空？

是的，这是设计使然。 musl 将所有内容放入 libc.a/so 以避免内存膨胀。

空文件只是出于兼容性原因而存在。

官方解释：http://openwall.com/lists/musl/2012/07/25/3 

## 性能：

加载1个共享库比加载3个以上共享库要快。

现代多线程程序可能至少使用 libc、libm、libpthread 和 librt。



## 节省内存：

每个额外的共享库都会浪费至少一页提交费用和脏物理内存，

尽管它可能只是用于 GOT，

但 libc 除外，因为 libc 需要一些全局数据。

从技术上讲，libm 可能能够完全不需要 GOT，但我怀疑链接器是否会创建一个无 GOT 的库，即使它在技术上可以。

## 避免暴露实现内部和版本不兼容：

如果 libc/libm/libpthread/etc.是单独的库，

它们需要对实现内部函数和数据的跨库引用。

如果它们之间存在版本不匹配，这反过来可能会导致严重损坏，

更糟糕的是，

如果静态版本的 libm 或 libpthread 与动态 libc 一起使用，

则二进制文件现在将永久挂钩到特定版本的 libc，

因为使用特定于该版本的临时内部接口。

如果您使用静态链接，这些问题都不适用，

但我也选择不拆分静态库文件的原因与上面第 3 点的末尾相同：

如果 libpthread.a 包含 pthread 函数的静态版本，

它可能会使用动态 libc.so 链接到程序中，并引入上述版本锁定。

为了避免这种情况，我们必须确保名为 libpthread.so 的文件作为无操作链接描述文件存在（如果它作为空 ELF 共享库文件存在，它可能会被添加到程序的 DT_NEEDED 中，然后点 1 和上述 2 条适用）。

由于将标准库分离为分解的 .a 文件没有任何好处，并且存在许多潜在的陷阱，因此我选择也不将其分离以进行静态链接。

至于为什么存在空的 .a 文件，这是因为 POSIX 要求 -lm、-lpthread 等是 C 编译器的有效选项，并且要求可移植程序在其构建脚本中使用这些选项，即使实现不需要他们。制作空的 .a 文件是满足该要求的最简单方法。

# musl的ldd在哪里

musl 的动态链接器内置了 ldd 功能。

只需创建一个从 ld-musl-$ARCH.so 到 /bin/ldd 的符号链接。

如果动态链接器以“ldd”启动，它将检测到并打印适当的 DSO 信息。

# `ldconfig` 在哪里？

没有。

您可以通过创建或编辑文件 `/etc/ld-musl-$ARCH.path` 来指定库搜索路径，

其中 `$ARCH` 是标识您的架构的字符串（如果不确定，请查看 `/lib/ld-musl-*.so.1` 使用的内容） 。

路径可以用换行符或冒号分隔。

**对于一次性情况，还支持环境变量 `LD_PRELOAD` 和 `LD_LIBRARY_PATH` 。**

# 为什么不包含 `sys/queue.h` ？

sys/queue.h 是一个在头文件中实现的完整库，

它没有理由成为 libc 的一部分；

该文件是完全独立的。 

musl 的目标是

不在公共头文件中包含代码/重要的、受版权保护的内容（即不是直接接口定义的重要内容）

# 为什么不包含 `fts.h` ？

fts 不可能匹配 glibc ABI，

因为 glibc ABI 已被破坏得无法使用。

这也意味着无法使用 glibc 的内置 fts 构建任何可用的软件；

任何使用 fts 的东西要么已经包含了它自己的副本（有一个规范的 BSD 版本，gnulib 也有它），

要么在 glibc 上无可救药地被破坏，

而维护者只是没有意识到这一事实。

所以此时将其包含在 musl 中不会有任何帮助。

如果通过在 glibc 中添加 fts64 接口来修复 glibc bug 15838，

我们可以考虑在 musl 中使用匹配的 ABI 来支持它，

但 glibc 似乎更有可能弃用此接口。

# 我需要定义 `_LARGEFILE64_SOURCE` 才能获得 64 位 `off_t` 吗？

这些选项用于构建应用程序，而不是构建 libc。

`-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE` 与正确支持大文件无关，

而是暴露了名称末尾带有 64 的愚蠢遗留接口（例如 open64、lseek64 等）。

在任何地方，即使在 glibc 上，也只能使用 `-D_FILE_OFFSET_BITS=64` 。

在 musl 下， `off_t` 始终是 64 位。

然而， `-D_LARGEFILE64_SOURCE` 选项很荣幸支持使用旧版open64等来编译应用程序，

但它只是将它们#defines到最后没有64的版本。

请注意，如果您正在使用 musl 构建整个系统，则您永远不需要它们中的任何一个。

你不需要它们来构建 musl，也不需要它们来构建针对 musl 的应用程序（但通常它们也不会造成伤害）。



# 为什么我收到“错误：重新定义 struct ethhdr/tcphdr/etc”？

您尝试编译的应用程序混合了用户空间和内核头文件（/include/linux）。

众所周知，内核头文件在用户空间中被破坏，并且与 musl 提供的定义发生冲突。

它仅适用于（在某些情况下）GLIBC，因为……

# 为什么 utmp/wtmp 功能仅作为stub实现？

如果实施该功能，您需要采取额外措施来保护用户的隐私

为了使用 utmp/wtmp 功能，

您需要一个 suid/sgid 二进制文件来修改数据库，

这为安全问题打开了大门：

如果您破坏这些二进制文件，您可以将任意数据注入数据库，其他程序可能会以可利用的方式解释这些数据

为了一个基本无用且可能有害的“功能”而付出巨大的风险



musl 对命名空间非常严格。

作为快速修复，

请为 GNU 和 Linux 特定函数（如 strndup）添加到 CFLAGS `-D_GNU_SOURCE` ，

并为 BSD 特定函数（如 strlcpy）添加 `-D_BSD_SOURCE` 。

如果您是包的维护者，请考虑确定正确的命名空间并将其添加到相关的 .c 文件中。 

lwn.net 上有关功能测试宏的文章。

# Bionic  C库跟 musl C库对比

Bionic C库和Musl C库都是用于Android系统的C标准库，但它们在设计和特性上有一些不同：

1. **目标平台**：
   - Bionic C库：是Google为Android系统专门开发的C标准库，主要用于Android平台。
   - Musl C库：是一个通用的C标准库，可以用于各种Linux系统，包括但不限于Android。

2. **特性和功能**：
   - Bionic C库：由于专门为Android系统设计，因此包含了一些Android特定的功能和扩展，如binder IPC机制支持、Android运行时（ART）的支持等。
   - Musl C库：致力于提供符合POSIX标准的轻量级C标准库，尽量保持简洁和高性能，不包含任何与POSIX标准不相关的功能。

3. **体积和性能**：
   - Bionic C库：由于专门为嵌入式系统设计，因此相对轻量级，适合用于资源受限的环境，如移动设备。在Android系统上具有良好的性能。
   - Musl C库：也是一个轻量级的C库，但相对于Bionic来说，它更加通用，具有更广泛的适用性。在一些嵌入式系统和轻量级环境下，Musl也表现出良好的性能。

4. **开发社区和维护**：
   - Bionic C库：由Google维护，作为Android开源项目的一部分。
   - Musl C库：由开源社区维护，得到了全球各地的开发者的支持和贡献。

综上所述，Bionic C库和Musl C库都是为嵌入式系统设计的C标准库，它们各有特点，适用于不同的场景和需求。在选择使用哪个库时，需要考虑到目标平台、功能需求以及性能要求等因素。



# 参考资料

1、Feature Test Macros

https://www.gnu.org/software/libc/manual/html_node/Feature-Test-Macros.html

2、官方wiki

https://wiki.musl-libc.org/

3、使用musl库作为默认库的系统

https://wiki.musl-libc.org/projects-using-musl.html