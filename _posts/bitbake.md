---
title: bitbake
date: 2019-06-22 16:38:37
tags:
	- 编译
---



bitbake是自动化构建工具。类似与make。但是比make要强大。

主要用来收集和管理大量没有依赖关系的描述文件，然后自动按照正确的顺序进行构建。



这里还涉及到一个概念：OpenEmbedded。

这个是类似buildroot的东西。

在程序员看来，OpenEmbeded是由shell脚本、python脚本和一些数据文件组成。



我们先用bitbake构建一个最小工程。

bitbake是用python写的。

先安装bitbake。bitbake没法通过apt-get来安装。

bitbake是openembeded下面的一个项目。

代码地址在这里：

https://github.com/openembedded/bitbake

安装很简单：

```
1、把bitbake/bin添加到PATH环境变量。
2、把bitbake/lib添加到PAYTHONPATH环境变量。
```

新建目录结构如下：

```
hlxiong@hlxiong-VirtualBox:~/work/test/bitbake/bbTutorial$ tree
.
├── build
│   ├── conf
│      └── bblayers.conf
└── meta-tutorial
    ├── classes
    │   └── base.bbclass
    └── conf
        ├── bitbake.conf
        └── layer.conf
```

bitbake.conf和base.bbclass从bitbake的目录下拷贝出来。

bblayers.conf内容如下：

```
BBPATH := "${TOPDIR}"
BBFILES ?= ""
BBLAYERS = "${BBPATH}/../meta-tutorial"
```

layer.conf内容如下：

```
BBPATH .= ":${LAYERDIR}"
BBFILES += ""
```

然后我们进入到build目录，执行bitbake。

如下，则是正常的。

```
hlxiong@hlxiong-VirtualBox:~/work/test/bitbake/bbTutorial/build$ bitbake
Nothing to do.  Use 'bitbake world' to build everything, or run 'bitbake --help' for usage information.
```

我们可以用verbose模式看看详细日志：

```
bitbake -vD
```



参考资料

1、bitbake 使用指南

https://blog.csdn.net/lu_embedded/article/details/80634368

2、OpenEmbedded 入门 （一）：OpenEmbedded 简介

https://www.cnblogs.com/fah936861121/articles/7193137.html

3、Buildroot vs OpenEmbedded or Yocto Project

https://www.jianshu.com/p/eb6f7f7d5a97

4、Welcome to OpenEmbedded

http://www.openembedded.org/wiki/Main_Page

5、BitBake 实用指南

https://www.jianshu.com/p/2b5df45e614f