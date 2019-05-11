---
title: 加密之pbkfd2算法
date: 2019-05-11 09:56:11
tags:
	- 加密

---



pbkdf2是Password-Based Key Derivation Function。

是用来导出秘钥的函数。

一般用来生成加密的密码。

函数的定义：

```
DK = PBKDF2(PRF, Password, Salt, c, dklen)
PRF：伪随机函数。
Password：密码原文。
Salt：加密用的盐值。
c：重复计算的次数。
dkLen：期望得到的秘钥的长度。
DK：最后得到的秘钥结果。
```



参考资料

1、PBKDF2 算法概述

https://blog.csdn.net/xy010902100449/article/details/52078767