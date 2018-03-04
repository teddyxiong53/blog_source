---
title: uboot之gd全局变量
date: 2018-03-04 16:05:59
tags:
	- uboot

---



分析的代码是uboot 2018-02的。

定义是这样的：

```
#define DECLARE_GLOBAL_DATA_PTR		register volatile gd_t *gd asm ("r9")
```

这个指针放在寄存器R9里。

gd指向的结构体是struct global_data 。

