---
title: cgi规范
date: 2019-01-16 20:05:45
tags:
	- cgi

---



看wsgi，还是需要先看cgi。

看cgi，就看规范。



属于Internet draft。更新比较频繁。



cgi是一个简单的接口，用来运行外部程序。在服务器上。平台无关。

所指的服务器，是http服务器。



请求包含：

uri、方法、辅助信息。



cgi定义了抽象参数，就是环境变量。描述了client的请求。



草案的规格有：

1、必须。must。

2、推荐。should。

3、可选。may。



url编码，用%来编码特殊字符。



环境变量

大小写不敏感。



# 参考资料

1、cgi规范原稿

https://tools.ietf.org/html/draft-robinson-www-interface-00