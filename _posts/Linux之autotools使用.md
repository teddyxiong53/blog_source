---
title: Linux之autotools使用
date: 2019-07-05 11:47:37
tags:
	- Linux
---

--

autotools是指3个gnu工具包。

autoconf、automake、libtool。

gnu软件的安装步骤，一般是三步走：

```
1、configure。
2、make
3、make install。
```

configure这一步，就需要一个configure文件，而这个文件比较复杂，手写不现实。

autoconf这个工具就是用来帮我们生成configure文件的。



当然如果你想搭建自己的采用automake编译的项目，那么你需要再去学习一下如何编写configure.ac和Makefile.am文件。

一般我们从github上clone下来的需要采用automake编译的项目都包含了configure.ac和Makefile.am文件或者里面还包含了一个autogen.sh的脚本（一般都是调用了autoreconf这个工具）。编译这样一个项目基本上可以三步完成：

1. 在项目根目录运行"autoreconf　-if",　你会发现项目目录下会多出m4文件目录, config.h.in文件, Makefile.in文件, configure脚本, compile脚本, depcomp脚本等文件；
2. 接着运行./configure进行配置生成makefile文件，譬如enbale/disbale一些特性，设置交叉编译平台（例如--host=linux-mips），设置编译安装目录（例如--prefix=path_to_your_build_directory）具体可以查看help信息；
3. 执行make && make install。



# autoconf

为什么出现了autoconf？

最开始，发布的代码，都是直接带Makefile的，拿到源代码，直接make就好了。

但是随着软件在不同平台上使用，Makefile需要做很多的调整。

而且有些平台可能没有某些函数，例如有些平台不支持strdup这个系统调用。

这些调整比较多，而且琐碎，所以大家就开始手动写configure脚本来自动做这些调整工作。

configure脚本做的事情：

1、先检查当前的环境的，

2、生成一个config.h文件。里面就各种宏定义。

3、生成一个正对当前平台的Makefile。

很快，大家就发现，写configure脚本也是一个很烦人的事情。

于是就开发了autoconf来帮助生成configure文件。

**但是还是需要一个简单的配置文件configure.ac。**



# automake

前面说到autoconf帮我们生成了configure脚本。

但是Makefile的模板文件Makefile.in还是需要程序员手动来写。

这个又是一个烦人的事情，而且是很多重复性的工作。

所以最好也是靠工具来生成。这个工具就是automake。

**程序员只需要手写一个Makefile.am文件来描述依赖关系就好了。**



# 一个简单的例子

代码我放在这里：

https://github.com/teddyxiong53/c_code/tree/master/autotools/earth

执行：

```
autoreconf --install
```

这个会生成configure等文件。

然后就可以执行：

```
./configure
make
```

我增加了一个myclean.sh脚本。可以把生成的所有文件都清除掉。



![img](../images/random_name/753880-20160605121846586-1241135412.jpg)



## autoscan: 

扫描源代码以搜寻普通的可移植性问题，比如检查编译器，库，头文件等，生成文件configure.scan,它是configure.ac的一个雏形。

（xhl：这一步可以不这么做。找一个configure.ac的模板手动修改就行了）

## aclocal:

根据已经安装的宏，用户定义宏和acinclude.m4文件中的宏

将configure.ac文件所需要的宏集中定义到文件 aclocal.m4中。

aclocal是一个perl 脚本程序，

它的定义是：“aclocal - create aclocal.m4 by scanning configure.ac”



## automake:

将Makefile.am中定义的结构建立Makefile.in，

然后configure脚本将生成的Makefile.in文件转换 为Makefile。

如果在configure.ac中定义了一些特殊的宏，

比如AC_PROG_LIBTOOL，它会调用libtoolize，

否则它 会自己产生config.guess和config.sub



## autoconf:

将configure.ac中的宏展开，生成configure脚本。

这个过程可能要用到aclocal.m4中定义的宏。



以一个main.c和hello.h为例。

先执行autoscan命令，得到configure.scan文件。

**手动修改configure.scan文件。然后把文件改名为configure.ac。**

然后执行aclocal命令。

得到了aclocal.m4文件。内容较多，不去读里面的内容。

然后执行autoconf命令。

就生成了configure这个文件。

内容也很多，不可读。

然后执行autoheader命令。生成config.h.in文件。

然后需要手动写Makefile.am文件。

```
AUTOMAKE_OPTIONS=foreign 
bin_PROGRAMS=hello 
hello_SOURCES=hello.cpp hello.h
```

然后执行automake，

```
automake --add-missing
```

这一步是为了上传Makefile.in，`--add-missing`是为了自动补全缺少的脚本。

然后就可以进行configure和make了。





noinst_HEADERS：

这个表示该头文件只是参加可执行文件的编译，而不用安装到安装目录下。

如果需要安装到系统中，可以用include_HEADERS来代替。



**一般推荐使用libtool库编译目标，**

因为automake包含libtool，这对于跨平台可移植的库来说，肯定是一个福音。



下面分别展示下软件发布和安装的命令：

发布：

```text
aclocal # 设置m4 环境
autoconf # 生成 configure 脚本
automake --add-missing # 生成 Makefile.in 脚本
./configure # 生成 Makefile 脚本
make distcheck # 使用 Makefile 构建一个发布软件并测试
```

安装：

```text
./configure # 生成 Makefile 脚本
make # 构建软件
make install # 使用 Makefile 安装软件
```





# configure检查过程

configure过程会检查各种依赖的东西是否存在。

这个是怎么做的？

我主要是想搞清楚，buildroot时，configure是检查哪里的配置。能不能改。

sysroot可以改，configure选项加上

```
DIRECTFB_CONF_OPTS += --with-sysroot=$(STAGING_DIR)
```



evtest的编译分析

这个是一个实际项目，足够简单，依赖也不多。正好可以用来分析。

代码目录是这样：

```
├── autogen.sh
├── configure.ac
├── COPYING
├── evtest.c
├── evtest.txt
├── INSTALL
├── Makefile.am
└── README
```

https://github.com/freedesktop-unofficial-mirror/evtest

看一下提交记录。从2009年开始的。

最开始的编译文件是2个：configure.ac和Makefile.am



# configure.ac写法

https://blog.csdn.net/yhd1019896930/article/details/78488256





新建一个目录

```
auto-test
└── src
    ├── audio
    │   ├── audio.c
    │   └── audio.h
    ├── image
    │   ├── image.c
    │   └── image.h
    ├── main.c
    └── video
        ├── video.c
        └── video.h
```

这样看起来比较正式一点。

然后在auto-test目录下，执行：

```
autoscan
```

 Generate a preliminary configure.in

读懂这些，应该就足够了。总结一下，基本步骤如下：
1、autoscan ./
2、修改生成的configure.scan文件，增加AM_INIT_AUTOMAKE ，AC_CONFIG_FILES([Makefile])
3、aclocal
4、核心步骤：根据情况，编写Makefile.am
5、autoheader
6、touch NEWS README AUTHORS ChangeLog
7、automake -a
8、autoconf

注：运行autoscan时，会出现以下提示：

[shell]
autom4te: configure.ac: no such file or directory
autoscan: /usr/bin/autom4te failed with exit status: 1
[/shell]

这个提示不影响下面的步骤，因为configure.scan文件已经生成了。



之前一直把所有的h文件和c文件都放在同一个目录下，用的是通用Makefile，现在觉得需要现代化一点，

于是进行了一些改造，分多个目录，多级目录，

因此，学习一下autoscan，aclocal，autoconf，automake这些工具的使用。



configure.ac由一些宏组成

（如果已经有源代码，你可以运行autoscan来产生一个configure.scan文件，在此基础修改成configure.ac将更加方便）

最基本的组成可以是下面的

```
AC_INIT([PACKAGE], [VERSION], [BUG-REPORT-ADDRESS])
# Checks for programs.
# Checks for libraries.
# Checks for header les.
# Checks for typedefs, structures, and compiler characteristics.
# Checks for library functions.
# Output les.
AC_CONFIG_FILES([FILES])
AC_OUTPUT
```



## 参考资料

1、

https://blog.csdn.net/john_crash/article/details/49889949

2、

这里有个简单的例子。

https://renenyffenegger.ch/notes/development/GNU/toolchain/Build-System/Autoconf/macros/AC_SUBST

# Makefile.am变量

```
1. SUBDIRS  

说明下面当前目录下的哪些子目录需要编译，多个目录用空格分开

如

SUBDIRS=src tests tools

说明需要进入到src、tests 、tools三个目录中编译

 

2. DIST_SUBDIRS 

（待确认）

 

3. noinst_LIBRARIES

表示该工程用于生成库文件

如

noinst_LIBRARIES = libcommon.a

表示用于该工程生成库文件名为libcommon.a

4. XXX_SOURCES

表示要编译的源文件，XXX需要用生成的目标文件名替换，如果文件名中含".",则需要改为“_”； 多个源文件用空格分开，也可以用变量表示文件

如

libcommon_a_SOURCES = ${common_sources}  

表示生成libcommon.a需要编译的源文件来源变量common_sources

 

5. 自定义变量

如

common_sources = common.h common.cpp

表示定义common_sources 为 common.h common.cpp

 

6. clean-local:

执行make clean命令是，实际执行的命令，其中，命令如下文-rm前面不能是空格，必须是Tab；*表示通配符号，多个文件用空格隔开

如

clean-local:

-rm -f *.gcov *.gcno *.gcda 

表示执行make clean清理*.gcov、*.gcno、*.gcda

7. AM_CPPFLAGS 、AM_CFLAGS 

预定义变量，，g++编译器的附加参数

如

AM_CPPFLAGS = -I${top_srcdir}/src  

AM_CFLAGS = -I${top_srcdir}/src  

 

-I表示搜索头文件时的附加路径

8. LDADD 

表示编译本工程的附加链接库

如

LDADD = ${top_srcdir}/src/common/libcommon.a 

表示编译时需要连接 ${top_srcdir}/src/common/libcommon.a

 

9. top_srcdir

预定义变量，工程的顶层目录

 

10. bin_PROGRAMS

表示该工程生成可执行文件

如

bin_PROGRAMS = prog2  

prog2_SOURCES = main.cpp  
表示生成可执行文件prog2，其中源文件为main.cpp  
```



Makefile.am将指明工程需要哪些源文件，建造的是什么，如何安装它们。
具体语法如下：
**option_where_PRIMARY = targets …**

**targets**是要建造的目标
**PRIMARY**可以是下面的一个：

| 可能值          | 解释             |
| --------------- | ---------------- |
| **PROGRAMS**    | 目标是可执行程序 |
| **LIBRARIES**   | 目标是静态库     |
| **LTLIBRARIES** | 目标是动态库     |
| **HEADERS**     | 目标是头文件     |
| **SCRIPTS**     | 目标是脚本       |
| **DATA**        | 目标是数据       |

**where** 表示目标被安装那里，可以是下面的值:

| 可能项 | 解释                 |
| ------ | -------------------- |
| bin    | $(bindir)            |
| lib    | $(libdir)            |
| custom | 自定义目录           |
| noinst | 不安装               |
| check  | 由’make check’建造。 |



**在where前面还可以有一个可选项option**
dist_ 分发目标(默认)。
nodist_ 不分发。



举例：Makefile.am

```shell
bin_PROGRAMS = foo run-me
foo_SOURCES = foo.c foo.h print.c print.h
run_me_SOURCES = run.c run.h print.c
```

首先第一句表示产生两个程序foo,run-me，并且将它们安装到bin中。
foo_SOURCES 表示foo需要的源文件。
run_me_SOURCES 表示run-me需要的源文件。
**注意：不能转换的符号用’_’代替。**

头文件不参加编译，列出来用于分发。automake将自动计算列表对象并编译链接它们。

第二个例子：Makefile.am

```shell
lib_LIBRARIES = libfoo.a libbar.a
libfoo_a_SOURCES = foo.c privfoo.h
libbar_a_SOURCES = bar.c privbar.h
include_HEADERS = foo.h bar.h
```

这将产生两个静态库文件libfoo.a,libbar.a。
libfoo_a_SOURCES 表明编译libfoo.a需要的源文件。
libbar_a_SOURCES 表明编译libbar.a需要的源文件。
include_HEADERS 表明需要安装的头文件。



也许你在几个目录里面编译，这些目录里面都放置Makefile.am文件。它们必须在configure.ac文件中声明。例如：configure.ac、



参考资料

https://codeantenna.com/a/SvqqMUpkgb

# acmkdir



# BUILT_SOURCES

现在碰到一个问题，

It’s a different story if foo.h doesn’t exist by the first `make` run. For instance, there might be a rule to build foo.h.

The `BUILT_SOURCES` variable is a workaround for this problem. 

A source file listed in `BUILT_SOURCES` is made when ‘make all’, ‘make check’, ‘make install’, ‘make install-exec’ (or `make dist`) is run, before other targets are processed.

So, to conclude our introductory example, we could use ‘BUILT_SOURCES = foo.h’ to ensure foo.h gets built before any other target (including foo.o) during ‘make all’ or ‘make check’.

需要注意的是，`BUILT_SOURCES`只支持`make all`，`make check`和`make install`，如果单个执行`make A`是不行的。

https://www.gnu.org/software/automake/manual/html_node/Sources.html

http://vinllen.com/makefile-amzhi-built_sources/



```
AC_PREREQ
	autoconf的最低版本，例如AC_PREREQ([2.59])
AC_INIT([x],[y],[z])
	告诉autoconf自己的名字，版本，自己的email
	例如：AC_INIT([mybluealsa],[1.0],[1073167306@qq.com])
AM_INIT_AUTOMAKE
	初始化automake，后面跟一下选项。
	常用选项：
	-Wall
	-Werror
	foreign：放宽一下gnu标准要求。
	-1.11.1 automake的最低版本。
	例如：AM_INIT_AUTOMAKE([foreign -Wall])
AC_CHECK_HEADERS([string.h])
	检查是否有string.h这个头文件。
	代码里是这样使用：
	#if HAVE_STRING_H
	#include <string.h>
AC_CONFIG_HEADERS([config.h])
AC_CONFIG_MACRO_DIR([m4])
	local Autoconf macros autoconf宏定义的目录，一般有一个m4的目录。
```



https://www.gnu.org/software/autoconf/manual/autoconf-2.69/html_node/Input.html

https://blog.csdn.net/qigaohua/article/details/112028018

# libtool.m4

这个的作用是什么？

```
当autoconf和automake时使用时，用户自定义宏应该放在 acinclude.m4和m4/*.m4（GNU autoconf手册上说好像是 aclocal/*.m4），流程是这样的：

acinclude.m4 \

aclocal/*.m4 ｜ === aclocal perl script （由automake提供） ===> aclocal.m4

configure.ac /

然后 autoconf 会在处理 configure.ac 之前先处理 aclocal.m4，使 acinclude.m4 aclocal/*.m4中包含的宏定义可在configure.ac中使用
```



在代码中适当的运用宏，创造优雅易读的代码，这样或许更能体现编程是一种艺术。虽然有些编程语言未提供宏功能，但是我们总是会有 GNU m4 这种通用的宏处理器可用。



m4 是一种宏处理器，它扫描用户输入的文本并将其输出，期间如果遇到宏就将其展开后输出。

宏有两种，一种是内建的，另一种是用户定义的，

它们能接受任意数量的参数。

**除了做展开宏的工作之外，m4 内建的宏能够加载文件，执行 Shell 命令，做整数运算，操纵文本，形成递归等等。**

**m4 可用作编译器的前端，或者单纯作为宏处理器来用**。

所有的 Unix 系统都会提供 m4 宏处理器，因为它是 POSIX 标准的一部分。

通常只有很少一部分人知道它的存在，这些发现了 m4 的人往往会在某个方面成为专家。

这不是我说的，这是 m4 手册说的。



有些人对 m4 非常着迷，他们先是用 m4 解决一些简单的问题，然后解决了一个比一个更大的问题，

直至掌握如何编写一个复杂的 m4 宏集。

若痴迷于此，往往会对一些简单的问题写出复杂的 m4 脚本，然后耗费很多时间去调试，

反而不如直接手动解决问题更有效。

所以，对于程序猿中的强迫症患者，要对 m4 有所警惕，

它可能会危及你的健康。这也不是我说的，是 m4 手册说的。



让这世界再多一份 GNU m4 教程 (1)

https://segmentfault.com/a/1190000004104696



# 用autotools来创建一个开源项目

https://github.com/happyAnger6/anger6_autotools

这个脚本很好，靠gen.sh就生成了一个不错的autotools框架。



这篇文档不错，还可以用eclipse插件来做。

https://blog.csdn.net/xlxxcc/article/details/51112826

# top_srcdir

top_srcdir应该是Makefile.am里内置的变量，指向的是代码顶层目录。

对于yocto里使用，就有问题了。

buildroot是正常的，因为编译目录和代码目录是同一个。

现在yocto里分开了。

所以top_srcdir里不会生成o文件和lib文件。



`it is sufficient to use just ‘$srcdir’ instead of ‘$top_srcdir’.`

```
— Variable: top_builddir
The relative name of the top level of the current build tree. In the top-level directory, this is the same as builddir.
```

就是用top_builddir就可以了。



参考资料

https://blog.csdn.net/qq_31324949/article/details/106439197



https://www.gnu.org/software/autoconf/manual/autoconf-2.67/html_node/Preset-Output-Variables.html





# 一篇文章的分析



这篇文章不错

https://blog.csdn.net/u012839187/article/details/102903345

学习记录一下。



下面我根据自己的工作中的一些应用，来讨论Makefile.am的编写。

我觉得主要是要注意的问题是：

将编译什么文件？

这个文件会不会安装？

这个文件被安装到什么目录下？

可以将文件编译成可执行文件来安装，也可以编译成静态库文件安装，常见的文件编译类型有下面几种：

PROGRAMS。表示可执行文件
LIBRARIES。表示库文件
LTLIBRARIES。这也是表示库文件，前面的LT表示libtool。
HEADERS。头文件。
SCRIPTS。脚本文件，这个可以被用于执行。如：example_SCRIPTS，如果用这样的话，需要我们自己定义安装目录下的example目录，很容易的，往下看。
DATA。数据文件，不能执行。



## 一，可执行文件

先看一个实例：

```
bin_PROGRAMS = client
 
client_SOURCES = key.c connect.c client.c main.c session.c hash.c
client_CPPFLAGS = -DCONFIG_DIR=\"$(sysconfdir)\" -DLIBRARY_DIR=\"$(pkglibdir)\"
client_LDFLAGS = -export-dynamic -lmemcached
noinst_HEADERS = client.h
INCLUDES = -I/usr/local/libmemcached/include/
client_LDADD = $(top_builddir)/sx/libsession.la \
            $(top_builddir)/util/libutil.la
```

上面就是一个全部的Makefile.am文件，

这个文件用于生成client可执行应用程序，

引用了两个静态库和MC等动态库的连接。

分析一下：

bin_PROGRAMS：

表示指定要生成的可执行应用程序文件，这表示可执行文件在安装时需要被安装到系统中，

如果只是想编译。不想被安装到系统中，可以用noinst_PROGRAMS来代替。



一个简单的问题是：bin_PROGRAMS=client 这一行表示什么意思？

解释如下：

PROGRAMS知道这是一个可执行文件。

client表示编译的目标文件。

**bin表示目录文件被安装到系统的目录。**（这个点我之前倒是不知道。）

后面的包括头文件，静态库的定义都是这种形式，如lib_LIBRARIES=util，表示将util库安装到lib目录下。

继续解释上面的文件

client_SOURCES：

表示生成可执行应用程序所用的源文件，

这里注意，client_是由前面的bin_PROGRAMS指定的，

如果前面是生成example,那么这里就是example_SOURCES，其它的类似标识也是一样。



client_CPPFLAGS：

这和Makefile文件中一样，表示C语言**预处理器参数**，这里指定了CONFIG_DIR，

以后在程序中，就可以直接使用CONFIG_DIR,

**不要把这个和另一个CFLAGS混淆，后者表示编译器参数。**



client_LDFLAGS：

这个表示在连接时所需要的库文件选项标识。这个也就是对应一些如-l,-shared等选项。



noinst_HEADERS：

这个表示该头文件只是参加可执行文件的编译，而不用安装到安装目录下。

**如果需要安装到系统中，可以用include_HEADERS来代替。**



INCLUDES：连接时所需要的头文件。



client_LDADD：连接时所需要的库文件,这里表示需要两个库文件的支持，下面会看到这个库文件又是怎么用Makefile.am文件后成的。



再谈谈关于上文中的全局变量引用，

可能有人注意到`$(top_builddir)`等全局变量（因为这个文件之前没有定义），

其实这个变量是Makefile.am系统定义的一个基本路径变量，

表示生成目标文件的最上层目录，

如果这个Makefile.am文件被其它的Makefile.am文件，这个会表示其它的目录，而不是这个当前目录。

还可以使用`$(top_srcdir)`，这个表示工程的最顶层目录，

其实也是第一个Makefile.am的入口目录，因为Makefile.am文件可以被递归性的调用。



下面再说一下上文中出现的`$(sysconfdir)`，

在系统安装时，我们都记得先配置安装路径，

如./configure --prefix=/install/apache 

其实在调用这个之后，就定义了一个变量`$(prefix)`,

表示安装的路径，如果没有指定安装的路径，会被安装到默认的路径，一般都是/usr/local。

在定义`$(prefix)`，还有一些预定义好的目录,

其实这一些定义都可以在顶层的Makefile文件中可以看到，如下面一些值：

```
bindir = $(prefix)/bin。

libdir = $(prefix)/lib。

datadir=$(prefix)/share。

sysconfdir=$(prefix)/etc。

includedir=$(prefix)/include。
```



这些量还可以用于定义其它目录，例如我想将client.h安装到include/client目录下，这样写Makefile.am文件：

```
clientincludedir=$(includedir)/client
clientinclude_HEADERS=$(top_srcdir)/client/client.h
```

这就达到了我的目的，相当于定义了一个安装类型，这种安装类型是将文件安装到include/client目录下。

我们自己也可以定义新的安装目录下的路径，如我在应用中简单定义的：

```
devicedir = ${prefix}/device
device_DATA = package
```

这样的话，package文件会作为数据文件安装到device目录之下，这样一个可执行文件就定义好了。

注意，这也相当于定义了一种安装类型：devicedir，所以你想怎么安装就怎么安装，

后面的XXXXXdir，dir是固定不变的。



## 二，静态库文件

编译静态库和编译动态库是不一样的，

我们先看静态库的例子，这个比较简单。

直接指定 XXXX_LTLIBRARIES或者XXXX_LIBRARIES就可以了。

如果不需要安装到系统，将XXXX换成noinst就可以。

还是再罗嗦一下：

**一般推荐使用libtool库编译目标，因为automake包含libtool，**

这对于跨平台可移植的库来说，肯定是一个福音。

看例子如下：

```
noinst_LTLIBRARIES = libutil.la
 
noinst_HEADERS = inaddr.h util.h compat.h pool.h xhash.h url.h device.h 
 
libutil_la_SOURCES = access.c config.c datetime.c hex.c inaddr.c log.c device.c pool.c rate.c sha1.c stanza.c str.c xhash.c

libutil_la_LIBADD = @LDFLAGS@
```



第一行的noinst_LTLIBRARIES，

这里要注意的是LTLIBRARIES，另外还有LIBRARIES，两个都表示库文件。

前者表示libtool库，用法上基本是一样的。

如果需要安装到系统中的话，用lib_LTLIBRARIES。

注意：

静态库编译连接时需要其它的库的话，采用XXXX_LIBADD选项，而不是前面的XXXX_LDADD。

编译静态库是比较简单的，因为直接可以指定其类型。



## 三，动态库文件

想要编译XXX.so文件，需要用_PROGRAMS类型，

这里一个关于安装路径要注意的问题是，

我们一般希望将动态库安装到lib目录下，按照前面所讨论的，只需要写成lib_PROGRAMS就可以了，

因为前面的lib表示安装路径，

但是automake不允许这么直接定义，可以采用下面的办法，也是将动态库安装到lib目录下

```
projectlibdir=$(libdir) //新建一个目录，就是该目录就是lib目录
projectlib_PROGRAMS=project.so
project_so_SOURCES=xxx.C
project_so_LDFLAGS=-shared -fpic //GCC编译动态库的选项
```



## 四，SUBDIRS的用法

这是一个很重要的关键词，

我们前面生成了一个一个的目标文件，

但是一个大型的工程项目是由许多个可执行文件和库文件组成，也就是包含多个目录，

每个目录下都有用于生成该目录下的目标文件的Makefile.am文件，

但顶层目录是如何调用，才能使下面各个目录分别生成自己的目标文件呢？

就是SUBDIRS关键词的用法了。



看一下我的工程项目，这是顶层的Makefile.am文件

```
EXTRA_DIST = Doxyfile.in README.win32 README.protocol contrib UPGRADE
 
devicedir = ${prefix}/device
device_DATA = package
 
SUBDIRS = etc man
if USE_LIBSUBST
SUBDIRS += subst
endif
SUBDIRS += tools io sessions util client dispatch server hash storage sms
```

SUBDIRS表示在处理目录之前，要递归处理哪些子目录，

**这里还要注意处理的顺序。**

比如我的client对sessions和utils这两上目标文件有依赖，就在client之前需要处理这两个目标文件。

EXTRA_DIST：将哪些文件一起打包。

## 五，关于打包

Automake会自动的打包，自动打包的内容如下：

所有源文件。
所有的Makefile.am文件。
configure读取的文件。
Makefile.am中包含的文件。
EXTRA_DIST指定的文件。

采用dist及nodist指定的文件，如可以将某一源文件指定为不打包：
nodist_client_SOURCES = client.c



# AUTOMAKE_OPTIONS=subdir-objects

这个选项的作用是什么？

所有的automake的options在这里：

https://www.gnu.org/software/automake/manual/automake.html#List-of-Automake-options

这个选项，从名字上看，是subdir（子目录），object（指生成的o文件）。

整体理解就是生成的o文件在各个子目录下。

表示生成的build目录下生成跟代码目录一样对应的目录层次。

这个一般加上就好了。

# 自定义数据的安装

```
voicepromptdir = $(bindir)/../../usr/audio
voiceprompt_DATA = display_module/speak/audio/*
```

这样就会自动把提示音文件安装到目标目录下。



# 参考资料

1、Autotools 使用入门

https://darktea.github.io/notes/2012/06/24/autotools.html

2、

这个很好，可以照着操作。

https://blog.csdn.net/mao834099514/article/details/79544467

3、

https://blog.csdn.net/zmxiangde_88/article/details/8024223

4、

https://zhuanlan.zhihu.com/p/77813702

5、

https://www.cnblogs.com/alexyuyu/articles/3106482.html

6、

这个很好，讲得很详细，照着这个做就好了。

https://blog.csdn.net/pangudashu/article/details/47664639

7、第二部分 Automake的标准工程组织

https://blog.csdn.net/wh8_2011/article/details/78828020

8、

https://blog.csdn.net/weixin_33985507/article/details/85636537

9、

这篇文章非常好。

https://blog.csdn.net/u010020404/article/details/82770848

10、

https://blog.csdn.net/qigaohua/article/details/112028018