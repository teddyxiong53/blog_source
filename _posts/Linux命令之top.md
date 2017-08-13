---
title: Linux命令之top
date: 2017-08-11 21:14:24
tags:
	- Linux

---

top是最常用的Linux性能监控工具，有点类似windows下的任务管理器，可以看到各个程序的CPU占用情况和内存占用情况。

最早的ps命令，是基于ps命令来做的，后面重构了，为了可以支持proc文件系统，后面又陆续经历了几次大的重构，才有今天的模样。

# 1. top命令输出内容分析

最简单的使用方法就是输入top，然后就可以看到输出内容了。内容总体上分为两个部分：一个是系统信息，一个是进程信息。

下面是一个top命令输出的系统信息部分。现在我们分析一下所有的数据代表的含义。

```
teddy@teddy-ubuntu:~$ top
top - 23:21:32 up  1:07,  3 users,  load average: 0.00, 0.01, 0.05
Tasks: 269 total,   1 running, 268 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.2 us,  0.2 sy,  0.0 ni, 99.4 id,  0.2 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   3864528 total,  1389344 used,  2475184 free,   306556 buffers
KiB Swap:  3916796 total,        0 used,  3916796 free.   479536 cached Mem
```

其实很简单，这个内容之前在其他命令里都有谈到的。不做展开了。

# 2. top的输出配置

top输出的内容是可以进行配置的，而且配置的内容可以保存起来，是在`~/.toprc`里。

保存的方法是：在top运行时，输入大写字母W，就可以保存了。

内容是这样的。

```
teddy@teddy-ubuntu:~$ cat .toprc 
top's Config File (Linux processes with windows)
Id:h, Mode_altscr=0, Mode_irixps=1, Delay_time=3.0, Curwin=0
Def     fieldscur=&')*+,-./012568<>?ABCFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
        winflags=193844, sortindx=18, maxtasks=0
        summclr=1, msgsclr=1, headclr=3, taskclr=1
Job     fieldscur=+,-./012568>?@ABCFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
        winflags=193844, sortindx=0, maxtasks=0
        summclr=6, msgsclr=6, headclr=7, taskclr=6
Mem     fieldscur='()*+,-./0125689BFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
        winflags=193844, sortindx=21, maxtasks=0
        summclr=5, msgsclr=5, headclr=4, taskclr=5
Usr     fieldscur=+,-./1234568;<=>?@ABCFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
        winflags=193844, sortindx=3, maxtasks=0
        summclr=3, msgsclr=3, headclr=2, taskclr=3
Fixed_widest=0, Summ_mscale=0, Task_mscale=0, Zero_suppress=0
```

# 3. top的一些技巧

1、在top界面，输入数字1，可以看到多核的情况。

