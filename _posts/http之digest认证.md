---
title: http之digest认证
date: 2019-05-21 10:06:51
tags:
	- http

---

1

digest认证是摘要认证的意思。

因为basic认证，有很多的缺点。

digest认证是对basic认证的改进。

```
1、通过传递用户名、密码等信息的摘要，而不是直接传递用户名和密码来避免泄露。
2、通过随机数来避免重放认证过程。
3、通过客户端产生随机数cnonce的方式，来对服务器进行认证，避免被钓鱼网站欺骗。
4、对报文内容也加入摘要计算，来防止中间人对报文的篡改。
```



nginx的摘要认证，没有在nginx源代码内，需要另外安装。

网上找一个测试网站试一下这个过程。

httpbin.org就可以。

用docker拉一个镜像下来。

这样搭建环境最快。

```
docker run -p 80:80 kennethreitz/httpbin
```

看看nodejs怎么弄。





参考资料

1、详解HTTP中的摘要认证机制

https://blog.csdn.net/tenfyguo/article/details/8661517

