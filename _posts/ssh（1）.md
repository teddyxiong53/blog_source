---
title: ssh（1）
date: 2018-08-10 22:22:17
tags:
	- 网络

---



ssh和telnet有什么区别？

1、telnet的明文的，ssh是加密的。

2、telnet的端口号是23号，ssh的端口号是22 。

3、ssh使用公钥进行身份验证。

4、telnet专门为局域网设计的。



ssh是Secure SHell的缩写。



实现免密登录的方法

基本原理是：

```
1、本机用ssh-keygen生成id_rsa和id_rsa.pub。在~/.ssh后面带pub的公钥，不带pub的是私钥。
2、复制id_rsa.pub里的内容，实际上就是一行字符串，虽然比较长。
3、到目标机器上的~/.ssh目录下，有一个authorized_keys文件，我们打开它，然后把刚刚复制的那一行公钥内容粘贴进去。
4、再尝试登陆，就可以看到已经不需要密码了。
```

这个视频将得很清楚了。

https://www.bilibili.com/video/BV1y4411q7PW

# 参考资料

ssh与telnet的异同点

https://blog.csdn.net/bbc955625132551/article/details/69196911

细述Telnet与SSH两大协议的区别

https://www.cnblogs.com/louis88/articles/5135708.html