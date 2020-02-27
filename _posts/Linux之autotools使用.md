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



参考资料

1、Autotools 使用入门

https://darktea.github.io/notes/2012/06/24/autotools.html