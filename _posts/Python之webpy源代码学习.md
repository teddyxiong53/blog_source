---
title: Python之webpy源代码学习
date: 2017-10-01 11:45:08
tags:
	- Python
	- webpy

---



webpy的代码量不是很大，可以用做学习材料。

策略：

1、先读utils.py这个工具模块，这个是基础，不依赖整个系统运行。

2、 webpy的doctest用得很好。每个文件都可以单独运行，方便观察函数的运行结果，加深理解。

方法：把testmode的verbose模式打开。就可以观察测试的详细打印信息。

```
doctest.testmod(verbose=True)

```



