---
title: python之blinker模块
date: 2019-10-14 11:15:32
tags:
	- Python

---

1

Blinker 是一个基于Python的**强大的信号库**，

它既支持简单的对象到对象通信，也支持针对多个对象进行组播。

Flask的信号机制就是基于它建立的。

Blinker的内核虽然小巧，但是功能却非常强大，它支持以下特性：

- 支持注册全局命名信号
- 支持匿名信号
- 支持自定义命名信号
- 支持与接收者之间的持久连接与短暂连接
- **通过弱引用实现与接收者之间的自动断开连接**
- 支持发送任意大小的数据
- **支持收集信号接收者的返回值**
- 线程安全



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



```
import blinker
from blinker import signal


def subscriber(sender):
    print('get a signal from {}'.format(sender))
# 创建一个有名信号
ready = signal('ready')
# 给这个信号注册处理函数
ready.connect(subscriber)

x = 'xx'
# 发送信号
ready.send(x)
```

打印如下：

```
get a signal from xx

```



一般在什么场景下进行使用呢？

Flask 集成 blinker 作为解耦应用的解决方案。在 Flask 中，信号的使用场景如：请求到来之前，请求结束之后。同时 Flask 也支持自定义信号。



信号的优点：

1. 解耦应用：将串行运行的耦合应用分解为多级执行
2. 发布订阅者：减少调用者的使用，一次调用通知多个订阅者

信号的缺点：

1. 不支持异步
2. 支持订阅主题的能力有限



# 参考资料

1、基于Python的信号库 Blinker

https://www.jianshu.com/p/829da3cd70b6

2、

https://zhuanlan.zhihu.com/p/435076618