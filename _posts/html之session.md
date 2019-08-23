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



cookie和session的关系

cookie是记录在客户端，在进行请求的时候，一起传递给服务端，用来标识客户端的某些特性的。

session是保存在服务端，用来识别特定的用户的。

cookie和session都是会话的一种方式。

典型的使用场景是购物车。

当你点击下单按钮后，服务端并不清楚用户的具体操作。

为了标识并跟踪这个用户，了解购物车里的东西，服务端为这个用户场景了cookie和session。



客户端和服务端交互的过程

服务端向客户端回复的http response header里包含一个set-cookie的字段。

分为6个部分。

```
Set-Cookie: 
logcookie=3qjj;//名字。
expires=Wed, 13-Mar-2019 12:08:53 GMT;//过期时间。
Max-Age=31536000;//
path=/;
domain=fafa.com;
secure;
HttpOnly;

```



# 参考资料

1、HTTP Session、Cookie机制详解

https://www.cnblogs.com/lyy-5518/p/5460994.html

2、详解 Cookie 和 Session 关系和区别

https://ruby-china.org/topics/33313

3、Cookie 和 Session 关系和区别

https://juejin.im/post/5aa783b76fb9a028d663d70a