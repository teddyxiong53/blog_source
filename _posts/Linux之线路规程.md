---
title: Linux之线路规程
date: 2020-05-11 13:41:31
tags:
	- Linux

---

1

在串口驱动里，有线路规程这个概念，这个具体是指什么呢？

线路规程的英文是line discipline，缩写为ldisc。

discipline字面含义是原则。

线路规程是Linux终端子系统的一个软件驱动层。

终端子系统，从上到下可以分为3个层次：

```
顶层 tty core提供 /dev/ttyN 字符设备接口
中间层 就是线路规程，实现终端输入输出的处理策略
底层 tty driver，和硬件通信，对上提供tty_operations给线路规程使用。
```



Linux终端设备缺省的线路规程是N_TTY。

对于输入数据，它处理特殊的中断字符，例如ctrl+c。删除字符等。

当uart作为普通的串口使用时，使用N_TTY线路规程。

当uart作为serial modem的Internet拨号连接时，使用PPP线路规程。



参考资料

1、linux 终端设备 - 线路规程

https://blog.csdn.net/kickxxx/article/details/8512309