---
title: C语言之goto用法
date: 2020-10-19 15:40:30
tags:
	- c语言
---

1

写代码时出现了这种错误：

```
error: jump to label ‘err2’ [-fpermissive]
```

这个是为什么呢？

就是goto xxx和xxx之间，不能有变量定义。

必须在前面或者后面。

一个都不能有。有一个就报错。



参考资料

1、

https://www.jianshu.com/p/254abfa7caed