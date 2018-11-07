---
title: http之post和put方法区别
date: 2018-11-06 13:26:27
tags:
	- http

---



put和post方法都可以用来创建或者更新一个资源。

粗看之下，没有区别。

但是还是有区别的。

post方法不是幂等的。多次调用会导致多个不同的资源创建。

而put会对资源进行替换。



# 参考资料

1、HTTP中post和put的根本区别和优势？

https://www.zhihu.com/question/48482736

2、HTTP协议中PUT和POST使用区别

https://blog.csdn.net/mad1989/article/details/7918267

3、RESTFUL服务中POST/PUT/PATCH方法的区别

https://blog.csdn.net/iefreer/article/details/10414663