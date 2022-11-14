---
title: python之类型注解
date: 2022-11-13 15:20:32
tags:
	- Python

---

--

typing是python3.5开始新增的用于类型注解的模块。

作用是为python提供静态类型检查。

typing这个模块内部常用的类型有：

* Any
* Union
* Tuple
* Callable
* TypeVar
* Optional
* Generic

typing模块虽然已经加入到标准库里，但是如果核心开发者认为有必要，api可能会发生变化，也就是不保证向后的兼容性。



# 给类型定义别名

```
from typing import List
Vector = List[float]
# 这个就把Vector定义为List[float]的别名，表示一个内部是float类型的数组。

```

一般是用来组合类型里。

```python
from typing import Dict, Tuple, Sequence

ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]

```

# 用NewType定义一个自定义类型

```python
from typing import NewType

UserId = NewType('UserId', int)
```



这些类型只会在静态检查时有用。

运行时没有用。

# TypeVar泛型

可以是任意类型

```
T = TypeVar('T')

def test(name: T) -> T:
	print(name)
	
test(11)
test('aa')
```

可以指定类型

```
T = TypeVar('T', int, str)
a:T = 1
a:T = 'aa'
a:T = [] # 这个就会报错。
```



# 参考资料

1、

https://blog.csdn.net/jeffery0207/article/details/93734942

2、

https://blog.csdn.net/xiao_yi_xiao/article/details/122302445