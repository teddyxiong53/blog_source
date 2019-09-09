---
title: Python之新式类和经典类
date: 2018-06-26 22:32:54
tags:
	- Python

---

1

在python3里，已经没有新式类和经典类的区别了。都是新式类。

新式类和经典类的区别，主要体现在菱形继承的情况下。

经典类的菱形继承是深度优先搜索算法。

新式类的则采用C3算法。



如果一个新式类定义了`__get__,__set__, __delete__`方法中的一个或者多个。

那么这个类就叫做描述器descriptor。

descriptor又分为两种：

```
1、data descriptor。
2、non-data descriptor。
```

descriptor通常用来改变默认的属性访问。

property装饰器就是descriptor的一个应用。

大量新式类的实现都基于descriptor。



对于经典类，类都是classobj类型。对应的实例都是Instance类型。

```

In [83]: class A:
   ....:     pass
   ....: 

In [84]: type(A)
<type 'classobj'>

In [85]: a = A()

In [86]: type(a)
<type 'instance'>
```

对于新式类，是这样：

```
In [87]: class B(object):
   ....:     pass
   ....: 

In [88]: type(B)
<type 'type'>

In [89]: b = B()

In [90]: type(b)
<class '__main__.B'>
```



参考资料

1、Python新式类与经典类的区别

https://www.cnblogs.com/blackmatrix/p/5630515.html

2、python descriptor 详解

https://www.cnblogs.com/xybaby/p/6266686.html

