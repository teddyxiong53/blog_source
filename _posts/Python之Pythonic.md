---
title: Python之Pythonic
date: 2018-06-23 17:16:14
tags:
	- Python

---



Pythonic，就是极具Python特色的Python代码。

常见的例子：

交互2个变量的内容：

```
a,b = b,a
```

判断值的范围：

```
1 < x <10
```

文件处理：

```
with open(path) as fp:
	pass
```



pythonic是一个模糊的概念，有点像python惯用法的意思。

惯用法往往不能从其他语言移植过来。

例如for循环。



反向遍历：

```
for l in reversed(lyst):
	print(l)
```

遍历一个集合及其下标：

```
for i, l in enumerate(lyst):
	print("{}->{}".format(i,l))
```

遍历两个集合：

```
names = ['allen', 'bob', 'charles']
colors = ['red', 'green', 'blue']

for name, color in zip(names, colors):
    print("{} -> {}".format(name, color))
```

有序遍历：

```
colors = ['red', 'green', 'blue']

for color in sorted(colors):
    print(color)
for color in sorted(colors, reverse=True):
    print(color)
```

自定义遍历规则：

```
colors = ['red', 'green', 'blue']

for color in sorted(colors, key=len):
    print(color)
```



调用一个函数直到遇到标记值

普通写法：

```
blocks = []
with open('1.txt', 'r') as f:
    while True:
        block = f.read(32)
        if block == '':
            break
        blocks.append(block)
print(blocks)
```

pythonic写法：

```
from functools import partial
blocks = []
with open('1.txt', 'r') as f:
    for block in iter(partial(f.read, 32), ''):
        blocks.append(block)
print(blocks)
```

unpack一个序列

```
person = 'teddy', 'xiong', 20, 'basketball'
fname, lname, age, habbit = person
print(fname, lname, age, habbit)
```





参考资料

1、Pythonic到底是什么玩意儿？

https://blog.csdn.net/gzlaiyonghao/article/details/2762251

2、写出优雅又地道的pythonic代码

https://blog.csdn.net/weixin_30408739/article/details/96212940