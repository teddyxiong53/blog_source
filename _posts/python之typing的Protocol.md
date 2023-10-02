---
title: python之typing的Protocol
date: 2023-10-01 10:29:11
tags:
	- python
---

--

`Protocol`是Python 3.8及更高版本中引入的`typing`模块中的一个类，用于定义抽象基类（Abstract Base Classes，ABC）的协议。

协议是一种接口规范，它定义了一组方法、属性或描述符的集合，用于描述对象应具有的行为。协议不同于传统的抽象基类，它不需要继承自特定的基类，也不要求实现特定的魔法方法。协议可以用于静态类型检查、文档化和代码提示等目的。

使用`Protocol`类定义的协议可以包含方法、属性和描述符的声明。协议中的方法和属性可以没有具体的实现，只需要定义其名称和类型注解。协议还可以继承其他协议，形成更复杂的接口规范。

下面是一个使用`Protocol`定义协议的示例：

```python
from typing import Protocol

class Printable(Protocol):
    def print(self) -> None:
        pass

class MyClass:
    def print(self) -> None:
        print("Printing...")

def process(obj: Printable) -> None:
    obj.print()

my_obj = MyClass()
process(my_obj)
```

在上述示例中，我们定义了一个名为`Printable`的协议，它包含了一个名为`print`的方法声明。然后我们定义了一个名为`MyClass`的类，它实现了`Printable`协议中的`print`方法。最后，我们定义了一个名为`process`的函数，它接受一个`Printable`类型的参数，并调用其`print`方法。

通过`Protocol`类，我们可以在类型注解中指定`Printable`类型，从而在`process`函数中实现对协议的约束。这样，类型检查工具可以确保传递给`process`函数的对象具有符合`Printable`协议的行为。

需要注意的是，`Protocol`类是在Python 3.8中引入的，它提供了更灵活的协议定义方式。在之前的版本中，可以使用`typing_extensions`模块中的`Protocol`类来实现类似的功能。

总结来说，`Protocol`类允许我们定义抽象基类的协议，用于描述对象应具有的行为。它对于静态类型检查、文档化和代码提示等方面非常有用。

# tinydb里的例子

```
class QueryLike(Protocol):
    """
    A typing protocol that acts like a query.

    Something that we use as a query must have two properties:

    1. It must be callable, accepting a `Mapping` object and returning a
       boolean that indicates whether the value matches the query, and
    2. it must have a stable hash that will be used for query caching.

    In addition, to mark a query as non-cacheable (e.g. if it involves
    some remote lookup) it needs to have a method called ``is_cacheable``
    that returns ``False``.

    This query protocol is used to make MyPy correctly support the query
    pattern that TinyDB uses.

    See also https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols
    """
    def __call__(self, value: Mapping) -> bool: ...

    def __hash__(self) -> int: ...
```

