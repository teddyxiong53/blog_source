---
title: python之类和对象的生命周期
date: 2020-05-03 17:04:30
tags:
	- python

---

1

```
from __future__ import print_function

class Person(object):
    def __new__(cls, *args, **kwargs):
        print("new")
    def __init__(self):
        print("init")
    def __del__(self):
        print("del")
p=Person()
```

这样看，只调用了new。

如果Person没有继承object。那么就只调用了init和del。

不过，后面都是默认继承object的新式类了。就不管经典类的情况了。

上面的new，其实是写得不对，应该返回的。

改为下面这样，则正常了。

```
class Person(object):
    def __new__(cls, *args, **kwargs):
        print("new")
        return super(Person, cls).__new__(cls, *args, **kwargs)
```

现在再改成经典类的看，还是不会调用new。那么可见这就是经典类跟新式类的区别。



参考资料

1、python---核心知识8之对象的生命周期以及内存管理机制

<https://www.jianshu.com/p/22a8bedc39fd>