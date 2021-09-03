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

NumPy是Python中科学计算的基础包。

它是一个Python库，提供多维数组对象，各种派生对象（如掩码数组和矩阵），

以及用于数组快速操作的各种API，

有包括数学、逻辑、形状操作、排序、选择、输入输出、离散傅立叶变换、基本线性代数，基本统计运算和随机模拟等等。

NumPy包的核心是 *ndarray* 对象。它封装了python原生的同数据类型的 *n* 维数组，为了保证其性能优良，其中有许多操作都是代码在本地进行编译后执行的。



NumPy 的数组中比较重要 ndarray 对象属性有：

| 属性             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| ndarray.ndim     | 秩，即轴的数量或维度的数量                                   |
| ndarray.shape    | 数组的维度，对于矩阵，n 行 m 列                              |
| ndarray.size     | 数组元素的总个数，相当于 .shape 中 n*m 的值                  |
| ndarray.dtype    | ndarray 对象的元素类型                                       |
| ndarray.itemsize | ndarray 对象中每个元素的大小，以字节为单位                   |
| ndarray.flags    | ndarray 对象的内存信息                                       |
| ndarray.real     | ndarray元素的实部                                            |
| ndarray.imag     | ndarray 元素的虚部                                           |
| ndarray.data     | 包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。 |

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



# 疑问

## reshap -1是什么意思

表示自动推算这一个维度的值。不明确指定的意思。

但是我们一般是用来把二维数组拍平成一维的。

```
>>> z = np.array([[1, 2, 3, 4],[5, 6, 7, 8],[9, 10, 11, 12],[13, 14, 15, 16]])

>>> print(z)
[[ 1  2  3  4]
 [ 5  6  7  8]
 [ 9 10 11 12]
 [13 14 15 16]]
>>> print(z.shape)
(4, 4)
>>> print(z.reshape(-1))
[ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16]
>>> print(z.reshape(-1,1))  #我们不知道z的shape属性是多少，
                            #但是想让z变成只有一列，行数不知道多少，
                            #通过`z.reshape(-1,1)`，Numpy自动计算出有16行，
                            #新的数组shape属性为(16, 1)，与原来的(4, 4)配套。
[[ 1]
 [ 2]
 [ 3]
 [ 4]
 [ 5]
 [ 6]
 [ 7]
 [ 8]
 [ 9]
 [10]
 [11]
 [12]
 [13]
 [14]
 [15]
 [16]]
>>> print(z.reshape(2,-1))
[[ 1  2  3  4  5  6  7  8]
 [ 9 10 11 12 13 14 15 16]]
```





# 参考资料

1、NumPy 教程

https://www.runoob.com/numpy/numpy-tutorial.html

2、

https://baike.baidu.com/item/numpy/5678437?fr=aladdin