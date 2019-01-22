---
title: 网页之x-www-form-urlencoded
date: 2019-01-22 11:22:55
tags:
	- 网页

---



看express的post例子里，有这么一行：

```
// 创建 application/x-www-form-urlencoded 编码解析
var urlencodedParser = bodyParser.urlencoded({ extended: false })
```

在http的例子里，没有这一行。

x-www-form-urlencoded具体是什么意思？

通常http协议是以ASCII编码进行传输的。

http报文格式：

```
<method> <request-url> <version>
<headers>

<entity-body>
```

http协议规定post请求提交的数据，必须放在entity-body里。

但是协议没有规定使用什么编码。

数据发出去后，服务端进行解析。

服务端一般是根据Content-Type字段来知道客户端的消息主体的编码。

然后再对主体进行解码。

#application/x-www-form-urlencoded

```
application/x-www-form-urlencoded
```

这个是最常见的post提交数据的方式了。

浏览器的原生form表单，如果不设置enctype属性。

最终就会用这种方式进行提交。

请求类似下面这样：

```
POST http://xx.com HTTP/1.1
Content-Type: application/x-www-form-urlencoded;charset=utf-8

name=xx&domain=com
```

提交的数据都按照：

```
key1=value1&key2=value2
```

这种方式进行编码。

key和value都进行了url转码。

大多数服务端语言都对这种方式有很好的支持。

很多时候，我们用ajax提交数据时，都是用这种方式。

例如，jQuery，Content-Type的默认值就是application/x-www-form-urlencoded。



# multipart/form-data

这也是很常见的post数据提交方式。

我们使用表单上传文件时，必须让form的enctype等于这个。

两部分：文件名和文件内容。

```
POST http://xx.com HTTP/1.1
Content-Type: multipart/form-data;boudary=xyz

--xyz
Content-Disposition: form-data;name="text"

title

--xyz
Content-Disposition: from-data;name="file";filename="logo.png"
Content-Type: image/png
0000111

--xyz--
```

xyz是一个boundary字符。可以随意定义，尽量奇怪一点，不要跟正常内容重叠。



# application/json

前面两种方式是浏览器原生支持。

这种现在也都支持了。

# text/xml

一般是做远程调用。

```
POST http://xx.com HTTP/1.1
Content-Type: text/xml

<!--?xml version="1.0"?-->
<methodcall>
	<methodname>xx.getStateName</methodname>
	<params>
		<param>
			<value><i4>11</i4></value>
		</param>
	</params>
</methodcall>
```





参考资料

1、

https://hongjiang.info/http-application-x-www-form-urlencoded/

2、HTTP协议-POST方法详解

http://www.qmailer.net/archives/245.html