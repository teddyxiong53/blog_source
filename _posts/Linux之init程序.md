---
title: Linux之init程序
date: 2018-01-28 10:36:38
tags:
	- Linux
	- init

---



Linux系统的启动首先从bios开始，然后是bootloader把内核镜像load到内存，内核然后启动init进程。

init进程是系统的第一个进程，pid为1，也叫做根进程。它负责产生其他所有用户进程。

一个进程的父进程退出了，这个进程就成为孤儿进程了，那么它就会被挂到init进程下。相当于被init进程收养了。init进程是所有进程的祖宗，它有这个义务。

（pid为0的是内核的一部分，主要用于内存换页操作）

init程序发展也经过了几个阶段，依次是sysvinit、upstart、systemd。

# sysvinit

init和传统的uinx system V是兼容的，所以也叫sysvinit。发布于1983年，在unix system V里带的。

sysvinit下有几种运行模式，叫runlevel。

配套的目录有：

```
/etc/init.d/
/etc/rc[X].d, X取值就是runlevel的数字了。
```



# upstart

sysvinit用了多年，也算稳定。但是现在时间来到了2006年，linux内核进入到具有里程碑意义的2.6版本，有了很多革命性的更新。**而且linux开始进军桌面系统。**

桌面系统跟服务器系统的不同在于，**桌面系统经常会开关机，而且用户会经常进行热拔插操作。sysvinit对于这些场景难以应付。**

**sysvinit没有自动检测的机制，它只能一次性启动所有的服务。**

Ubuntu的开发人员在评估了几种可选的init系统后，决定自己重新设计这个系统。于是就有了upstart。

upstart基于事件驱动机制，把之前完全串行的同步启动服务的方式改成了由事件驱动的异步的方式。

这样很多事情可以并行走，用事件进行通信来同步。

**但是upstart也有缺点，就是事件设计得比较复杂凌乱。但是还是得到了广泛应用。**

# systemd

时间又来到了2010年，RedHat的工程师开始研发新的init系统，就是systemd，这是一个很有野心的项目，它不仅想要取代已有的init系统，而且还想干更多的事情。

**RedHat觉得upstart不错，但是不够快。并行化处理，还是有相互等待的情况。**

RedHat认识和到，init系统的第一目标就是让用户可以快速进入到桌面操作环境。

所以systemd的设计原则就2条：

1、少启动东西。

2、尽量并行化。

用C语言取代传统的脚本式的启动。脚本启动过程中，生成了很多进程，这些进程只做了一点点事情就退出。这个是一个比较大的优化点。

systemd是成功的。

但是也引起了很大的争议。最大的争论点就是systemd破坏了UNIX的设计哲学，做了一件大而全而且相当复杂的事情。不过RedHat不同意这个观点。

2014年，debian为了要换systemd，在网上起了大的争论，导致了Debian的分裂。

不过，到今天，systemd已经是绝对的主流了。



Ubuntu的etc目录下，不仅有system的，还有init.d的。

这两种启动脚本机制，如何进行共存？

先说结论，只能有一种init机制在起作用，在Ubuntu16.04上，是systemd。

但是实际上安装了多套init机制，但是不能同时运行。

systemd在设计上，已经考虑了兼容之前是sysvinit和upstartd。

一个sysvinit的init.d脚本，不一定会被执行。

例如，我们一般使用Ubuntu带图形界面启动的，是level5。

看/etc/rc5.d下面，只有这下面的脚本才会被执行，而这些脚本都是软链接，执行init.d目录下的脚本，但不是全部。例如network-manager就没有。

所以network-manager的，就是systemd自己去管理的。







systemd是怎样管理sysvinit的init.d脚本的呢？



早期的Linux发行版本，包括MCC和TAMU。Miquel van Smoorenburg这个人创造的sysvinit。sysvinit最初是为minix开发的，1992年2月开发，7月移植到Linux上。

```
MCC是Manchester computer  center的缩写。
1992年发布。
这个第一个面向普通用户的Linux发行版本。
基于菜单的安装程序。
内核是Linux0.12 。
```

```
TAMU
是德州的一个大学。
```

sysvinit有两种风格：

```
1、inittab + rc.x.d风格。
2、init.d风格。
```

slackware选择了第一种风格，而debian选择了第二种风格。

systemd的基础单元是service unit。是一些以service为后缀的脚本。

有4个地方会有这些脚本：

```
/etc/systemd/system
/run/systemd/system
/usr/local/lib/systemd/system
/usr/lib/systemd/sytem
```

兼容rc脚本，是靠一个转换工具，叫systemd-sysv-generator。



service命令就是跟sysvinit配套的命令。

而systemctl就是跟systemd配置的。



跟踪service命令的执行。

sudo strace service network-manager restart





参考资料

1、

https://www.ibm.com/developerworks/cn/linux/1407_liuming_init1/index.html

2、SysV, Upstart and systemd init script coexistence

https://askubuntu.com/questions/867843/sysv-upstart-and-systemd-init-script-coexistence

3、What init system was used in early Linux distributions?

https://retrocomputing.stackexchange.com/questions/8289/what-init-system-was-used-in-early-linux-distributions/8290#8290