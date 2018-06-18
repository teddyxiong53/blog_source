---
title: Python之typing
date: 2018-06-18 11:41:03
tags:
	- Python

---



Python作为一种弱类型的语言，就可能出现这样的一种情况。

很多人写完代码，一段时间后，再去看，不知道自己写的函数的参数类型是啥，返回的又是什么类型。

这个很影响阅读代码的效率。

为了解决这种问题，就引入了typing这个模块。



typing模块只有Python3.5以上版本才支持。

一个典型用法。

```
#!/usr/bin/python3

from typing import List, Tuple, Dict

def func(a:int, string:str, f:float, b:bool) -> Tuple[List, Tuple, Dict, bool]:
	list1 = list(range(a))
	tup = (string, string, string)
	d = {"a": f}
	bl = b
	return list1, tup, d, bl
	
print(func(5, "aaa", 2.3, False))
```

其实，我觉得这么搞的话，比c语言的写法还麻烦。

