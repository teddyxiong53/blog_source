---
title: Python之yield关键字
date: 2017-09-25 21:59:36
tags:
	  Python

---



先看一个简单的例子：

```
def mygenerator():
    print "start ..."
    yield 5
mygenerator()
mygenerator().next()
```

1、一个函数里有yield了，它就不再是一个普通的函数了。它变成了一个生成器。

2、这个函数被调用时，不是执行，而是暂停了。

3、要调一下next函数才会执行。

4、如果一个函数里有多个yield，则调一下next，会停在下一个yield前面。

5、yield只能出现在函数里面。不能单独存在。



# 典型应用

yield 最典型的一个应用就是生成一个很大的序列。

简单列表推导是这样的：

```
squares = [n*n for n in range(3)]
for i in squares:
    print i
```

这种用法的最大的问题是，如果range里的值很大，就会消耗大量的内存。

而要改造为生成器，只需要把上面的中括号换成小括号就好了。

```
squares = (n*n for n in range(3))
for i in squares:
    print i
```

生成器表达式不会创建序列形式的对象。而是逐个生成的。





看看另外一个简单的例子：

```
def gen():
    a = yield 1
    print('yield a % s' % a)
    b = yield 2
    print('yield b % s' % b)
    c = yield 3
    print('yield c % s' % c)


r = gen()
x = next(r)
print('next x %s' % x)
y = r.send(10)
print('next y %s' %y)
z = next(r)
print('next z %s' % z)
```

输出结果是：

```
C:\Python27\python.exe D:/work/pycharm/py_test/test.py
next x 1
yield a 10
next y 2
yield b None
next z 3

Process finished with exit code 0
```

