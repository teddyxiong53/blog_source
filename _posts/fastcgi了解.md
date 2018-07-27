---
title: fastcgi了解
date: 2018-07-26 19:10:28
tags:
	- 网络

---



fastcgi是常驻型的CGI。传统的CGI最大的问题，就是fork的效率低。

还支持分布式。

占用内存也比传统CGI的少。



web server向CGI输入是stdin和环境变量。输出是stdout。



用lighttpd和CGI来举例说明。



# 参考资料

1、百科

https://baike.baidu.com/item/fastcgi/10880685

2、

https://www.cnblogs.com/wanghetao/p/3934350.html