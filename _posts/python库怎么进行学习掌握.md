---
title: python库怎么进行学习掌握
date: 2017-01-05 19:27:23
tags:
	- python
---
python里有很多的库，有的是自带的，有的是第三方的。python的文档比起java，并没有那么规范齐备。对于库的使用，应该怎样进行查阅和学习呢？

# 1. dir函数
这是一个內建函数。
```
>>> import json
>>> dir
<built-in function dir>
>>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'help', 'json']
>>> dir(json)
['JSONDecoder', 'JSONEncoder', '__all__', '__author__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', '__version_
_', '_default_decoder', '_default_encoder', 'decoder', 'dump', 'dumps', 'encoder', 'load', 'loads', 'scanner']
```
dir函数不带参数的时候，会返回当前范围内的变量、方法、类型列表。带参数的时候，返回参数的属性和方法列表。
如果参数对应的对象含有`__dir__()`这个函数，就会调用`__dir__()`这个函数，否则就最大限度地收集参数信息。
这个就可以对某个模块或者库有个简单的了解，知道有哪些东西可以用。

# 2. help函数
dir看的内容比较简略，help函数则可以看到详细的信息。
还是以json库为例来分析。
```
>>> help(json)

Help on package json:Save  <F8> Pastebin  <F9> Pager  <F2> Show Source 

NAME
    json

FILE
    /usr/lib/python2.7/json/__init__.py

MODULE DOCS
    http://docs.python.org/library/json

DESCRIPTION
    JSON (JavaScript Object Notation) <http://json.org> is a subset of
    JavaScript syntax (ECMA-262 3rd edition) used as a lightweight data
    interchange format.
```
可以看到输出了非常详细的文档。我们看到的这个内容其实是写在代码的注释里的。在`json/__init__.py`开头的注释里的。这个内容可以像javadoc那样输出成很规范的文档。

有了dir和help函数，基本够用了。

python默认的命令行没有补全功能，用起来比较低效。在Ubuntu下可以安装bpython。这个代码提示和补全功能都比较强大。
```
# sudo apt-get install bpython
# bpython 
```





