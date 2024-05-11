---
title: python之super方法调用
date: 2019-11-02 17:37:49
tags:
	- Python

---

--

继承一个类的时候，你有三种选择：

1、自己不实现一个`__init__`函数。这样会自动调用父类的`__init__`。

2、自己实现一个`__init__`函数，但是不调用父类的`__init__`。这样就不会调用父类的`__init__`。父类在`__init__`里添加的属性，在子类里无法访问。

3、子类实现一个`__init__`函数，同时在`__init__`函数里调用父类的`__init__`函数。这种方式是最稳妥的，也是最常用的。

```
class Person:
    def __init__(self, name):
        self.name = name

class Allen(Person):
    pass


class AllenInit(Person):
    def __init__(self, age):
        self.age = age

class AllenSuper(Person):
    def __init__(self, name ,age):
        self.age = age
        super().__init__(name)


p1 = Allen('allen')
print(p1.name)

p2 = AllenInit(20)
# print(p2.name)

p3 = AllenSuper('bob', 20)
print(p3.name)

```



# `super().__setitem__(key, []) 和  super(MultiDict, self).__setitem__() `这种写法 区别

这两种写法都是使用 `super()` 来调用父类的方法，但它们之间有一些细微的区别：

1. **super().__setitem__(key, [])：**
   - 这种写法是 Python 3.x 中推荐的隐式调用父类方法的方式。它会自动查找当前类的 MRO（Method Resolution Order，方法解析顺序）中的下一个类，并调用该类中的同名方法。
   - 在上下文中，`super().__setitem__(key, [])` 调用了父类的 `__setitem__()` 方法，并传递了 `key` 和 `[]` 两个参数。
   - 这种写法适用于多重继承的情况，它会动态地查找 MRO 中的下一个类来调用方法。

2. **super(MultiDict, self).__setitem__()：**
   - 这种写法是显式指定父类的方式，其中 `MultiDict` 是当前类的父类，`self` 是当前类的实例。
   - 在上下文中，`super(MultiDict, self).__setitem__()` 显式地调用了 `MultiDict` 类的父类的 `__setitem__()` 方法。
   - 这种写法通常用于在多重继承中明确调用特定父类的方法。

总的来说，这两种写法都是调用父类的方法，但它们的调用方式略有不同。隐式调用父类方法的方式更简洁和灵活，而显式指定父类的方式则更明确和可控。根据具体的需求和情况选择合适的写法。



# 参考资料

1、`Python—子类构造函数调用super().__init__()`

https://blog.csdn.net/paopaohll/article/details/83063349