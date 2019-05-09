---
title: 网页之content-type常用
date: 2019-05-09 17:12:11
tags:
	- 网页
---

1

content-type的作用是什么？

用来说明返回的body使用什么方式进行编码。



常用的有：

```
1、application/x-www-form-urlencoded
	浏览器的原生表单
2、multipart/form-data
	常见的post数据提交方式。
	在使用form上传文件的时候，我们必须让form的enctype等于这个。
3、application/json
	body是json字符串。这个现在用得越来越多。
	尤其适合restful api。
4、text/xml
	
```



参考资料

1、

https://www.jianshu.com/p/ba40da728806

