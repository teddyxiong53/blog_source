---
title: Flask之Local分析
date: 2018-11-24 16:27:51
tags:
	- Flask
---



在使用Flask或者werkzeug的时候，经常碰到这3个东西：

1、Local。

2、LocalStack。

3、LocalProxy。

什么是Local？

为什么需要Local？

Python提供了thread local对象用来存储thread safe的数据。

thread local对象在有些情况下，还是不能保证安全，所以flask开发了自己的Local。





参考资料

1、Werkzeug(Flask)之Local、LocalStack和LocalProxy

https://www.jianshu.com/p/3f38b777a621