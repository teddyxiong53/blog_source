---
title: https之mbetls
date: 2020-07-15 15:53:51
tags:
	- 网络

---

1

mbedtls这个库是arm开源的。

主要是在嵌入式产品里支持ssl/tls功能。

从功能角度来看，mbedtls可以分为3个部分：

1、ssl协议。

2、加密库。

3、X.509证书处理库。

在Linux上进行编译测试。

```
git clone https://github.com/ARMmbed/mbedtls.git
```

从这个地址快一点：

```
git clone https://gitee.com/ilylia/mbedtls
```

直接make就好了。





参考资料

1、mbedtls入门和使用

https://blog.csdn.net/weixin_41965270/article/details/88687320