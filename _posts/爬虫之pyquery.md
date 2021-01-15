---
title: 爬虫之pyquery
date: 2021-01-12 11:00:11
tags:
	- 爬虫

---

--

pyquery，是一个类似jquery的python库。

api尽量跟jquery保持一样的风格。

使用lxml来解析html和xml文件。

不能产生和跟js代码交互。

作者写这个库的动力是：他很喜欢jquery，所以在python里实现一个jquery。

快速入门

```
from pyquery import PyQuery as pq
d = pq("<html></html>")#可以从一个html字符串
d = pq(url='http://google.com') #可以从一个url
d = pq(filename='1.html')#可以从一个文件名
# d现在相当于jquery里的$了。d就是dollar缩写。只是一个变量名。用得顺手而已。
p = d("#hello") 
print(d.html())
```



参考资料

1、官网

https://pythonhosted.org/pyquery/