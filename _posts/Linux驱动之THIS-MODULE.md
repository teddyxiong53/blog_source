---
title: Linux驱动之THIS_MODULE
date: 2018-03-26 17:35:20
tags:
	- Linux驱动

---



在Linux驱动里，经常看到THIS_MODULE这个宏。

这个宏具体代表了什么样的内涵呢？

先看定义的地方：

```
#ifdef MODULE
extern struct module __this_module;
#define THIS_MODULE (&__this_module)
#else
#define THIS_MODULE ((struct module *)0)
#endif
```

