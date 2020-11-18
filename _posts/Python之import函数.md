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



在 Python 中使用 import 关键字来实现这个操作，但不是唯一的方法，还有 `importlib.import_module()` 和 `__import__()` 等。



导入单元有多种，可以是模块、包及变量等。

对于这些基础的概念，对于新手还是有必要介绍一下它们的区别。

**模块**：类似 *.py，*.pyc， *.pyd ，*.so，*.dll 这样的文件，是 Python 代码载体的最小单元。

**包** 还可以细分为两种:

- Regular packages：是一个带有 `__init__.py` 文件的文件夹，此文件夹下可包含其他子包，或者模块
- Namespace packages



Namespace packages 是由多个 部分 构成的，每个部分为父包增加一个子包。 

各个部分可能处于文件系统的不同位置。

 部分也可能处于 zip 文件中、网络上，或者 Python 在导入期间可以搜索的其他地方。 

命名空间包并不一定会直接对应到文件系统中的对象；**它们有可能是无实体表示的虚拟模块。**



参考资料

1、深入探讨 Python 的 import 机制：实现远程导入模块

https://iswbm.com/84.html