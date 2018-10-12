---
title: cpp之构造函数的default和delete
date: 2018-10-12 17:03:51
tags:
	- cpp
---



一般是这样：

```
Env() = default;//默认存在，可以构造。
Env(const Env&) = delete;//不允许拷贝构造。
```



# 参考资料

1、C++构造函数的default和delete

https://blog.csdn.net/u010591680/article/details/71101737