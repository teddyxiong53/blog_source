---
title: Python之import函数
date: 2017-09-25 22:58:20
tags:
	- Python

---



`__import__`函数用于动态加载类和函数。

假如有个一个a.py的文件，你可以在b.py文件里，这样来进行加载。

```
__import__('a')
```

基本等价于

```
import a
```



