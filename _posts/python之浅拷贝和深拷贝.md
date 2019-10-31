---
title: python之浅拷贝和深拷贝
date: 2019-10-29 13:37:18
tags:
	- Python

---

1

```
a = ['a', 1, ['aa']]
b = a #id(a)和id(b)一样。里面内容的id也都一样。
import copy
c = a.copy() # id(a)和id(b)不一样，里面内容的id一样。
d = a.deepcopy() #
```

对于非容器类型，没有拷贝的说法。



参考资料

1、图解Python深拷贝和浅拷贝

https://www.cnblogs.com/wilber2013/p/4645353.html

