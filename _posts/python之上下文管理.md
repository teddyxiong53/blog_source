---
title: python之上下文管理
date: 2019-01-15 16:40:59
tags:
	- python
---



所谓上下文管理协议，就是我们平时用的with。

开始执行with的时候，执行`__enter__`。

结束执行with的时候，执行`__exit__`。

主要用途是保证资源在无论什么情况下都可以正常清理释放。

contextlib.contextmanager就是为了方便，用装饰器的方式，很容易地把一个generator装饰成一个有上下文管理功能的类型。

举例如下。yield之前的，在enter时调用，yield之后的，在exit时调用。

```
from contextlib import contextmanager

@contextmanager
def tag(name):
    print '<%s>' % name
    yield
    print '</%s>' % name

with tag('div'):
    print 'test'
```





参考资料

1、Python概念-上下文管理协议中的`__enter__和__exit__`

https://www.cnblogs.com/DragonFire/p/6764066.html

2、Python——with语句、context manager类型和contextlib库

https://www.cnblogs.com/Security-Darren/p/4196634.html