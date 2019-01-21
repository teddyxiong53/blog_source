---
title: Python之魔法方法
date: 2017-09-29 20:43:46
tags:
	- Python

---



# 1. 什么是魔法方法

魔法方法就是可用给你的类增加魔力的特殊方法，注意是针对类的。名字上的特点是前后都有两个下划线。如`__init__`这种。

```
构造相关
	__init__
	__new__
	__del__
操作相关
	比较操作符
        __cmp__
            实现这个就够了。
            类似的还有：__le__/__ge__/...
    数值操作符
    	一元操作符：就是只有一个参数的。
    		__pos__：取正。
    		__neg__：取负。
    		__abs__
    		__invert__
    		__round__
    		__floor__
    		__ceil__
    		__trunc__
    	常见算术操作符：
    		__add__(self, other)
    		__sub__
    		__mul__
    		__floordiv__
    		__div__
    		__mod__
    		__divmod__
    		__pow__
    		__rshift__
    	反射算术运算符：在上面的基础上加上一个r前缀。
    		__radd__(self, other)
    		...
    	增强赋值运算符：就是+=的实现。
    		__iadd__
    		__isub__
    		...
    	类型转换操作符
    		__int__(self)
    		__float__(self)
    		...
类的表示
	就是用字符串来打印类。
	__str__
	__repr__
	__unicode__
	__format__
	__hash__
	__nonzero__
	__dir__
		对应dir(XX)的行为。
访问控制
	很多人抱怨python无法实现真正意义的封装，就是定义私有变量，然后用setter、getter进行访问。
	魔法方法其实可以做到。
	__getattr__
	__setattr__
	__delattr__
	__getattribute__
		这个跟前面的不同，这个只能用于新式类。
		尽量别用这个。
自定义序列
	__len__
	__getitem__
	__setitem__
	__iter__
	__reversed__
	__contains__
	__missing__
反射
	__instancecheck__
	__subclasscheck__
可调用对象
	__call__
	
上下文管理
	__enter__
	__exit__
描述符对象
	 __get__
	 __set__
	 __delete__
拷贝
	__copy__
	__deepcopy__
pickle
	__getinitargs__
	__getnewargs__
	__getstate__
	__setstate__
	__reduce__
	__reduce_ex__
	
```



什么时候使用呢？

自己定义继承了dict、list等基础类的工具类的时候，需要自己实现一些魔法方法。



# 2. 创建相关的

有3个：

`__init__, __new__, __del__`。



`__new__`的特点：

1、是一个对象实例化时调用的第一个方法。

2、`__new__`决定是是否要调用`__init__`方法。

3、主要用途是用来继承一个不可变的类型，比如tuple、string。

4、返回的是一个构建的实例。

举例，用`__new__`来实现一个单例模式。**注意new的的第一个参数是cls，而不是self。**

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

`__del__`在对象被销毁时调用。被垃圾回收器调用。

del xx的时候，不是调用`__del__`。

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





我自己新建一个类，空的。看看有哪些属性。

```
>>> class MyClass():
...     pass
... 
>>> dir(MyClass)
['__doc__', '__module__']
>>> print MyClass.__doc__
None
>>> print MyClass.__module__
__main__
>>> help(MyClass)
Help on class MyClass in module __main__:

class MyClass
```

新建一个继承了object的class。

```
>>> class MyClass2(object):
...     pass
... 
>>> dir(MyClass2)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__']
>>> help(MyClass2)
Help on class MyClass2 in module __main__:

class MyClass2(__builtin__.object)
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
```



参考资料

1、

https://pyzh.readthedocs.io/en/latest/python-magic-methods-guide.html