---
title: Linux之telnet交叉编译
date: 2018-10-08 15:58:17
tags:
	- Linux

---



busybox里把telnet的关闭了。但是不方便重新编译busybox，所以想要找一个第三方的telnetd程序。

尝试了这些方式：

1、inetutils。这个需要被inetd启动。没有弄起来。麻烦。

2、utelnetd。这个死活没有找到代码。

最后用dropbear搞定的。

