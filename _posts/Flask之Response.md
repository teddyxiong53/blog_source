---
title: Flask之Response
date: 2018-11-24 16:05:51
tags:
	- Flask
---



Response可以用来包装普通的字符串。

```
@app.route('/1')
def hello1():
	return 'hello 1'
	
@app.route('/2')
def hello2():
	return Response('hello 2')
```



参考资料

1、flask response对象

https://blog.csdn.net/claroja/article/details/78853499

2、flask第十五篇——Response

http://www.cnblogs.com/captainmeng/p/8649113.html