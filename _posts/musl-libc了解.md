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