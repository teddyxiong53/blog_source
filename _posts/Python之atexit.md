---
title: Python之atexit
date: 2017-11-20 15:44:14
tags:
	- Python

---



atexit模块很简单，就定义了一个register函数，用来注册在退出程序时要做的操作，一般是释放一些资源。

注意注册的顺序和执行的顺序是相反的，这个很容易理解。

```
#!/usr/bin/python 

import atexit

def exit0(*args ,**kwargs):
	print "exit0"
	print "args:"
	for arg in args:
		print ' ' , arg
	
	print "**kwargs"
	for k in kwargs:
		print ' ', k,kwargs[k]
	
def exit1():
	print "exit1"
	
atexit.register(exit0, *[1,2,3], **{"a":1, "b":2})
atexit.register(exit1)

```

输出：

```
pi@raspberrypi:~/work/test/py-test$ ./test.py 
exit1
exit0
args:
  1
  2
  3
**kwargs
  a 1
  b 2
pi@raspberrypi:~/work/test/py-test$ 
```

