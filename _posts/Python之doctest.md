---
title: Python之doctest
date: 2017-09-24 23:28:40
tags:
	- Python

---



doctest的用途是对于在函数的注释里写了测试的情况，进行测试。

doctest有两种使用方式：

1、写在python代码文件里。

2、单独写一个文件。



一个简单例子：

```
def multiply(a, b):
    """
    >>> multiply(4, 3)
    12
    >>> multiply('a', 3)
    'aaa'
    """
    return a * b
if __name__=='__main__':
    import doctest
    doctest.testmod(verbose=True)
```

输入如下：

```
C:\Python27\python.exe D:/work/pycharm/py_test/test.py
Trying:
    multiply(4, 3)
Expecting:
    12
ok
Trying:
    multiply('a', 3)
Expecting:
    'aaa'
ok
1 items had no tests:
    __main__
1 items passed all tests:
   2 tests in __main__.multiply
2 tests in 2 items.
2 passed and 0 failed.
Test passed.

Process finished with exit code 0
```



参考资料

1、

http://liuchunming033.github.io/posts/2016/06/13/python-doctest.html