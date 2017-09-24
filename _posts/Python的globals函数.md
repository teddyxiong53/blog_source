---
title: Python的globals函数
date: 2017-02-11 18:10:57
tags:
	- python
---
globals函数和locals是一对，用来提供基于字典来访问局部和全局变量的方式。
这里需要先解释一下Python的一个核心概念，名字空间（namespace）。名字空间是表示一个name到一个object的映射关系。这个概念就相当于C语言的变量的作用域了。
```
Type "help", "copyright", "credits" or "license" for more information.
>>> print globals()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', '__doc__': None, '__package__': None}
>>>
>>> x = 1
>>> print locals()
{'__builtins__': <module '__builtin__' (built-in)>, '__name__': '__main__', 'x': 1, '__doc__': None, '__package__': None}
>>>
```

locals是只读的，globals不是。

