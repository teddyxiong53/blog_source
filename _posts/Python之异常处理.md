---
title: Python之异常处理
date: 2017-09-29 21:17:20
tags:
---



先从最简单的错误开始看，在Python shell里去打开一个不存在的文件。

```
>>> open('1.txt', 'r')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IOError: [Errno 2] No such file or directory: '1.txt'
>>> 
```

可以看到报了IOError。

# 用try except

如果我们想要不管这种错误，怎么办呢？这样我们就可以忽略这个错误了。用try except。

```
try:
	open('abc.txt', 'r')
except IOError:
	print "xxx"
```

我们再试图使用一个不存在的变量看看。

```
>>> print aa
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'aa' is not defined
```

可以看到报了NameError。可以用msg来把错误信息打出来。这个msg是随便写的名字，随便什么名字都行。

```
try:
	print aa
except NameError, msg:
	print msg
	
```

# 用try finally

finally部分放必须执行的代码，一般是释放资源的代码。



# 用raise把异常往上抛



# 常见的异常类型

AssertionError：断言异常

AttributeError：试图访问一个不存在的属性。

IOError：IO异常。一般是文件打不开。

ImportError：import异常。基本是路径不对。

IndentationError：语法错误，代码缩进不正常。一般是空格和tab混用。

IndexError：索引超出范围。

KeyError：访问dict里面不存在的key。

KeyboardInterrupt：按下Ctrl+C。

NameError：访问不存在的变量。

SyntaxError：代码逻辑错误。

TypeError：参数类型不对。

UnboundLocalError：试图访问没有初始化过的全局变量。

ValueError：传入一个不被期望的值。



