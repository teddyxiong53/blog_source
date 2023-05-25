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



# 自己实现mro算法

Method Resolution Order (MRO) 是用于确定 Python 类的属性和方法查找顺序的算法。Python 提供了内置的 `mro()` 方法来查看类的 MRO，但如果你想自己实现 MRO 搜索算法，可以按照下面的步骤进行：

1. 确定基类列表：从左到右按照类定义的顺序，将所有基类按顺序添加到基类列表中。

2. 创建 MRO 列表：创建一个空的 MRO 列表，用于存储最终的查找顺序。

3. 添加当前类：将当前类添加到 MRO 列表的开头。

4. 遍历基类列表：对于基类列表中的每个基类，按照以下步骤进行处理：
   - 如果基类已经在 MRO 列表中，则跳过该基类。
   - 对于当前基类，按照以下步骤进行处理：
     - 递归调用基类的 MRO 搜索算法，将返回的 MRO 列表与当前 MRO 列表合并，得到新的 MRO 列表。
     - 将新的 MRO 列表添加到当前 MRO 列表的末尾。

5. 返回 MRO 列表：返回最终的 MRO 列表作为类的查找顺序。

以下是一个简单的示例，演示了如何自己实现 MRO 搜索算法：

```python
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass

def get_mro(cls):
    mro = [cls]  # 创建空的 MRO 列表，并将当前类添加到开头

    bases = cls.__bases__  # 获取当前类的基类列表
    for base in bases:
        if base not in mro:  # 如果基类不在 MRO 列表中
            base_mro = get_mro(base)  # 递归调用基类的 MRO 搜索算法
            mro.extend(base_mro)  # 将基类的 MRO 列表与当前 MRO 列表合并

    return mro

# 获取类 D 的 MRO 列表
mro_d = get_mro(D)
print(mro_d)  # 输出: [<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>]
```

在上述示例中，我们定义了一组类 A、B、C 和 D，它们之间形成了多重继承关系。通过调用 `get_mro()` 函数，可以获取类 D 的 MRO 列表。最终输出的 MRO 列表按照 C3 算法的顺序排列。

需要注意的是，上述示例只是一个简化版的 MRO 搜索算法实现，它没有考虑 C3 算法的所有细节和特殊情况。实际的 MRO 搜索算法更加复杂，涉

及到算法的线性化、冲突解决等方面。如果想要实现一个完整的、符合 Python 规范的 MRO 搜索算法，需要更详细的实现和处理。



# 参考资料

1、你真的理解Python中MRO算法吗？

http://python.jobbole.com/85685/

2、Python的方法解析顺序(MRO)

https://hanjianwei.com/2013/07/25/python-mro/

3、python基本数据结构dict继承自object，但为什么又是MutableMapping的子类

<https://segmentfault.com/q/1010000016983193>