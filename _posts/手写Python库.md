---
title: 手写Python库
date: 2023-01-16 21:55:31
tags:
	- Python

---

有一些python库，难度不大，但是场景有很典型，代码写得也漂亮，对于这样的代码，我要自己手写一遍，甚至多遍，通过这种方式来提高自己的编码水平。

我现在对python的定位就是，thinking in python。对于一切新的概念，先找python实现，通过python的方式来理解和掌握对应的知识点。

# web框架microdot



这个非常小巧。就一个文件，大概1000行代码，只依赖socket，就实现了一个风格跟flask类似的Python web框架，并且可以在micropython跑起来，还支持了wsgi、asgi、asyncio等方式，所以知识点是非常全面。

值得反复阅读，直到完全掌握。

# 数据库tinydb

这个没有使用价值，但是可以帮助我理解nosql数据库。

类型系统使用非常完善，可以作为类型注解的研究材料。

还有很多人给它写插件，可以学习怎么做一个框架。

# 数据库pickledb

这个也是很小巧的一个库。

一个key-value的数据库。

也不知道有什么具体的应用场景。

https://github.com/patx/pickledb

总共代码不到300行。



# 前端pywebio

这个也是很不错的，代码里也不大，非常实用的项目。

# web框架flask

flask的代码量也不是很大，也可以尝试写一遍。

# 任务队列huey

作者coleifer很擅长写这些小巧的库。

代码质量很不错。

# 简单数据库simpledb

https://github.com/coleifer/simpledb

使用上类似