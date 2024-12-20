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



# 怎么学习

学习和掌握 OpenSSL 的命令行工具可以通过以下几个步骤系统进行：

### 1. **了解基础概念**
   - 学习加密、解密、证书、密钥等基本概念。
   - 了解对称加密与非对称加密的区别。

### 2. **安装 OpenSSL**
   - 在你的操作系统上安装 OpenSSL。可以在 [OpenSSL 官网](https://www.openssl.org/) 下载并安装。

### 3. **查阅官方文档**
   - 阅读 [OpenSSL 文档](https://www.openssl.org/docs/) 来了解各个命令和参数的详细信息。
   - 关注常用命令的使用示例。

### 4. **学习常用命令**
   - 开始时专注于一些常用命令，如：
     - 生成私钥：`openssl genpkey`
     - 生成证书签名请求（CSR）：`openssl req`
     - 自签名证书：`openssl req -x509`
     - 转换文件格式：`openssl pkcs12`、`openssl x509`
   - 每个命令的参数可以通过 `man openssl` 或 `openssl help` 查看。

### 5. **动手实践**
   - 在本地环境中进行实际操作，生成密钥、创建证书等。
   - 尝试使用不同的参数组合，观察其效果。

### 6. **学习示例和案例**
   - 查找网上的教程或案例，了解不同场景下 OpenSSL 的使用。
   - GitHub 等平台上有很多开源项目，可以学习他们的配置和使用方法。

### 7. **解决常见问题**
   - 记录遇到的问题及其解决方案，可以帮助加深理解。
   - 参与相关社区或论坛，向其他用户请教。

### 8. **进阶学习**
   - 学习 OpenSSL 的编程接口（如 C 语言 API）。
   - 了解 OpenSSL 的安全性和漏洞，保持对最新版本和更新的关注。

### 9. **持续练习**
   - 经常使用 OpenSSL 进行各种加密和解密操作，保持技能的熟练度。

通过以上步骤，逐步掌握 OpenSSL 的使用，形成系统的知识结构。

# 参考资料

1、OpenSSL源码库目录解析

https://blog.csdn.net/starboybenben/article/details/50549854

2、

https://xghost.blog.csdn.net/article/details/110099236