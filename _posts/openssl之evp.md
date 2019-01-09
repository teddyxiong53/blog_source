---
title: openssl之evp
date: 2019-01-09 15:03:22
tags:		
	- openssl

---



看ssr代码，看到了evp函数，了解一下。

evp是什么意思呢？

官方没有给解释，从代码里推测，是envelope（封装）的缩写。

意思也对得上，就是封装了对外的接口。

对应的头文件是evp.h。大概1500行。

函数分为3类：

1、加密。

2、摘要。

3、编码。



参考资料

1、OpenSSL中文手册之EVP库详解

https://blog.csdn.net/liao20081228/article/details/76285896

2、What does OpenSSL's EVP mean? OpenSSL中的EVP是什么意思?

https://blog.csdn.net/zahuopuboss/article/details/8632672