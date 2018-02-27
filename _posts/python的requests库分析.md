---
title: python的requests库分析
date: 2017-01-04 21:09:24
tags:
	- python
---




requests是基于urllib写的，是第三方库，不是python自带的。它在使用上比urllib要更加方便，更加适合在python中使用。
安装就用`pip install requests`来安装。

先看一个最简单的使用例子。

```
#!/usr/bin/python

import requests
r = requests.get(url='http://www.baidu.com')
print r.status_code
r = requests.get(url='http://dict.baidu.com/s', params={'wd':'python'})
print r.url
```
这个例子只用到了GET方法，POST等其他方法的接口跟这个都是类似的。

使用requests里的函数后，都会返回一个response的对象。



# requests的用途

requests是对urllib的封装。有了requests库，http操作就变得更加简单了。



# 快速上手

下面的操作在Python命令行里进行就可以了。更加方便。

1、发送请求。

```
import requests
r = requests.get('http://httpbin.org/get')
print r.content
```

2、进行post、put、head、delete、options操作。

```
r = requests.put('http://httpbin.org/put')
r = requests.post('http://httpbin.org/post')
r = requests.head('http://httpbin.org/get')
r = requests.delete('http://httpbin.org/delete')
```

3、传递url参数。

打印url，可以看到url已经被正确编码。

```
>>> payload = {'key1':'value1', 'key2':'value2'}
>>> r = requests.get('http://httpbin.org/get',params=payload)
>>> print r.url
http://httpbin.org/get?key2=value2&key1=value1
```

4、json内容。

requests内置了一个json解码器。帮你进行json数据处理。



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

