---
title: 网络之oAuth
date: 2018-05-19 14:00:37
tags:
	- 网络
---



oAuth协议

是用来为用户资源的授权的。

任何第三方都可以使用oAuth服务。

有php、js、java、ruby等版本。

特点：

1、简单。

2、安全。没有涉及用户密钥等信息。

3、开放。



典型案例

有两个网站，一个网站A，提供了图片在线存储功能。

一个网站B，提供了图片在线打印的功能。

用户在这2个网站上的用户名和密码都不同。

用户在网站B上进行图片打印的时候，图片是存在A网站上的。

所以需要网站B得到网站A授权。

但是不能采取B直接得到A网站上的用户名和密码的方式，这样太不安全了。

于是oAuth就为了解决这种场景而出现了。标准1.0版本在2007年12月发布。







# 参考资料

1、oAuth

https://baike.baidu.com/item/oAuth/7153134?fr=aladdin

2、OAuth 授权的工作原理是怎样的？足够安全吗？

https://www.zhihu.com/question/19781476

3、OAuth 2.0 的一个简单解释

http://www.ruanyifeng.com/blog/2019/04/oauth_design.html