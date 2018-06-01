---
title: Python之glob库
date: 2018-06-01 22:55:57
tags:
	- glob

---



glob字面含义是一滴、一团的意思。

glob是Python自带的库，用来进行文件操作的一个库。

主要目的就是用来查找符合条件的文件。

类似于windows下是文件搜索功能。

支持三个通配符。

```
* ? []
```

主要方法就是glob方法。

帮助信息是这样。就这么点。

```
>>> help(glob)
Help on module glob:

NAME
    glob - Filename globbing utility.

FILE
    /usr/lib/python2.7/glob.py

MODULE DOCS
    http://docs.python.org/library/glob

FUNCTIONS
    glob(pathname)
        Return a list of paths matching a pathname pattern.
        
        The pattern may contain simple shell-style wildcards a la
        fnmatch. However, unlike fnmatch, filenames starting with a
        dot are special cases that are not matched by '*' and '?'
        patterns.
    
    iglob(pathname)
        Return an iterator which yields the paths matching a pathname pattern.
        
        The pattern may contain simple shell-style wildcards a la
        fnmatch. However, unlike fnmatch, filenames starting with a
        dot are special cases that are not matched by '*' and '?'
        patterns.

DATA
    __all__ = ['glob', 'iglob']
```

我们就用一个glob方法就够了。

举例：

```
import glob
files = glob.glob("./*.jpg")
print files
```





# 参考资料

1、python中的一个好用的文件名操作模块glob

https://blog.csdn.net/suiyunonghen/article/details/4517103