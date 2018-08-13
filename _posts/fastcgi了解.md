---
title: fastcgi了解
date: 2018-07-26 19:10:28
tags:
	- 网络
typora-root-url: ..\
---



fastcgi是常驻型的CGI。传统的CGI最大的问题，就是fork的效率低。

还支持分布式。

占用内存也比传统CGI的少。



web server向CGI输入是stdin和环境变量。输出是stdout。



用lighttpd和CGI来举例说明。



CGI是一套接口标准。具体实现可以用asp、php、jsp等语言实现。

交互图是这样的：

![](/images/fastcgi了解-CGI架构.png)

常用的CGI环境变量。

CONTENT_TYPE：表示传递过来的信息的mime类型。一般是application/x-www-form-urlencoded。

CONTENT_LENGTH：如果是post方法，表示从stdin读取到的字节数。

HTTP_COOKIE：客户机里的cookie内容。

HTTP_USER_AGENT：浏览器信息。

PATH_INFO：



fastcgi的工作流程是这样的：

1、web server启动时载入fastcgi进程管理器。

2、fastcgi进程管理器自身初始化。启动多个cgi解释器进程，等待来自web server的连接。

3‘、当客户端请求到达web server的时，fastcgi进程管理器选择并连接到一个cgi解释器。

4、返回内容。


# 参考资料

1、百科

https://baike.baidu.com/item/fastcgi/10880685

2、

https://www.cnblogs.com/wanghetao/p/3934350.html