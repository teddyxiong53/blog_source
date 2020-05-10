---
title: Python之GIL
date: 2018-06-18 10:22:59
tags:
	- Python

---



GIL是Global Interpreter Lock。全局解释器锁。

因为CPython解释器本身就不是线程安全的。

这里讲解比较清楚。

https://www.bilibili.com/video/BV12x411R7Wr

cpython的多线程就是假的。

你在一个进程里写2个线程，线程就是执行pass。在一个双核的电脑上。实际表现是，每个核心只占用50%。

如果使用2个进程，则可以2个核心都占用100%。

现在为什么不优化掉呢？因为很难移除。之前尝试解决过，没法完美解决。

而且多进程可以绕过这个问题。

还有可以通过python调用C语言函数来做一些计算密集型的操作，也可以解决这个问题。





参考资料

1、深入理解 GIL：如何写出高性能及线程安全的 Python 代码

http://python.jobbole.com/87743/