---
title: Python之werkzeug
date: 2017-09-17 14:48:53
tags:
	- python

---



官网http://werkzeug.pocoo.org/

是一个WSGI工具库。

注意，是一个工具库，而不是一个web server。它是web server的底层。

封装了很多web相关的东西，例如request，response。

flask就是基于werkzeug的。

https://github.com/mitsuhiko/werkzeug.git





我们现在基于werkzeug来自己实现一个简单的web server。

```
import os
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

class Shortly(object):
	def dispatch_request(self, request):
		return Response('hello werkzeug')
	def wsgi_app(self, environ, start_response):
		request = Request(environ)
		response = self.dispatch_request(request)
		return response(environ, start_response)
		
	def __call__(self, environ, start_response):
		return self.wsgi_app(environ, start_response)
		
def create_app(with_static=True):
	app = Shortly()
	if with_static:
		app.wsgi_app = SharedDataMiddleware(app.wsgi_app, 
			{
				'static':os.path.join(os.path.dirname(__file__), 'static')
			})
		return app
		
if __name__ == '__main__':
	app = create_app()
	run_simple('0.0.0.0', 8000, app, use_debugger=True)
```



# local模块

werkzeug的local模块，跟python的标准库的thread.local是类似的。

但是功能更多。

为什么需要自己增强local模块呢？

因为python里处理并发可以用协程，一个线程里可以包含多个协程。

可以用一个协程处理一个请求，那么在一个线程里就会有多个请求，

用thread.local无法很好地处理这种情况。

werkzeug自己写的local模块，实现了4个类：

1、Local。

2、LocalStack。

3、LocalProxy。

4、LocalManager。



在flask里，重要的变量都是LocalStack和LocalProxy的，所以需要弄清楚用法。



# 参考资料

1、

https://www.cnblogs.com/eric-nirnava/p/werkzeug2-1.html

2、

http://werkzeug-docs-cn.readthedocs.io/zh_CN/latest/

3、Python 工具包 werkzeug 初探

http://python.jobbole.com/84765/

4、Werkzeug库——local模块

http://python.jobbole.com/87738/