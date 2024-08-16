---
title: 脚本解释器之tinypy
date: 2024-08-13 11:34:33
tags:
	- python

---

--

http://www.tinypy.org/

https://github.com/philhassey/tinypy

文档在这里：（有点奇葩，文档是放在另外一个branch里）

https://github.com/philhassey/tinypy/blob/wiki/Index.md

这个是作者的博客。

https://www.philhassey.com/blog/category/tinypy/

有下面这些特征：

- 用 Tinypy 编写的解析器和字节码编译器
- 完全自举
- 用 C 语言编写的带有垃圾回收的 luaesque 虚拟机
- 一个相当不错的 Python 子集
  - 类和单继承
  - 具有变量或关键字参数的函数
  - 字符串、列表、字典、数字
  - 模块，列表推导式
  - 具有完整回溯功能的异常
  - 一些内置函数

因为原项目已经很多年不更新了。

这个issue里提到了另外一个人的fork。

https://github.com/philhassey/tinypy/issues/61

这个fork看起来还比较新一些。

https://github.com/rainwoodman/tinypy

下载这个看看。

这个作者是个华人，YuFeng。看起来是在Berkeley的一个宇宙学的教授。

https://rainwoodman.github.io/website/

rainwoodman的版本做了非常大的改动，完善了很多。

整个代码结构也更加合理了。

值得深入分析学习。

