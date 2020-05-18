---
title: python之blinker模块
date: 2019-10-14 11:15:32
tags:
	- Python

---

1

 blinker是一个信号库，支持一对一、一对多的订阅发布模式。



支持发送任意大小的数据。而且是线程安全的。

这个模块代码不多，就4个文件。

从base.py的注释里看，这个模块是从django里的提取出来的。

作用是解耦。

创建消息

```
from blinker import signal

initialized = signal('initialized')
print(initialized is signal('initialized'))
```

每次调用signal('name')都会返回同一个信号对象。

因此这里signal方法使用了单例模式。

订阅消息





参考资料

1、基于Python的信号库 Blinker

https://www.jianshu.com/p/829da3cd70b6

