---
title: Linux内核之bin_attribute
date: 2018-04-02 16:30:30
tags:
	- Linux内核

---



bin_attribute和attribute有什么不同？

1、bin_attribute比attribute多了一个size变量来描述文件大小。而普通的attribute文件总是4096字节。就是一个page的大小。

2、bin_attribute多了mmap接口的支持。