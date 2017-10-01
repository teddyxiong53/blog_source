---
title: Python之魔法方法
date: 2017-09-29 20:43:46
tags:
	- Python

---



# 1. 什么是魔法方法

魔法方法就是可用给你的类增加魔力的特殊方法，注意是针对类的。名字上的特点是前后都有两个下划线。如`__init__`这种。



# 2. 创建相关的

有3个：

`__init__, __new__, __del__`。



`__new__`的特点：

1、是一个对象实例化时调用的第一个方法。

2、`__new__`决定是是否要调用`__init__`方法。

3、主要用途是用来继承一个不可变的类型，比如tuple、string。

4、返回的是一个构建的实例。

举例，用`__new__`来实现一个单例模式。

```
class Person(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age
		
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, 'instance'):
			cls.instance = super(Person, cls).__new__(cls)
		return cls.instance
		
p1 = Person(20, 'a')
p2 = Person(21, 'b')
print p1 == p2

```

可以看到结果的True。

`__del__`在对象被销毁时调用。



# 3. 成员相关的

也有3个。`__call__, __getitem__, __setitem__`。

`__call__`允许一个类的实例像函数一样被调用。看下面的例子。

```
class Person(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self.instance = add
		
	def __call__(self, *args):
		return self.instance(*args)
		
def add(args):
	return args[0] + args[1]
	
p = Person(20, 'a')
print p([1,2])

```

`__getitem__`定义获取容器中指定元素的行为。相当于self[key]。

```
class Person(object):
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self._resgitry = {
			'name': name,
			'age': age
		}
		
	def __call__(self, *args):
		return self.instance(*args)
		
	def __getitem__(self, key):
		if key not in self._resgitry.keys():
			raise Exception('please register key :%s ' % (key, ))	
		return self._resgitry[key]
	
p = Person('a', 20)
print p.age

```



# 4. 属性相关的

`__getattr__, __setattr__, __delattr__, __get__, __set__ , __delete__, __getattribute__`。

