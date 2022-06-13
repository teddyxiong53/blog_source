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



bitbake脚本语法

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

6、Bitbake基本语法

https://blog.csdn.net/guoqx/article/details/117447512

7、bitbake

https://blog.csdn.net/super_zhangfei/article/details/120148321

8、官网文档

https://docs.yoctoproject.org/bitbake/2.0/index.html