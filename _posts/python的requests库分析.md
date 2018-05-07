---
title: Python之requests库
date: 2017-01-04 21:09:24
tags:
	- python
---



requests是基于urllib写的，是第三方库，不是python自带的。它在使用上比urllib要更加方便，更加适合在python中使用。
安装就用`pip install requests`来安装。

下面内容参考http://docs.python-requests.org/en/latest/user/quickstart/ 。



先看一个最简单的使用例子。

```
>>> import requests
>>> r = requests.get("https://api.github.com/events")
>>> print r.status_code
200
```

再看post、delete、head、options方法。

```
>>> r = requests.post("http://httpbin.org/post", data={'key':'value'})             
>>> print r.status_code
200
>>> r = requests.put('http://httpbin.org/put', data={'key':'value'})               
>>> print r.status_code
200
>>> r = requests.delete('http://httpbin.org/delete')
>>> print r.status_code
200
>>> r = requests.head('http://httpbin.org/get')
>>> print r.status_code
200
>>> r = requests.options('http://httpbin.org/get')
>>> print r.content

>>> print r.status_code
200
```



如果我们要在url里带上参数，直接的做法就是用'?'来做。

例如这样：

```
http://httpbin.org/get?key=val
```



但是requests支持用字典的方式来传递参数。

我们可以这样：

```
>>> payload = {'key1':'value1', 'key2':'value2'}
>>> r = requests.get('http://httpbin.org/get', params=payload)
>>> print r.url
http://httpbin.org/get?key2=value2&key1=value1
>>> 
```

如果key的value是None的话，就不会被加入到url里。

还可以在params里加入list。

```
>>> payload = {'key1':'value1', 'key2':['value2','value3']}
>>> r = requests.get('http://httpbin.org/get', params=payload)
>>> print r.url
http://httpbin.org/get?key2=value2&key2=value3&key1=value1
```



然后我们查看response里的内容。

```
>>> r = requests.get('http://httpbin.org/get')
>>> r.text
u'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": 
"gzip, deflate", \n    "Connection": "close", \n    "Host": "httpbin.org", \n    "U
ser-Agent": "python-requests/2.5.0 CPython/2.7.9 Linux/4.14.24-v7+"\n  }, \n  "orig
in": "59.63.206.223", \n  "url": "http://httpbin.org/get"\n}\n'
```

```
>>> r.content
'{\n  "args": {}, \n  "headers": {\n    "Accept": "*/*", \n    "Accept-Encoding": "
gzip, deflate", \n    "Connection": "close", \n    "Host": "httpbin.org", \n    "Us
er-Agent": "python-requests/2.5.0 CPython/2.7.9 Linux/4.14.24-v7+"\n  }, \n  "origi
n": "59.63.206.223", \n  "url": "http://httpbin.org/get"\n}\n'
```

content和text区别在于，text的是Unicode编码的。

content不是。



```
>>> payload = {'key1':'value1','key2':'value2'}
>>> r = requests.post('http://httpbin.org/post', data=payload)
>>> print r.text
{
  "args": {},
  "data": "",
  "files": {},
  "form": {
    "key1": "value1",
    "key2": "value2"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "close",
    "Content-Length": "23",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.5.0 CPython/2.7.9 Linux/4.14.24-v7+"          
  },
  "json": null,
  "origin": "59.63.206.223",
  "url": "http://httpbin.org/post"
}
```



# 高级用法



## session对象

session可以帮你保存多个request的参数。

这样当你想一个机器发送多个请求的时候，性能就会得到很大的提升。

跨请求来保持一下cookie。

```
>>> s = requests.Session()
>>> s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
<Response [200]>
>>> r = s.get('http://httpbin.org/cookies')
>>> print r.text
{
  "cookies": {
    "sessioncookie": "123456789"
  }
}

>>> 
```



# 身份认证

