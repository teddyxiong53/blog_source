---
title: Linux之X11了解
date: 2020-03-13 10:42:13
tags:
	- Linux

---

1

什么是X11？它的发展历史是怎样的？当前的发展情况是怎样的？

X11，是X Window System的简称，也可以叫做X，X-Windows。

之所以叫做X，是因为字母表里，X在W字母之后。

MIT开发过一套图形界面系统叫W。

之所以叫X11，是因为在1987年的时候，X Window System已经到了版本11了。

而后续的所有的X，都是基于版本11发展而来。而且没有很大的变化。

为了方便，我们都简称X。



X最开始是由X.org来维护。

后来基于X11R6发展出来专门给X86架构用的X。也叫做XFree86 。

XFree86占据了很大的份额，但是从2004年起，XFree86不再使用GPL协议。

所以很多Linux发行版本，开始弃用XFree86，转而使用Xorg。

现在xorg又称为主流。



X的设计理念是：

```
It is important to decide what a system is not as to what it is.
```

这句话的翻译是：决定一个系统不是什么，跟决定一个系统是什么，这两件事情一样重要。

X只提供实现GUI的框架，

它提供了绘制基本点线面的方法，跟鼠标键盘的交互。

但是不提示button这些具体控件。

X包括3个部分：

```
X server ：守护进程。
X client 
X protocol
```



Qt for embedd linux在这方面则完全不同，它并没有构建在X Window之上，

而是构建在Linux的Framebuffer之上，把在界面上需要显示的内容直接写入了framebuffer。

**因为在嵌入式系统上 把X System给省略了，这样会节省许多的系统开销。**

**而直接写framebuffer，又会加快显示速度。**



# 从fbtft探索x11

现在看fbtft的，看到可以在很小的tft屏幕上显示linux图形界面。

https://github.com/notro/fbtft-spindle/wiki/Appendix#x-windows-backlight-script

而且还提供了不少可操作的系统，我觉得这个可以作为一个了解x11的切入点。

可以同时有2个X windows会话，一个在lcd上，一个在hdmi上。

但是这样有一个问题，就是input device只能属于其中一个。

```
startx -- -layout HDMI &
startx -- -layout TFT &
```

startx 这个命令值得玩味。



# 参考资料

1、

https://www.cnblogs.com/yuanqiangfei/p/11612815.html

2、linux-x11架构

https://www.cnblogs.com/xuzhaoping/p/11074290.html

3、Qt for destop Linux 和 Qt/E最大的区别

https://blog.csdn.net/sh_danny/article/details/6115902