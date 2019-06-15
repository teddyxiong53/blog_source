---
title: http之上传文件multipart
date: 2019-06-15 09:52:37
tags:
	- http
---

1

现在有个需求，是基于libcurl，向服务武器上传日志文件。

具体怎么做呢？

关于http文件上传，有一个RFC1867协议文档。

主要就是给input标签增加了file属性。

同时限定了form的method只能是post，enctype必须是multipart/form-data。



RFC1867对HTTP头的变更

```
RFC1867对HTTP头作了适当地变更，但变更很小。首先content-type头由以前的：
content-type: application/x-www-form-urlencoded
变为
content-type: multipart/form-data; +空格+
boundary=---------------------------7d52b133509e2
即增加了boundary，所谓的boundary其实就是分割线，下文将看到，RFC1867利用boundary分割HTTP实体数据。boundary中数字字符区是随机生成的。
```

RFC1867对http body的变更

```
因为RFC1867增加了文件上传得功能，而上传文件内容自然也会被加入到HTTP的实体中。现在因为既有HTTP一般的参数实体，又有上传文件的实体，所以用boundary把每种实体进行了分割，HTTP的实体看起来将是下面的样子： 

-----------------------------7d52b133509e2
Content-Disposition: form-data; name="file1"; filename="c:/aa.txt"
Content-Type: text/plain

文件内容在此处
-----------------------------7d52b133509e2
Content-Disposition: form-data; name="userName"
zhangsan
-----------------------------7d52b133509e2
Content-Disposition: form-data; name="password"
123
-----------------------------7d52b133509e2--
```



参考资料

1、

https://blog.csdn.net/u013379553/article/details/79832909

2、C语言 HTTP上传文件-利用libcurl库上传文件

https://www.cnblogs.com/lidabo/p/4159574.html