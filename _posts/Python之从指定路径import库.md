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



import的查找路径的顺序是怎样的？

```
标准库
第三方库
当前路径
```



什么是绝对导入？什么是相对导入？

```
绝对导入
import A.B
from A import B
```

```
相对导入
from . import B
from ..A imprt B
```

python2里是默认是相对路径导入。python3默认为绝对路径导入。

有时候，在python2的代码里，会加上这句：

```
from __future__ import absolute_import
```

这个又是为了达到什么目标呢？

是为了禁止隐式相对导入。

对于下面这个目录结构。

```
thing
├── books
│ ├── adventure.py
│ ├── history.py
│ ├── horror.py
│ ├── __init__.py
│ └── lovestory.py
├── furniture
│ ├── armchair.py
│ ├── bench.py ---这个
│ ├── __init__.py
│ ├── screen.py
│ └── stool.py 这个
└── __init__.py
```

如果我们要在stool.py里音乐bench.py。有下面三种方式：

```
import bench # 这个就是隐式相对导入。不推荐。python3废弃了。这种方式只适合用来导入系统路径下的。
from . import bench # 这个是显式相对导入
from furniture import bench # 这个就是绝对导入。
```



import特点，防止重复导致，你import多次，只有第一次有用。

如果你的py文件修改了，希望另外一个脚本里把这个修改体现出来。

例如服务器运行后，不让停止的情况下，重新load某个脚本。

```
from imp import reload
reload(xxx)
```

imp里的reload已经是过时的了。

sys.reload可以用。



# 参考资料

1、ImportError:attempted relative import with no known parent package

https://blog.csdn.net/nigelyq/article/details/78930330

2、Python import搜索的路径顺序

https://blog.csdn.net/csdn912021874/article/details/83017425