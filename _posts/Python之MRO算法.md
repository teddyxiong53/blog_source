---
title: Python之MRO算法
date: 2018-06-26 22:25:37
tags:
	- Python

---



看python的标准库，看到了mro这个东西。

```
    def __subclasshook__(cls, C):
        if cls is Hashable:
            try:
                for B in C.__mro__: #就是这里。
```

mro是什么？

是Method Resolution Order。



对于支持继承的编程语言来说，一个类的方法，可能定义在自己里面，也可以在父类里面。

所以在调用的时候，就要进行搜索，看具体是调用哪里的方法。

对于单继承的语言，mro比较简单，但是python是多继承的，所以mro就复杂一些。

```
class MyDict(dict):
	pass

print MyDict.__mro__
```

输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python test.py 
(<class '__main__.MyDict'>, <type 'dict'>, <type 'object'>)
```

这就是继承关系。







# 参考资料

1、你真的理解Python中MRO算法吗？

http://python.jobbole.com/85685/

2、Python的方法解析顺序(MRO)

https://hanjianwei.com/2013/07/25/python-mro/

3、python基本数据结构dict继承自object，但为什么又是MutableMapping的子类

<https://segmentfault.com/q/1010000016983193>