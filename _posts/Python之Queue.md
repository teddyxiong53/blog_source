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

支持多个生产者和多个消费者。



简单的例子：

```
import Queue
myqueue = Queue.Queue(maxsize=10)
myqueue.put('aa')
print myqueue.get()
print 'xxxxxxxxxx'
print myqueue.get(block=True,timeout=1)
```

```
import Queue
q = Queue.Queue()
for i in range(5):
    q.put(i)

while not q.empty():
    print q.get()
```

# collections.deque和queue.Queue比较

- **`deque`**: 适用于需要高效双端操作的场景，如实现栈或队列。它更灵活，但在多线程环境中需要手动管理线程安全。--------简单来说，就是属于底层的库。
- **`queue.Queue`**: 适合多线程应用，提供了线程安全的队列操作，使用简单，但功能相对较少，只支持 FIFO 操作。-----------上层适合使用这个，简单。

实际是queue.Queue的内部就是持有了一个deque。

```
    def _init(self, maxsize):
        self.queue = deque()
```



# 参考资料

1、python队列Queue

http://www.cnblogs.com/itogo/p/5635629.html