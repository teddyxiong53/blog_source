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



基本的socket，client操作过程是：

```
gethostbyname()
socket()
connect()
write()
read()
```

改成SSL之后，mbedTLS对应上述函数，分别对应为

```
gethostbyname()   \ 
socket()          -+--> mbedtls_net_connect() + mbedtls_ssl_handshake()
connect()         /
write()           ----> mbedtls_ssl_write()
read()            ----> mbedtls_ssl_read()
```

mbed tls库的设计可以轻松地与现有(嵌入式)应用程序集成,并为安全通讯、密码学和密钥管理提供构建模块

mbed tls 被设计成尽可能松散耦合,让你只需要整合你需要的部分,而不需要关注其余部分.

这也为mbed tls 带来了非常低内存占用和构建足迹.

通过消除你系统中不需要的部分,你可以将构建版本从低至45kB的版本升级到更典型的300kB版本,以实现更加全面

的功能.



mbedtls/program/ssl目录下，有ssl_server.c和ssl_client1.c这2个文件。可以运行测试。

可以验证ssl通信。

把头文件梳理一下。

```
aes.h
	结构体
	mbedtls_aes_context
	函数都是mbedtls_aes_xx格式。
	主要是加密和解密函数。
	mbedtls_aes_encrypt
	mbedtls_aes_decrypt
aesni.h
	这个表示在某些Intel芯片上的硬件加速。
arc4.h
	就是rc4算法。
asn1.h
	
asn1write.h
base64.h
bignum.h
	大数计算。
blowfish.h
bn_mul.h
camellia.h
ccm.h
certs.h
	放一些证书的示例。
check_config.h
cipher.h
cipher_internal.h
cmac.h
compat-1.3.h
config.h
ctr_drbg.h
debug.h
des.h
dhm.h
ecdh.h
ecdsa.h
ecjpake.h
ecp.h
entropy.h
entropy_poll.h
error.h
gcm.h
havege.h
hmac_drbg.h
md2.h
md4.h
md5.h
md.h
md_internal.h
memory_buffer_alloc.h
net.h
net_sockets.h
	结构体：
	mbedtls_net_context：这个里面就一个fd。
	有send、recv、connect等接口。
oid.h
padlock.h
pem.h
pkcs11.h
pkcs12.h
pkcs5.h
pk.h
pk_internal.h
platform.h
platform_time.h
ripemd160.h
rsa.h
sha1.h
sha256.h
sha512.h
ssl_cache.h
ssl_ciphersuites.h
ssl_cookie.h
ssl.h
	
ssl_internal.h
ssl_ticket.h
threading.h
timing.h
version.h
x509_crl.h
x509_crt.h
x509_csr.h
x509.h
xtea.h
```

分析一下Makefile

```
DESTDIR=/usr/local
PREFIX=mbedtls_
```

```
all: programs tests
programs: lib
	$(MAKE) -C programs
lib:
	$(MAKE) -C library
```

所以，主要代码在library目录下。

得到3个库。

```
OBJS_CRYPTO  libmbedcrypto.a
OBJS_X509   libmbedx509.a
OBJS_TLS  libmbedtls.a
```

我用ssl_client1.c的来测试httpbin.org。是可以的。

但是测试iflyos.cn的，就不行。

这个是用默认的证书的。

```
The certificate is not correctly signed by the trusted CA
```

从chrome里导出iflyos.cn的证书，不行。



建立ssl加密通信，认证不是必须的。

不过一般ssl client会认证ssl server的身份，这个叫做单向认证。

我把这个改成none，不认证。还是不行。

```
mbedtls_ssl_conf_authmode( &conf, MBEDTLS_SSL_VERIFY_NONE );
```

httpbin.org的post是没有问题的。

那么就应该是iflyos的服务器要求验证client导致的。

也不对，我把之前的xr872里的注册证书的注释掉，也可以注册通信。

那就看一下xr872里的http库的实现。



知道原因了，是因为没有计算content-length导致的。计算content-length后，使用默认的证书就可以了。



# X.509

X.509是一直格式标准。是公钥证书的格式。

应用场合：

```
1、ssl通信。
2、电子签名。
```

X.509证书里包括的信息有：

```
1、公钥。
2、身份信息，例如主机名，组织名称，个体名称。
3、签名信息。可以是CA的签名，也可以是自签名。
```

除了证书本身的功能，X.509还附带了证书吊销列表和合法性验证算法。

X.509从1988年发布。

它假设有一套严格的层次化的证书颁发机构，叫做CA。



数字签名 = hash + 非对称加密。



参考资料

1、mbedtls入门和使用

https://blog.csdn.net/weixin_41965270/article/details/88687320

2、mbedTLS（PolarSSL）简单思路和函数笔记（Client端）

https://segmentfault.com/a/1190000005998141

3、mbed TLS 简明教程(一)

https://www.jianshu.com/p/26084e8665cd

4、mbed TLS 简明教程(二)

https://blog.csdn.net/z2066411585/article/details/79179906

5、mbedtls学习（10）数字证书X.509

https://blog.csdn.net/weixin_41572450/article/details/103224058

6、SSL/TLS 双向认证(三) -- ESP8266与mosquitto的MQTT双向认证

https://blog.csdn.net/ustccw/article/details/76977004

7、乐鑫esp8266 ssl使用

https://www.espressif.com/sites/default/files/documentation/5a-esp8266_sdk_ssl_user_manual_cn.pdf

8、mbedtls的ssl x509协议API

https://www.jianshu.com/p/97e27cd74ebb

9、X.509 数字证书的基本原理及应用

https://zhuanlan.zhihu.com/p/36832100