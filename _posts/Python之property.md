---
title: Python之property
date: 2018-06-10 11:26:54
tags:
	- Python

---



看代码看到`@property`这个内容。了解一下。



我们在定义数据库字段类的时候，往往需要对其中的类属性做一些限制，一般是用get和set方法来写。

在Python里，怎样才能少写代码，用更加优雅的方式来实现呢？

这个就是property这个装饰器的作用了。

先看一个例子。

一个类Student，属性有成绩。

```
#!/usr/bin/python

class Student(object):
	def get_score(self):
		return self._score
		
	def set_score(self, value):
		if not isinstance(value, int):
			raise ValueError('score must be a integer')
		if value < 0 or value > 100:
			raise ValueError("value must be 0 <= value <= 100")
		self._score = value
		
s = Student()
s.set_score(60)
print s.get_score()

s.set_score(60.5)
print s.get_score()
```



但是s.set_score(60)这种写法，比s.score这种写法要麻烦，我们怎么可以用后面这种方式，而且要要保证把检查做了呢？

这么改。

```
class Student(object):
	@property
	def score(self):
		return self._score
		
	@score.setter
	def score(self, value):
		if not isinstance(value, int):
			raise ValueError("score must be integer")
		if value <0 or value > 100:
			raise ValueError("0 <= score <= 100")
		self._score = value
		
s = Student()
s.score = 90
print s.score
```

这样get和set，都可以直接用s.score来做了。



# 参考资料

1、对于Python中@property的理解和使用

https://blog.csdn.net/u013205877/article/details/77804137