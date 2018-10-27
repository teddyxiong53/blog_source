---
title: Python之tornado
date: 2018-05-18 21:50:08
tags:
	- Python

---



tornado是一个Python写的web框架。字面意思是龙卷风。

它的特点是：

非阻塞，速度快。

它的原理是使用了非阻塞方式和epoll。

每秒可以处理数以千计的连接。

# 基本例子

```
#!/usr/bin/env python

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("hello tornado")
		
application = tornado.web.Application(
	[
		(r"/index", MainHandler),
	]
)

application.listen(8888)
tornado.ioloop.IOLoop.instance().start()
```

访问这个地址：

http://192.168.0.9:8888/index

就可以得到页面了。

这个逻辑跟Flask和类似。



# 参考资料

1、Tornado基本使用

https://www.cnblogs.com/chenchao1990/p/5413547.html