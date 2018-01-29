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

#先编译一下

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

