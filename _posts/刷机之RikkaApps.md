---
title: 刷机之RikkaApps
date: 2020-12-21 13:32:30
tags:
- 刷机
---

1



官网：

https://rikka.app/zh-hans/

代码：

https://github.com/RikkaApps



rikka和riru是什么关系？

Rikka相当于一个项目组，下面有多个项目，Riru是其中一个。



riru是什么意思？

Riru只有一个作用，就是注入到zygote进程，从而可以运行特定的代码。

Riru对于Android6.0以后的机器，需要机器用magisk root过。

安装方法：

有几种安装方法，任选其中一中就好：

方法一：在Magisk Manager里搜索Riru，安装。

方法2：在Riru的github release里下载zip包进行安装。

配置方法：

当/data/adb/riru/disable文件存在的时候，Riru会被禁用。

当/data/adb/riru/enable_hide文件存在的时候，隐藏机制会被使能。



Riru的工作原理

怎样注入到zygote进程的？

在v22.0之前，使用的方法是替换掉一个系统库，libmemtrack，这个库会被zygote载入。

这种方式导致了一些奇怪的问题。

所以换了一种非常简单的方式，使用native bridge（ro.dalvik.vm.native.bridge）。



参考资料

1、

