---
title: Python之collections
date: 2018-06-18 11:56:58
tags:
	- Python

---



Python里的容器类。

我们先看help可以看到信息。

```
DESCRIPTION
    This module implements specialized container datatypes providing
    alternatives to Python's general purpose built-in containers, dict,
    list, set, and tuple.
    
    * namedtuple   factory function for creating tuple subclasses with named fields
    * deque        list-like container with fast appends and pops on either end
    * Counter      dict subclass for counting hashable objects
    * OrderedDict  dict subclass that remembers the order entries were added
    * defaultdict  dict subclass that calls a factory function to supply missing values
```

collections模块，是用来提供对python内建容器tuple/list/dict/set的替代选择。

```
Counter
	dict的子类。提供了可哈希对象的计数功能。
	里面的内容是：以对象的hash值为key，以该对象的出现次数为value。
	具体可以运用在哪些场景呢？
	
```



我们一个个学习一下。

# namedtuple

有名元组。

为什么要引入这个类呢？

tuple，我们知道它的作用就是表示一个不变的集合。

一个坐标点，我们可以这样表示：

```
p = (1,2)
```

但是我们也难直接看出这个tuple是表示一个坐标的。

当然我们可以自己定义一个类来表示，但是这样太小题大做了。

所以就引入了namedtuple这个东西。

可以这样用：

```
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(1,2)
print(p.x, p.y)
```



# deque

双向队列。

这个是为了解决list插入删除元素很慢的问题。

```
#!/usr/bin/python3

from collections import deque

q = deque(['a', 'b', 'c'])
q.append('x')
q.appendleft('y')
print(q)
```

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
deque(['y', 'a', 'b', 'c', 'x'])
```



# Counter

Counter是一个简单的计数器。

例如可以用来统计字符出现的次数。

```
#!/usr/bin/python2

from collections import Counter
c = Counter()
for ch in 'programming':
	c[ch] = c[ch] + 1
print c
```

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
Counter({'g': 2, 'm': 2, 'r': 2, 'a': 1, 'i': 1, 'o': 1, 'n': 1, 'p': 1})
```



# OrderedDict

对于dict，key是无序的，所以在对dict进行迭代的时候，无法确定key的顺序。

如果我们要保证是有序的。

就要使用OrderedDict。

```
#!/usr/bin/python2

from collections import OrderedDict
d = dict([('a',1), ('b',2), ('c', 3)])
print d
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
print od
```

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
{'a': 1, 'c': 3, 'b': 2}
OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```



# defaultdict

defaultdict跟dict的不同在于：

dict在key不存在的时候，会抛出KeyError，

而defaultdict会返回一个默认值。

```
#!/usr/bin/python2

from collections import defaultdict
dd = defaultdict(lambda: 'N/A')
dd['key1'] = 'aaa'
print dd['key1']
print dd['key2']
```





# 参考资料

1、Python中collections的用法

https://blog.csdn.net/u013007900/article/details/55271530