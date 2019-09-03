---
title: python之object
date: 2019-09-03 17:15:03
tags:
	- python
---



我在分析魔术方法的时候，发现继承和不继承object，调用到的init和new函数情况不一样。

网上找了一下，发现确实是有区别的。

我目前默认都是基于python2.7.12这个版本进行实验，因为这个已经固定了。我非常讨厌改来改去的东西。

对于python2.7来说，

不继承ojbect。那么情况是这样的：

```
In [153]: class A():
   .....:     def say_hello(self):
   .....:         print "hello"
   .....:     
```

```
In [155]: dir(A)
Out[155]: ['__doc__', '__module__', 'say_hello']
```

```
In [156]: help(A)
Help on class A in module __main__:

class A
 |  Methods defined here:
 |  
 |  say_hello(self)
```

继承object。

```
In [157]: class B(object):
   .....:     def say_hello(self):
   .....:         print "hello"
   .....:         

In [158]: dir(B)
Out[158]: 
['__class__',
 '__delattr__',
 '__dict__',
 '__doc__',
 '__format__',
 '__getattribute__',
 '__hash__',
 '__init__',
 '__module__',
 '__new__',
 '__reduce__',
 '__reduce_ex__',
 '__repr__',
 '__setattr__',
 '__sizeof__',
 '__str__',
 '__subclasshook__',
 '__weakref__',
 'say_hello']
```

```
In [159]: help(B)
Help on class B in module __main__:

class B(__builtin__.object)
 |  Methods defined here:
 |  
 |  say_hello(self)
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
```



继承object的，叫做新式类。

不继承object的，叫做经典类。

新式类和经典类在多继承的时候，会有区别。



参考资料

1、python的class(类)中继承object 与不继承的区别

https://blog.csdn.net/qq_27828675/article/details/79358893

2、Python 为什么要继承 object 类？

https://www.zhihu.com/question/19754936