---
title: python之用attr库来简化类的定义
date: 2020-05-07 21:37:54
tags:
	- Python

---



搜索的时候，无意中发现了参考资料里这篇文章，里面提到的attrs这个库，看起来非常实用。

可以学习一下这个库的使用。

python面向对象编程时，有很多属性，需要定义一堆的配套函数进行处理，这个有很多繁琐的重复性工作。这个是可以简化的。

我们以rgb颜色这个类为例来看看。

```
class Color(object):
    def __init__(self, r, g ,b):
        self.r = r
        self.g = g
        self.b = b
```

然后我们打印一下看看。

```
c = Color(255,255,255)
print(c)
```

结果是这样：

```
<__main__.Color object at 0x11072ed10>
```

不符合我们的预期。

这是因为我们需要去实现`__repr__`函数。

```
    def __repr__(self):
        return f'{self.__class__.__name__} (r={self.r}, g={self.g}, b={self.b}) '
```

现在打印就符合我们预期了。

但是看到没有，我们有把r/g/b这些变量名又罗列了一遍。

如果我们要继续实现`__gt__`等方法，可以想象，我们要一次又一次罗列这些变量。

还有json和对象的相互转换。

在scrapy、Django等框架里，例如Django的Model，只需要定义几个字段属性就可以完成整个类的定义。非常方便。

那么，我们能不能把Django里的这个机制拿过来用呢？答案是：可以，但没必要。

因为已经有专门帮助我们实现这个功能的库了。就是attrs和cattrs这2个库。

cattrs是转对json转换的。

我们先安装这个库。

```
python3 -m pip install attrs cattrs
```

这2个库的名字叫attrs和cattrs。但是我们使用的时候，import的包的名字是叫attr和cattr。不带s的。

在attr这个包里，又有2个组件，是我们常用的。叫attrs和attr。

attrs这个组件是修改类的。attr是修饰字段的。

我们用这个来改造上面的Color类。

```
from attr import attrs, attrib

@attrs
class Color(object):
    r = attrib(type=int, default=0)
    g = attrib(type=int, default=0)
    b = attrib(type=int, default=0)

c = Color(255,255)
print(c)
```

这样打印，就直接是符合我们的预期的了。



参考资料

1、Python 使用 attrs 和 cattrs 实现面向对象编程的实践

<https://www.jb51.net/article/162909.htm>