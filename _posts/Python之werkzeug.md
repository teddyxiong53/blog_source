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



# 参考资料

1、

https://www.cnblogs.com/eric-nirnava/p/werkzeug2-1.html

2、

http://werkzeug-docs-cn.readthedocs.io/zh_CN/latest/

3、Python 工具包 werkzeug 初探

http://python.jobbole.com/84765/