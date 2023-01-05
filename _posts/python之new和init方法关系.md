---
title: python之new和init方法关系
date: 2020-05-03 17:26:30
tags:
	- python

---

--

先说结论：

**创建一个类的实例的时候，先调用`__new__`，再调用`__init__`。**

可以这样理解：

new是分配内存，init是进行初始化赋值。

new和init的区别：

```
1、new的第一个参数是cls，而不是self。
2、new要进行return。
```



不过，我们平时很少自己实现一个`__new__`，好像也没有什么问题。

**那么什么时候，我们需要自己实现`__new__`呢？**

一般是在继承一些不可变的class（例如int、str、tuple）时，提供了一种修改这些类的实例化的过程的方法。

还有一个用途，就是实现自定义的metaclass。

例如，我想顶一个正整数类型。代码如下：

```
class PositiveInteger(int):
    def __init__(self, val):
        super(PositiveInteger, self).__init__(self, abs(val))

if __name__ == '__main__':
    i = PositiveInteger(-2)
    print i
```

但是，结果还是输出了-2。

这是因为对于int这种不可变的类型，我们需要重载它的`__new__`方法才能让起作用。

修改如下：

```
class PositiveInteger(int):
    def __new__(cls, val):
        return super(PositiveInteger, cls).__new__(cls, abs(val))
```

这样就正常了。



还有单例模式，也需要借助new来做到。



# 完整例子

```
class Test():
    def __new__(cls, *args, **kwargs):
        print("new ")
        return super(Test,cls).__new__(Test)
    def __init__(self):
        print("init")

    def __del__(self):
        print("del")
    def func(self):
        print('func')

t = Test()
t.func()
del t
```

注意点：

new必须要返回一个对象。否则默认返回None。

init是对new返回的对象进行初始化。



# 参考资料

1、python的`__new__`方法

<https://www.cnblogs.com/Sweepingmonk/p/11626971.html>

2、python的单例模式

<https://www.jianshu.com/p/6ca1b0cdef3b>