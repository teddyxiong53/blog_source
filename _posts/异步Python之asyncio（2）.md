---
title: Python之asyncio（2）
date: 2018-06-17 22:45:48
tags:
	- Python

---



上一篇文章，主要是了解了Python里异步io的历史。

现在我们就看看asyncio这个库的具体使用。

适合asyncio api的协程在定义函数里，必须使用yield from，而不能使用yield。

# helloworld

代码：

```
#!/usr/bin/python3

import threading, asyncio

@asyncio.coroutine
def hello():
	print('start hello', threading.currentThread())
	yield from asyncio.sleep(5)
	print('end hello', threading.currentThread())
	
@asyncio.coroutine
def world():
	print('start world', threading.currentThread())
	yield from asyncio.sleep(3)
	print('end world', threading.currentThread())
	
loop = asyncio.get_event_loop()
tasks = [hello(), world()]

loop.run_until_complete(asyncio.wait(tasks))

loop.close()
```

运行：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
start world <_MainThread(MainThread, started 140485439031040)>
start hello <_MainThread(MainThread, started 140485439031040)>
end world <_MainThread(MainThread, started 140485439031040)>
end hello <_MainThread(MainThread, started 140485439031040)>
```

代码分析：

1、要用装饰器`@asyncio.coroutine`来装饰。

# 第二个例子

代码：

```
#!/usr/bin/python3

import asyncio

@asyncio.coroutine
def worker(text):
	i = 0
	while True:
		print(text, i)
		try:
			yield from asyncio.sleep(1)
		except asyncio.CancelledError:
			break
			
		i+=1
		
@asyncio.coroutine
def client(text, io_used):
	worker_fu = asyncio.ensure_future(worker(text))
	yield from asyncio.sleep(io_used)
	worker_fu.cancel()
	
	return 'done'
	
loop = asyncio.get_event_loop()
tasks = [client('aaa', 3), client('bbb', 5)]
result = loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print('answer', result)
```



运行：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
aaa 0
bbb 0
aaa 1
bbb 1
aaa 2
bbb 2
bbb 3
bbb 4
answer ({<Task finished coro=<client() done, defined at ./test.py:17> result='done'>, <Task finished coro=<client() done, defined at ./test.py:17> result='done'>}, set())
teddy@teddy-ubuntu:~/work/test/python$ 
```

# asyncio.Task和threading.Thread对比

1、二者作用基本相同。

2、Task不需要自己手动实例化。

3、想要结束Task，就调用Task.cancel方法。



# 使用asyncio和aiohttp包

从Python3.4开始。asyncio只支持tcp和udp，如果要支持http或者其他的上层协议，就需要使用aiohttp。

下面代码是示例，跑不起来的。

```
#!/usr/bin/python3

import asyncio

cc_list = ['China', 'USA']

@asyncio.coroutine
def get_flag(cc):
	url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
	resp = yield from aiohttp.request('GET',url)
	image = yield from resp.read()
	return image
	
@asyncio.coroutine
def download_one(name):
	image = yield from get_flag(name)
	save_flag(image, name.lower()+'.gif')
	return name
	
	
loop = asyncio.get_event_loop()
wait_coro = asynio.wait([download_one(cc) for cc in sorted(cc_list)])
res, _ = loop.run_until_complete(wait_coro)

loop.close()
```



# async和await

为了简化和更好地标识异步io，从Python3.5，开始引入新的语法async和await。

这样可以让coroutine的代码变得更加容易理解。

基本替换规则是：

1、把`@asyncio.coroutine`替换为async。

2、把yield from替换为await。

看一个例子。

```
#!/usr/bin/python3

import asyncio, aiohttp

urls = [
	'http://www.163.com',
	'http://www.sina.com',
]

async def get_url_data(u):
	print('running ', u)
	async with aiohttp.ClientSession() as session:
		async with session.get(u) as resp:
			print(u, resp.status, type(resp.text()))
	return resp.headers
	
async def request_url(u):
	res = await get_url_data(u)
	return res
	
loop = asyncio.get_event_loop()
task_lists = asyncio.wait([request_url(u) for u in urls])
all_res , _ = loop.run_until_complete(task_lists)
loop.close()
print(all_res)
```

运行：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
running  http://www.sina.com
running  http://www.163.com
./test.py:14: RuntimeWarning: coroutine 'ClientResponse.text' was never awaited
  print(u, resp.status, type(resp.text()))
http://www.sina.com 200 <class 'coroutine'>
http://www.163.com 200 <class 'coroutine'>
{<Task finished coro=<request_url() done, defined at ./test.py:17> result=<CIMultiDictP...a7c7e837197')>>, <Task finished coro=<request_url() done, defined at ./test.py:17> result=<CIMultiDictP...-Value': '0')>>}
```



# 参考资料

1、Python 使用 asyncio 包处理并发

https://blog.csdn.net/andybegin/article/details/77891053