---
title: python之threading之event
date: 2017-07-22 23:38:45
tags:

	- python

	- threading

---

Python线程的event主要用于main现场控制其他线程的执行，event主要提供了3个方法：wait、set、clear。实现线程间通信。

简单描述，机制是这样的：有一个全局的flag，如果flag是true，那么wait会阻塞，如果flag是false，则wait不会导致阻塞。

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





