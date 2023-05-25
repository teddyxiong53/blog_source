---
title: python之threading之event
date: 2017-07-22 23:38:45
tags:

	- python

	- threading

---

--

# event分析

Python线程的event主要用于main线程控制其他线程的执行，

event主要提供了3个方法：wait、set、clear。

实现线程间通信。

简单描述，机制是这样的：

有一个全局的flag，如果flag是true，那么wait会阻塞，如果flag是false，则wait不会导致阻塞。

set是用来把flag设置为true。clear则是把flag设置为false的。

test.py

```
#!/usr/bin/python

import threading
import time

class MyThread(threading.Thread):
	def __init__(self, signal):
		threading.Thread.__init__(self)
		self.signal = signal
	def run(self):
		print "I am %s, now I will sleep..." %self.name
		self.signal.wait()
		print "I am %s, now I am running ..."%self.name
		
if __name__ == '__main__':
	signal = threading.Event()
	for i in range(0,3):
		thread = MyThread(signal)
		thread.start()
		
	print "main thread sleep 3 seconds "
	time.sleep(3)
	signal.set()
	
```

运行效果如下：

```
I am Thread-1, now I will sleep...
I am Thread-2, now I will sleep...
I am Thread-3, now I will sleep...
main thread sleep 3 seconds 
I am Thread-1, now I am running ...
 I am Thread-3, now I am running ...
I am Thread-2, now I am running ...
teddy@teddy-ubuntu:~/work/test/py-test/
```



Event其实就是一个简化版的 Condition。Event没有锁，无法使线程进入同步阻塞状态。

# threading.py对外接口

`threading.py` 是 Python 标准库中用于多线程编程的模块。

它提供了创建和管理线程的类和函数，以及同步机制和线程间通信的工具。

下面是 `threading.py` 模块的一些常用对外接口：

1. `Thread` 类：`Thread` 类是 `threading` 模块中最重要的类之一，用于创建和管理线程。可以通过创建 `Thread` 类的实例来定义一个新的线程，并指定线程要执行的目标函数。

2. `Thread` 类的方法：
   - `start()`: 启动线程，使其开始执行。
   - `join([timeout])`: 等待线程终止。如果提供了 `timeout` 参数，则最多等待 `timeout` 秒。
   - `run()`: 线程执行的目标函数。
   - `name`: 线程的名称。
   - `is_alive()`: 检查线程是否正在运行。
   - `ident`: 线程的唯一标识符。

3. `Lock` 类：`Lock` 类提供了简单的互斥锁对象，用于在多个线程之间实现资源的互斥访问。

4. `Event` 类：`Event` 类提供了一个简单的线程同步工具，用于线程之间的事件通知和等待。

5. `Condition` 类：`Condition` 类提供了一个条件变量，用于在多线程之间实现复杂的同步和通信。

6. `Semaphore` 类：`Semaphore` 类提供了一个计数信号量，用于控制对资源的并发访问。

7. `ThreadLocal` 类：`ThreadLocal` 类提供了线程本地数据的机制，每个线程都可以独立地访问自己的数据。

8. `current_thread()` 函数：返回当前线程的 `Thread` 对象。

9. `active_count()` 函数：返回当前活动线程的数量。

10. `enumerate()` 函数：返回当前所有活动线程的列表。

11. `Lock`、`RLock`、`Condition`、`Semaphore` 等类和函数提供了更高级的同步和互斥机制，用于控制多线程环境下的资源访问。

这些是 `threading.py` 模块中一些常用的对外接口，用于创建和管理线程，实现线程间的同步和通信。通过使用这些接口，可以编写并发和多线程的程序，处理多个任务并实现线程间的协调和交互。

# threading.Condition

`threading.Condition` 是 Python 中用于线程间协调和通信的高级同步工具之一。

它基于底层的锁（`Lock`）和条件变量（`Condition`）机制，

提供了更复杂的同步操作。

`threading.Condition` 的主要作用是允许线程在满足特定条件时等待，

直到其他线程满足条件后进行通知。

它通常与一个共享资源相关联，

用于在多个线程之间进行通信和协调，以确保线程在适当的时机进行操作。

以下是 `threading.Condition` 的一般用法：

1. 创建 `Condition` 对象：使用 `threading.Condition()` 构造函数创建一个 `Condition` 对象。

2. 获取锁：在使用 `Condition` 对象之前，需要先获取与之关联的锁。可以使用 `with` 语句获取锁，或者手动调用 `acquire()` 和 `release()` 方法。

3. 等待条件：使用 `wait()` 方法在等待条件时释放锁，并进入等待状态。线程将一直等待，直到其他线程调用相同的 `Condition` 对象的 `notify()` 或 `notify_all()` 方法来通知条件满足。

4. 通知条件：通过调用 `notify()` 方法或 `notify_all()` 方法来通知等待中的线程条件已满足。被通知的线程将从等待状态返回，并重新获取锁。

下面是一个简单的示例，演示了如何使用 `Condition` 实现线程间的协调和通信：

```python
import threading,time

def producer(condition):
    with condition:
        print("Producer thread started")
        # 执行一些生产操作
        time.sleep(1)
        print("Producer thread notifying consumers")
        condition.notify_all()

def consumer(condition, i):
    with condition:
        print(f"Consumer {i} thread waiting")
        condition.wait()
        print(f"Consumer {i} thread resumed")

def main():
    condition = threading.Condition()

    producer_thread = threading.Thread(target=producer, args=(condition,))
    consumer_thread1 = threading.Thread(target=consumer, args=(condition,1,))
    consumer_thread2 = threading.Thread(target=consumer, args=(condition,2,))

    consumer_thread1.start()
    consumer_thread2.start()

    producer_thread.start()

    producer_thread.join()
    consumer_thread1.join()
    consumer_thread2.join()
if __name__ == "__main__":
    main()

```

在上述示例中，我们创建了一个 `Condition` 对象，并将它作为参数传递给生产者和消费者线程函数。在生产者线程中，我们获取了 `Condition` 对象的锁，并执行一些生产操作后调用 `notify_all()` 方法通知消费者线程条件已满足。在消费者线程中，我们先获取了锁，并调用 `wait()` 方法进入等待状态，直到收到来自生产者线程的通知。

通过使用 `Condition`，生产者线程和消费者线程可以进行同步和通信，确保在适当的时机进行操作。`Condition` 提供了一个更高级的机制，允许线程在满足特定条件时等待，并在条件满足后进行通知。

# `threading.Barrier` 

`threading.Barrier` 是 Python 中的一个同步原语，用于线程间的同步和协调。`Barrier` 可以使多个线程在某个点上进行同步，只有当所有线程都达到该点时，它们才能继续执行。

`Barrier` 的主要特点如下：

- 在创建 `Barrier` 对象时，需要指定参与同步的线程数量。
- 当线程达到 `Barrier` 点时，调用 `wait()` 方法会阻塞当前线程，直到所有线程都达到该点。
- 一旦所有线程都达到 `Barrier` 点，它们将同时被释放，继续执行后续代码。
- 在所有线程被释放后，`Barrier` 会被重置，可以再次使用。
- 可以通过 `parties` 属性获取参与同步的线程数量。

下面是一个简单的示例，演示了如何使用 `Barrier` 实现线程间的同步：

```python
import threading

def worker(barrier):
    print("Worker thread started")
    barrier.wait()
    print("Worker thread released from barrier")

def main():
    barrier = threading.Barrier(3)  # 创建一个 Barrier，参与同步的线程数量为 3

    threads = []
    for _ in range(3):
        t = threading.Thread(target=worker, args=(barrier,))
        threads.append(t)
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
```

在上述示例中，我们创建了一个 `Barrier` 对象，并指定参与同步的线程数量为 3。然后创建了 3 个线程，每个线程执行 `worker` 函数。在 `worker` 函数中，线程首先输出一条消息表示线程已启动，然后调用 `wait()` 方法进行同步，直到所有线程都到达 `Barrier` 点。一旦所有线程都到达该点，它们将同时被释放，并继续执行后续代码。

通过使用 `Barrier`，我们可以使多个线程在某个点上同步，确保它们在同一时间点上继续执行。这对于协调并行任务的执行非常有用，尤其是需要等待所有任务完成后再进行下一步操作的场景。

# 参考资料

1、

https://blog.csdn.net/brucewong0516/article/details/84588804