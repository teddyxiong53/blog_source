---
title: python之super方法调用
date: 2019-11-02 17:37:49
tags:
	- Python

---

1

继承一个类的时候，你有三种选择：

1、自己不实现一个init函数。这样会自动调用父类的init。

2、自己实现一个init函数，但是不调用父类的init。这样就不会调用父类的init。父类在init里添加的属性，在子类里无法访问。

3、子类实现一个init函数，同时在init函数里调用父类的init函数。这种方式是最稳妥的，也是最常用的。

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



参考资料

1、`Python—子类构造函数调用super().__init__()`

https://blog.csdn.net/paopaohll/article/details/83063349