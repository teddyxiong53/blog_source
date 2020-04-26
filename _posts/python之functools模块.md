---
title: python之functools模块
date: 2019-09-30 13:46:22
tags:		
	- python

---

1

这个模块是用来为**高阶函数**提供支持。

什么是高阶函数？

返回函数的函数，或者使用函数作为参数的函数，就叫高阶函数。

这个模块里主要的方法有：

# partial

自己实现以下partial，就是下面这样。

主要作用是减少函数的参数。

```
def mypartial(func, *args, **keywords):
    def newfunc(*fargs, **fkeywords):
        newkeywords = keywords.copy()
        newkeywords.update(fkeywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc

def add(a, b):
    return a+b

plus1 = mypartial(add, 1)
plus2 = mypartial(add, 2)
print(plus1(2))
print(plus2(2))
```

# wraps

有2个函数，一个是update_wrapper，一个wraps。

wraps是对update_wrapper的更进一步的封装。

默认的partial对象，没有name和doc，这个对于debug非常不方便。

使用update_wrapper就是用来把原始对象的name、doc这些属性拷贝到现有的partial对象。

简单说就是这样：

没有加wraps的函数，装饰器@返回的是函数名是原本的，但是它的函数签名却是装饰函数的。

wraps就是用来解决这个问题的。

hello

```
def wrap(func):
    def call_it(*args, **kwargs):
        '''call it'''
        print("before call")
        return func(*args, **kwargs)
    return call_it

@wrap
def hello():
    '''hello1'''
    print("hello world")

hello()
print(hello.__name__)
print(hello.__doc__)

```

这个得到的name和doc都是call_it的。不是我们想要的。

hello2

这个用update_wrapper了。

```
from functools import update_wrapper

def wrap2(func):
    def call_it(*args, **kwargs):
    	'''call it'''
        print("before call")
        return func(*args, **kwargs)
    return update_wrapper(call_it, func)

@wrap2
def hello2():
    """say hello2"""
    print("hello world2")

hello2()
print(hello2.__name__)
print(hello2.__doc__)
```

这个就是正常的了。

```
import functools
def wrap2(func):
    @functools.wraps(func)
    def call_it(*args, **kwargs):
        '''call it'''
        print("before call")
        return func(*args, **kwargs)
    return call_it

@wrap2
def hello3():
    '''hello3'''
    print("hello world3")

hello3()
print(hello3.__name__)
print(hello3.__doc__)
```



```
cmp_to_key
	从字面上看，是把老的比较函数转成新的key函数。
	那什么是比较函数？什么是key函数？
	比较函数，是类似C语言的strcmp的风格的，相对返回0，大于返回1，小于返回-1 。
	这个风格跟python不怎么搭。所以后面就要改这种风格。
	python3里不支持cmp函数了。
	key函数，反正是起一个筛选作用的。
	有5个内置函数，如max/min、sorted这些，都接受一个key函数作为参数。
```







参考资料

1、python基础（functools）

https://www.jianshu.com/p/710a3ad32a1a