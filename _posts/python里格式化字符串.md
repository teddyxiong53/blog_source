---
title: python里格式化字符串
date: 2017-06-07 22:00:53
tags:

	- python

---

需要把一个数字用%02这样的方式来格式化一下，再进行使用。

C语言了里是有sprintf这样的函数，Python里是没有的，怎么处理呢？

在Python里有两种方式来格式化字符串，一个是%来格式化，一个是用format函数。

# 1. %符号方式

这种方式跟C的很类似。

语法格式化是：`%[(name)][flags][width].[precision]typecode`。

(name)：这是指定key。

flags：

`+`：右对齐。

`-`：左对齐。

空格：右对齐。

0：右对齐。用0填补空的地方。

width：指定宽度。

.precision：指定小数点位数。

typecode：就是s（字符串），d（整数）这些了。



举例：

```
#!/usr/bin/env python 
num1 = 1
num2 = 2

mystr = "%d--%d"%(num1,num2)
print mystr

```





