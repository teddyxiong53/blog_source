---
title: Python之写自己的实用工具组件包
date: 2017-09-29 22:21:43
tags:
	- Python

---



这个的目的有：

1、学习Python包的写法。

2、学习setup.py的写法。

3、把平时见到的好用的组件整理起来，方便自己使用。



# 1. 目录搭建

新建一个myutils的目录。下面先新建两个空文件：`__init__.py`，setup.py。

```
pi@raspberrypi:~/work/test/python$ tree
.
└── myutils
    ├── __init__.py
    └── setup.py

1 directory, 2 files
```

我们在当前目录启动Python shell。

我们第一个要做的事情，是把我们的myutils这个包可以被import使用。直接在`~/work/test/python`

这个目录下，import myutils就可以了。

查看help信息和dir信息：

```
>>> help(myutils)
Help on package myutils:

NAME
    myutils

FILE
    /home/pi/work/test/python/myutils/__init__.py

PACKAGE CONTENTS
    setup
    
>>> dir(myutils)
['__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__']
```

# 2. 开始加入第一个小的模块storage

这个模块是从webpy里弄出来的，就实现用xxx.yyy这种方式来访问属性。

代码内容如下：

```
class Storage(dict):
	"""
	a storage object is like a dict, you can use obj.foo as obj['foo']
	
	"""
	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError,k:
			raise AttributeError, k
			
	def __setattr__(self, key, value):
		self[key] = value
		
	def __delattr__(self, key):
		try: 
			del self[key]
		except KeyError, k:
			raise AttributeError,k
	def __repr__(self):
		return '<Storage ' + dict.__repr__(self) + '>'
		
storage = Storage

if __name__ == "__main__":
	s1 = storage(a=1)
	print s1.a
```

现在你用help查看storage的信息，你会发现有很多的帮助信息，实际上你并没有写这些帮助信息。现在你可以知道help查看的信息从哪里来的了。

我们单独执行storage.py。可以把我们写在main里的小测试跑一下，是没有问题的。

现在我们试图在Python shell里进行使用看看。

这样看看。

```
from myutils import storage

s1 = storage(a=1)
```

居然报错了。

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'module' object is not callable
```

```
>>> print storage
<module 'myutils.storage' from 'myutils/storage.py'>
```

可以看到现在的storage是一个module的名字。而不是类的名字。

网上找到解决的方法：

```
>>> from myutils.storage import storage
>>> print storage
<class 'myutils.storage.Storage'>
```

这样，storage才是作为一个类被引入进来。





