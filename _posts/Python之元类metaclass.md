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

很多书都会翻译成 **元类**，

仅从字面理解， meta 的确是元，本源，翻译没毛病。

但理解时，**应该把元理解为描述数据的超越数据**，

事实上，metaclass 的 meta 起源于希腊词汇 meta，包含两种意思：

- “Beyond”，例如技术词汇 metadata，意思是描述数据的超越数据。
- “Change”，例如技术词汇 metamorphosis，意思是改变的形态。

因此可以理解为 metaclass 为描述类的超类，同时可以改变子类的形态。

你可能会问了，这和元数据的定义差不多么，这种特性在编程中有什么用？

用处非常大。

在没有 metaclass 的情况下，子类继承父类，父类是无法对子类执行操作的，

但有了 metaclass，就可以对子类进行操作，

就像装饰器那样可以动态定制和修改被装饰的类，

**metaclass 可以动态的定制或修改继承它的子类。**



## metaclass 能解决什么问题？

你已经知道了 metaclass 可以像装饰器那样定制和修改继承它的子类，

这里就说下它能解决什么实际问题。

比方说，在一个智能语音助手的大型项目中，

我们有 1 万个语音对话场景，每一个场景都是不同团队开发的。

作为智能语音助手的核心团队成员，你不可能去了解每个子场景的实现细节。



在动态配置实验不同场景时，

经常是今天要实验场景 A 和 B 的配置，明天实验 B 和 C 的配置，

光配置文件就有几万行量级，工作量不可谓不小。

而应用这样的动态配置理念，我就可以让引擎根据我的文本配置文件，动态加载所需要的 Python 类。



现在你有 1 万个不同格式的 YAML 配置文件，

本来你需要写 1 万个类来加载这些配置文件，

有了 metaclass，你只需要实现一个 metaclass 超类，

然后再实现一个子类继承这个 metaclass，

就可以根据不同的配置文件自动拉取不同的类，这极大地提高了效率。

在pycharm里写测试代码。

test.py

```
class Mymeta(type):
    def __init__(self, name, bases, dic):
        super().__init__(name, bases, dic)
        print('Mymeta.__init__')
        print(self.__name__)
        print(dic)
        print(self.yaml_tag)

    def __new__(cls, *args, **kwargs):
        print('Mymeta.__new__')
        print(cls.__name__)
        return type.__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print('Mymeta.__call__')
        obj = cls.__new__(cls)
        cls.__init__(cls, *args, **kwargs)
        return obj


class Foo(metaclass=Mymeta):
    yaml_tag = 'foo'
    def __init__(self, name):
        print('Foo.__init__')
        self.name = name

    def __new__(cls, *args, **kwargs):
        print('Foo.__new__')
        return object.__new__(cls)
```

然后pycharm里打开python console。

导入模块，会看到Mymeta的打印。这个是定义Foo类的打印。

```
from test import *
Mymeta.__new__
Mymeta
Mymeta.__init__
Foo
{'__module__': 'test', '__qualname__': 'Foo', 'yaml_tag': 'foo', '__init__': <function Foo.__init__ at 0x04997108>, '__new__': <function Foo.__new__ at 0x049970C0>}
foo
```

然后用Foo类实例化一个对象。

```
f = Foo('aa')
Mymeta.__call__
Foo.__new__
Foo.__init__
```



从上面的运行结果可以发现在定义 class Foo() 定义时，

会依次调用 MyMeta 的 `__new__` 和 `__init__` 方法构建 Foo 类，

然后在调用 foo = Foo() 创建类的实例对象时，

才会调用 MyMeta 的 `__call__` 方法来调用 Foo 类的 `__new__` 和 `__init__` 方法。

把上面的例子运行完之后就会明白很多了，

正常情况下我们在父类中是不能对子类的属性进行操作，但是元类可以。

换种方式理解：元类、装饰器、类装饰器都可以归为元编程。



Python 底层语言设计层面是如何实现 metaclass 的？

要理解 metaclass 的底层原理，你需要深入理解 Python 类型模型。下面，将分三点来说明。

第一，所有的 Python 的用户定义类，都是 type 这个类的实例。

可能会让你惊讶，事实上，类本身不过是一个名为 type 类的实例。在 Python 的类型世界里，type 这个类就是造物的上帝。这可以在代码中验证：





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

3、一文搞懂什么是Python的metaclass

https://zhuanlan.zhihu.com/p/98440398