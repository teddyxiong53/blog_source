---
title: Python之抽象类
date: 2017-11-20 20:11:24
tags:
	- Python

---



Python语言本身没有提供抽象类、接口这些内容。如果需要，要依赖一个叫abc的模块。

abc.py的abc是ABstract Class的缩写。这个模块提供了一个元类ABCMeta和一组装饰器`@abstractmethod`、`@abstractproperty`。

使用时，这么用：

```
#!/usr/bin/python

from abc import ABCMeta, abstractmethod, abstractproperty

class People:
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def set_name(self, name):
		pass
		
	@abstractproperty
	def pro(self):
		pass
		
```

要定义抽象类：

1、要把元类设置为ABCMeta。这个是必须的。因为抽象类的实现离不开元类。

2、用@abstractmethod和@abstractproperty修饰的内容，子类必须进行实现。





