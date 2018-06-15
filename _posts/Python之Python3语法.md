---
title: Python之Python3语法
date: 2018-06-15 22:13:46
tags:
	- Python

---



#数据类型转换

转成int。

```
int(x,10) #10表示十进制
```

转成浮点数

```
float(x)
```

转成字符串

```
str(x)
```

转成表达式字符串

```
repr(x)
```

计算一个字符串

```
eval(str)
```

转成十六进制

```
hex(x)
```

转成八进制

```
oct(x)
```



删除一个变量

del x

# 字符串

格式化字符串

```
print("My name is %s, I'm % years old" % ('xhl', 27))
```



# 函数后面的->符号

在Python2里， 有docstrings这个东西，它允许你附加一个metadata字符串到各种类型的对象上去。

这个比较随意。

Python3对这个进行了规范化。

用来描述参数和返回值。

这个东西被称为函数注解。

一个例子。

```
def func(x) -> int:
	return x
```

用来说明函数返回值类型，这个是最常见的用法。



# 参考资料

1、PEP 3107 -- Function Annotations

https://www.python.org/dev/peps/pep-3107/

2、What does -> mean in Python function definitions?

https://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions