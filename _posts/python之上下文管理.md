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



为什么要使用上下文管理器？

在我看来，这和 Python 崇尚的优雅风格有关。

1. 可以以一种更加优雅的方式，操作（创建/获取/释放）资源，如文件操作、数据库连接；
2. 可以以一种更加优雅的方式，处理异常；

第一种，我们上面已经以资源的连接为例讲过了。

而第二种，会被大多数人所忽略。这里会重点讲一下。

大家都知道，处理异常，通常都是使用 `try...execept..` 来捕获处理的。这样做一个不好的地方是，在代码的主逻辑里，会有大量的异常处理代理，这会很大的影响我们的可读性。

好一点的做法呢，可以使用 `with` 将异常的处理隐藏起来。


在上面的例子中，我们只是为了构建一个上下文管理器，却写了一个类。如果只是要实现一个简单的功能，写一个类未免有点过于繁杂。这时候，我们就想，如果只写一个函数就可以实现上下文管理器就好了。

这个点Python早就想到了。它给我们提供了一个装饰器，你只要按照它的代码协议来实现函数内容，就可以将这个函数对象变成一个上下文管理器。



使用contextmanager的关键是：

中间的yield，yield前面的部分，相当于enter，yield后面的部分，相当于exit。

```
import contextlib

@contextlib.contextmanager
def open_func(filename):
    print("open file")
    f = open(filename, 'r')
    yield f
    print('close file')
    f.close()
    return

with open_func("param.json") as f:
    for line in f:
        print(line)
```



参考资料

1、Python概念-上下文管理协议中的`__enter__和__exit__`

https://www.cnblogs.com/DragonFire/p/6764066.html

2、Python——with语句、context manager类型和contextlib库

https://www.cnblogs.com/Security-Darren/p/4196634.html

3、

https://juejin.im/post/6844903795403522056