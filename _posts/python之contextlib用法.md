---
title: python之contextlib用法
date: 2023-05-18 17:36:11
tags:
	- python
---

--

# closing

在pywebio里看到用到这个。

用chatgpt查询得到的答案是这样：

```
from contextlib import closing

# Define a resource class with a close() method
class MyResource:
    def __init__(self):
        print("Initializing resource")

    def close(self):
        print("Closing resource")

# Use the resource within a context manager
with closing(MyResource()) as resource:
    # Perform some operations with the resource
    print("Using resource")
    raise Exception('xx')

# After the with block, the resource will be closed automatically
```

使用`contextlib.closing`的好处是它简化了代码，通过自动处理资源的关闭，确保资源得到正确清理，即使发生异常也不会被遗漏。

上面的关键代码是定义一个close函数。

这个即使有异常也可以准确处理释放。

这样运行的打印是：

```
Initializing resource
Using resource
Closing resource
Traceback (most recent call last):
  File "test.py", line 15, in <module>
    raise Exception('xx')
Exception: xx
```

那么close函数跟`__exit__`函数关系是什么？

总而言之，

`close()`方法用于显式关闭资源，

而`__exit__()`方法是上下文管理器协议的一部分，

定义了上下文管理器在退出时的行为，

包括资源的关闭和异常处理。

具体如何使用和实现这两个方法取决于上下文管理器的具体实现和需求。



通常情况下，`__exit__()`方法会在`close()`方法内部被调用，以确保资源的关闭和清理。

但是，`close()`方法可以根据需要实现自定义的关闭逻辑，

而`__exit__()`方法是用于实现上下文管理器协议的标准方法。



在pywebio里的用法是：

```
def get_free_port():
    """
    pick a free port number
    :return int: port number
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
```

