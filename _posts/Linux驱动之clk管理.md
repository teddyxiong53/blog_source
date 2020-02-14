---
title: Linux驱动之clk管理
date: 2018-03-01 11:29:17
tags:
	- Linux驱动

---

1

clk framework是用内核用来统一管理clock的子系统。

代码在driver/clk目录下。

主要的结构体：

```
struct clk_ops
	函数指针。
	是soc厂家需要实现的。
	
```



参考资料

1、linux clk驱动框架

https://blog.csdn.net/rikeyone/article/details/51672720

