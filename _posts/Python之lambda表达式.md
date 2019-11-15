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

上面这个是最基本的用法。

还有很多复杂的用法。

lambda表达式是用来创建匿名函数的方式。

lambda的优点是：代码非常简洁。

缺点是：有时候不容易理解。



参考资料

1、求解释此python的lambda表达式

https://segmentfault.com/q/1010000015482828/