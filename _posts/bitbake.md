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

# 终极教程

https://a4z.gitlab.io/docs/BitBake/guide.html

这个文档，搭配这个仓库，可以完全探索bitbake的用法。

https://github.com/teddyxiong53/bbTutorial

bitbake可以自己安装。用1.46版本就好了。版本高了的话，教程就不适用了。



# 搭建测试环境

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



https://github.com/conglinux/bitbake-test

直接把这个例子下载下来看看。

但是python3运行不起来。

用virtualenv创建一个python2的环境看看。

这样可以运行起来。

```
virtualenv bb-test -p python2
source bb-test/bin/activate
```

bitbake -s

```
Recipe Name                                    Latest Version         Preferred Version
===========                                    ==============         =================

first                                                 :0.1-r1                          
priority                                               :01-r1                          
second                                                :1.0-r1    
```

https://a4z.gitlab.io/docs/BitBake/guide.html

对应的教程是这里。讲得很详细。



mybuild.bbclass里

```
addtask build
等价于
addtask do_build
```



# bitbake脚本语法

bitbake脚本包括了bb，bbappend，bbclass，conf，还有inc文件。

变量赋值 

```
VARIABLE = "value"

或者

VARIABLE = ‘ I have a " in my value ’

可以对一个变量多次赋值。
```

变量扩展

```
A = “aval”

B = "pre${A}post"

B的值为“preavalpost”
```

设置默认值

```
A ?= "aval"

如果在解析BB脚本时，A没有被定义或赋值，则使用上面的默认值。

注：对同一个变量多次设置默认值，只第一个有效。
```

设置弱默认值

```
A ??= "somevalue"

和普通的设置默认值不同，弱默认值优先级最低。

会在变量没有赋值和设置默认值时起作用，并且赋值发生在脚本解析完成前。

多个设置弱默认值，只有最后一个生效。
```

变量立即扩展

```
这时A的值是“test 123”.

B := "123 ${C}"

C = "cval"

C := "${C}append"

B的值是“123 cval”，C的值是“cvalappend”。

因为使用立即扩展时，如果遇到未定义的变量，会暂时保留扩展操作。
```

Appending += 和 prepending =+

```
B = "bval"

B += "additionaldata"

C = "cval"

C =+ "test"

B的值是“bval additionaldata”，C的值是“test cval”。
```

Variable Flag Syntax

```
这个语法特性是BitBake为了给变量添加属性的一种特殊实现。

直接使用，不需要定义。比如：

FOO[a] = "abc"

FOO[b] = "123"

FOO[a] += "456"

变量FOO有两个flag，[a]和[b]，值分别为"abc"和“abc 456”。
```

嵌入Python变量扩展

```
比如调用func来给FOO赋值：

FOO = “${@func( )}”

举例：

DATE = "${@time.strftime('%Y%m%d',time.gmtime())}"
```

注销变量

```
使用unset关键字，从bitbake的内部字典移除某个变量。

unset VARIABLE
```

给路径赋值

```
注意不要使用“~”，并不会解析成home路径。

要提供全路径来赋值：

BBLAYERS ?= " \

                        /home/scott-lenovo/LayerA \
```



BitBake是一个Python程序，它由用户创建的配置驱动，可以为用户指定的目标执行用户创建的任务

通过一种 BitBake 领域特定语言写 Config、tasks 与 recipes，

这种语言包含变量与可执行的 shell、python 代码。

所以理论上，BitBake 可以执行代码，你也可以用 BitBake 做除**构建软件**之外的事情，但是并不推荐这么做。



BitBake 是一种构建软件的工具，因此有一些特殊的功能，比如可以定义依赖关系。

BitBake 可以解决依赖关系，并将其任务以正确顺序运行。

此外，构建软件包通常包含相同或相似的任务

- 下载源代码包，
- 解压源代码，
- 跑 configure，跑 make，或简单的输出 log。

Bitbake 提供一种机制，可通过一种可配置的方式，抽象、封装和重用这个功能。



运算符

- = 赋值
- ?= 设置默认值 如果变量具有值，则可以保留该值,无则赋值
- ??= 弱默认值 任何" =“或”？=“分配都将覆盖用” ?? ="设置的值
- += =+ 这些运算符在当前值和前置或附加值之间**插入一个空格**
- .= =. 附加或添加值**不插入空格**
- _append 前追加
- _prepend后追加 在可变扩展时间应用的，而不是立即应用的
- _remove 移除 在可变扩展时间应用的，而不是立即应用的
- unset 完全删除变量或变量标志
- export 将变量导出到环境

内联Python变量扩展

```sh
DATE = "${@time.strftime('%Y%m%d',time.gmtime())}"
#DATE变量设置为当前日期。

#此功能最常见的用途可能是从BitBake的内部数据字典中提取变量的值d。
#以下各行分别选择软件包名称及其版本号的值：
PN = "${@bb.parse.BBHandler.vars_from_file(d.getVar('FILE', False),d)[0] or 'defaultpkgname'}"
PV = "${@bb.parse.BBHandler.vars_from_file(d.getVar('FILE', False),d)[1] or '1.0'}"

```

向环境导出变量

```sh
export ENV_VARIABLE
ENV_VARIABLE = "value from the environment"

export ENV_VARIABLE = "variable-value"

#通常导出到环境中的变量是CC和 CFLAGS，许多构建系统都会使用和。
```



bb文件引入和继承

BitBake允许通过包含文件（.inc）和类文件（.bbclass）共享元数据。
例如，假设您具有一项通用功能，例如要在多个配方之间共享的任务定义。在这种情况下，创建.bbclass包含通用功能的文件，
然后inherit 在配方中使用指令继承类将是共享任务的通用方法。

主要包括 include, inherit, INHERIT, and require BitBake

- inherit 编写配方或类文件时，可以使用inherit
  指令继承类（.bbclass）的功能，覆盖配方中继承类的任何值和函数。
- include
  解析您指定的任何文件，并将该文件插入该位置，**路径是相对路径，找不到文件时，include指令不会产生错误。**
- require
  解析您指定的任何文件，并将该文件插入该位置，找不到文件时，require指令会产生错误。
- INHERIT 创建配置文件（.conf）时，可以使用 INHERIT配置指令来继承类。

# 依赖关系

- build time依赖项

1. DEPENDS变量来管理build time依赖性
   [deptask]任务的varflag表示其中列出的每个项目的任务DEPENDS必须先完成，然后才能执行该任务。
2. do_configure[deptask] = “do_populate_sysroot”
   do_populate_sysroot每个项目的任务DEPENDS必须先完成，然后do_configure才能执行。

- 运行时依赖

1. PACKAGES，RDEPENDS和RRECOMMENDS 变量来管理运行时依赖项。
2. PACKAGES变量列出了运行时软件包。每个这些软件包可以拥有RDEPENDS和RRECOMMENDS运行时依赖。在
   [rdeptask]对任务标志用于表示，能够执行任务前，必须完成每个项目的运行时依赖的任务。

- 递归依赖性

1. recrdeptask标志来管理递归任务依赖性。

- 任务间依赖性

1. depends标志来管理任务间依赖性

# bitbake函数

## 函数

BitBake支持以下类型的函数

- Shell函数：用Shell脚本编写并直接作为函数和/或任务执行的函数。也可以由其他Shell函数调用它们。
- BitBake样式的Python函数：用Python编写的函数，并由BitBake或其他Python函数执行
  bb.build.exec_func()。
- Python函数：用Python编写并由Python执行的函数。
- 匿名Python函数：在解析过程中自动执行的Python函数。



自定义任务

```
do_task()

#定义task
python do_printdate () {
   import time
   print time.strftime('%Y%m%d', time.gmtime())
}
#任务间依赖声明
addtask printdate after do_fetch before do_build
#删除任务
deltask printdate

```

提取器

- 本地文件提取器（file://）
- HTTP / FTP wget的提取器（http://，ftp://，https://）
- CVS提取程序（(cvs://）
- Subversion（SVN）提取程序（svn://）
- Git提取程序（git://）
- Git子模块访存器（gitsm://）
- ClearCase访存器（ccrc://）
- Perforce提取程序（p4://）



Yocto tips (5): Yocto如何更改source code的下载与git clone地址

- Yocto中在fetch一些软件包的时候经常出现一天也下载不下来，这种情况极大浪费了我们的时间。
- 确定下载的地址，手动下载
- clone下来以后，我们就可以让软件包使用我们本地的这个repo了，而不需要忙忙的去远程repo去clone。
- 找到软件包对应的bb文件
- 更改bb文件,注意里面添加了一个protocol指定。
- 再一次获取,提示找不到branch，于是我们到我们本地的repo中将此branch切出来，也可以将其制作成bare repo：
- 然后再一次进行fetch就可以了：



# 参考资料

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

6、Bitbake基本语法

https://blog.csdn.net/guoqx/article/details/117447512

7、bitbake

https://blog.csdn.net/super_zhangfei/article/details/120148321

8、官网文档

https://docs.yoctoproject.org/bitbake/2.0/index.html

9、

https://www.codeleading.com/article/77045928434/

10、

https://a4z.gitlab.io/docs/BitBake/guide.html