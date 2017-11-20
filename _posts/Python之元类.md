---
title: Python之元类
date: 2017-11-20 20:28:17
tags:
	- Python

---



在理解元类之前，需要先掌握Python的类。Python里类的概念借鉴自Smalltalk。

Smalltalk是历史上公认的第二个面向对象的编程语言（第一个是simula 67），Smalltalk直接影响了后续的大部分面向对象的编程语言，被称为面向对象编程之目。这个语言来自于施乐公司。

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



# `__metaclass__`属性





