---
title: python之并行编程
date: 2019-01-14 13:17:59
tags:
	- python
	- 异步

---



并行编程就是充分利用cpu的多核。

并行计算的内存架构

```
根据指令和数据处理的同时性，分为4种：
1、单指令单数据。SISD。传统的单核cpu的计算机就是这种。
2、MISD。这个没有现实意义。
3、SIMD。gpu编程就属于这种。
4、MIMD。超级计算机。
```

这种分类方法叫费林分类。



参考资料

1、python并行编程

https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter1/index.html



