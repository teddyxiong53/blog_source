---
title: qt之qmake文件编写
date: 2021-06-22 19:39:33
tags:
	- qt

---

--

我们编写Qt应用程序时，

不管使用Qt Creator还是VS或者Eclipse，

不管是Qt Widgets还是Qt Quick，

总会发现有.pro文件，

**我们称.pro文件为Qt的工程管理文件，**

它存在的目的是列举工程中包含的源文件。

类似于makefile，

**一个工程中可以包含一个或多个.pro文件。**

因此对于使用Qt的开发人员来说，熟悉.pro工程文件的语法，懂得阅读和修改.pro文件，

将有利于对项目工程的文件组织和管理。



qmake、.pro文件、makefile文件的关系简单来说就是：

qmake工具使用了与平台无关的.pro文件生成与平台相关的makefile文件。



所以虽然本文标题为.pro文件语法学习，实际上应该是qmake的语法学习，

但是因为IDE把qmake隐藏起来了，我们接触地更多的是.pro文件，因此还是使用这样的标题。



**TARGET变量 & TEMPLATE变量 & CONFIG变量：**

首先我们需要知道工程文件主要分为三种：

app（单独的应用程序）

lib（静态或动态库）

subdirs（递归编译）。

工程文件的类型可以使用TEMPLATE变量来指定。



TARGET是用来定义应用程序的名字的，

而程序的扩展名则由TEMPLATE来定义。

例如：TARGET = hello，TEMPLATE = app，

则在Linux下会生成hello（无后缀的ELF可执行文件），对应的在Windows下会生成hello.exe。



TEMPLATE和CONFIG共同定义了目标类型，以下是几种常见情况：

TEMPLATE = app，生成标准程序（注意如果没有TEMPLATE这一项，那么默认工程就是app）。

TEMPLATE = subdirs，子项目工程模板，可以用它来创建一个能够进入特定目录并且编译子目录里的目标文件。此时除了TEMPLATE = subdirs，还需要指定SUBDIRS变量，在每个子目录中，qmake会搜寻以目录命名的.pro文件，并且会编译该工程。

TEMPLATE = lib，生成库文件，**若不指定CONFIG变量，则编译为共享库；若CONFIG += staticlib**，则编译为静态库；若CONFIG += plugin，则编译为插件（插件总是动态库）。


**.pro文件中的注释：**
　　注释以井号（#）开头，在行尾处结束。

**.pro文件中的一个条目的语法通常具有如下形式：**

```
variable = values
```

那就只能直接去kernel的配置里手动加了。这样反而好点。

menuconfig方式有点乱。



```
qtHaveModule(dbus): SUBDIRS += dbus
```

这个属于qmake内置的测试函数。





参考资料

1、Qt的.pro工程文件语法学习

https://blog.csdn.net/lu_embedded/article/details/50522921

2、

https://doc.qt.io/qt-5/qmake-test-function-reference.html

3、官网手册

https://doc.qt.io/qt-5/qmake-manual.html