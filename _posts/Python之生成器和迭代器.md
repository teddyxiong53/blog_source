---
title: Python之生成器和迭代器
date: 2018-04-21 11:44:18
tags:
	- Python

---

--

python的for循环抽象程度高于C语言。python的for循环可以作用在所有的可迭代对象上。

怎样看一个对象是不是可迭代的呢？

这样来判断就可以：

```
from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
>>> isinstance(123, Iterable) # 整数是否可迭代
False
```

如果要对list进行下标索性迭代，怎么办呢？

用enumerate函数就可以。

```
for i, value in enumerate(['a', 'b', 'c']):
	print(i, value)
```





序列可以迭代的原因：iter这个内置函数。

**当解释器需要迭代对象x的时候，会自动调用iter(x)。**

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



为什么python需要生成器？
是大部分效率提高的基础。
因为它不需要记住以前的值，
创建python迭代器的过程虽然强大，但是很多时候使用不方便。生成器是一个简单的方式来完成迭代。简单来说，Python的生成器是一个返回可以迭代对象的函数。



生成器的优点：

1、更容易使用，代码量小。

2、内存使用效率更高。

3、代表了一个无限的流。



**跟函数相比，生成器就是在返回的时候，保留当前的状态（例如局部变量的值），下次执行可以接着上次的位置继续执行。**

迭代器是靠延迟计算来返回元素，这个就是迭代器跟list的区别。

本质上 for 循环就是不断地调用迭代器的next方法。

**理解的关键在于：下次迭代时，代码从yield的下一条语句开始执行。**

什么时候使用生成器？在内容无法预测长度的时候，最好使用生成器。

例如，遍历一篇文章，文章可能有上百万字。



# 迭代器

迭代器是Python最强大的功能之一。

是访问集合元素的一种方式。

**迭代器只能往前不能后退，就像过河的卒子一样。**

**迭代器有2个基本方法：**

**iter() / next()**

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



# iter()和next()关系

iter()函数用来把一个对象转换成可迭代对象。

而next()函数用来把可迭代对象进行迭代。

看这个例子就懂了。

```
my_list = [1, 2, 3, 4, 5]
my_iterator = iter(my_list)
print(next(my_iterator))  # 输出：1
print(next(my_iterator))  # 输出：2

```

# list是迭代器吗

不是。因为迭代器是指实现了 `__iter__` 方法的对象。而list没有。

但是list是可迭代对象。

可以用iter(my_list)来把一个list转换为一个迭代器。

# 迭代器本质

迭代器是一种惰性计算的机制

# 迭代器协议

迭代器协议（Iterator Protocol）是一种在 Python 中定义迭代器的约定，通过实现特定的方法，使对象成为一个迭代器。

迭代器协议要求迭代器对象实现两个特殊方法：

1. `__iter__()` 方法：返回迭代器对象自身。该方法被用于支持可迭代对象的语法，使迭代器可以在需要可迭代对象的地方使用。
2. `__next__()` 方法：返回迭代器中的下一个元素。如果没有更多的元素可供迭代，应该抛出 `StopIteration` 异常。

根据迭代器协议的要求，一个对象只要实现了这两个方法，就可以被视为迭代器。

# 把一个生成器函数当前普通函数来运行

这个也是pywebio里看到的。

因为single_input这个函数一定是有yield在里面。

而对于thread方式的，需要把这个当成普通函数来调用。

所以是这样做的：

```
def run_as_function(gen):
    res = None
    while 1:
        try:
            res = gen.send(res)
        except StopIteration as e:
            if len(e.args) == 1:
                return e.args[0]
            return

```

而这个知识点，在chatgpt上查到是这样：

要将生成器函数转换为普通函数并运行，可以使用 `yield from` 或 `yield` 语句来逐步迭代生成器，并获取生成器的值。以下是一个示例：

```python
def generator_func():
    yield 1
    yield 2
    yield 3

def normal_func():
    generator = generator_func()  # 创建生成器对象
    result = []

    # 使用 yield from 语句迭代生成器并获取值
    try:
        while True:
            value = next(generator)  # 获取生成器的下一个值
            result.append(value)
    except StopIteration:
        pass

    return result

output = normal_func()
print(output)  # 输出: [1, 2, 3]
```

在上述示例中，`generator_func()` 是一个生成器函数，通过使用 `yield` 语句生成数值。`normal_func()` 是一个普通函数，它将生成器函数转换为普通函数来运行。

在 `normal_func()` 中，首先创建了生成器对象 `generator`，然后使用 `yield from` 语句逐步迭代生成器并获取值。`next(generator)` 用于获取生成器的下一个值，直到生成器抛出 `StopIteration` 异常为止。

通过将生成器的值添加到 `result` 列表中，最后返回包含所有生成器值的列表。

请注意，生成器在每次迭代时都会保留其内部状态，因此可以在不同的函数调用之间保持生成器的状态。这意味着在每次调用 `normal_func()` 时，将继续从上次停止的位置继续迭代生成器。

使用 `yield from` 或 `yield` 可以将生成器函数转换为普通函数来运行，并逐步获取生成器的值。这样可以在普通函数中利用生成器的特性，进行灵活的数据处理和控制流程操作。

# 把一个生成器函数转成协程来使用

还是pywebio里的。

```
async def to_coroutine(gen):
    res = None
    while 1:
        try:
            c = gen.send(res)
            res = await c
        except StopIteration as e:
            if len(e.args) == 1:
                return e.args[0]
            return

```

# 怎么理解生成器的send函数

理解生成器的 `send()` 函数需要先理解生成器（Generator）和其工作原理。

生成器是一种特殊的迭代器，

它可以在需要时动态生成值，

而不是一次性生成并存储所有值。

生成器函数（Generator function）使用 `yield` 关键字来定义，

==在每次调用生成器的 `next()` 方法时，生成器会执行到下一个 `yield` 语句，并将其值返回。==

生成器函数的执行状态会被暂时保存，直到下一次调用 `next()` 方法。

==`send()` 方法是用于与生成器进行双向通信的方法之一，==

它允许在生成器内部发送数据，并且可以将这些数据赋值给生成器函数中的变量。

以下是一个简单的示例来说明 `send()` 方法的用法：

```python
def my_generator():
    value = yield 0  # 第一次调用next()时，执行到此处，yield 0返回0，等待下一次send()
    while True:
        value = yield value  # 返回接收到的值，并等待下一次send()

gen = my_generator()
result = next(gen)  # 启动生成器，执行到第一个yield语句，返回0
print(result)  # 输出0

result = gen.send(1)  # 发送数据给生成器，并将接收到的值赋值给value，此时生成器继续执行，返回1
print(result)  # 输出1

result = gen.send(2)  # 同上
print(result)  # 输出2
```

在这个例子中，`my_generator()` 是一个生成器函数，它定义了一个无限循环，每次循环会等待接收一个值，并将该值返回。在第一次调用 `next()` 方法时，生成器函数执行到 `yield 0` 处，返回了0，并等待接收下一个值。然后通过 `gen.send(1)` 方法发送了值1给生成器，生成器函数继续执行，返回了接收到的值1，以此类推。

需要注意的是，第一次调用生成器的 `next()` 方法是启动生成器的必要步骤，因为生成器需要执行到第一个 `yield` 语句处才能等待接收数据。

# 参考资料

1、Python3 迭代器与生成器

http://www.runoob.com/python3/python3-iterator-generator.html

2、python的 a,b=b,a+b 和 a=b b=a+b 的区别

https://zhidao.baidu.com/question/304727322833271364.html

3、一文读懂Python可迭代对象、迭代器和生成器

https://blog.csdn.net/zhusongziye/article/details/80246910