---
title: Flask之Local分析
date: 2018-11-24 16:27:51
tags:
	- Flask
---



在使用Flask或者werkzeug的时候，经常碰到这3个东西：

1、Local。

2、LocalStack。

3、LocalProxy。

什么是Local？

为什么需要Local？

Python提供了thread local对象用来存储thread safe的数据。在多线程环境下，用线程id来区分不同的线程。

thread local对象在有些情况下，还是不能保证安全，而且在python web开发中，很多使用了协程。

**所以flask开发了自己的Local。优先使用greenlet的线程，如果没有，则使用线程id。**

是这么个处理逻辑。

```
try:
    from greenlet import getcurrent as get_ident
except ImportError:
    try:
        from thread import get_ident
    except ImportError:
        from _thread import get_ident
```



看一个简单的例子。

```
import threading

import time
from werkzeug.local import LocalStack

my_stack = LocalStack()
my_stack.push(1)
print("in main thread, after push, value is {}".format(my_stack.top))

def worker():
    print("in new thread, before push, value is {}".format(my_stack.top))
    my_stack.push(2)
    print("in new thread, after push, value is {}".format(my_stack.top))

t = threading.Thread(target=worker)
t.start()
time.sleep(1)
```

输出结果：

```
in main thread, after push, value is 1
in new thread, before push, value is None
in new thread, after push, value is 2
```



看一下LocalStack的代码实现。

LocalStack的本质是stack，特点是Local。



这里就牵涉到一个话题：flask的多线程处理。

flask是一个web app，它必须放到一个web server里才能运行。

flask是不会进行开启线程的操作的，这个操作是靠web server来做的。

flask的app.run，就是使用了flask内置的web server，正式使用的时候，不能用这个。

默认情况下，flask自带的webserver是用单进程单线程的模式来运行的。

但是你可以通过参数来修改运行模式。

```
app.run(host='0.0.0.0', debug=True, threaded=True, processes=2)#这个就是指定多进程多线程模式了。
```

用线程id来唯一标识一个线程。



参考资料

1、Werkzeug(Flask)之Local、LocalStack和LocalProxy

https://www.jianshu.com/p/3f38b777a621

2、flask高级编程-LocalStack线程隔离

https://www.cnblogs.com/wangmingtao/p/9372611.html

3、Python flask中的多线程深入剖析

https://www.jianshu.com/p/8efdc122233e

4、werkzeug（flask）中的local，localstack，localproxy探究

http://www.mamicode.com/info-detail-2218251.html