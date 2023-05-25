---
title: Python之装饰器
date: 2017-11-20 14:26:40
tags:
	- Python

---

--

这个视频讲得很清楚了：

https://www.bilibili.com/video/BV11s411V7Dt

这个总结一些口诀，也不错。

https://www.bilibili.com/video/BV1ZJ411y7Te

这个讲了多种装饰器，也讲得好。讲到了functools.wraps出现的原因。

https://www.bilibili.com/video/BV1Wa4y1x7Kk

# 1. 什么是装饰器



要理解装饰器，需要理解一些函数式编程的概念。

使用装饰器很简单，但是写一个装饰器却比较复杂。

內建函数globals得到一个dict，包含了Python能够识别到的变量的情况。

变量有作用范围和生命周期，就是有空间和时间限制。

Python运行函数内部再定义函数。

Python里，函数和其他任何东西都是对象。这一点我们可以用issubclass(int, object)这样来进行证明。

Python里的类也是对象。这就弄得有点迷糊了。不过从实用角度出发，我们可以不纠缠这些细节。





先看下面的代码。感觉还能理解。

```
#!/usr/bin/python 

def outer():
	def inner():
		print "inner func"
	return inner
	
foo = outer()
foo()
```

接下来我们要看闭包的概念。我们先把上面这段代码再改一下。

```
#!/usr/bin/python 

def outer():
	x = 1
	def inner():
		print x
	return inner
	
foo = outer()
foo()
print foo.func_closure
```



Python支持一种名叫函数闭包的特性。英语叫做func_closure。

闭包代表的实际意义是这样的：

在非全局作用域定义的inner函数，它会记得它的外层的命名空间的样子。

**闭包的存在意义，就是为了实现装饰器的。**

好，到这里，我们可以给装饰器一个明确的定义了。

1、装饰器是一个函数。

2、特点是：**用函数名作为参数输入。返回的也是一个函数名。**

我们先写一个简单的装饰器。

```
#!/usr/bin/python 

def outer(some_func):
	def inner():
		print "before some_func"
		ret = some_func()
		return ret+1
	return inner
	
def foo():
	return 1
	
decorated = outer(foo)
print decorated()

```

我们可以说decorated函数是foo函数的装饰版本。

但是在实际中，我们不想再为装饰版本另外取一个名字了。我们就用foo这个名字。

```
foo = outer(foo)
```

你后面再用foo，其实就已经是装饰过的了。

```
foo = outer(foo)
print foo
```

看到的结果是这样的：

```
pi@raspberrypi:~/work/test/py-test$ ./test.py 
<function inner at 0x76af6430>
```

# 装饰器的分类


Python 装饰器可以根据其应用和功能进行不同的分类。下面是一些常见的装饰器分类：

1. 函数装饰器（Function Decorators）：这是最常见的装饰器类型，它们用于修改、增强或包装函数的行为。函数装饰器在函数定义之前使用 `@` 符号进行声明，并将目标函数作为参数传递给装饰器函数。常见的函数装饰器包括 `@property`、`@staticmethod`、`@classmethod` 等。
2. 类装饰器（Class Decorators）：类装饰器用于修改、增强或包装类的行为。与函数装饰器类似，类装饰器也使用 `@` 符号进行声明，并将目标类作为参数传递给装饰器类。类装饰器可以在类定义之前或之后应用，并对类进行修改或封装。类装饰器的使用相对较少，但在某些场景中非常有用。
3. 方法装饰器（Method Decorators）：方法装饰器用于修改、增强或包装类的方法行为。方法装饰器在方法定义之前使用 `@` 符号进行声明，并将目标方法作为参数传递给装饰器函数。方法装饰器可以应用于实例方法、静态方法和类方法，用于扩展其功能或为其提供额外的行为。
4. 参数化装饰器（Parameterized Decorators）：参数化装饰器是一种装饰器，它本身接受参数并返回实际的装饰器函数。这样的装饰器可以根据传入的参数动态地生成不同的装饰器。参数化装饰器可以通过额外的函数嵌套层次或使用类来实现。
5. 类型检查装饰器（Type Checking Decorators）：这些装饰器用于在运行时对函数参数和返回值进行类型检查。它们可以帮助捕获类型错误并提供更强的类型安全性。常见的类型检查装饰器包括 `mypy`、`pylint` 等第三方库提供的装饰器。

# 2.一个实用的实例

假设我们现在要用一个二维坐标对象的库。坐标对象不支持数学运算。

现在我们要做的事情有：

1、给它加上加减运算。

```
#!/usr/bin/python 

class Coordinate(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def __repr__(self):
		return "coordinate:" + str(self.__dict__)
		
def add(a,b):
	return Coordinate(a.x+b.x, a.y+b.y)
	
def sub(a,b):
	return Coordinate(a.x - b.x, a.y - b.y)
	
p1 = Coordinate(100,200)
p2 = Coordinate(200,300)

print add(p1, p2)
```

然后我们希望在加减运算的时候，进行范围限制。

如果值小于0了，那么就给0，反正保证值不小于0 。

增加如下代码：

```
def wrapper(func):
	def checker(a,b):
		if a.x <0 or a.y < 0:
			a = Coordinate(a.x if a.x >0 else 0, a.y if a.y>0 else 0)
		if b.x <0 or b.y < 0:
			b = Coordinate(b.x if b.x >0 else 0, b.y if b.y> 0 else 0)
		ret = func(a,b)
		return ret
add = wrapper(add)
sub = wrapper(sub)
```

实际上，`add = wrapper(add)`这种写法，Python给我们提供了一种更加简洁的方法来做，就是@符号。

可以可以这样来写：

```
@wrapper
def add(a, b):
	#xxxxx
```



装饰器有4种情况：

```
主体有2个：函数和类。
组合起来就是4种情况。
函数装饰函数。
函数装饰类。
类装饰函数。
类装饰类。
```



## 函数装饰函数

```
def myWrapper(func):
    def inner(a,b):
        print "xhl func wrapper func"
        r = func(a,b)
        return r
    return inner

@myWrapper
def myadd(a, b):
    return a+b
print myadd(1,2)
```

## 函数装饰类

相当于在构造函数之前执行。

```
def myWrapper(cls):
    def inner(a):
        print 'class name:', cls.__name__
        return cls(a)
    return inner

@myWrapper
class Foo():
    def __init__(self, a):
        self.a = a
    def func(self):
        print "self.a=", self.a

f = Foo('xhl')
f.func()
```

## 类装饰函数

```
class ShowFuncName():
    def __init__(self, func):
        self._func = func
    def __call__(self, a):
        print "func name:", self._func.__name__
        return self._func(a)

@ShowFuncName
def bar(a):
    return a
print bar('xhl')
```

# 参数化装饰器

```
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")

```



# python自带的常用装饰器

## @property

```
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def diameter(self):
        return self.radius * 2

    @diameter.setter
    def diameter(self, value):
        self.radius = value / 2

circle = Circle(5)

print(circle.radius)    # 输出：5
print(circle.diameter)  # 输出：10

circle.diameter = 14
print(circle.radius)    # 输出：7
print(circle.diameter)  # 输出：14

```

Python 自带的一些常用装饰器包括：

1. `@property`: 将方法转换为只读属性，允许通过属性访问的方式调用方法。
2. `@staticmethod`: 将方法定义为静态方法，不需要访问实例属性或调用实例方法，直接通过类名调用。
3. `@classmethod`: 将方法定义为类方法，可以访问类属性，并通过类名调用或在子类中进行覆盖。
4. `@abstractmethod`: 用于定义抽象方法，必须在子类中实现，否则会引发 `TypeError`。
5. `@staticmethod` 和 `@classmethod` 都是用于修饰类方法的装饰器，**两者之间的主要区别是 `@classmethod` 可以访问类的属性，而 `@staticmethod` 不能。**

```
from abc import abstractmethod

class MyClass:
    @property
    def my_property(self):
        return "This is a property"

    @staticmethod
    def my_static_method():
        return "This is a static method"

    @classmethod
    def my_class_method(cls):
        return f"This is a class method of {cls.__name__}"

    @abstractmethod
    def my_abstract_method(self):
        pass

class MyDerivedClass(MyClass):
    def my_abstract_method(self):
        return "Implementation of abstract method"

obj = MyClass()

print(obj.my_property)
print(MyClass.my_static_method())
print(MyClass.my_class_method())

derived_obj = MyDerivedClass()
print(derived_obj.my_abstract_method())
```



staticmethod和classmethod的区别举例：

```
class MyClass:
    class_attribute = "Class Attribute"

    @staticmethod
    def static_method():
        return "Static Method"

    @classmethod
    def class_method(cls):
        return f"Class Method. class_attribute: {cls.class_attribute}"

obj = MyClass()

# 调用静态方法
print(obj.static_method())  # 输出：Static Method
print(MyClass.static_method())  # 输出：Static Method

# 调用类方法
print(obj.class_method())  # 输出：Class Method. class_attribute: Class Attribute
print(MyClass.class_method())  # 输出：Class Method. class_attribute: Class Attribute


```



# 参考资料

1、python装饰器的4种类型：函数装饰函数、函数装饰类、类装饰函数、类装饰类

https://blog.csdn.net/xiemanR/article/details/72510885