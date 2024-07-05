---
title: buildroot之工具链分析
date: 2022-08-12 10:41:08
tags:
	- buildroot

---

--

最近在升级buildroot的工具链。碰到了一些问题，发现自己对工具链的组成不太了解。

所以需要把工具链深入了解一下。

就以aarch64和arm的7.3.1的为例，这个是我们之前一直在用的版本。

# aarch64工具链

aarch64的放在这个目录下：

```
toolchain/gcc/linux-x86/aarch64/gcc-linaro-7.3.1-2018.05-x86_64_aarch64-linux-gnu
```

这一层的目录组成是：

```
aarch64-linux-gnu
bin
gcc-linaro-7.3.1-2018.05-linux-manifest.txt
include
lib
libexec
share
```

## aarch64-linux-gnu目录

```
.
├── bin
├── include
├── lib
├── lib64
└── libc
```

### bin目录：

```
.
├── ar
├── as
├── ld
├── ld.bfd
├── ld.gold
├── nm
├── objcopy
├── objdump
├── ranlib
├── readelf
└── strip
```

### include目录：

下面的目录层次是：c++/7.3.1。就只有这一个目录栈。总共747个c++头文件。

就是标准的c++头文件。应该是兼容了c的头文件。

### lib目录

这个并不是lib64的软链接。

下面就一个ldscripts的子目录。里面有150个左右的这样的文件：

```
    ├── armelfb.xsc
    ├── armelfb.xsw
    ├── armelfb.xu
    ├── armelfb.xw
    ├── armelf_linux_eabi.x
    ├── armelf_linux_eabi.xbn
    ├── armelf_linux_eabi.xc
    ├── armelf_linux_eabi.xd
```

都是链接脚本文件。那就没啥特别的。

### lib64目录

这个下面就是so和a文件。

```
├── debug 这个下面就是没有strip的库文件。调试用的。
│   ├── libstdc++.a
│   ├── libstdc++fs.a
│   ├── libstdc++.so -> libstdc++.so.6.0.24
│   ├── libstdc++.so.6 -> libstdc++.so.6.0.24
│   └── libstdc++.so.6.0.24
├── libasan.a  AddressSanitizer  内存错误检测
├── libasan_preinit.o
├── libasan.so -> libasan.so.4.0.0
├── libasan.so.4 -> libasan.so.4.0.0
├── libasan.so.4.0.0
├── libatomic.a
├── libatomic.so -> libatomic.so.1.2.0
├── libatomic.so.1 -> libatomic.so.1.2.0
├── libatomic.so.1.2.0
├── libgcc_s.so -> libgcc_s.so.1
├── libgcc_s.so.1
├── libgfortran.a
├── libgfortran.so -> libgfortran.so.4.0.0
├── libgfortran.so.4 -> libgfortran.so.4.0.0
├── libgfortran.so.4.0.0
├── libgfortran.spec
├── libgomp.a
├── libgomp.so -> libgomp.so.1.0.0
├── libgomp.so.1 -> libgomp.so.1.0.0
├── libgomp.so.1.0.0
├── libgomp.spec
├── libitm.a
├── libitm.so -> libitm.so.1.0.0
├── libitm.so.1 -> libitm.so.1.0.0
├── libitm.so.1.0.0
├── libitm.spec
├── liblsan.a
├── liblsan.so -> liblsan.so.0.0.0
├── liblsan.so.0 -> liblsan.so.0.0.0
├── liblsan.so.0.0.0
├── libsanitizer.spec
├── libssp.a
├── libssp_nonshared.a
├── libssp.so -> libssp.so.0.0.0
├── libssp.so.0 -> libssp.so.0.0.0
├── libssp.so.0.0.0
├── libstdc++.a
├── libstdc++fs.a
├── libstdc++.so -> libstdc++.so.6.0.24
├── libstdc++.so.6 -> libstdc++.so.6.0.24
├── libstdc++.so.6.0.24
├── libstdc++.so.6.0.24-gdb.py
├── libsupc++.a
├── libtsan.a
├── libtsan_preinit.o
├── libtsan.so -> libtsan.so.0.0.0
├── libtsan.so.0 -> libtsan.so.0.0.0
├── libtsan.so.0.0.0
├── libubsan.a
├── libubsan.so -> libubsan.so.0.0.0
├── libubsan.so.0 -> libubsan.so.0.0.0
└── libubsan.so.0.0.0
```

AddressSanitizer  内存错误检测

https://blog.csdn.net/tq08g2z/article/details/90347700

libgcc_s.so的作用

里面包含了一些底层函数，是gcc的运行时支持库。例如在32位cpu上进行long long 除法的函数。

https://unix.stackexchange.com/questions/1812/what-does-libgcc-s-so-contain

libgfortran.a

Fortran编译初步

https://blog.csdn.net/Augusdi/article/details/7348421

libgomp.a

libgomp, the GNU Offloading and Multi Processing Runtime Library. 

libitm.a

GNU Transactional Memory Library

liblsan.a

还是内存检测的。

### libc目录

这个下面有2000多个文件。

```
.
├── etc
├── lib
├── sbin
├── usr
└── var
```

#### etc目录

下面就一个rpc的文本文件。

#### lib目录

看起来跟lib64下面的差不多。多了一些。

重要有：

```
├── ld-2.25.so
├── ld-linux-aarch64.so.1 -> ld-2.25.so
├── libc-2.25.so
├── libm-2.25.so
├── libmemusage.so
├── libpthread-2.25.so
├── libpthread.so.0 -> libpthread-2.25.so
├── libresolv-2.25.so
├── libresolv.so.2 -> libresolv-2.25.so
├── librt-2.25.so
├── librt.so.1 -> librt-2.25.so
├── libutil-2.25.so
├── libcrypt.so.1 -> libcrypt-2.25.so
├── libc.so.6 -> libc-2.25.so
├── libdl-2.25.so
├── libdl.so.2 -> libdl-2.25.so
└── libutil.so.1 -> libutil-2.25.so
```

那这个目录应该是更加关键的。链接应该主要就是链接这个目录下的。

#### sbin目录

下面就2个aarch64格式的可执行文件。

ldconfig和sln文件。

#### usr目录

这个下面的文件就比较多了。

```
.
├── bin
├── include
├── lib
├── libexec
├── sbin
└── share
```

**bin目录：**

下面有ldd、mtrace等aarch64格式的文件或者脚本。

**include目录：**

下面有1200个头文件。

标准c的，linux的头文件。都有。

这个应该是主要的头文件查找目录。

**lib目录**

这个下面有300个库文件。

gconv目录：下面是各种编码的so文件。包括gbk.so等。

重要的库文件有：

libc.a/libc.so

libcrypt.a/so

libm.a/so

libmcheck.a/so

libpthread.a/so

librt.a/so

**libexec**

下面就3个可执行文件。posix相关的。

**sbin目录**

下面就4个可执行文件。都不常用。

**share目录**

i18n等内容。



#### var目录

下面就一个db/Makefile文件。

## bin目录

这个下面放的是aarch64-linux-gnu-xx的工具。

一共31个。

这个是x86格式的文件。

## gcc-linaro-7.3.1-2018.05-linux-manifest.txt

这个是100多行文本的描述文件。

说明了工具链的组成的代码的版本和下载的地址。

编译工具链的机器的信息，各种flag的配置。

## include目录

就6个头文件。

```
.
├── gdb
│   └── jit-reader.h
├── gmp.h
├── gmpxx.h
├── mpc.h
├── mpf2mpfr.h
└── mpfr.h
```

## lib目录

目录层次是：

lib/gcc/aarch64-linux-gnu/7.3.1

有一些头文件。

## libexec目录

下面的目录层次是：

```
.
└── gcc
    └── aarch64-linux-gnu
        └── 7.3.1
            ├── cc1
            ├── cc1plus
            ├── collect2
            ├── f951
            ├── install-tools
            │   ├── fixincl
            │   ├── fixinc.sh
            │   ├── mkheaders
            │   └── mkinstalldirs
            ├── liblto_plugin.so -> liblto_plugin.so.0.0.0
            ├── liblto_plugin.so.0 -> liblto_plugin.so.0.0.0
            ├── liblto_plugin.so.0.0.0
            ├── lto1
            ├── lto-wrapper
            └── plugin
                └── gengtype
```

## share

下面有3000多个文件。

目录层次：

```
.
├── doc 这个最多，就有3000多个。都是html的。
├── gcc-7.3.1
├── gdb 下面是一些python文件。
├── info
├── locale
└── man
```

gcc-7.3.1目录：下面是这样目录

```
.
└── python
    └── libstdcxx
        ├── __init__.py
        └── v6
            ├── __init__.py
            ├── printers.py
            └── xmethods.py
```

# arm工具链

跟aarch64的层次是差不多的。不看了。

# 问题解决



libgcc是GCC的一部分。

C语言不仅仅是由编译器构成，还包括了一个标准库。

编译器在GCC包里，

标准库则位于GNU C库里，即glibc包里。

C编译器（cc1）肯定是要依赖glibc库才能正常运行。



但是编译器本身还使用了一个内部库，名为libgcc，

这个库位于GCC包里，并不属于GNU C库。

**这个库实现了一些复杂指令，**

这些指令并不能由汇编器指令集提供，

因此补充了汇编器的不足。

但是这个libgcc库也需要链接到glibc库才能完全运行。

注：GNU的标准C++库（libstdc++）也需要链接到glibc库。



这样在交叉编译时就产生了一个“鸡与蛋”的问题。

我们需要编译器来编译glibc，但是编译器又依赖glibc才能运行。

解决办法如下：
1）首先编译一个 “降级C/C++编译器”，这个降级编译器使用libgcc，但是缺少了一些功能，例如线程支持与异常处理。

2）然后使用这个降级编译器编译glibc，glibc不降级，功能完备。

3）然后编译libstdc++库，但是这个C++也是降级的。



GCC: libgcc的用途以及交叉编译

https://blog.csdn.net/qq_43401808/article/details/115723462

这个是libgcc的中文说明

http://gccint.cding.org/Libgcc.html

这篇文档对libgcc进行较好的介绍

https://www.cnblogs.com/dream397/p/16127022.html

# buildroot里gcc的编译过程分析

在Buildroot中，GCC工具链通常需要编译两次，分别是gcc-initial和gcc-final。

1. **gcc-initial**：gcc-initial是一个用来引导编译过程的GCC工具链。它通常是一个非常精简的工具链，只包含最基本的编译器和库，足以用来编译Buildroot中其他软件包的第一阶段。这个阶段的目标是生成一个可以用于编译完整GCC的初始版本。

2. **gcc-final**：一旦生成了gcc-initial，接下来的步骤是使用这个初始工具链来编译完整的GCC。gcc-final是一个包含完整功能的GCC工具链，它会被编译两次，第一次编译生成一个中间版本的GCC，然后使用这个中间版本的GCC来编译最终的GCC工具链，也就是gcc-final。最终的gcc-final工具链包含了完整的GCC编译器和相关工具，可以用于编译目标系统上的应用程序和库。

这个两步编译的过程是为了确保生成的GCC工具链在目标系统上能够正常工作，而gcc-initial则只是一个临时的工具链，用于引导整个编译过程。这种分阶段的编译方式有助于确保编译工具链的稳定性和可靠性。





一个编译工具链模块是允许为系统编译代码的一组工具。

它由一个编译器(在我们的例子中是 gcc)、

像汇编器和链接器这样的二进制 utils(一般是 binutils)

和一个C标准库(例如 GNU Libc, uClibc-ng)组成。



一个交叉编译工具链是可有在主机上运行的，

但是编译出来的二进制文件只能运行在目标板或机器上。

在我们的宿主机上也有工具链，它只能编译适用于我们的宿主机，编译出来的程序也只能运行在我们的宿主机上。

当前我们要使用 buildroot 编译出来一个交叉编译工具链，适用于我们的目标板。

目标板是 S3C2440，它是 ARM 架构的，arm920t 的核心。

内部工具链是 Buildroot 在为目标嵌入式系统构建用户空间应用程序和库之前，自行构建的交叉编译工具链。

此交叉编译工具链支持几种 C 库：uClibc-ng, glibc 和 musl。



更改构建工具链需要的内核头文件版本。

- 在构建交叉编译工具链的过程中，C 库也在被构建。这个库提供了用户空间应用程序和 Linux 内核之间的接口。==为了知道如何与 Linux 内核“对话”，C 库需要访问Linux内核头文件(即来自内核的.h文件)，它定义了用户空间与内核之间的接口(系统调用、数据结构等)。==

- 由于此接口是向后兼容的，因此用于构建工具链的 Linux 内核头的版本不需要与我们打算在嵌入式系统上运行的 Linux 内核的版本完全匹配。==它们只需要有一个与我们要运行的 Linux 内核版本相同或更老的版本。==

值得注意的是，每当修改其中一个选项时，就必须重新构建整个工具链和系统。

这种方式也有好处：与 Buildroot 有很好的集成并且快速，只构建必要的内容

缺点是：make clean 后需要重新构建工具链，这需要时间。如果我们试图减少构建时间，可以考虑使用外部工具链。

外部工具链允许使用现有的预先构建的交叉编译工具链。

Buildroot知道许多著名的交叉编译工具链(来自用于 ARM 的 Linaro、用于 ARM 的 Sourcery CodeBench、x86-64、PowerPC 和 MIPS)，并且能够自动下载它们，或者指向一个定制的工具链，可以下载，也可以在本地安装。



## package\gcc\gcc-final\gcc-final.mk



## package\gcc\gcc-initial\gcc-initial.mk

https://www.cnblogs.com/kele-dad/p/13125808.html



## buildroot\toolchain\toolchain-buildroot\Config.in

toolchain-buildroot的编译。

这个Config.in就是包含了：

```
source "package/linux-headers/Config.in.host"
source "package/linux-headers/Config.in"
source "package/musl/Config.in"
source "package/uclibc/Config.in"
source "package/glibc/Config.in"
source "package/binutils/Config.in.host"
source "package/gcc/Config.in.host"
source "package/gcc/Config.in"
```

这也说明工具链的本质是linux-header + libc + binutils + gcc。



# toolchain-wrapper 

`toolchain-wrapper` 是一个工具链包装器，用于在构建软件时管理和使用交叉编译工具链。它的主要作用是将交叉编译工具链的路径和参数传递给编译器、链接器和其他构建工具，以确保正确地生成目标体系结构上的可执行文件和库。

以下是 `toolchain-wrapper` 的一些主要功能和用途：

1. **路径管理**：`toolchain-wrapper` 负责管理交叉编译工具链的路径，包括编译器、链接器、头文件和库文件的位置。这有助于确保构建过程中使用的工具链是正确的。

2. **工具链参数传递**：它负责将构建过程所需的参数传递给工具链。这包括编译器选项、链接器选项以及其他相关的参数。通过这种方式，它可以确保生成的代码和可执行文件是针对目标体系结构的。

3. **多架构支持**：`toolchain-wrapper` 可以处理多个不同的目标体系结构，这对于交叉编译非常有用。开发人员可以使用不同的工具链来构建针对不同体系结构的软件。

4. **简化构建过程**：它可以简化构建过程，因为开发人员无需手动设置工具链路径和参数。这降低了构建过程的复杂性，并有助于确保构建的一致性。

5. **可定制性**：`toolchain-wrapper` 通常是可定制的，允许用户根据项目的需要配置工具链的路径和参数。这可以通过配置文件或环境变量来实现。

`toolchain-wrapper` 是交叉编译工具链的重要组成部分，用于确保开发人员能够轻松地构建适用于目标体系结构的软件。它在许多嵌入式开发和交叉编译环境中都有广泛的应用。不同的工具链包装器可能有不同的实现细节，但它们的基本目标都是相似的，即简化交叉编译过程并确保生成的代码与目标平台兼容。



当构建嵌入式系统时，

假设你正在使用 Buildroot 来生成针对 ARM 架构的嵌入式 Linux 系统。

在这种情况下，toolchain-wrapper 的作用是确保正确的交叉编译工具链被调用以构建针对 ARM 架构的软件包。

例如，在编译一个针对 ARM 架构的简单 C 程序时，toolchain-wrapper 确保正确的交叉编译器被调用，以生成可在 ARM 目标系统上运行的可执行文件。下面是一个示例：

假设有一个简单的 hello.c 文件：

```c
#include <stdio.h>

int main() {
    printf("Hello, ARM!\n");
    return 0;
}
```

使用 Buildroot 构建系统时，在 Makefile 或构建脚本中，toolchain-wrapper 会被调用来编译这个程序：

```bash
$(CROSS_COMPILE)gcc -o hello hello.c
```

在这里，$(CROSS_COMPILE) 是一个由 Buildroot 设置的变量，它包含了交叉编译工具链的前缀，如 arm-linux-gnueabi-。而实际上执行的命令可能是：

```bash
arm-linux-gnueabi-gcc -o hello hello.c
```

toolchain-wrapper 确保正确的编译器（这里是 arm-linux-gnueabi-gcc）被调用，并且传递了正确的编译选项和标志，以便将 hello.c 编译为针对 ARM 架构的可执行文件 hello。这个可执行文件可以在目标 ARM 硬件上运行。

通过使用 toolchain-wrapper，Buildroot 确保了正确的交叉编译工具链被使用，从而使生成的软件包适用于目标嵌入式系统的架构和环境。



这段注释描述了 `toolchain-wrapper` 的作用：

它是用于处理工具链的一个包装器。

它的主要功能是执行真实的工具链，

==同时传递了一些参数（如 sysroot、arch 等）==

，这些参数在代码中是硬编码的，以确保工具链使用了正确的配置。

通常情况下，这个包装器可能会设置一些环境变量或者传递一些特定的参数，以确保在交叉编译环境中正确地调用工具链。

注释中提到的硬编码路径参数是相对于包装器实际位置的，这样可以确保在不同位置执行时也能正确地定位到相关的系统根路径、架构等信息。

这个包装器的主要目的是确保工具链使用了正确的配置和路径，以便在构建过程中正确地生成适用于目标系统的可执行文件和库。通过这种方式，它能够保证所构建的软件包和可执行文件在目标环境中能够正常运行。



# crosstool-ng手动编译工具链

https://blog.csdn.net/birencs/article/details/124677373

# 手动编译工具链

这个脚本可以手动编译工具链。

https://github.com/zhouronghua/CCC/blob/main/the_compiler_of_the_cross_compiler.sh

对应的文章：

https://www.cnblogs.com/zhouronghua/p/15236755.html

## libgmp-dev libmpfr-dev libmpc-dev 这3个软件包的作用

这三个软件包 `libgmp-dev`、`libmpfr-dev`、`libmpc-dev` 是用于支持 GNU MPC（Multiple Precision Complex Arithmetic Library）的开发的。它们提供了用于开发和编译与 GMP（GNU Multiple Precision Arithmetic Library）、MPFR（Multiple Precision Floating-Point Reliable Library）和 MPC 相关的软件的头文件和库文件。

下面是它们各自的作用：

1. **libgmp-dev:**
   - 提供 GMP（GNU Multiple Precision Arithmetic Library）的开发文件。
   - 包含 GMP 库的头文件和静态库，用于在程序中使用 GMP 提供的多精度整数和有理数算法。
   - 在编译需要使用 GMP 功能的软件时，需要安装这个软件包。

2. **libmpfr-dev:**
   - 提供 MPFR（Multiple Precision Floating-Point Reliable Library）的开发文件。
   - 包含 MPFR 库的头文件和静态库，用于在程序中进行高精度浮点数运算。
   - 在编译需要使用 MPFR 功能的软件时，需要安装这个软件包。

3. **libmpc-dev:**
   - 提供 MPC（Multiple Precision Complex Arithmetic Library）的开发文件。
   - 包含 MPC 库的头文件和静态库，用于在程序中进行复数运算。
   - 在编译需要使用 MPC 功能的软件时，需要安装这个软件包。

这些软件包通常是在编译数学库、科学计算软件或其他需要高精度算法支持的应用程序时所需的依赖项。在使用这些库的时候，安装相应的开发文件可以确保程序正确链接和调用这些库的功能。



# toolchain\toolchain-external\pkg-toolchain-external.mk

这段注释描述了 Buildroot 中用于支持外部工具链（external toolchains）的基础设施。

外部工具链是指预先构建好、可直接使用的工具链，

可以通过网络（如 Linaro、Sourcery CodeBench、处理器供应商提供的工具链）获取，

也可以使用 Crosstool-NG 或 Buildroot 自身构建。

Buildroot 的外部工具链基础设施已在一些环境中进行了测试，

包括 Crosstool-NG 生成的工具链、Buildroot 生成的工具链、Linaro 为 ARM 和 AArch64 架构提供的工具链、Sourcery CodeBench 为 ARM、MIPS、PowerPC、x86_64 和 NIOS 2 架构提供的工具链，

以及 Synopsys DesignWare 为 ARC 核心提供的工具链。

这个基础设施的基本原则包括以下几个步骤：

1. 如果工具链未预安装，则下载并解压缩到 `$(TOOLCHAIN_EXTERNAL_INSTALL_DIR)`。否则，`$(TOOLCHAIN_EXTERNAL_INSTALL_DIR)` 指向用户已经安装工具链的位置。

2. 对于所有外部工具链，检查 Buildroot 菜单配置系统中工具链配置与外部工具链的实际配置之间的一致性。这对于确保 Buildroot 配置系统知道工具链是否支持 RPC、IPv6、locales、大文件等非常重要。这些信息无法在配置时自动检测，因为这些选项（例如 `BR2_TOOLCHAIN_HAS_NATIVE_RPC`）的值在配置时是必需的，由于这些选项用作其他选项的依赖项。在配置时，我们无法检索外部工具链的配置。

3. ==将运行时所需的库复制到目标目录 `$(TARGET_DIR)`。显然，如果在目标系统上执行动态应用程序，则需要像 C 库、动态加载器和其他一些实用库。==

4. ==将库和头文件复制到 staging 目录。这将允许所有后续对 gcc 的调用都使用 `--sysroot $(STAGING_DIR)`，从而大大简化使用外部工具链时软件包的编译。==因此，最终只有交叉编译器二进制文件保持外部，所有库和头文件都导入 Buildroot 树中。

5. 构建一个工具链包装器（toolchain wrapper），==该包装器使用硬编码的一些参数（如 sysroot/march/mtune/..）执行外部工具链，以确保始终使用正确的配置，并且工具链的行为类似于内部工具链。==此工具链包装器和符号链接被安装到 `$(HOST_DIR)/bin`，其余 Buildroot 的处理与内部工具链的处理相同。