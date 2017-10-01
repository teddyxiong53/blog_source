---
title: Python之lambda表达式
date: 2017-09-30 23:47:50
tags:
	- Python

---



对于一般的if else，我们可以用三元运算来表示。例如：

```
if True:
	name = "xxx"
else:
	name = "yyy"
可以表示为：
name = "xxx" if True else "yyy"
```

lambda表达式是用类似的方法来处理简单的函数的。lambda就把简单函数写得更加简洁，就是这个作用。

例如：

```
def myfunc(arg):
	return arg+1

my_lambda = lambda arg: arg+1
my_labmda(123)
```



