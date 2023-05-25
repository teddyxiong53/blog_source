---
title: python之subprocess和multiprocessing比较
date: 2019-10-19 15:11:25
tags:
	- python

---

--

# subprocess

subprocess模块允许你spawn新的进程。连接它们的0、1、2的fd。

获取它们的返回值。

这个模块的主要设计目的是用来取代：

```
os.system
os.spawn*
```

主要的接口有：

```
run
	这个是3.5新增的。
	举例：
	subprocess.run(['ls', './']) 
call
	subprocess.call(['ls', './']) 
check_call
	subprocess.check_call(['ls', './']) 
	这个的不同在于在命令出错的时候，会抛出异常。
	
```

```
import subprocess
child = subprocess.Popen(['ping', '-n', '4', 'www.baidu.com' ])
child.wait() # 等待子进程。
print("end of parent ")
```



subprocess对已的pep324。文档在2003年提出的。

在这个文档里，说明了设计这个模块的动机：

1、不合适的启动进程的函数，会导致风险。

2、让python更好地替换掉难用的shell脚本。

当前python有很多的函数用来做进程创建。让开发者难以选择。

subprocess相当于之前的其他模块，做了这些事情：

```
1、一个统一的模块。
2、跨进程的异常。父进程可以检测到子进程的异常。
3、提供了一个hook，可以在fork跟exec之间来执行。这个一般用来修改uid。
4、不会隐式调用/bin/sh
5、所有fd的重定向的组合都支持。
6、支持连接多个子进程。相当于管道。
7、统一的换行符支持。
```

设计

```
1、subprocess基于popen2这个函数。
```

# multiprocessing

multiprocessing设计的目的是进行多进程操作的。

目的是提高并发能力。

## 对外主要接口

`multiprocessing` 是 Python 中用于实现多进程编程的标准库。它提供了一组丰富的功能和接口，用于创建、管理和通信多个进程。以下是 `multiprocessing` 常用的对外接口：

1. `Process` 类：`multiprocessing.Process` 类是创建子进程的主要接口。可以通过继承该类，重写 `run()` 方法来定义子进程要执行的任务。使用 `start()` 方法启动子进程，并通过 `join()` 方法等待子进程结束。

2. `Pool` 类：`multiprocessing.Pool` 类用于创建进程池，可用于并行执行多个任务。通过创建 `Pool` 对象，可以使用其方法（如 `apply()`、`map()` 等）提交任务，进程池会自动分配任务给可用的进程进行执行。

3. `Queue` 类：`multiprocessing.Queue` 类提供了进程间通信的队列，用于在多个进程之间安全地传递数据。可以使用 `put()` 方法将数据放入队列，使用 `get()` 方法从队列中获取数据。

4. `Pipe` 类：`multiprocessing.Pipe` 类提供了进程间通信的管道，用于在两个进程之间传递数据。通过 `Pipe()` 函数创建管道对象，其中一个端口用于发送数据，另一个端口用于接收数据。

5. `Lock` 类：`multiprocessing.Lock` 类是一个进程锁，用于在多个进程之间实现互斥访问共享资源。可以使用 `acquire()` 方法获取锁，使用 `release()` 方法释放锁。

6. `Event` 类：`multiprocessing.Event` 类是一个进程间事件，用于在多个进程之间进行信号通知。可以使用 `set()` 方法设置事件为真，使用 `clear()` 方法将事件设置为假，使用 `wait()` 方法等待事件的触发。

7. `Semaphore` 类：`multiprocessing.Semaphore` 类是一个进程信号量，用于在多个进程之间控制并发访问资源的数量。可以使用 `acquire()` 方法获取信号量，使用 `release()` 方法释放信号量。

这些是 `multiprocessing` 中常用的对外接口，可以帮助你创建、管理和通信多个进程。通过这些接口，你可以充分利用多核处理器，并实现并行计算、并发任务等多进程编程的需求。

### Process

`multiprocessing.Process` 类是 `multiprocessing` 模块中用于创建子进程的主要接口。它允许你以面向对象的方式定义子进程要执行的任务，并提供了一些方法来管理和控制子进程的行为。

下面是 `multiprocessing.Process` 的常用用法：

1. 创建子进程对象：通过创建 `Process` 类的实例来创建子进程对象。构造函数接受以下参数：
   - `target`：指定子进程要执行的函数。
   - `args`：传递给目标函数的参数，以元组形式提供。
   - `kwargs`：传递给目标函数的关键字参数，以字典形式提供。

2. 定义子进程执行的任务：可以通过继承 `Process` 类，并重写 `run()` 方法来定义子进程要执行的任务。`run()` 方法中包含了子进程的具体逻辑。

3. 启动子进程：调用子进程对象的 `start()` 方法来启动子进程。子进程会执行其 `run()` 方法中定义的任务。

4. 等待子进程结束：可以使用 `join()` 方法来等待子进程执行完成。调用 `join()` 方法会阻塞当前进程，直到子进程执行完成或超时。

下面是一个简单的示例，演示了如何使用 `multiprocessing.Process` 创建和管理子进程：

```python
import multiprocessing
import time

def worker(name):
    print(f"Worker {name} started")
    time.sleep(2)
    print(f"Worker {name} finished")

if __name__ == "__main__":
    # 创建子进程对象，传递目标函数和参数
    p1 = multiprocessing.Process(target=worker, args=("A",))
    p2 = multiprocessing.Process(target=worker, args=("B",))

    # 启动子进程
    p1.start()
    p2.start()

    # 等待子进程结束
    p1.join()
    p2.join()

    print("All processes finished")
```

在上述示例中，我们定义了一个 `worker` 函数，它会在子进程中执行。然后我们创建了两个子进程对象 `p1` 和 `p2`，分别传递目标函数和参数。接着，我们调用 `start()` 方法启动子进程，它们会并行执行各自的任务。最后，我们使用 `join()` 方法等待子进程执行完成，并打印出 "All processes finished"。

通过使用 `multiprocessing.Process`，我们可以方便地创建和管理子进程，实现并行计算、并发任务等多进程编程的需求。



### multiprocessing.Pool

`multiprocessing.Pool` 是 `multiprocessing` 模块中的一个类，用于创建进程池。进程池可以用于并行执行多个任务，提高程序的性能和效率。

`multiprocessing.Pool` 的主要特点如下：

1. 创建进程池：通过创建 `Pool` 对象来创建进程池。可以指定要创建的进程数量，默认为 CPU 的核心数。

2. 提交任务：使用进程池的方法（如 `apply()`、`map()`、`imap()` 等）来提交任务给进程池进行执行。这些方法会自动将任务分配给空闲的进程。

3. 获取结果：使用进程池的方法（如 `apply()`、`map()` 等）来获取任务的执行结果。这些方法会阻塞当前进程，直到任务执行完成并返回结果。

4. 关闭进程池：使用 `close()` 方法关闭进程池，不再接受新的任务。

5. 等待任务完成：使用 `join()` 方法等待所有任务执行完成。

下面是一个简单的示例，演示了如何使用 `multiprocessing.Pool` 创建进程池并执行任务：

```python
import multiprocessing

def worker(x):
    return x ** 2

if __name__ == "__main__":
    # 创建进程池，进程数量为默认的 CPU 核心数
    pool = multiprocessing.Pool()

    # 提交任务给进程池，并获取结果
    result1 = pool.apply(worker, (5,))
    result2 = pool.apply(worker, (10,))
    result3 = pool.apply(worker, (15,))

    # 关闭进程池
    pool.close()

    # 等待任务完成
    pool.join()

    print(result1)  # 输出: 25
    print(result2)  # 输出: 100
    print(result3)  # 输出: 225
```

在上述示例中，我们创建了一个进程池对象 `pool`。然后通过调用 `apply()` 方法将任务提交给进程池执行，并使用 `result1`、`result2` 和 `result3` 分别获取任务的执行结果。最后，我们关闭进程池并调用 `join()` 方法等待任务完成。

通过使用 `multiprocessing.Pool`，我们可以方便地实现并行执行多个任务，利用多核处理器的能力，提高程序的性能和效率。同时，进程池的接口设计简单易用，使得并行编程变得更加简便。

### `multiprocessing.Queue`

`multiprocessing.Queue` 是 `multiprocessing` 模块中的一个类，

用于在多个进程之间安全地传递数据。

它提供了一个先进先出（FIFO）的队列，用于进程间的通信。



`multiprocessing.Queue` 的主要特点如下：

1. 创建队列：通过创建 `Queue` 对象来创建进程间通信的队列。

2. 放入数据：使用 `put()` 方法将数据放入队列。该方法会将数据放入队列的末尾，并阻塞当前进程，直到队列有空闲位置。

3. 获取数据：使用 `get()` 方法从队列中获取数据。该方法会从队列的开头获取数据，并阻塞当前进程，直到队列中有可用数据。

4. 队列大小：可以通过在创建 `Queue` 对象时指定 `maxsize` 参数来设置队列的最大大小。如果不指定，则队列的大小为无限制。

下面是一个简单的示例，演示了如何使用 `multiprocessing.Queue` 进行进程间通信：

```python
import multiprocessing

def producer(queue):
    for i in range(5):
        item = f"Item {i}"
        queue.put(item)
        print(f"Produced: {item}")

def consumer(queue):
    while True:
        item = queue.get()
        print(f"Consumed: {item}")

if __name__ == "__main__":
    # 创建队列对象
    queue = multiprocessing.Queue()

    # 创建生产者和消费者进程
    p1 = multiprocessing.Process(target=producer, args=(queue,))
    p2 = multiprocessing.Process(target=consumer, args=(queue,))

    # 启动进程
    p1.start()
    p2.start()

    # 等待进程结束
    p1.join()
    p2.terminate()
```

在上述示例中，我们创建了一个 `Queue` 对象 `queue`。

然后创建了生产者进程和消费者进程，分别通过 `producer()` 和 `consumer()` 函数来进行数据的放入和获取。

生产者进程将数据放入队列，消费者进程从队列中获取数据。

通过启动和等待进程的方式，实现了进程间的通信。

`multiprocessing.Queue` 提供了一种安全且方便的方式来在多个进程之间传递数据。

它可以在并发编程中广泛应用，例如任务分发、结果收集等场景，以实现进程间的协同工作。

### `multiprocessing.Pipe` 

`multiprocessing.Pipe` 是 `multiprocessing` 模块中的一个类，用于在两个进程之间创建一个双向（双工）的管道通信。

`multiprocessing.Pipe` 的特点如下：

1. 创建管道：通过调用 `Pipe()` 函数创建一个管道对象，返回两个 `Connection` 对象，分别用于父进程和子进程之间的通信。

2. 发送和接收数据：使用 `send()` 方法在一个连接上发送数据，使用 `recv()` 方法从一个连接上接收数据。这两个方法都是阻塞的，即发送和接收操作会阻塞当前进程，直到对应的连接上有可用的数据。

3. 关闭管道：通过调用 `close()` 方法关闭管道的连接。关闭连接后，对应的进程无法再发送或接收数据。

4. 进程间通信：`Pipe()` 创建的管道通信是双向的，即父进程和子进程都可以在管道上进行发送和接收操作，实现进程间的双向通信。

下面是一个简单的示例，演示了如何使用 `multiprocessing.Pipe` 进行进程间通信：

```python
import multiprocessing

def child_process(conn):
    # 从管道接收数据
    data = conn.recv()
    print(f"Received data in child process: {data}")

    # 向管道发送数据
    conn.send("Hello from child process!")

    # 关闭连接
    conn.close()

if __name__ == "__main__":
    # 创建管道
    parent_conn, child_conn = multiprocessing.Pipe()

    # 创建子进程
    p = multiprocessing.Process(target=child_process, args=(child_conn,))
    p.start()

    # 向管道发送数据
    parent_conn.send("Hello from parent process!")

    # 从管道接收数据
    data = parent_conn.recv()
    print(f"Received data in parent process: {data}")

    # 关闭连接
    parent_conn.close()

    # 等待子进程结束
    p.join()
```

在上述示例中，我们创建了一个管道对象，通过 `multiprocessing.Pipe()` 获得父进程和子进程之间的连接。然后创建子进程，将连接对象传递给子进程函数 `child_process()`。

在父进程中，我们使用 `parent_conn` 对象向管道发送数据，并使用 `recv()` 方法从管道接收数据。在子进程中，我们使用 `conn` 对象接收父进程发送的数据，并向管道发送回复。

通过使用 `multiprocessing.Pipe`，我们可以实现两个进程之间的双向通信，进行数据的发送和接收。这在并行计算、任务协作等场景中非常有用。

# 参考资料

1、python subprocess 和 multiprocess选择以及我遇到的坑

https://www.cnblogs.com/pengyusong/p/6113148.html

2、python subprocess模块使用总结

https://www.cnblogs.com/lincappu/p/8270709.html