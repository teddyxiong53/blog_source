---
title: Python之dict的使用
date: 2017-09-30 23:01:25
tags:
	- Python
	- dict

---



# values()和itervalues()使用比较

```
d = {"a":1, "b":2}
d.values()等价于list(d.itervalues())，都是得到[1，2]这样一个结果。

```

上面这个list，是一个类的名字，相当于用一个iterable对象构造了一个list出来。

# 嵌套dict效果

```
>>> redirect = dict(headers=dict(location='/redirect'))
>>> print redirect
{'headers': {'location': '/redirect'}}
```



