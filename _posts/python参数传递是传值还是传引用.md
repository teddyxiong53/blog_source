---
title: python参数传递是传值还是传引用
date: 2019-11-30 09:50:59
tags:
	- python
---

1

首先明确一下函数的参数传递机制。

函数参数传递机制，本质上是caller跟callee在调用发生的时候，进行通信的方法。

基本的参数传递机制有两种：

1、传值。

2、传引用。



传值，pass-by-value。

参数作为局部变量处理，也就是在栈上开辟了一块空间来放传递进来的实参。

也就是形成了一个参数的副本。

传值的特点是不会改变实参的内容。



传引用，pass-by-reference

也在栈上开辟了空间，但是空间里放的是参数的地址，而不是参数的副本。



在python里，是怎样的情况呢？

看一个例子。

```
from ctypes import *
import os.path
import sys

def test(c):
    print("test before ")
    print (id(c))
    c+=2
    print ("test after +")
    print (id(c))
    return c

def printIt(t):
    for i in range(len(t)):
        print (t[i])

if __name__=="__main__":
    a=2
    print ("main before invoke test")
    print (id(a))
    n=test(a)
    print ("main after invoke test")
    print (a)
    print (id(a))
```

运行输出是这样：

```
main before invoke test
8791238759488
test before 
8791238759488
test after +
8791238759552
main after invoke test
2
8791238759488
```

通过id函数，可以看到传递参数的时候，是传递了引用。

但是在对参数进行修改的时候，就另外分配了一个副本了。



但是对list是不一样的：

```
from ctypes import *
import os.path  
import sys

def test(list2):
    print "test before "
    print id(list2)
    list2[1]=30
    print "test after +"
    print id(list2)
    return list2

def printIt(t):
    for i in range(len(t)):
        print t[i]

if __name__=="__main__":
    list1=["loleina",25,'female']
    print "main before invoke test"
    print id(list1)
    list3=test(list1)
    print "main afterf invoke test"
    print list1
    print id(list1)
```



**python不允许程序员选择传值还是传引用。**

python使用的是传对象引用的方式。

这种方式是传值和传引用的综合。

如果函数接收到一个可变对象（dict或者list）的引用，就可以修改对象的原始值。这个时候相当于传引用。

如果函数收到一个不可变对象（如数字、字符、元组）的引用，就不能修改原始值。





参考资料

1、python函数传参是传值还是传引用？

https://www.cnblogs.com/loleina/p/5276918.html