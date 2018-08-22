---
title: html之session
date: 2018-08-22 22:09:47
tags:
	- html

---



http协议本身是无状态的。本身并不能支持服务端保存客户端的状态信息。

所以，web server就引入了session的概念。用来保存client的状态信息。



先用一个比喻来描述session的工作方式。

把web server想象成商场的存包处。一个http request就是一个顾客，第一次来到存包处，管理员把顾客的物品存放在一个柜子里，这个柜子就相当于session。然后把一个号码牌交给顾客（session id）。

顾客（http request）下一次来的时候，就把号码牌（session id）交给存包处（web server）。存包处根据session id拿到session。根据顾客（http request）的要求，可以往柜子里拿出、放入、更换物品。



实现session的方法有两种：

1、url重写。

2、cookie。





# 参考资料

1、HTTP Session、Cookie机制详解

https://www.cnblogs.com/lyy-5518/p/5460994.html