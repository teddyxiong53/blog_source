---
title: Python之abc模块
date: 2018-02-26 10:14:37
tags:
	- Python

---



Python语言本身没有提供抽象类和抽象方法的机制。但是提供了一个模块叫abc（Abstract Base Class）来模拟抽象类的行为。

使用方法是，把一个基类用abc声明为抽象类型，然后注册具体类来做为这个基类的实现。

```
抽象基类，缩写是ABC。
是对duck-typing的补充。
它提供了一种定义接口的新方式。
相比之下，其他的技巧，例如hasattr就显得比较笨拙而且容易出错。
ABC引入了虚拟子类，这种类并不是继承自其他的类。
但是可以被isinstance和issubclass认可。
python里许多内置的ABC用于：
1、实现数据结构。例如collections.abc。
2、数字。在numbers模块里。
3、流。在io模块里。
4、导入查找器和加载器（在importlib.abc里）
```



下面用代码做一个说明。



1、新建一个abc_base.py文件，定义一个抽象基础类PluginBase。这个类的作用我们就定为加载和存储数据。

```
import abc
class PluginBase(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def load(self, input):
        return

    @abc.abstractmethod
    def save(self, output, data):
        return
```

用`@abc.abstractmethod`来声明方法为抽象方法。

2、新建一个abc_register.py文件，在里面定义一个具体类。

```
import abc
from abc_base import PluginBase

class RegisteredImplementation(object):
    def load(self, input):
        return input.read()

    def save(self, output, data):
        return output.write(data)

PluginBase.register(RegisteredImplementation)

if __name__ == '__main__':
    print 'Subclass:', issubclass(RegisteredImplementation, PluginBase)
    print 'Instance:', isinstance(RegisteredImplementation(), PluginBase)
    
```

并且把这个类注册为PluginBase的类型。

后面的测试打印都是True。

当然，其实也可以这样来进行继承：

```
class SubclassImplementation(PluginBase):
```

所以，把抽象类具体化，有2个方法，一个是注册，一个是继承。

继承的话，需要子类完全实现所有的抽象方法，否则就不行。



抽象类里可以放具体方法。子类要调用的时候，就用super来调用。



参考资料

1、定义接口或者抽象基类

https://python3-cookbook.readthedocs.io/zh_CN/latest/c08/p12_define_interface_or_abstract_base_class.html