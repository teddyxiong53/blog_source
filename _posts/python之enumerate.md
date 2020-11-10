---
title: python之enumerate
date: 2019-01-08 15:58:25
tags:
	- python

---



```
In [40]: grps
Out[40]: ['aaaa', 'bbbb', 'cccc', 'dddd', 'eeee', 'ffff', '0000', '1111']
In [42]: for i, v in enumerate(grps):
   ....:     print i,v
   ....:     
0 aaaa
1 bbbb
2 cccc
3 dddd
4 eeee
5 ffff
6 0000
7 1111
```



枚举是一组符号名称（枚举成员）的集合，

枚举成员应该是唯一的、不可变的。

在枚举中，可以对成员进行恒等比较，并且枚举本身是可迭代的。

要使用enum。需要import enum。对应lib/enum.py文件。

对外暴露的符号

```
__all__ = [
        'EnumMeta',
        'Enum', 'IntEnum', 'Flag', 'IntFlag',
        'auto', 'unique',
        ]
```

成员值可以为任意类型: int, str 等等。 

如果具体的值不重要，你可以使用 auto 实例，将为你选择适当的值。

 但如果你混用 auto 与其他值则需要小心谨慎。

```
import enum

class Color(enum.Enum):
    RED = 1
    GREEN =2
    BLUE =3
```

类 `Color` 是一个 *enumeration* (或称 *enum*)

属性 `Color.RED`, `Color.GREEN` 等等是 *枚举成员* (或称 *enum 成员*) 并且被用作常量。

枚举成员具有 *名称* 和 *值* (`Color.RED` 的名称为 `RED`，`Color.BLUE` 的值为 `3` 等等。)

虽然我们使用 [`class`](https://docs.python.org/zh-cn/3.7/reference/compound_stmts.html#class) 语法来创建 Enum，但 Enum 并不是普通的 Python 类。

枚举有自定义的元类。

它会影响枚举类及实例的各个方面。



# EnumMeta

枚举元类，提供了[`__contains__()`](https://docs.python.org/zh-cn/3.7/reference/datamodel.html#object.__contains__), [`__dir__()`](https://docs.python.org/zh-cn/3.7/reference/datamodel.html#object.__dir__), [`__iter__()`](https://docs.python.org/zh-cn/3.7/reference/datamodel.html#object.__iter__) 及其他方法

这个类是帮我们实现普通类不具备的某些特性

例如你这样：

```
list(Color)
for c in Color
```

普通类就不能。但是枚举类可以。



有关**枚举成员最有趣的特点是它们都是单例对象**。

 `EnumMeta` 会在创建 [`Enum`](https://docs.python.org/zh-cn/3.7/library/enum.html#enum.Enum) 类本身时将它们全部创建完成，

然后准备好一个自定义的 [`__new__()`](https://docs.python.org/zh-cn/3.7/reference/datamodel.html#object.__new__)，通过**只返回现有的成员实例来确保不会再实例化新的对象。**



# 使用枚举

这两种方式都可以。

```
print(Color['RED'])
print(Color.RED)
```



# 注意

枚举成员实际上就是key-value对。

同一个key不能给多个value。

但是多个key可以用同一个value。相当于别名。

这个跟C语言的枚举类似。

```
class Color(enum.Enum):
    RED = 1
    GREEN =2
    BLUE =3
    ALIAS_RED = 1 # 这个可以
    RED = 2 # 这个不行
```

有时候，我们要确定key跟value都的唯一对应的。

可以用unique来修饰一下。

```
from enum import Enum, unique
@unique
class Color(Enum):
	RED  =1
	GREEN = 2
	OTHER_RED = 1 # 因为unique修饰了。所以这个不合法。
```

有时候，我们不想要明确写1、2、3这些值。我们不具体关心key对应的value。

那就可以使用auto来自动递增。

```
from enum import auto
class Color(Enum):
	RED = auto()
	GREEN = auto()
```

这个实际上是通过`_generate_next_value_`这个方法来做的。

我们可以自己重载这个方法。



# IntEnum

所提供的第一个变种 [`Enum`](https://docs.python.org/zh-cn/3.7/library/enum.html#enum.Enum) 同时也是 [`int`](https://docs.python.org/zh-cn/3.7/library/functions.html#int) 的一个子类。

 [`IntEnum`](https://docs.python.org/zh-cn/3.7/library/enum.html#enum.IntEnum) 的成员可与整数进行比较；

通过扩展，不同类型的整数枚举也可以相互进行比较:



# IntFlag

这个是对于位域类型的枚举。

例如Linux权限这种。

```
class Perm(enum.IntFlag):
    R = 4
    W = 2
    X = 1
```



参考资料

1、Python——枚举（enum）

https://www.cnblogs.com/-beyond/p/9777329.html

2、enum --- 枚举类型支持

https://docs.python.org/zh-cn/3.7/library/enum.html

3、各种枚举有何区别？

https://docs.python.org/zh-cn/3.7/library/enum.html#how-are-enums-different