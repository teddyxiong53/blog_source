---
title: Linux之检查socket状态变化
date: 2020-05-06 16:34:51
tags:
	- Linux
---

1

我现在有个需求，就是希望知道某个listen状态的socket，是否有client连接过来，状态变成establish。

是在进程外面。不改动程序的代码。

希望依赖类似文件系统的inotify类似的机制来做。

先是在谷歌上搜索到systemtap这个东西。

看看systemtap可以做到哪些事情。



systemtap是一个跟dtrace类似的工具。

安装：

```
sudo apt install systemtap
```

这个安装完之后的命令是stap。而不是systemtap。

stap运行，需要脚本文件，脚本文件，一般以stp为后缀。

也可以在脚本头部加上：

```
#!/usr/bin/stap
```

安装工具的时候，默认给带了很多有用的脚本。

在/usr/share/systemtap/tapset目录下。



典型应用

不知道哪个进程在进行大量的写入操作。可以用这个来查出来。



systemtap是内核开发者必须用要掌握的一个工具。

为什么会产生systemtap这种工具？

假设现在有这样的一个需求：获取正在运行的Linux系统的系统调用的情况。

最原始的解决办法是：

在内核里加上我们的代码，编译安装内核，这种方式效率非常低，而且如果需求有变动，得反复做这种操作。

后来内核引入了kprobe机制。可以用来动态地收集调试和性能信息。是一种非破坏性的工具。

用户可以用kprobe机制来跟踪内核里任何的函数。

这个相比于之前的方法，是有了本质的改变。但是没有提供一个易用的框架。用户需求自己去写模块，然后安装模块。这样还是有较高的门槛的。

systemtap则是利用kprobe提供的api来实现动态地监控和跟踪Linux内核。

用户只需要编写systemtap脚本即可。



但是，使用systemtap也有前提条件，就是需要内核里带调试信息。

```
1、用-g选项编译内核。
2、内核选配kprobe和debugfs。
```

这个还是要编译内核，很多时候，也是不方便的。

但是，也可以有其他的方法来做。

其实，你在安装systemtap的时候，默认就帮你把匹配你电脑版本的带调试信息的内核镜像下载了下来了。



参考资料

1、Systemtap 两个实用的小例子

https://www.jianshu.com/p/84b3885aa8cb

2、systemtap

https://baike.baidu.com/item/systemtap/4328222?fr=aladdin

3、内核探测工具systemtap简介

https://www.cnblogs.com/rex-2018-cloud/p/10442583.html