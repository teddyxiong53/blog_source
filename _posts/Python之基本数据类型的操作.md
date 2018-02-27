---
title: Python之基本数据类型的操作
date: 2018-02-27 13:48:33
tags:
	- Python

---



Python的 基本数据类型就是5种：

1、number。

2、string。

3、元组。

4、列表。

5、字典。



另外还有一个set。

set相当于dict把key去掉了一样。类似一个list，但是set里的元素不能重复。

set从2.6版本开始就过时了。不推荐用。



下面依次看看这些类型有哪些常用的操作。

# number

数字类型有有4种，int、long、float、complex。

没有什么特别的操作。

# 字符串

1、索引的方法。从左到右，和从右到左两种方式。

```
>>> mystr = "abc"
>>> print mystr[-2]
b
>>> print mystr[-2:]
bc
>>> print mystr[:-2]
a
```

2、加和乘的操作。

```
>>> mystr2 = "xyz"
>>> mystr+mystr2
'abcxyz'
>>> mystr*3
'abcabcabc'
>>> 
```



# 元组

元组的出现，对于函数返回多个值很有用。



1、相加和相乘。

```
>>> mytuple1 = (1,2,3)
>>> mytuple2 = ('a','b','c')
>>> mytuple1 + mytuple2
(1, 2, 3, 'a', 'b', 'c')
```

2、索引。



# 列表

1、相加相乘。

2、索引。



# 字典

