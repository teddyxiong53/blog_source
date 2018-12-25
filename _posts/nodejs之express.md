---
title: nodejs之express
date: 2018-12-18 20:28:55
tags:
	- nodejs

---



express 是一个web应用框架。用来快速搭建一个网站的。

核心功能：

1、可以设置中间件来响应http请求。

2、定义路由表来执行不同的http请求动作。

3、可以通过向模板传递参数来动态渲染html页面。



# app.get和app.use区别

看N-blog的代码，看到有的时候用app.get，有的用app.use。

有什么规律？

app.get相当于app.use的get方法版本。

一般在很简单的时候用。



参考资料：

https://blog.csdn.net/wthfeng/article/details/53366169

# 参考资料

1、Node.js Express 框架

http://www.runoob.com/nodejs/nodejs-express-framework.html