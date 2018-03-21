---
title: Python之字符串常用操作
date: 2018-03-21 23:03:11
tags:
	- Python

---



1、查找子串。find和index都可以，带r前缀的，就是从后往前查找。

```
str = "/aa/bb"
print str.index("/")
print str.rindex("/")
print str.find("/")
print str.rfind("/")
```

find没找到，是返回-1 。而index是抛出异常。

