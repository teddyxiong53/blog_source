---
title: python之numpy学习
date: 2019-09-29 16:57:48
tags:
	- python

---

1

numpy主要是用来做矩阵计算的。

numpy + scipy + matplotlib 可以用来取代matlab。

实用的线性代数、傅里叶变换和随机数生成函数。

numpy和稀疏矩阵运算包scipy配合使用更加方便。

https://www.numpy.org.cn/



# ndarray

n维数组。这个是numpy一个重要的基础数据。

opencv的imread函数，返回的就是这么一个对象。

```python
#coding: utf-8
from __future__ import print_function
import numpy as np


# 一维数组
a = np.array([1,2,3])
print(a)

# 二维数组
a = np.array([[1,2],[3,4]])
print(a)
# 指定最小维度
a = np.array([1,2,3], ndmin=2)
print(a)
#指定dtype
a = np.array([1,2,3], dtype=complex)
print(a)
```

# 数据类型

numpy支持的数据类型比python要多。

有int8、uint8这些跟C语言里一一对应的类型。

还有float16这个一般没有见过的类型。

另外有complex64、complex128 这种复数类型。

dtype可以用来定义类似C语言结构体的类型。

```
#coding: utf-8
from __future__ import print_function
import numpy as np


dt = np.dtype(np.int32)
print(dt)

#int8、int16、int32、int64可以写成'i1'到'i8'这样的字符串，是等价的。
dt = np.dtype('i8')
print(dt)

# 定义复杂类型
dt = np.dtype([('age', np.int8)])
print(dt)
a = np.array([(10,),(20,)], dtype=dt)
print(a)

# 定义一个student数据结构
student = np.dtype(
    [
        ('name', 'S20'),
        ('age', 'i1'),
        ('marks', 'f4')
    ]
)
print(student)
a = np.array([
    ('aaa', 10, 90),
    ('bbb', 11,95)
])
print(a)
```

# 数组属性

```
#coding: utf-8
from __future__ import print_function
import numpy as np

a = np.arange(24)
print(a)
print(a.ndim)
b = a.reshape(2,4,3)
print(b)
print(b.ndim)
print(b.shape)
print(b.flags)
```

# 创建数组

除了array方法可以用来创建数组之外。

还有这些方法：

```
empty：
	创建矩阵，里面的元素是随机的。
	3个参数。
	参数1：
		shape。就是维度说明。
	参数2：
		dtype。默认是float。
	参数3：
		order。表示在计算机里存储的顺序。有两种选择，默认是C，还可以是Fortan。
zeros：
	创建空矩阵。
	参数跟empty一样，区别是内容会初始化为0 。
ones：
	这个是填1 。
	
```

# 从已有数组创建数组

```
asarray
frombuffer
fromiter
```

# 从数值范围创建数组

```
arange
	4个参数：
	参数1：
		start。默认是0 。
	参数2：
		stop。
	参数3：
		step。默认是1.
	参数4：
		dtype。
linspace
logspace
```

# 切片和索引

有两种方式

1、借助默认的slice函数。

```
a = np.arange(10)
s = slice(2,7,2)
print(a)
print(a[s]) #注意这里是a[s]，而不是s
```

2、用冒号分割。

```
a = np.arange(10)
b = a[2:7:2]
print(b)
```







# 参考资料

1、NumPy 教程

https://www.runoob.com/numpy/numpy-tutorial.html

2、

https://baike.baidu.com/item/numpy/5678437?fr=aladdin