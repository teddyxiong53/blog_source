---
title: shadowsocks之加密算法
date: 2017-07-22 12:09:48
tags:

	- shadowsocks

---

shadowsocks里的可选的加密有好几种，这些加密方法分别有什么特点？

以windows客户端为例。有table、rc4-md5、salsa20、chacha20、aes-256-cfb、aes-192-cfb、aes-128-cfb、rc4共8种可选。我看手机客户端上可选择的更加多。当前我都是使用chacha20的。

# 1. table

table加密是通过生成一个字符置换表，是很容易被破解的。





