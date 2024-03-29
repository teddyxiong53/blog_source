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

支持gun的特性。

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

而libc5如今还是广泛用于BSD等系统中。



性能上musl比glibc差多少呢？

恐怕不会有人给你确切答案。

从感觉上说，glibc应该比musl快一些，

毕竟经过20多年的持续优化，不是其它项目一朝一夕能追上的。

但是要说快多少，恐怕也不会很明显，不会有压倒性优势。

libc的代码相比其它上层复杂项目，

比如浏览器或图形系统，还是相对简单的，层次少，也不需要复杂的架构。

已知的热点，比如memory相关模块，都是需要汇编优化，这点musl有差距，

毕竟没有公司持续投钱，用爱发电，开发效率还是低。

相比android/bionic，有公司持续投入，很快就追上来。

至于对于系统调用的封装，就这么点层次，谁也不会比谁快到哪里去。



musl相比glibc，最大的问题就是兼容性问题了。

musl号称严格遵循各种国际标准进行开发。

glibc从来就不这么宣扬自己，因为GNU自成一派。

于是在二十多年的发展中，glibc添加了很多自有的独特的特性，

相类似的，gcc也是如此，

然后无数的开源应用软件有意无意的也使用了这些特性，

也就是说开源软件大多无意识地绑定了gcc/glibc，

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

# 参考资料

1、Feature Test Macros

https://www.gnu.org/software/libc/manual/html_node/Feature-Test-Macros.html

2、官方wiki

https://wiki.musl-libc.org/

3、使用musl库作为默认库的系统

https://wiki.musl-libc.org/projects-using-musl.html