---
title: 《Python高级编程和异步IO并发编程》视频学习笔记
date: 2018-06-26 22:01:59
tags:
	- Python

---



# 第四章 深入类和对象

抽象基类abc。少用。

鸭子类型才是Python的基础，abc只是一个补充。

鸭子类型是python里的多态。

java里实现多态。

```
class Animal {
  public void say() {
    print("I am animal");
  }
}
class Cat extends Animal {
  @override
  public void say() {
    print("I am cat");
  }
}
class Dog extends Animal {
  @override
  public void say() {
    print("I am dog");
  }
}
```

Python里实现多态。

```
class Cat:
	def say(self):
		print "I am cat"
class Dog:
	def say(self):
		print "I am dog"
		
anaimal = Dog()
animal.say()
animal = Cat()
animal.say()
```



##  isinstance和type区别

```
class A():
    pass

class B(A):
    pass
xx = B()

print isinstance(xx,A)
print isinstance(xx,B) #都是True
```

尽量用isinstance来做判断。



## 类变量和实例变量

向上查找。或者说，先看局部，局部找不到，再找全局。

```
#coding: utf-8
class A:
    aa = 1 #这个就是类变量。
    def __init__(self, x, y):
        self.x = x #这个就是实例变量
        self.y = y
a = A(2,3)
a.aa = 100
print a.aa  #这个是100
print A.aa #这个还是1，注意这个特性。
```

## 类属性和实例属性及查找顺序

```
#coding: utf-8
class A:
    name = "A"
    def __init__(self):
        self.name = "a"
a = A()
print  a.name
```



mro算法。

Method Resolution Order。方法查找顺序。

以前的搜索算法是深度优先的，但是这种方式对于菱形继承有问题。

## 类里的三种方法

Python类里的有3种方法：

1、classmethod，要一个cls参数。代表的类。classmethod是对staticmethod的改进。

2、staticmethod，不需要self参数，也不要cls参数。相当于一个普通方法，被放到了类的命名空间里了。

3、对象方法。要一个self参数。代表的是对象。



但是为什么classmethod没有完全替代staticmethod呢？

## 数据封装和私有属性

私有属性是双下划线开头的。

## Python对象的自省机制

Python里的字典是用C语言写的，做了很多的优化，效率很高。

# super函数



## Django里的多继承设计



## with的使用

with是一种上下文管理器。

python是基于协议的语言。

上下文管理器协议。





## contextlib简化上下文管理

```
#coding: utf-8
import contextlib
@contextlib.contextmanager
def file_open(filename):
    print "file open"
    yield #关键是这里。
    print "file end"

with file_open("1.txt") as f:
    print "processing file"
    
```

输出是：

```
file open
processing file
file end
```



# 第五章 序列类

序列就是Python里一个重要的协议。

序列类型的分类：

按照装的内容来分：

1、容器序列。list、tuple、deque。

容器序列就是里面可以放任意类型的数据。

2、扁平序列。str、bytes、bytearray、array.array。

按照可变和不可变来分：

1、可变序列。

2、不可变序列。str、tuple、bytes。

## 序列类型的abc继承关系

```
from collections import abc
```

这个在Python3里才有的。

## 序列的扩展extend

append和extend的区别。

## 实现可切片的对象



# 第六章 dict和set深入

dict属于Mapping类型。



dict的实现是C语言写的，我们在PyCharm里跳转进去看到的，只是代码形式的文档而已。

dict.copy是一个浅拷贝。

如何做深拷贝？

```
import copy
a = [1,2]
b = copy.deepcopy(a)

```



dict的子类有哪些？

