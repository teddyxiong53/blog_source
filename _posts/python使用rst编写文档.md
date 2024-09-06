---
title: python使用rst编写文档
date: 2023-01-09 14:47:32
tags:
	- Python

---

--

# 一篇好文

https://shaoer.cloud/detail/86.html

## docstring

docstring是python独有的注释方式。

是字符串的形式。

是文件、class、method里的第一行字符串。

这些字符串可以通过对象的`__doc__`来获取。

举例：

新建一个docdemo.py文件，内容如下：

```
'''
文件头部的注释
'''
class Test:
    '''class的注释'''
    def test():
        '''函数的注释'''
        pass
def func():
    '''function的注释'''
    pass
```

然后新建test.py，内容如下：

```
import docdemo
print(docdemo.Test.__doc__)
print(docdemo.Test.test.__doc__)
print(docdemo.func.__doc__)
```

执行test.py

```
python .\test.py
class的注释
函数的注释
function的注释
```

docstring的规范

* 首先是一行概述。
* 然后是一个空行。
* 然后是详细的说明部分。

### 函数

函数必须要有docstring，除非：

* 外部不可见。
* 非常短小。
* 简单明了。

在docstring里，应该分为机组：

* Args
* Returns，或者Yields
* Raises

## 在pycharm里设置自动doc

# docstring的几种风格

```
# Plain
def foo1(a, b):
    """

    """
    return a+b

# reStructuredText
def foo2(a, b):
    """
    :param a:
    :param b:
    :return:
    """
    return a+b

# Numpy
def foo3(a, b):
    """
    Parameters
    ----------
    a
    b

    Returns
    -------

    """
    return a+b

# Google
def foo4(a, b):
    """
    Args:
        a:
        b:

    Returns:

    """
    return a + b

# Epytext
def foo(a, b):
    """
    @param a:
    @param b:
    @return:
    """
    return a+b
```

# docstring的重要特征

https://peps.python.org/pep-0287/ 的对应章节



# rst风格的docstring

https://peps.python.org/pep-0287/

这个是对应的pep文档。

一旦 reStructuredText 成为 Python 标准，我们就可以将精力集中在工具上，而不是争论标准。 Python 需要一套标准的文档工具。

reStructuredText 中的section标题通过下划线（也可能是上划线）而不是缩进使用装饰。例如：

```
This is a Section Title
=======================

This is a Subsection Title
--------------------------

This paragraph is in the subsection.

This is Another Section Title
=============================

This paragraph is in the second section.
```



# restructureText Primer

https://docutils.sourceforge.io/docs/user/rst/quickstart.html

## 段落

空行分割的就是段落。

## text style

```
*xx* 斜体
**xx**  加粗
``xx``  2个反引号包起来的是保留内部的*等符号
\*  保留* 的原始含义

```

## List

List有3种类型：

* 编号，也就是order list
* 项目符号，也就是unorder list
* 定义

列表前面一定要有一个空行，它必须是一个独立的段落。

### order list

以字母、数字开始一行，后面可以跟`.`，`)`， `()`

```
1. xx
A. xx
a. xx
I. xx 
i. xx
(1) xx
1) xx
```

### unorder list

以`-`  `+`  `*`开始的。

```
* xx
	- yy
		+ zz
	- aa
```

### 定义

与其他两个不同，定义列表由术语和该术语的定义组成。定义列表的格式为：

```
what
  Definition lists associate a term with a definition.

*how*
  The term is a one-line phrase, and the definition is one or more
  paragraphs or body elements, indented relative to the term.
  Blank lines are not allowed between term and definition.
```

## preformatting

就是一段已经有格式的文本。希望保留它内部的格式。

需要使用双冒号来结束前面的段落：

```
An example::

    Whitespace, newlines, blank lines, and all kinds of markup
      (like *this* or \this) is preserved by literal blocks.
  Lookie here, I've dropped an indentation level
  (but not far enough)

no more example
```

## section

可以使用的分节的符号有：

一共14种。可以划分14个level的内容。

```````
-----
=====
~~~~~
``````
'''''''
"""""""
________
+++++++
*******
<<<<<<
>>>>>>
######
:::::::
^^^^^
```````

## 标题和副标题

```
================
 Document Title
================
----------
 Subtitle
----------

Section Title
=============
```

## 图片

要在文档中包含图像，请使用image[指令](https://docutils.sourceforge.io/docs/ref/rst/directives.html)。例如：

```
.. image:: images/biohazard.png
```

# rst文档

https://docutils.sourceforge.io/docs/user/rst/quickref.html#contents

# vscode进行实时编辑预览

https://ebf-contribute-guide.readthedocs.io/zh-cn/latest/install-sphinx-env/vscode.html

# retext编辑器

https://github.com/retext-project/retext

https://itmyhome.com/markdown/article/tools/retext.html



# 参考资料

1、

https://promisechen.github.io/doc_guide/howto.html

2、

https://www.cnblogs.com/zhaojiedi1992/p/zhaojiedi_python_013_rst_spinx.html

3、

https://learn-rst.readthedocs.io/zh_CN/latest/reST-%E5%85%A5%E9%97%A8.html