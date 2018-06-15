---
title: Python之生成器和迭代器
date: 2018-04-21 11:44:18
tags:
	- Python

---



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







# 参考资料

1、Python3 迭代器与生成器

http://www.runoob.com/python3/python3-iterator-generator.html

2、python的 a,b=b,a+b 和 a=b b=a+b 的区别

https://zhidao.baidu.com/question/304727322833271364.html