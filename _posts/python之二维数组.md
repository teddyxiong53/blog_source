---
title: python之二维数组
date: 2019-10-29 13:23:18
tags:
	- Python

---

1

一个直观的方式是这样，但是这个方式是有问题的。

如下所示：

```
m = n =3                             

test = [[0]*m] *n                    

test                                 
[[0, 0, 0], [0, 0, 0], [0, 0, 0]]

test[0][0] = 1                       

test                                 
[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
```

原因是`matrix= [array]*3`这样使用的时候，实际上是创建了3个指向array的引用。

所以不能用这种方法。

可行的方式有：

# 直接创建法

```
matrix = [[0,0,0],[0,0,0],[0,0,0]]
```

这种方式太麻烦了。不用。

# 列表生成式法

```
matrix = [[0 for i in range(m)] for j in range(n)]  
```

这个可以用。

# 使用numpy

```
import numpy as np
matrix = np.zeros((m,n), dtype=np.int)
```



参考资料

1、Python创建二维数组(关于list的一个小坑)

https://www.cnblogs.com/PyLearn/p/7795552.html