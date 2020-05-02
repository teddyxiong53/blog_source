---
title: Python之asyncio
date: 2018-06-16 22:46:49
tags:
	- Python

---



网络模型有很多种，为了实现高并发，也有很多种方案，多进程、多线程这些。

无论是多线程还是多进程。io的调度更多地取决于os。

**而协程的方式，调度来自于用户，用户可以在函数中yield一个状态。**

使用协程可以实现高效的并发任务。

Python从3.4版本开始引入协程的概念。这时的协程还是以生成器为基础的。

在3.5版本里，协程开始加入到Python的原生语法里。



asyncio就是一个官方的协程的库。

asyncio的编程模型就是一个EventLoop。把需要运行的协程扔到loop里，就实现了异步io。



这里列出了支持asyncio的库。

https://github.com/aio-libs



重要概念

```
event_loop
	事件循环。
coroutine：
	协程。从代码上看，是指用async修饰的函数。
	调用这样的函数，不会马上执行，而是返回一个协程对象。
	需要把这个协程对象注册到event_loop才能执行。
task：
	任务。任务是对协程的进一步封装了。增加了状态管理。
	task是future的子类。
	加入到时间循环之前，状态是pending。完成后，状态是
future：
	表示将要执行的任务的结果。跟task没有本质的区别。

```



async是之前的装饰器的语法糖。

await是之前的yield from的语法糖。

await的作用是挂起当前这个协程。先去执行其他的协程。这个调度是由loop完成的。



# 定义一个协程

```
#!/usr/bin/python3
import time,asyncio

now = lambda : time.time()

async def do_some_work(x):
	print("waiting: ", x)
	
start = now()

coroutine = do_some_work(2)

loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)

print('TIME: ', now() - start)
```

运行结果：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
waiting:  2
TIME:  0.0005123615264892578

```



分析一下上面的程序。

1、通过关键字async来定义一个协程。

协程也是一个对象。协程不能直接运行，必须要把协程加入到时间循环。



# 创建一个task

协程对象不能 直接运行，需要借助于task对象。

task是Future类的子类。保存了协程运行后的状态，用于在未来获取协程的结果。

```
#!/usr/bin/python3
import time,asyncio

now = lambda : time.time()

async def do_some_work(x):
	print("waiting: ", x)
	
start = now()

coroutine = do_some_work(2)

loop = asyncio.get_event_loop()
task = loop.create_task(coroutine)
print(task)
loop.run_until_complete(task)
print(task)
print('TIME: ', now() - start)
```

运行结果：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
<Task pending coro=<do_some_work() running at ./test.py:6>>
waiting:  2
<Task finished coro=<do_some_work() done, defined at ./test.py:6> result=None>
TIME:  0.00044083595275878906
```



我看到这里，觉得都是晕的。所以我要先理清楚Python的异步编程的相关概念。



Tornado、Twisted、Gevent这些都是异步编程框架。

**Flask、Django都是传统的同步编程框架。**

从2013年开始，Python之父Guido亲自上阵，主持了Tulip（也就是后面的asyncio）的开发。也打磨了4年，才能被纳入到Python3.6里面。所以这一块是很复杂的。

什么是异步编程？

异步意味着无序。

从同步演化到异步，中间走过了漫长的探索过程。

# 异步io进化之路

下面我们以一个爬虫为例，从网上下载10个网页这种场景。

我们描述的时间尺度，用CPU一条指令时间对应1s这样来描述。这样大家就能够对效率有更加直观的印象。

最原始的解决方法，就是依次下载。

```
import socket

def blocking_way():
	sock = socket.socket()
	sock.connect(('www.xxx.com', 80))
	request = 'GET / HTTP/1.0\r\nHost: www.xxx.com\r\n\r\n'
	sock.send(request.encode('ascii'))
	response = b''
	chunk = sock.recv(4096)
	while chunk:
		response += chunk
		chunk = sock.recv(4096)
	return response
	
def sync_way():
	res = []
	for i in range(10):
		res.append(blocking_way())
	return len(res)
```

这样下载，耗时4.5秒左右。

上面的代码有2个关键点，第一个是sock.connect这里。

第二个是sock.recv。

这2个函数默认是阻塞的。

假如网络环境很差，connect需要1秒钟，对于CPU来说，这一秒钟，就相当于过去了83年。

同步的方式，效率是非常低下的。

我们看看，可以怎么改进？

第一个想法是多进程。

```
from concurrent import futures
def process_way():
	workers = 10
	with futures.ProcessPoolExecutor(workers) as executor:
		futs = {executor.submit(blocking_way) for i in range(10) }
	return len([fut.result() for fut in futs])
```

总体时间优化到0.6秒。

为什么总体耗时没有优化到之前的十分之一呢？而是九分之一呢？

因为切换进程需要花时间。

当进程数多于CPU核心数的时候，进程切换就是不可避免的。

除了切换开销，多进程还有另外的缺点，进程数多了，系统运行的稳定性就没那么好了。



后面为了减小多进程的开销，发明了线程的概念。

```
def thread_way():
	workers = 10
	with futures.ThreadPoolExecutor(workers) as executor:
		futs = {executor.submit(blocking_way) for i in range(10) }
	return len([fut.result() for fut in futs])
```

总体耗时为0.43秒。比多进程要好一些。

看起来，多线程似乎可以解决问题了。

但是，多线程也有问题，特别是Python的多线程。

1、Python的多线程因为GIL的存在，它并不能利用CPU多核的优势。一个进程里，只运行一个线程处于运行状态。

2、os的调度策略是抢占式的。所以可能会有竞争问题。所以需要用锁进行同步。我们上面的代码没有进行这种保护。

下面我们开始看非阻塞方式的。

先看最原始的非阻塞方式怎么写。

```
import socket

def nonblocking_way():
	sock = socket.socket()
	sock.setblocking(False)
	try:
		sock.connect(('www.xxx.com', 80))
	except BlockingIOError:
		pass
	request = 'GET / HTTP/1.0\r\nHost www.xxx.com\r\n\r\n'
	data = request.encode('ascii')
	while True:
		try:
			sock.send(data)
			break
		except OSError:
			pass
	response = b''
	while True:
		try:
			chunk = sock.recv(4096)
			while chunk:
				response += chunk
				chunk = sock.recv(4096)
			break
		except OSError:
			pass
	return response
	
def sync_way():
	res = []
	for i in range(10):
		res.append(nonblocking_way())
	return len(res)
```

这个耗时是4.3秒，看起来跟阻塞方式耗时差不多。

既然如此，要非阻塞方式有什么用？

我们继续改进非阻塞方式。

**判断非阻塞调用是否就绪，如果OS可以判断这一点，那么就不需要应用自己去等待和判断了。**

所以os就提供了select这个东西。

后来，select因为它的算法效率比较低，所以推出了poll，再推出了epoll。

所以现在主要是讨论epoll。

现在看看用epoll改进的程序。

```
import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3'}

class Crawler:
	def __init__(self, url):
		self.url = url
		self.sock = None
		self.response = b''
		
	def fetch(self):
		self.sock = socket.socket()
		self.sock.setblocking(False)
		try:
			self.sock.connect(('www.xxx.com', 80))
		except BlockingIOError:
			pass
		selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)
		
	def connected(self, key, mask):
		selector.unregister(key.fd)
		get = 'GET {0} HTTP/1.0\r\nHost: www.xxx.com\r\n\r\n'.format(self.url)
		self.sock.send(get.encode('ascii'))
		selector.register(key.fd, EVENT_READ, self.read_response)
		
	def read_response(self, key, mask):
		global stopped
		chunk = self.sock.read(4096)
		if chunk:
			self.response += chunk
		else:
			selector.unregister(key.fd)
			urls_todo.remove(self.url)
			if not urls_todo:
				stopped = True
```

我们看看做了什么改进。

1、不断尝试send和recv的2个循环被干掉了。

2、导入了selectors模块，并且创建了DefaultSelector实例。这个是对os里的select/poll/epoll的封装。会自动选择最好的那一种。



现在虽然代码结构清晰了，阻塞操作也交给os去等待和通知了。

但是，我们要抓取10个界面，就得创建10个Crawler的实例。就有20个事件将要发生，那么怎样从selectors里获取当前正在发生的事情，并且得到对应的回调函数去执行呢？

为了解决上面的问题，我们只能采取老办法，写一个循环，去访问selector模块。等待它告诉我们当前哪个事情发生了。

我们加的这个循环，就叫做事件循环。

```
def loop():
	while not stopped:
		events = selector.select()
		for event_key, event_mask in events:
			callback = event_key.data
			callback(event_key, event_mask)
```

然后我们再写入口函数。

```
if __name__ == '__main__':
	import time
	start = time.time()
	for url in urls_todo:
		crawler = Crawler(url)
		crawler.fetch()
	loop()
	print(time.time() - start)
```

这样测试得到的结果是，0.45秒。

os支持的线程数量一般是比较大的，现在我们就可以让单机支持足够多的并行任务了。

这就是我们总结出来的很有用的模式：事件循环+回调的模式。

对于一些编程语言来说，到这里，优化就基本结束了。

但是对于Python来说，要开始进入下一个环节的讨论了。

Python引入了协程的概念。协程是Python异步编程的主角。

其实回调的方式，存在着不少的问题，这个是导致我们需求进一步优化的动力。

回调的缺点有：

1、回调层次过多时，导致代码可读性变差。

2、破坏代码结构。

```
对于同步代码，关联的操作都是从上到下依次执行。
do_a()
do_b()
如果do_a是异步的，那我们就不知道do_a什么时候返回，我们只能这样来调用：
do_b(do_a())
如果流程再边长，这个就又会嵌套很多层。
嵌套很多层，还不是最关键的。
错误处理困难。
```

正是因为回调的这些问题，很多的编程语言都在致力于解决这些问题。

Python生态，秉承这“程序员不必为难程序员”的原则，让语言和框架开发者苦逼一点，让应用开发者更加轻松。

所以推出了基于协程的异步io 。

下面我们就跟随Python里异步io的发展过程来进行学习了解。



异步编程里最核心的问题是什么？

就是不知道任务什么时候执行完。

要异步，必回调。

有没有办法规避回调的缺点？

为什么回调是必须的？



协程coroutine。

C语言里也可以实现协程，就是用setjmp来做。



早期的Python开发者发现Python里有一个特殊的对象，生成器。它的特点跟协程很像。

每一次迭代之间，会暂停执行，继续执行下一次迭代的时候，还不会丢失之前的状态。

为了支持用生成器做简单的协程，在Python2.5里，对生成器进行了增强。

就是PEP342里描述的。

有了PEP 342的加持，生成器可以通过yield暂停执行和向外返回数据。也可以通过send向生成器内发送数据。

还可以通过throw向生成器内部抛出异常以便随时终止生成器的运行。



# 未来对象

好，既然我们不用回调的方式来做了，那我们怎么知道异步调用的结果呢？

先设计一个对象，异步调用执行完成的时候，就把结果放在里面。

我们把这个对象叫做未来对象。

```
class Future:
	def __init__(self):
		self.result = None
		self._callbacks = []
		
	def add_done_callback(self, fn):
		self._callbacks.append(fn)
	def set_result(self, result):
		self.result = result
		for fn in self._callbacks:
			fn(self)
```

未来对象有一个result属性，用来存放未来对象的执行结果。

但是，等等，这里面的callback是怎么回事？不是说好了不用回调的吗？

我们前面说过，有异步，必回调。

这里的回调，跟我们前面的回调，还是不一样的。我们后面再说。

我们用Future对象来重构Crawler代码。

```
class Crawler:
	def __init__(self, url):
		self.url = url
		self.response = b''
		
	def fetch(self):
		sock = socket.socket()
		sock.setblocking(False)
		try:
			sock.connect(('www.xxx.com', 80))
		except BlockingIOError:
			pass
		f = Future()
		def on_connected():
			f.set_result(None)
			
		selector.register(sock.fileno(), EVENT_WRITE, on_connected)
		yield f
		selector.unregister(sock.fileno())
		
		get = 'GET {0} HTTP/1.0\r\nHost: www.xxx.com\r\n\r\n'.format(self.url)
		sock.send(get.encode('ascii'))

		global stopped
		while True:
			f = Future()
			def on_readable():
				f.set_result(sock.recv(4096))
			selector.register(sock.fileno(), EVENT_READ, on_readable)
			chunk = yield f
			selector.unregister(sock.fileno())
			

			if chunk:
				self.response += chunk
			else:
				urls_todo.remove(self.url)
				if not urls_todo:
					stopped = True
				break
```

可以看到代码结构有很大的改动，现在只剩下了一个fetch函数了。里面有两处调用了yield。

所以fetch函数现在就是一个生成器了。

我们知道，生成器是需要先调用next函数来迭代一次，或者是先send启动，遇到yield之后便暂停。

那么，fetch生成器如何再次恢复执行呢？

**为了解决这个问题，我们只需要遵循一个编程原则，单一原则。**

既然选择还有工作没有角色来做，那我们就创建一个角色去做。

现在没人来恢复生成器的执行是吧？没人来管理生成器的状态是吧？

好，我们创建一个，名字就叫Task好了。

```
class Task:
	def __init__(self, coro):
		self.coro = coro
		f = Future()
		f.set_result(None)
		self.step(f)
		
	def step(self, future):
		try:
			next_future = self.coro.send(future.result)
		except StopIteration:
			return
		next_future.add_done_callback(self.step)
```

到这里，我们已经把Coroutine、Task、Future这3个概念串联起来了。

接下来怎么继续？

该看事件循环了。

```
def loop():
	while not stopped:
		events = selector.select()
		for event_key, event_mask in events:
			callback = event_key.data
			callback() #跟之前的不同就是这里没有参数了。
```

事件循环，就相当于系统的心脏，它现在只管往外输血，不管血是给大脑，还是给脚指头 。

通过我们这个基于生成器的协程，我们已经解决了回调的那些问题。

但是目前代码很丑。

而且会有生成器里的生成器的这种嵌套问题。

为了解决这种问题，加入了新的语法：

yield from

# 用yield from来改造生成器协程

yield from 是PEP 380里规定的。从Python3.3开始引入。

主要就是解决在生成器里玩生成器不方便的问题。

主要有2个功能：

1、让嵌套生成器不必通过循环迭代yield，而是直接yield from。

2、在子生成器和父生成器的调用者之间打开双向通道。



有了yield from的加持，协程变得更加容易了。

但是由于协程在Python里发展的历史包袱所致，很多人仍然弄不明白生成器和协程的联系与区别。

也弄不清yield和yield from的区别。

**于是Python开发者又马上在Python3.5里加入了async和await语法。**

这对于协程有了明确的支持，称为原生协程。



下面我们就要重点看asyncio和async、await的具体用法了。

因为在Python2到Python3的过度期间，3.0到3.4的使用者很少，所以我们不再考虑yield from。

而是直接看3.6里的async和await就够了。



# 什么是协程

协程，也叫微线程。

**协程的概念产生已经很久了，但是没有在实际中得到广泛应用，近几年才开始的。**

函数在所有的语言里都是层级调用的。

协程相当于在函数执行中间，转去执行其他的函数（并不是被调用的），然后再回来继续执行。

有点类似CPU的中断。

Donald Knuth的一句话就是：

函数是协程的特例。



## 协程跟多线程比，有什么优势？

1、没有线程切换到开销。

2、不需要多线程的锁的机制。

**多进程+协程的方式，可以最大化利用CPU。**

例如，我们看生产者消费者的协程实现。

```
#!/usr/bin/python2

import time

def consumer():
	r = ''
	while True:
		n = yield r
		if not n:
			return
		print('[consumer] consuming %s...' % n)
		time.sleep(1)
		r = '200 ok'
		
def producer(c):
	c.next()
	n = 0
	while n< 5:
		n = n+1
		print('[producer] producing %s...' % n)
		r = c.send(n)
		print('[producer] consumer return: %s' %r)
	c.close()
	
if __name__ == '__main__':
	c = consumer()
	producer(c)
	
```

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
[producer] producing 1...
[consumer] consuming 1...
[producer] consumer return: 200 ok
[producer] producing 2...
[consumer] consuming 2...
[producer] consumer return: 200 ok
[producer] producing 3...
[consumer] consuming 3...
[producer] consumer return: 200 ok
[producer] producing 4...
[consumer] consuming 4...
[producer] consumer return: 200 ok
[producer] producing 5...
[consumer] consuming 5...
[producer] consumer return: 200 ok
```

这个代码用Python3来跑，会报错的。



这个代码，运行效果跟我们预期的不一样。

```
import asyncio

async def foo():
    print('----start foo')
    await asyncio.sleep(1)
    print('----end foo')

async def bar():
    print('****start bar')
    await asyncio.sleep(2)
    print('****end bar')

async def main():
    await foo()
    await bar()

if __name__ == '__main__':
    asyncio.run(main())
```

打印是这样：

```
----start foo
----end foo
****start bar
****end bar
```

还是同步的效果啊。

怎么才能让foo和bar交错执行呢？

有两种方法：

1、使用gather函数。

2、创建task。

使用gather是这样：

```
async def main():
    res = await asyncio.gather(foo(), bar())
```

使用task是这样：

```
async def main():
    task1 = asyncio.create_task(foo())
    task2 = asyncio.create_task(bar())
    await task1 #这2个await是需要的，否则会直接运行结束，导致sleep后面的打印没有出来。
    await task2
```





ensure_future

这个函数的参数是task或者future，如果是future，直接返回，如果是task，转化成一个future再返回。

就是确保是一个future对象。



协程嵌套

```
import time
import asyncio

now = lambda : time.time()
async def do_some_work(x):
    print('waiting:', x)
    await asyncio.sleep(x)
    return 'done after {}s'.format(x)

async def main():
    coroutine1 = do_some_work(1)
    coroutine2 = do_some_work(2)
    coroutine3 =do_some_work(4)
    tasks = [
        asyncio.ensure_future(coroutine1),
        asyncio.ensure_future(coroutine2),
        asyncio.ensure_future(coroutine3)
    ]
    dones, pendings = await asyncio.wait(tasks)
    for task in dones:
        print("task ret:", task.result())

start = now()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print("time:", now()-start)
```



协程的状态有4种。

```
pending
running
done
cancelled
```



**设计到异步编程了，一定是单线程的。多线程的异步问题复杂到无法分析。**

一旦采取异步编程，每个异步调用必须足够小。

如果碰到的第一个问题，就是如何拆分异步任务。

程序的下一步往往依赖上一步的结果，如何知道上一个异步已经执行完成并拿到它的结果？

回调成了必然选择，回调带来了回调地狱问题。

同步代码改成异步代码，必然改变代码结构。

解决问题的逻辑也需要转变，不再是一条道走到黑。需要精心安排异步任务。

asyncio模块在python3.6版本转正的。



回调，靠给future对象add_done_callback来做。



tornado的协程库是比较早的。后面从在这些第三方实践的基础上总结出了python的标准asyncio库。

所以了解tornado的协程库，可以帮助我们了解asyncio的发展历史。

tornado的协程库有这些特点：

```
1、支持python2.7，没有使用yield from。只用了yield来实现。
2、使用抛出异常的方式从协程返回值。
	因为没有使用 yield from，协程无法直接返回值，所以使用抛出异常的方式返回。
3、采用Future类代理协程。
4、使用IOLoop做事件循环。
```

这是一个python协程的经典实现。

实现代码在这里，值得仔细读一遍。

https://github.com/TheBigFish/simple-python/blob/master/tornado/simple_coroutine.py



**协程和生成器类似，都是包含了yield。**
**不同的是，协程的yield一般出现在等号的右边。可以产出值（y = yield a），也可以不产出值（这个实际是产出值None）。**
caller可以用send函数，给协程发送值。

```
def coroutine_example(name):
    print('start coroutine...name:', name)
    x = yield name #调用next()时，产出yield右边的值后暂停；调用send()时，产出值赋给x，并往下运行
    print('send值:', x)

coro = coroutine_example('Zarten')
print('next的返回值:', next(coro))
print('send的返回值:', coro.send(6))
```



yield from内部会自动捕获StopIteration异常，并且把异常对象的value属性编程yield from表达式的值。

yield from表达式内部首先是调用iter(x)，然后再调用next()，因此x是任何可迭代对象。

yield from的主要功能是打开双向通道。把最外层的caller跟最内层的子生成器连接起来。

yield from主要用于asyncio模块做异步io。



python3.5做的改动：

```
@asyncio.coroutine 改成了async
yield from改成了 await
```

**用户主动控制程序，在认为耗时的io处添加await。**



Task不能由用户直接创建，只能通过下面的函数：

```
loop.create_task()
asyncio.ensure_future
```



获取协程的返回值，有两种方法：

```
1、task.result()方法。
	这个如果还没有运行完成，试图去获取结果会抛出异常的。
2、task.add_done_callback
```



用asyncio.wait，可以同时控制多个协程。

多个协程时，如何获取每个协程的返回值？

```
wait_coro = asyncio.wait(tasks)
loop.run_until_complete(wait_coro)

for task in tasks:
    print(task.result())
```

也可以用add_done_callback来做。



动态添加协程

方法是创建一个线程，使得事件循环在线程内永久运行。

相关函数有这些：

```
loop.call_soon()
loop.call_later()
loop.call_at()
loop.call_soon_threadsafe()
asyncio.run_coroutine_threadsafe()
```

例子：

````
import asyncio
from threading import Thread

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def thread_example(name):
    print('正在执行name:', name)
    return '返回结果：' + name


new_loop = asyncio.new_event_loop()
t = Thread(target= start_thread_loop, args=(new_loop,))
t.start()

handle = new_loop.call_soon_threadsafe(thread_example, 'Zarten1')
handle.cancel()

new_loop.call_soon_threadsafe(thread_example, 'Zarten2')

print('主线程不会阻塞')

new_loop.call_soon_threadsafe(thread_example, 'Zarten3')

print('继续运行中...')
````



# 参考资料

1、python asyncio

http://python.jobbole.com/87310/

2、深入理解 Python 异步编程(上)

这个系列文章写得很好。

http://python.jobbole.com/88291/

3、协程

https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/0013868328689835ecd883d910145dfa8227b539725e5ed000

4、

https://python3.7中asyncio的具体实现www.cnblogs.com/btxlc/p/10792477.html

5、python协程进阶，原来实现一个事件循环可以如此简单！

https://blog.csdn.net/zhoulei124/article/details/94319248

6、Python 的异步 IO：Asyncio 简介

https://segmentfault.com/a/1190000008814676?utm_source=tag-newest

7、一次爬虫的并发改造过程

https://segmentfault.com/a/1190000020964802

8、tornado 源码之 coroutine 分析

https://segmentfault.com/a/1190000017909929

9、segmentfault的asyncio专题，值得看。

https://segmentfault.com/t/asyncio/blogs

10、

这篇文章很好。

https://zhuanlan.zhihu.com/p/59621713