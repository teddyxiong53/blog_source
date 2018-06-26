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

