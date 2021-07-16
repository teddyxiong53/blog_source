---
title: Linux之autotools使用
date: 2019-07-05 11:47:37
tags:
	- Linux
---

1

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

手动修改configure.scan文件。然后把文件改名为configure.ac。

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



一般推荐使用libtool库编译目标，

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