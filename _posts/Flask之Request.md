---
title: Flask之Request
date: 2018-11-24 16:00:51
tags:
	- Flask
---

--

服务器在收到客户端的请求后，会自动创建request对象。

是Flask框架自动创建的，request对象不可修改。

request是一个全局变量。可以直接用。

从Flask模块导入request：from flask import request

flask为了http协议的header这些情况，特意创建了对应的数据结构来处理。

MultiDict：这个库只在py3里用。为http header和url而设计。普通的dict，一个key只能对应一个value。而MultiDict的特点是：一个key可以有多个value，而这些value保持了它们插入的顺序。而且key是大小写不敏感的。



主要属性：

```
==========url相关，3个
url：完整的url。
base_url：去掉get参数的url
host_url：只包含host和port的url
=======remote相关，remote是指客户端
remote_addr：客户端的地址
remote_ip：客户端的ip
=======get相关
args：get请求的参数
======post相关
form：post请求的参数
files；文件上传。
=======其他
path：路由的路径。
method；请求方法。
headers：请求头
cookies：请求里的cookies
values：把args和form结合到一起的。
data：请求的数据，并转成了字符串。除非是二进制的。
environ：wsgi隐含的环境变量。
json：如果mimetype是json类型，

```



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

2、Flask的 Request常用请求操作

https://blog.csdn.net/hu1258123819/article/details/100044784

3、Flask request 属性详解

https://blog.csdn.net/u011146423/article/details/88191225