---
title: Python之Python2和Python3的主要区别
date: 2018-06-11 23:03:25
tags:
	- Python

---



之前一直是用Python2，现在看HomeAssistant的代码。这个是用Python3写的。

所以需要先把Python3的主要不同点在心里有个数。



为了不带入过多的累赘，Python3在设计的时候就没有考虑向下兼容。

为了照顾现有的程序，Python2.6作为过渡版本，基本使用Python2的语法，但是可以在里面使用Python3的语法。

# print

print在Python2里面是一个语句。

在Python3里面变为了一个函数。

在Python2.7里。下面三种写法是等价的。

```
print "hello"
print ("hello") #print和(之间有一个空格。
print("hello") #不能带任何其他的参数。
```

但是也可以这样来使用完整的Python3的语法。

```
from __future__ import print_function
print("hello","world",sep=',')
```

# unicode

在Python2里面，要使用Unicode字符，还需要加上coding注释才能用。

而Python3里，默认就是用Unicode了。省去了编码相关的问题的麻烦。

我们可以这样来做：

```
中国='china'
print(中国)
```

可以用汉字来做变量名。

# 除法

Python里的除法是比较复杂的，也比较强大。

Python里的除法有两种：

/和//。//叫做地板除法（floor divide）

Python2里

```
1/2 会得到0
```

在Python3里。

```
1/2会得到0.5
```

# 异常

在Python3里，异常处理有一点小的改动。

加入了as作为关键词。

捕获异常的语法由：

```
except IOError, e
这种写法比较奇葩，类型和变量名之间用逗号分隔。
```

变成了

```
except IOError as e
```

从Python2.6就已经支持上面两种写法了。

# xrange



# 八进制的表示

以前的八进制是0777这样写的。

现在要改成0o777 。

类似的，二进制是0b101 。

# 不等于

在Python2里。不等于有两种表示法：

```
!=
<>
```

Python3里，只留下了`!=`。

# 多个模块被改名

改名的依据的PEP8规范。



# 数据类型

1、去掉了long类型，只留下了int。

2、新增了bytes类型。注意是bytes。复数。

在python2里，bytes类型跟str类型是等价的。

```
In [78]: bytes == str
Out[78]: True
```

在python3里面是不同的。

```
>>> bytes == str
False
```

Python 2 将 strings 处理为原生的 bytes 类型，而不是 unicode， 
Python 3 所有的 strings 均是 unicode 类型。



python3里自带了一个2to3.py的程序，用来进行转化。但是可能不能完全正确。



python3为什么要去掉long类型？

不用你去操心数据的长度了，自动会帮你扩展的。就这样。

看以lib2to3的代码。



# 内置函数的改变

py3去掉了cmp函数。比较会调用`__gt__`和`__lt__`函数。

reduce函数移到了functools模块里。



# 参考资料

1、Python 2 和 Python 3 有哪些主要区别？

https://www.zhihu.com/question/19698598

2、Python2.x与3.x版本区别

http://www.runoob.com/python/python-2x-3x.html

3、python2 与 python3的区别

这篇讲得最细致最好。值得反复看。

https://www.cnblogs.com/meng-wei-zhi/articles/8194849.html

4、Python2和Python3的区别，以及为什么选Python3的原因

https://blog.csdn.net/qq_39521554/article/details/80855086

