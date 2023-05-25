---
title: Python使用__main__.py作为文件名的用途
date: 2023-05-19 14:17:11
tags:
	- python
---

--

在 Python 中，`__main__.py` 文件实际上是在包（package）的情况下使用的特殊文件名。当一个包中包含名为 `__main__.py` 的文件时，在运行该包的时候，会执行 `__main__.py` 文件中的代码。

这个特性允许将一个包作为可执行脚本运行，而不仅仅是作为一个导入的模块。

例如，假设有一个名为 `my_package` 的包，其结构如下：

```
markdownCopy codemy_package/
    __init__.py
    module.py
    __main__.py
```

在 `__main__.py` 文件中，可以放置作为包的入口点的代码。当通过以下方式运行包时：

```
python -m my_package
```

Python 解释器会执行 `my_package` 包中的 `__main__.py` 文件中的代码。

请注意，这种用法仅适用于作为包运行的情况，并且只对包级别的 `__main__.py` 文件有效。对于普通的脚本文件，没有特别的含义。

对于单个的脚本文件，入口点通常是直接在文件中定义的顶级代码，而不是通过 `__main__.py` 文件。



