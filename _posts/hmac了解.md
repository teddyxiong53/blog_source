---
title: hmac了解
date: 2017-10-01 10:17:05
tags:
	- web

---



hmac是Hash Message Authentication Code的缩写，意思是哈希信息验证码。

原理不看了。

# 主要应用

主要是用来验证身份的。使用方法是：

1、client发出登陆请求。

2、server返回一个随机值。并在session中记录这个随机值。

3、client把这个随机值作为秘钥，对用户密码进行hmac运算，然后提交给server。

4、server对client提交上来的用户密码和数据库里的进行比对，一致就认为验证通过。



