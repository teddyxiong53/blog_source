---
title: ssl（一）
date: 2018-04-15 13:54:31
tags:
	- ssl

---



我直接从rt-thread里集成的mbedtls的代码开始看。

这个mbed是arm的嵌入式商标。所以这个mbed tls是arm公司提供的ssl开源实现。

代码量不是很大，所以适合进行代码分析。

这个以前的名字是叫PolarSSL。



# tsl和ssl关系

**TLS 实际上只是SSL的更新版本**。它修复了早期SSL协议中的一些安全漏洞。

以下是SSL和TLS版本的完整历史：

- SSL 1.0 – 由于安全问题从未公开发布。
- SSL 2.0 – 1995年发布。2011年弃用。存在已知的安全问题。
- SSL 3.0 – 1996年发布。2015年弃用。存在已知的安全问题。
- TLS 1.0 – 1999年作为SSL 3.0的升级发布。计划在2020年弃用。
- TLS 1.1 – 2006年发布。计划在2020年弃用。
- TLS 1.2 – 2008年发布。
- TLS 1.3 – 2018年发布。

https://www.wbolt.com/tls-vs-ssl.html

# Python的ssl模块

先以python的ssl作为研究入口。

这个测试验证比较方便。

使用的前提是安装了openssl。

提供了一个类：ssl.SSLSocket。是socket.socket的子类。

对于更加复杂的应用，ssl.SSLContext类可以用于管理证书。



# 参考资料

1、官网

https://www.mbed.com/zh-cn/technologies/security/mbed-tls/

2、使用mbedtls的使用说明和AES加密方法（原来的PolarSSL）

https://www.cnblogs.com/fudong071234/p/6591844.html



