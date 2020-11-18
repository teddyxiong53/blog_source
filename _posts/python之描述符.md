---
title: python之描述符
date: 2020-11-18 16:21:30
tags:
	- python
---

1

如果要写一个学生管理类系统。

你可以这样很自然地写：

```
class Student:
    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english

    def __repr__(self):
        return "<Student:{}, math:{}, chinese:{}, english:{}>".format(self.name,self.math,self.chinese,self.english)

```

这个代码也没有什么问题。

但是不够健壮。

首先，没有加入成绩的合法性判断。

于是，我们这样加判断，成绩要在0到100之间。

```
if 0 <= math <= 100:
	self.math = math
else:
	raise ValueError("invalid ")
```

但是这样在构造函数里加入了大量的判断逻辑，而且大量的重复判断。

实在是非常不优雅，而且难以扩展和维护。

可以怎么改进？

借用property。

```
	@property
    def math(self):
        return self._math
    @math.setter
    def math(self, value):
        if 0 <= value <= 100:
            self._math = value
        else:
            raise ValueError("invalid")
```

当前只是把构造函数里的判断挪出来了。

扩展性的问题还没有解决。冗余代码仍然在。

这个时候，我们就需要借助描述符这东西了。

其实也很简单，一个实现了 `描述符协议` 的类就是一个描述符。

什么描述符协议：在类里实现了 `__get__()`、`__set__()`、`__delete__()` 其中至少一个方法。

- `__get__`： 用于访问属性。它返回属性的值，若属性不存在、不合法等都可以抛出对应的异常。
- `__set__ `：将在属性分配操作中调用。不会返回任何内容。
- `__delete__ `：控制删除操作。不会返回内容。

如前所述，Score 类是一个描述符，

当从 Student 的实例访问 math、chinese、english这三个属性的时候，

都会经过 Score 类里的三个特殊的方法。

这里的 Score 避免了 使用Property 出现大量的代码无法复用的尴尬。

这样改造就好了。

```
class Score:
    def __init__(self, default=0):
        self._score = default

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError("score must be int")
        if not 0 <= value <= 100:
            raise ValueError("score must between 0 to 100")
        self._score = value

    def __get__(self, instance, owner):
        return self._score

    def __delete__(self, instance):
        del self._score

class Student:
    math = Score(0)
    chinese = Score(0)
    english = Score(0)
    
    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english
```

到这里，你需要记住的只有一点，就是描述符给我们带来的编码上的便利，它在实现 `保护属性不受修改`、`属性类型检查` 的基本功能，同时有大大提高代码的复用率。



描述符分两种：

- 数据描述符：实现了`__get__` 和 `__set__` 两种方法的描述符
- 非数据描述符：只实现了`__get__` 一种方法的描述符



正常人所见过的描述符的用法就是上面提到的那些，

我想说的是那只是描述符协议最常见的应用之一，

或许你还不知道，其实有很多 Python 的特性的底层实现机制都是基于 `描述符协议` 的，

比如我们熟悉的`@property` 、`@classmethod` 、`@staticmethod` 和 `super` 等。



参考资料

1、深入理解 Python 描述符

https://juejin.im/post/6864517287316520967