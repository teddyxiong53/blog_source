---
title: Python之生成器和迭代器
date: 2018-04-21 11:44:18
tags:
	- Python

---

1

序列可以迭代的原因：iter这个内置函数。

当解释器需要迭代对象x的时候，会自动调用iter(x)。

内置的iter函数有如下作用：

```
1、检查对象是否实现了iter方法，如果实现了，就调用该函数，获取一个迭代器。
2、如果没有实现iter方法，但是实现了getitem方法，而切getitem函数的参数是从0开始的索引值，那么python就会创建一个迭代器，尝试按顺序获取元素。
3、如果前面2步都失败了，那么就抛出TypeError。
```

从上面的描述，我们可以得到可迭代对象的定义：

可迭代对象是指用iter函数获取到迭代器的对象。

看只实现了getitem方法的。

```
class A:
    def __init__(self,  text):
        self.text = text
        self.sub_text = text.split(" ")

    def __getitem__(self, index):
        return self.sub_text[index]

a = A("hello world")
for i in a:
    print(i)
```

实现了迭代器的。

```
class A:
    def __init__(self,  text):
        self.text = text
        self.sub_text = text.split(" ")

    def __iter__(self):
        return AIterator(self.sub_text)

class AIterator:
    def __init__(self, sub_text):
        self.sub_text = sub_text
        self.index = 0

    def __next__(self):
        try:
            subtext = self.sub_text[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return subtext
    def __iter__(self):
        return self


a = A("hello world")
for i in a:
    print(i)
b = A("aa bb cc")
it = iter(b)
print(next(it))
```

实现getitem方法，需要我们实现迭代器对象。

实现next方法，使用python内部的。

更加符合python习惯的写法是下面这样的。

```
class A:
    def __init__(self,  text):
        self.text = text
        self.sub_text = text.split(" ")

    def __iter__(self):
        for item in self.sub_text:
            yield item
```

使用yield，不需要自己去实现一个迭代器类了。



所有的生成器都是迭代器。



为什么需要生成器？其他语言有没有生成器？

为什么叫生成器？

生成器就是一个生成迭代器的函数。

因为直接创建迭代器使用不方便。

生成器就是一个

为什么python需要生成器？
是大部分效率提高的基础。
因为它不需要记住以前的值，
创建python迭代器的过程虽然强大，但是很多时候使用不方便。生成器是一个简单的方式来完成迭代。简单来说，Python的生成器是一个返回可以迭代对象的函数。



生成器的优点：

1、更容易使用，代码量小。

2、内存使用效率更高。

3、代表了一个无限的流。



跟函数相比，生成器就是在返回的时候，保留当前的状态（例如局部变量的值），下次执行可以接着上次的位置继续执行。

迭代器是靠延迟计算来返回元素，这个就是迭代器跟list的区别。

本质上 for 循环就是不断地调用迭代器的next方法。

**理解的关键在于：下次迭代时，代码从yield的下一条语句开始执行。**

什么时候使用生成器？在内容无法预测长度的时候，最好使用生成器。

例如，遍历一篇文章，文章可能有上百万字。



# 迭代器

迭代器是Python最强大的功能之一。

是访问集合元素的一种方式。

迭代器只能往前不能后退，就像过河的卒子一样。

迭代器有2个基本方法：

iter() / next()

看一个简单例子。

```
#!/usr/bin/python3

list = [1,2,3,4]
it = iter(list)
print (next(it))
print (next(it))
```

可以用for来进行遍历。

```
#!/usr/bin/python3

list = [1,2,3,4]
it = iter(list)
for x in it:
	print (x, end=',')
print("")
```

也可以用next来进行遍历。

```
import sys
list = [1,2,3,4]
it = iter(list)
while True:
	try:
		print(next(it))
	except StopIteration:
		sys.exit()
```

# 生成器

在Python里，只要使用了yield关键字的函数，都叫生成器。

所以，生成器是一种特殊的函数。

它特殊在哪儿？

就是它返回的是迭代器。只能进行迭代操作。

在 调用生成器函数的时候，每次碰到yield的时候，这个函数就会暂停，并保存当前所有的运行信息。返回yield的值。在下一次执行next的时候，从当前的位置继续运行。

我们看看生成器方式实现的斐波那契数列。

```
#!/usr/bin/python3
import sys
def fib(n):
	a = 0
	b = 1 
	counter = 0
	while True:
		if counter > n:
			return
		yield a
		#a = b
		#b = a + b
		a,b = b, a+b
		counter += 1
		
f = fib(5) #f是一个迭代器

while True:
	try:
		print(next(f),end=" ")
	except StopIteration:
		print("")
		sys.exit()
```

上面这里有个知识点。

```
#a = b
#b = a + b
a,b = b, a+b
```

注释的两行，跟第三行，不是等价的。

假设当前a=0，b=1 。

```
a,b= b,a+b
```

先把右边的值得出来。

b等于1

a+b当前等于1 。

把这2个1赋值给左边。



生成器的特点是：被调用的时候，不是执行函数体，而是返回一个迭代器。





# 参考资料

1、Python3 迭代器与生成器

http://www.runoob.com/python3/python3-iterator-generator.html

2、python的 a,b=b,a+b 和 a=b b=a+b 的区别

https://zhidao.baidu.com/question/304727322833271364.html

3、一文读懂Python可迭代对象、迭代器和生成器

https://blog.csdn.net/zhusongziye/article/details/80246910