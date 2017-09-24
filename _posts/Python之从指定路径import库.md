---
title: Python之从指定路径import库
date: 2017-09-24 10:35:02
tags:
	- python

---



学习python的module的写法，写了一个module，但是不知道怎么使用起来。

module1.py文件：

```
#!/usr/bin/python

def func1():
	print "module1 func1"
__all__ = [func1]
```

然后在命令行上进行import。

最简单的做法是这样的：

```
import sys
sys.path.append("./")
import module1

```

查看相关情况是这样的：

```
>>> import module1
>>> help(module1)
Help on module module1:

NAME
    module1

FILE
    /home/pi/work/test/python/module1.py

DATA
    __all__ = [<function func1>]

(END)

>>> dir(module1)
['__all__', '__builtins__', '__doc__', '__file__', '__name__', '__package__', 'func1']
```





