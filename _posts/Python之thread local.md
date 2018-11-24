---
title: Python之thread local
date: 2018-11-24 16:31:51
tags:
	- Python
---



先看一个简单例子。

```
import threading

def test():
	local_data = threading.local()
	local_data.x = 1
	def thread_func():
		print "has x in new thread: %s" % hasattr(local_data, 'x')
		local_data.x = 2
		
	t = threading.Thread(target=thread_func)
	t.start()
	t.join()
	
	print "x in pre thread is %s " % local_data.x
	
test()
```

运行结果：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python test.py 
has x in new thread: False
x in pre thread is 1 
```

在另外一个thread里，并不能看到属性x。所以修改也就改不到本线程的属性值。





参考资料

1、Python thread local

https://www.cnblogs.com/xybaby/p/6420873.html

