---
title: 《python黑魔法指南v2.0》读书笔记
date: 2020-11-18 16:27:30
tags:
	- python
---



# 1 魔法冷知识

## 1.1 省略号

...是Ellipsis。类型是ellipsis。

python3里才能用... 。在python2里，只能用Ellipsis这个单词。

bool(...)得到的是True。

...是单例的。id(...)得到的总是一个值。

具体有什么作用呢？

可以代替pass。

## 1.2 使用end来结束代码块

这个是一个小技巧。对于哪些习惯end的人有点用。

```
__builtins__.end = None

def func():
    if True:
        print("xx")
    else:
        print("yy")
    end
end
func()
```

pycharm会有语法错误提示，但是可以正常运行。

## 1.3 用zip包的方式直接运行python包

这样来制作。

```
python -m zipfile -c demo.zip demo/*
```

然后直接运行：

```
python demo.zip
```



## 1.6 简洁而优雅的链式比较

这个就是链式比较

```
if 80 < score <= 90:
    print("成绩良好")
```

## 1.8 连接多个链表最极客的方式

```
a = [1,2]
b = [3,4]
c = [5,6]

res = sum((a,b,c),[])
print(res)
```

## 1.9 字典居然是可以排序的？

在python3.6之前，字典确实不可以排序。

```
mydict = {str(i):i for i in range(5)}
print(mydict)
```

得到

```
{'0': 0, '1': 1, '2': 2, '3': 3, '4': 4}
```

## 1.11 用户无感知的小整数池

为避免整数频繁申请和销毁内存空间，Python 定义了一个小整数池 [-5, 256] 这些整数对象是提前建立好的，不会被垃圾回收。

```
a = -6
b = -6
a is b
Out[16]: False
a = 256
b = 256
a is b
Out[19]: True
```

## 1.12 神奇的intern机制

字符串类型作为Python中最常用的数据类型之一，Python解释器为了提高字符串使用的效率和使用性能，做了很多优化.

例如：Python解释器中使用了 **intern（字符串驻留）**的技术来提高字符串效率，

什么是intern机制？

就是同样的字符串对象仅仅会保存一份，放在一个字符串储蓄池中，是共用的，

当然，肯定不能改变，这也决定了字符串必须是不可变对象。

```
>>> s1="hello"
>>> s2="hello"
>>> s1 is s2
True

# 如果有空格，默认不启用intern机制
>>> s1="hell o"
>>> s2="hell o"
>>> s1 is s2
False

# 如果一个字符串长度超过20个字符，不启动intern机制
>>> s1 = "a" * 20
>>> s2 = "a" * 20
>>> s1 is s2
True
```



## 1.16 dict()和{}生成空字典有什么区别

在初始化一个空字典时，有的人会写 dict()，而有的人会写成 {}

很多人会想当然的认为二者是等同的，但实际情况却不是这样的。

在运行效率上，{} 会比 dict() 快三倍左右。

使用 timeit 模块，可以轻松测出这个结果

可以发现使用 dict()，会多了个调用函数的过程，而这个过程会有进出栈的操作，相对更加耗时。



## 1.19 return不一定是函数的终点

```
def func():
    try:
        return "111"
    finally:
        return "222"

print(func())
```

这个得到是222

## 1.20 字符串里的缝隙是什么？

不是应该返回 0 吗？怎么会返回 5？

实际上，在 Python 看来，两个字符之间都是一个空字符，通俗的说就是缝隙。

因此 对于 `aabb` 这个字符串在 Python 来看应该是这样的

![image1](../images/random_name/20200509172331.png)

# 2 魔法命令行

## 2.6 快速搭建http服务

```
python -m SimpleHTTPServer 8888
```

## 2.7 快速搭建html文档查看

```
python -m pydoc -p 8080
```

这样就可以在web界面查看本地模块的文档了。



参考资料

http://magic.iswbm.com/zh/latest/c01/c01_01.html

