---
title: python之ellipsis
date: 2019-10-12 17:49:32
tags:
	- Python

---

--

ellipsis是省略号的意思。表示三个点。

主要作用有：

1、等价于pass。相当于TODO的意思。

```
def func():
    ...
```

2、循环数据结构，一个复合对象包含指向自身。

```
L = [1,2,3]
L.append(L)
print(L)

输出为：
[1, 2, 3, [...]]
```

3、用来模拟一些情况，让代码看起来更加美观，例如等差数列。

Ellipsis是单例的。其布尔值是True。





参考资料

1、

