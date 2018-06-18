---
title: Python之itertools
date: 2018-06-18 20:59:28
tags:
	- Python

---



先看help信息。

```
NAME
    itertools - Functional tools for creating and using iterators.

FILE
    (built-in)
CLASSES
    __builtin__.object
        chain
        combinations
        combinations_with_replacement
        compress
        count
        cycle
        dropwhile
        groupby
        ifilter
        ifilterfalse
        imap
        islice
        izip
        izip_longest
        permutations
        product
        repeat
        starmap
        takewhile
```



# chain

##chain

创建一个新的迭代器，把参数里的迭代器都串联起来。

```
#!/usr/bin/python

from itertools import chain
mychain = chain('ab', 'cd', 'e')
for item in mychain:
	print item
```



```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py
a
b
c
d
e
```

## chain.from_iterable



# 参考资料

1、Python中itertools模块用法详解

https://www.jb51.net/article/55626.htm