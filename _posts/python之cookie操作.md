---
title: python之cookie操作
date: 2020-05-05 22:13:51
tags:
	- python
---



```
#将cookie以文本格式保存
import urllib.request
import http.cookiejar
filename = 'cookies.txt'
cookie = http.cookiejar.LWPCookieJar(filename)
handler = urllib.request.HTTPCookieProcessor()
openner = urllib.request.build_opener(handler)
response = openner.open('http://www.baidu.com')
cookie.save(ignore_discard=True,ignore_expires=True)

# # #读取cookie文件
cookie = http.cookiejar.LWPCookieJar()
cookie.load('cookies.txt',ignore_expires=True,ignore_discard=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
openner = urllib.request.build_opener(handler)
response = openner.open('http://www.baidu.com')
#print(response.read().decode('utf-8'))
```



参考资料

1、Python中Cookie的处理（一）Cookie库

<https://www.cnblogs.com/linxiyue/p/3536935.html>

2、Python对cookie的操作

<https://www.cnblogs.com/Osword/p/9824902.html>