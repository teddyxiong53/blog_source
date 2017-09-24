---
title: Python之多进程编程
date: 2017-09-22 23:36:05
tags:
	- Python
	- 多进程

---



Python中的多线程并不是真正的多线程，如果想要充分使用多核CPU的话，那么就用多进程吧。

Python提供了一个很好用的多进程库multiprocessing。

multiprocessing支持：子进程、通信、通信数据、同步。

提供了：Process、Queue、Pipe、Lock这些类。

# Process

构造函数：可以不带参数。可选的参数有：

group：没什么用。

target：执行函数。

name：别名。

args：元组参数。

kwargs：字典参数。

## 常用方法：

start()：创建后要用这个函数启动。

run()：如果创建时没有指定target，就会运行run函数。编程时一般是继承Process类，然后覆盖它的run方法。

join([timeout])：等待进程借宿。

is_alive()：

## 常用属性

pid：

name：

daemon：

示例程序：

```
#encoding: utf-8

import multiprocessing, time

def worker(itv):
	n = 5 
	while n> 0:
		print "time is : " + time.ctime()
		time.sleep(itv)
		n -= 1
		
if __name__ == '__main__':
	p = multiprocessing.Process(target=worker, args=(3,))
	p.start()
	print "p.pid = ", p.pid
	print "p.is_alive():", p.is_alive()
	print "p.name:", p.name
	
```



运行效果：

```
pi@raspberrypi:~/work/test/python$ python test.py 
p.pid =  749
p.is_alive(): True
p.name: Process-1
time is : Sat Sep 23 13:46:38 2017
time is : Sat Sep 23 13:46:41 2017
time is : Sat Sep 23 13:46:44 2017
time is : Sat Sep 23 13:46:47 2017
time is : Sat Sep 23 13:46:50 2017
pi@raspberrypi:~/work/test/python$ 

```



