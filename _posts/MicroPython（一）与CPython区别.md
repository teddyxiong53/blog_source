---
title: MicroPython（一）与CPython区别
date: 2018-02-11 10:57:37
tags:
	- MicroPython

---



决定还是把这个mp转成系列文章。进行系统学习。

# 语法

1、空格。数字和关键字之间要加上空。这个无关紧要。正常写法就行了。

2、mp不支持unicode。

# 语言核心

1、用户自己定义的class，没有实现`__del__`方法。

```
class MyClass():
	def __del__(self):
		print('del func')
mc = MyClass()
del mc
gc.collect()
```

在cpython上调用，会有del func的打印。mp的则没有。

2、方法解析顺序跟cpython不兼容。这个只是在对多继承有影响。不管。

# buildin类型

1、Exception。mp不支持exception链。

```
try:
	raise TypeError
except TypeError:
	raise ValueError
```

cp里两个exception都会打印。而mp只会打印ValueError。





nlr：non-local return

初步看了下mp的代码，还是比较复杂的。

