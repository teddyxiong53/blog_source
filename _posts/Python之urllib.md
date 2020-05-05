---
title: Python之urllib
date: 2018-06-03 14:52:41
tags:
	- Python

---



在python2里，urllib和urllib2是不能相互替代的，是共存的。简单说，urllib2是一个补丁。

在python3里，urllib2被合入到urllib了。

而urllib3，在py2和py3里都有的，urllib3和urllib/urllib2的区别是：urllib3是一个第三方的库。而不是一个系统标准库。

如果你使用python3，那么你只需要记住urllib这一个库就好了。其他的不用管。



urllib和urllib2的区别

1、urllib和urllib2都是接受url参数的。urllib2还可以接受Request类的参数。

2、我们一般两个都会用到。

```
urllib.request
urllib.error
urllib.parse
urllib.robotparser
```



#基本使用

urllib的request模块可以非常方便地抓取url内容。

也就是发送一个GET请求到目标地址，然后返回http的响应。

举例：

```
#!/usr/bin/python3

from urllib import request

with request.urlopen('http://httpbin.org') as f:
	data = f.read()
	print ("status:", f.status, f.reason)
	for k,v in f.getheaders():
		print("%s: %s"  % (k,v))
	#print ('data: ', data.decode('utf-8'))
```

运行：

```
teddy@teddy-ubuntu:~/work/test/python$ ./test.py 
status: 200 OK
Connection: close
Server: gunicorn/19.8.1
Date: Mon, 18 Jun 2018 13:14:19 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 8344
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Via: 1.1 vegur
```

#模拟浏览器

我们也可以模拟浏览器来进行GET请求，这就是需要使用Request对象了。

```
#!/usr/bin/python3

from urllib import request

req = request.Request('http://httpbin.org')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')

with request.urlopen(req) as f:
	print('status', f.status, f.reason)
```



```
import urllib
params = urllib.urlencode({'grant_type': 'client_credentials',
                                   'client_id': 'aa',
                                   'client_secret': 'bb'})
print params
```

运行结果：

```
client_secret=bb&grant_type=client_credentials&client_id=aa
```



# 参考资料

1、urllib — URL handling modules

https://docs.python.org/3/library/urllib.html

2、urllib

https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432688314740a0aed473a39f47b09c8c7274c9ab6aee000

3、Python urllib、urllib2、urllib3用法及区别

<https://blog.csdn.net/jiduochou963/article/details/87564467>

