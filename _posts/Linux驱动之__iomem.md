---
title: Linux驱动之__iomem
date: 2021-11-04 14:51:25
tags:
	- Linux

---

--

```
我已经看到__iomem用于存储ioremap()的返回类型，但我在ARM架构中使用了u32，它运行良好。

那么 __iomem 在这里有什么区别呢？我应该在什么情况下使用它？

__iomem 是 Sparse 使用的一个 cookie，一个用于查找内核中可能的编码错误的工具。如果您没有在启用 Sparse 的情况下编译内核代码，则无论如何都会忽略 __iomem。
```



参考资料

1、

https://stackoverflow.com/questions/19100536/what-is-the-use-of-iomem-in-linux-while-writing-device-drivers