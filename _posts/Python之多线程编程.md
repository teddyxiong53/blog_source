---
title: Python之多线程编程
date: 2017-09-22 23:02:07
tags:
	- Python
	- 多线程

---



Python中实现多线程，有2个库可以用：thread库和threading库。

threading库是对thread的封装，提供更简单易用的接口。所以我们先从基础的thread库看起。



# 1. thread

thread库提供了低级别的、原始的线程以及一个简单的锁。这个锁是一个mutex锁。

所以对象有2个：thread和lock。

这个库是可选的，底层支持是posix thread。所以需要系统上有posix thread支持。

这个库的学习策略是：只做了解，实际不用。

## thread

基本接口：

增：start_new等价于start_new_thread。参数是线程函数名字。另外还有传递给线程函数的参数，如果没有，给一个空的元组`()`。

删：exit等价于exit_thread。没有参数。

改：thread.stack_size(size)，如果有size这个参数，则是指定堆栈大小。没有则是返回当前堆栈大小。

查：thread.get_ident()。获取当前线程的标识符。

## lock

lock = thread.allocate_lock()：创建一个锁。

获取锁：lock.acquire()

释放锁：lock.release()

查询锁的状态：lock.locked()



# 2. threading

threading是基于Java的线程模型来进行设计的。Python里的thread是Java里thread的子集。

Python里的thread没有优先级，没有线程组，也不能被停止，恢复。

threading库提供这些类：

Thread, Lock, Rlock, Condition, Semaphore, Event, Timer, local

## Thread类

Thread类是线程类，和Java里类似，有两种使用方法，直接传入要运行的方法或者继承Thread并且覆盖run函数。

```
#encoding: utf-8

import threading

# 第一种方式
def func():
	print "thread run"
	
t = threading.Thread(target=func)
t.start()
# 第二种方式
class MyThread(threading.Thread):
	def run(self):
		print "thread class run"
		
t1 = MyThread()
t1.start()
```

一些方法的使用：

```
>>> import threading
>>> t1 = threading.Thread()
>>> print t1.name
Thread-1
>>> print t1.ident
None
>>> print t1.is_alive()
False
>>> print t1.isAlive()
False
>>> print t1.isDaemon()
False
>>> 
>>> print threading.currentThread()
<_MainThread(MainThread, started 1993302016)>
>>> 
>>> print threading.currentThread().name
MainThread
>>> 
```

