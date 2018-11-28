---
title: Python之pkgutil
date: 2018-11-28 21:00:44
tags:
	- Python

---



一个py文件就是一个模块，如果一个目录下有`__init__.py`文件，那么这个目录就是一个package。



pkgutil常用的函数就2个：

1、iter_modules

2、walk_packages



写一个简单的目录。

```
teddy@teddy-ubuntu:~/work/test/python$ tree
.
├── test_package
│   ├── __init__.py
│   ├── __init__.pyc
│   └── xx.py
└── test.py
```

test.py：

```
import pkgutil

pkg_dir="./test_package"

for finder, name, ispkg in pkgutil.walk_packages(pkg_dir):
	print name
```

xx.py内容：

```
def xx_func1():
	print "xx_func1"
	
```

其余文件为空。

运行结果：

```
teddy@teddy-ubuntu:~/work/test/python$ python test.py 
test
test_package
test_package.xx
```



# 参考资料

1、python中的import（涉及pkgutil和inspect包）

https://www.jianshu.com/p/4c440ea08e00

