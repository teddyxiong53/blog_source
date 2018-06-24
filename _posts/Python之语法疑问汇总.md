---
title: Python之语法疑问汇总
date: 2018-06-24 11:37:23
tags:
	- Python

---



## `__str__`和`__repr__`区别

定义一个类Company。

```
class Company(object):
	def __str__(self):
		print "str"
	def __repr__(self):
		print "repr"
company = Company()

print company  #这个调用的就是__str__
company #这个调用的就是__repr__
```

