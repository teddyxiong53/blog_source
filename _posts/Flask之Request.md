---
title: Flask之Request
date: 2018-11-24 16:00:51
tags:
	- Flask
---



request是一个全局变量。可以直接用。

```
@app.route('/hello', methods=['GET', 'POST'])
def hello():
	print "headers: %s" % request.headers
	print "method: %s" % request.method
	print "data: %s" % request.data
	print "form:%s" % request.form.get('name')
	print "arg:%s" % request.args.get('age')
	print "file: %s" % request.files
	file1 = request.get('file1')
	file1.save('./file1.txt')
	print "cookie:%s" % request.cookies
	return 'hello'
```



参考资料

1、flask中的请求对象request的使用

https://blog.csdn.net/longting_/article/details/80637002