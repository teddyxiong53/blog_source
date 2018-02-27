---
title: Python之Queue
date: 2018-02-26 22:23:54
tags:
	- Python

---



Python的queue有3种：

1、fifo的。就是默认的。

2、lifo的。Queue.LifoQueue。类似栈的行为。

3、优先级的。Queue.PriorityQueue。



简单的例子：

```
import Queue
myqueue = Queue.Queue(maxsize=10)
myqueue.put('aa')
print myqueue.get()
print 'xxxxxxxxxx'
print myqueue.get(block=True,timeout=1)
```

