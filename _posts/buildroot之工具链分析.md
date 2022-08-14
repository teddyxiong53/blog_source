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

C编译器（cc1）肯定是要以来glibc库才能正常运行。



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

