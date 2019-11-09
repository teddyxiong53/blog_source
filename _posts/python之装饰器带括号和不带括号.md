---
title: python之装饰器带括号和不带括号
date: 2019-11-09 09:12:49
tags:
	- python

---

1

看flasky代码，看到有些装饰器使用的时候，后面带了括号，而大多数时候，装饰器使用的时候都是不带括号的。

那么，带括号和不带括号的区别是什么？括号有什么用途？

带括号是因为装饰器内部多包了一层。带括号的话，可以传递一些额外的信息进去。

以下面这个定义一个测量函数运行时间的装饰器为例。

使用时需要带括号的：

```
from time import time ,sleep

def count_time(msg):
    def tmp(func):
        def wrapped(*args, **kwargs):
            begin_time = time()
            result = func(*args, **kwargs)
            end_time = time()
            cost_time = end_time - begin_time
            print("{} -- {} cost time {}:".format(msg, func.__name__, cost_time))
            return result
        return wrapped
    return tmp

@count_time("count the time of test")
def test():
    sleep(1)

test()
```

如果不带括号，就没法把那个msg传递进去了。

不带括号的版本：

```
from time import time ,sleep

def count_time(func):
    def wrapped(*args, **kwargs):
        begin_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        cost_time = end_time - begin_time
        print("{} cost time: {}".format( func.__name__, cost_time))
        return result
    return wrapped


@count_time
def test():
    sleep(1)

test()
```

就是把tmp那一层去掉了。



参考资料

1、使用装饰器时带括号与不带括号的区别

https://blog.csdn.net/weixin_34114823/article/details/93333650