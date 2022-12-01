---
title: openssl（1）
date: 2019-05-23 13:22:51
tags:
	- openssl

---

--

重新对openssl进行学习。

什么是openssl？有什么作用？什么情况下需要用openssl？

ssl是Secure Socket Layer。安全套接字层。是网景公司提出来的概念。

后面网景把ssl提交给国际组织进行标准化，改名为TLS。



根据私钥，可以很容易推导出公钥，而反向推算则很难。

私钥要由拥有者妥善保存。公钥则可以随意分发。



因为CA的地址是内嵌在浏览器中的，很难被篡改。

Ubuntu16.04默认安装的openssl是1.0.2g的。

连接需要2个库：libssl和libcrypto。





参考资料

1、

