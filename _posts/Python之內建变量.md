---
title: Python之內建变量
date: 2018-06-10 10:35:23
tags:
	- Python

---



Python里的內建变量有哪些？

```
__name__
	用来判断当前文件是不是执行的入口文件，如果是，__name__等于__main__。否则就是文件名。
__file__
__doc__

```



#`__init__.py`文件作用

如果没有这个文件，一个目录只是一个普通目录。

有了这个文件，一个目录就变成了一个package了。

# `__doc__`的作用

写在最前面的，用3个引号括起来的部分的注释。

```
#!/usr/bin/python
"""
xxxx
yyyy
"""
import os, os.path
from test import Test

print __doc__
```

得到结果：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test2.py 

xxxx
yyyy

```



这样得到的是None。

```
#!/usr/bin/python

import os, os.path
from test import Test
"""
xxxx
yyyy
"""
print __doc__
```

# `__file__`和sys.argv[0]

```
#!/usr/bin/python
import sys
print __file__
print sys.argv[0]
```

结果是一样的。

```
teddy@teddy-ubuntu:~/work/test/python$ ./test2.py 
./test2.py
./test2.py
```



# 参考资料

1、

