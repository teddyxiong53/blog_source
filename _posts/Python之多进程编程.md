---
title: Python之多进程编程
date: 2017-09-22 23:36:05
tags:
	- Python
	- 多进程

---



Python中的多线程并不是真正的多线程，如果想要充分使用多核CPU的话，那么就用多进程吧。

Python提供了一个很好用的多进程库multiprocessing。

multiprocessing支持：子进程、通信、通信数据、同步。

提供了：Process、Queue、Pipe、Lock这些类。

