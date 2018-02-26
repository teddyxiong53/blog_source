---
title: Python之常用内置方法
date: 2017-09-30 23:19:37
tags:
	- Python

---



Python提供了一些基本的函数，下面把常用的列出来。

从Python2.7的帮助文档里梳理出来的。

总数量是76个。



# abs(x)函数

x可以是int、float、复数。返回绝对值。

# all(iterable)函数

看元素是不是都是真，如果是，返回True。

```
>>> a = (1,2)
>>> all(a)
True
>>> a = (0,1)
>>> all(a)
False
```

# any(iterable)函数

和all对应，这个是只要一个位真，就返回True。

# basestring类

是str和unicode类的父类。不能直接用，一般是用来判断字符串。

```
>>> a = "xxx"
>>> isinstance(a, basestring)等价于isinstance(a, (str, unicode))
True
>>> a = (1,2)
>>> isinstance(a, basestring)
False
```

# bin(x)方法

这个就是返回一个int值对应的二进制字符串。

```
>>> bin(16)
'0b10000'
```

# bool([x])函数

不带参数，则返回False。

否则根据参数来看是返回True还是False。

# bytearray()函数

字节数组函数。返回一个字节数组。这个数组里的元素值在0到255。

用法：

```
>>> bytearray()
bytearray(b'')
>>> bytearray([1,2,3])
bytearray(b'\x01\x02\x03')
>>> bytearray('xxxyyy','utf-8')
bytearray(b'xxxyyy')
```





# callable(object)

用来检查一个对象是否可调用。

看例子就懂了。

```
>>> a = (1,2)
>>> callable(a)
False
>>> a = lambda x:x+1
>>> callable(a)
True
```

# chr(i)

传递进来的参数是一个int类型。从这个函数的形参的写法，就可以看出Python的形参的规律。

x：不限定。

i：整数。

iterable：

object：

```
>>> chr(90)
'Z'
```

这个函数返回的是一个ascii字符。输入的是一个整数。



# classmethod

就是`@classmethod`修饰符。



# cmp(x,y)函数

```
>>> cmp(1,2)
-1
>>> cmp(1,1)
0
>>> cmp(2,1)
1
```

# compile()函数

用来编译一个字符串的。

不常用。

# complex()函数

得到一个复数。

举例：

```
>>> complex(1,2)
(1+2j)
```



# delattr(object, name)

删除属性。

```
class Student(object):
    name = 'xxx'
    age = 15

stu1 = Student()
print "name:", stu1.name
print "age:", stu1.age

#delattr(stu1, "age") #这个是错误的。
delattr(Student, "age")
print "age:", stu1.age
```



# dict([arg])

创建一个字典。

参数可以是键值对，可以元素容器，也可以是可迭代对象。

```
>>> dict(a='aa',b='bb',c='cc')
{'a': 'aa', 'c': 'cc', 'b': 'bb'}
>>> dict(zip(['a','b'], ['aa','bb']))
{'a': 'aa', 'b': 'bb'}
>>> dict([('a','aa'),('b', 'bb')])
{'a': 'aa', 'b': 'bb'}
```



# dir([object])

1、不带参数的时候，返回当前范围内的变量、方法以及定义的类型列表。

2、带参数的时候，返回的是参数的相关内容。

3、如果参数有实现``__dir()__`方法，就会被调用到。

4、如果参数没有实现`__dir()__`方法，那么这个方法就会尽可能地收集信息。



# divmod()函数

得到一个包括2个元素的元组，里面是商和余数。

```
>>> divmod(7,2)
(3, 1)
```



# enumerate()函数

就是枚举遍历。

一般用来遍历元组、列表、字符串。

```
list1 = ['aa', 'bb', 'cc']
for i,content in enumerate(list1):
    print i, content
```

结果是这样：

```
0 aa
1 bb
2 cc
```





# eval(expression, globals, locals)

里面是放一个字符串，计算字符串里的内容。

```
>>> x = 7
>>> eval('x*3')
21
>>> eval('pow(2,3)')
8
>>>
```

# execfile()函数

参数就是一个py文件。执行对应的文件。

# file函数

file函数用来创建一个file对象。它有一个别名是open。

参数有3个：

1、文件名。

2、模式。

3、buffer。0不缓冲，1表示行缓冲，大于1表示缓冲区缓冲。

# filter函数

用来过滤掉不符合条件的元素。

语法是：

```
filter(func, iterable)
```

2个参数：

1、判断函数。用来判断是否符合条件。

2、可迭代对象。

```
def is_odd(n):
    return n%2==1

list_filtered = filter(is_odd, [1,2,3,4])
print list_filtered
```



# float函数

```
>>> float(2)
2.0
```

#format格式化函数

从Python2.6开始，新增了格式化字符串的函数str.format。

基本语法是用`{}`和`:`来替代之前的`%`。

基本用法：

```
>>> "{}--{}".format("aaa", "bbb")
'aaa--bbb'
>>> "{0}--{1}--{0}".format("aaa", "bbb")
'aaa--bbb--aaa'
```

还可以格式化数字：

```
print {:.2f}.format("3.1415926")
```

我感觉用途不大。

# frozenset函数

字面意思是冻结的集合。这样的集合不能增加元素。



# getattr函数

从一个object里获取属性。

```
class Student(object):
    name = "xxx"

student1 = Student()

print getattr(student1, "name")
```

# globals函数



# hasattr函数



# hash函数

获取一个object的hash值。

# help函数



# hex函数

把10进制转成16进制。



# id函数

获取object的内存地址。



# input函数

input等价于`eval(raw_input(prompt))`。

input和raw_input的区别：

1、raw_input把所有的输入当成字符串来看待。返回的是字符串类型。

2、而input对于数字输入会当成int和float来进行处理。

# int函数

得到一个整数。可以指定进制。

```
>>> int('123',16)
291
```



# isinstance函数

isinstance和type函数的区别：

1、isinstance会考虑继承关系，会认为一个子类是一种父类。

2、type则不会考虑继承关系。

# issubclass函数



# iter函数

iter函数用来生成迭代器。返回的就是一个迭代器。

```
list1 = [1,2,3]
for i in iter(list1):
    print i

print "-----------"
for i in list1:
    print i
```

这2个的输出结果是一样的。

迭代器可以用next来进行遍历。



# len函数

返回对象的长度。

```
>>> len("xxx")
3
```

# list函数

list函数是用来把元组转换为列表的。

元组和列表的区别：

1、元组的内容不能修改。列表的可以。

2、元组用小括号，列表用中括号。

```
mytuple = ('aaa', 1, 2)
mylist = list(mytuple)
print "mytuple:", mytuple
print "mylist:", mylist
```

结果是：

```
mytuple: ('aaa', 1, 2)
mylist: ['aaa', 1, 2]
```

# locals函数



# long函数

跟int类型。



# map函数

用提供的函数，对指定的序列进行映射。

格式是：

```
map(func, iterable, ...)
```

Python2返回的是列表，Python3返回的是迭代器。

```
def add_one(x):
    return x+1

print map(add_one, [1,2,3])
```







# max/min函数

```
max([1,2,3])
max(1,2,3)

>>> d = {"a":1,"b":2,"c":3}
>>> max(d)
'c'
```



# memoryview函数



# next函数

返回迭代器的下一个元素。

```
myiter = iter([1,2,3])

while True:
    try:
        x = next(myiter)
        print x
    except StopIteration:
        break
```



# oct函数

跟hex类型，这个是转成8进制的。



# open函数



# ord函数

ord函数跟chr函数是配对的。

ord是把ascii字符转成整数。



# pow函数

次方函数。



#print函数

1、在Python2里，print 是一个关键字。

2、在Python3里，print变成了一个函数。



# property函数



# range函数

得到一个列表。



# raw_input函数



# reduce函数

对元素进行累积。

格式是：

```
reduce(func, iterable)
```



```
def myadd(x,y):
    return x+y

print reduce(myadd, [1,2,3,4])
```



# reload函数

把之前import的模块进行重新载入一次。

一般是用来修改编码的时候用的。

```
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf8')
print sys.getdefaultencoding()
```

如果没有reload这一句，sys.setdefaultencoding都会报错的。



# repr函数

把object转化成解释器读取的形式。

```
>>> mystr = "xxyy"
>>> repr(mystr)
"'xxyy'"
>>> mydict = {'a':'aa','b':'bb'}
>>> repr(mydict)
"{'a': 'aa', 'b': 'bb'}"
```



# reverse函数

进行反向排序。是属于list的一个函数。

list.reverse()这样用的。



# round函数

对浮点数进行四舍五入。



# set函数

返回一个无序、不重复的元素集。

```
>>> set1 = set('baidu')
>>> set2 = set('google')
>>> set1
set(['a', 'i', 'b', 'u', 'd'])
>>> set2
set(['e', 'o', 'g', 'l'])
>>>
```



可以进行交集、并集、差集运算。

```
>>> set1 & set2
set([])
>>> set1 | set2
set(['a', 'b', 'e', 'd', 'g', 'i', 'l', 'o', 'u'])
>>> set1 - set2
set(['a', 'i', 'b', 'u', 'd'])
```



# setattr函数



# slice函数

对object进行切片。

一个用法是这样的：

```
>>> myslice = slice(3)
>>> myslice
slice(None, 3, None)
>>> mylist = range(10)
>>> mylist
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
>>> mylist[myslice]
[0, 1, 2]
```



# sorted函数

函数原型是这样：

```
sorted(...)
    sorted(iterable, cmp=None, key=None, reverse=False) --> new sorted list
```

```
>>> sorted("bca")
['a', 'b', 'c']
>>> sorted([3,1,2])
[1, 2, 3]
```



# staticmethod函数



# str函数







# sum函数

```
>>> sum([1,2,3],100)
106
>>> sum([1,2,3])
6
```



# super函数

调用父类的一个方法。

super是用来解决多重继承的问题的。

多重继承会有查找顺序，重复调用等问题。



# tuple函数

将列表转成元组的函数。



# type函数



# unichr函数



# vars函数

没什么用。



# xrange函数

跟range的区别就是xrange得到是一个生成器。而不是一个list。



# zip函数

将元素打包成一个个的元组。

