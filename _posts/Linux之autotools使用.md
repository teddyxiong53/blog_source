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



参考资料

1、Autotools 使用入门

https://darktea.github.io/notes/2012/06/24/autotools.html

2、

这个很好，可以照着操作。

https://blog.csdn.net/mao834099514/article/details/79544467

3、

https://blog.csdn.net/zmxiangde_88/article/details/8024223