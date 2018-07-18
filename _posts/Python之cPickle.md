---
title: Python之cPickle
date: 2018-07-15 11:20:02
tags:
	- Python

---



pickle的意思是腌制的意思。

在python里是用来对对象进行序列化的。

cPickle可以对任意一种类型的Python对象进行序列化操作。

主要的函数有：

1、dump。把python对象序列化保存到本地文件。

```
import cPickle

data = range(10)
cPickle.dump(data, open("./data.dat", "wb"))
```

我们打开data.dat文件看看。

```
(lp1
I0
aI1
aI2
aI3
aI4
aI5
aI6
aI7
aI8
aI9
a.
```

2、load。从文件里载入对象。

```
import cPickle

data = range(10)
cPickle.dump(data, open("./data.dat", "wb"))

data1 = cPickle.load(open("./data.dat", "rb"))
print data1
```

3、dumps和loads。跟上面函数的不同，就是保存到字符串里。

