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

# 相关的PEP

## 484

为了提供标准定义和工具，

本PEP引入了一个临时模块。

并且列出了一些不适用注解的情形的约定。

本PEP受到mypy的启发。

PEP 484 定义了类型注解的语法规则和约定，它并不要求在运行时进行类型检查，而是提供了一种静态类型检查的基础。通过类型注解，开发者可以在代码中明确指定变量和函数的期望类型，使得代码更加清晰和易于理解。

以下是 PEP 484 的一些主要内容：

1. 函数注解：使用 `->` 符号来标注函数的返回值类型，例如 `def func() -> int:`
2. 变量注解：使用冒号 `:` 后跟类型来标注变量的类型，例如 `x: int = 10`
3. 类型标注：使用 `typing` 模块中的类型来标注复杂类型，例如 `List[str]` 表示字符串列表
4. 类型别名：使用 `typing` 模块中的 `TypeVar` 来定义类型别名，例如 `MyType = Union[int, str]`
5. 可选类型注解：使用 `Optional` 表示可选类型，例如 `Optional[int]` 表示整数或者 `None`
6. 泛型类型：使用 `typing` 模块中的泛型类型来标注容器类型，例如 `List[int]` 表示整数列表

PEP 484 为 Python 提供了一种在代码中添加类型信息的方式，使得开发者可以更好地理解和维护代码。此外，它也为静态类型检查工具提供了基础，例如 `mypy` 等工具可以对代码进行类型检查，发现潜在的类型错误和逻辑问题。

https://peps.python.org/pep-0484/

https://www.cnblogs.com/popapa/p/PEP484.html

# 参考资料

1、

https://blog.csdn.net/jeffery0207/article/details/93734942

2、

https://blog.csdn.net/xiao_yi_xiao/article/details/122302445