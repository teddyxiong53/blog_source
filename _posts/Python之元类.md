---
title: Python之元类
date: 2017-11-20 20:28:17
tags:
	- Python

---



在理解元类之前，需要先掌握Python的类。Python里类的概念借鉴自Smalltalk。

Smalltalk是历史上公认的第二个面向对象的编程语言（第一个是simula 67），Smalltalk直接影响了后续的大部分面向对象的编程语言，被称为面向对象编程之母。这个语言来自于施乐公司。

相比于其他的面向对象语言，Python的类包括了更多。

类也是对象。你定义了一个类之后，这个类就是一个对象了。

# 动态创建类

因为类也是对象，所以可以在运行时动态创建。所以可以在函数里使用class关键字。

```
def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo
    else:
        class Bar(object):
            pass
        return Bar

MyClass = choose_class('foo')
print MyClass
```

输出情况：

```
C:\Python27\python.exe D:/work/pycharm/py_test/test.py
<class '__main__.Foo'>
```



# 什么是元类

元类就是类的父亲。

我们定义类，是为了用类来得到实例。

我们定义元类，就是为了用元类来得到类。

**函数type其实就是一个元类。type就是Python里用来创建所有类的元类。**

str是用来创建字符串对象的类。



type函数可以用来动态创建类。

语法是：

```
type(类名，父类的元组（可以为空），属性字典)
```

```
In [1]: Foo = type("Foo", (), {"a":1}
   ...: )

In [2]: type(Foo)
Out[2]: type

In [3]: x = Foo()

In [4]: x.a
Out[4]: 1
```

```
In [6]: FooChild = type("FooChild", (Foo,), {"b":2})

In [7]: y = FooChild()

In [8]: y.a
Out[8]: 1

In [9]: y.b
Out[9]: 2
```



# `__metaclass__`属性

可以在定义一个类的时候，指定元类。





为什么需要元类？

基本上用不到。

主要用途是创建api。所以写框架的人才需要用到。



参考资料

1、深刻理解Python中的元类(metaclass)以及元类实现单例模式

https://www.cnblogs.com/tkqasn/p/6524879.html

2、深度理解python中的元类

这篇文章写得不错。

https://www.cnblogs.com/vipchenwei/p/7239953.html

