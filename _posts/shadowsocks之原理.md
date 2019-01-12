---
title: ssr之原理
date: 2019-01-08 17:19:25
tags:
	- ssr

---





基础是socks5协议。

协议的rfc文档在这里。不长，只有7页。

https://www.ietf.org/rfc/rfc1928.txt

socks5是tcp/ip层的网络代理协议。

建立连接。

client向server发送的数据包如下：

```
ver nmethods methods
1    1          1    字节数
```

ver：默认为0x5 。

nmethods：表示第三个字段methods的长度。

methods：表示client支持的验证方式，长度为1到255字节。

目前支持的验证方式有：

```
0x00： 不需要验证。
0x01：GSSAPI
0x02：用户名和密码
0x03：
0x04：
0xff：保留。
```

server响应client的连接。

```
ver  method
1    1
```

例如，如果不需要验证，那么就是 ：

```
05 00
```



和真实目标连接

client跟server连接后，下一步就是把自己的真实意图告诉server。

server把这个请求转发到对应的网站。

这个消息的格式是：

```
ver   cmd   rsv    atyp    dst.addr     dst.port
1     1      0x00  1       available     2
```

cmd：代表client请求的类型。有3种可能。connect（1），bind（2），udp（3）。

rsv：保留。

atyp：表示远程服务器的地址类型。

```
1：ipv4地址。
3：domain name
4：ipv6地址。
```

server根据这些信息，跟目标网站进行交互，无论成功与否，都会给client一个反馈。

格式如下：

```
ver   rep   rsv   atyp    bnd.addr   bnd.port
```

rep：状态码。

```
0：成功。
1：一般错误。
2：连接不允许。
3：网络不可达。
4：host不可达。
5：连接拒绝。
6：ttl超时。
7：不支持的命令。
8：地址类型不支持。
9到0xff：还没有定义。
```



这里是lightsocks的python版本实现。

https://github.com/linw1995/lightsocks-python

使用了异步io编程。

所以需要在python3里跑。



使用io多路复用，而不是多线程，这样对资源的占用更少。



ssr设计上采用了reactor模式。

每一个tcp连接，分配一个TCPRelayHandler进行处理，类似多线程里，分配一个线程来处理一样。



sslocal+ssserver才是一个完整的sock5服务器，被拆分开来，主要是为了加密绕过gfw。

整个协议都是在sslocal端实现的，



sslocal端不会做dns的。

是ssserver做的dns。

不是，还是需要的，只是我当前配置的vps的是ip地址，所以直接走这个分支了。

```
elif common.is_ip(hostname):
            callback((hostname, hostname), None)
```

sslocal也就只需要做这一次就够了。

后面的域名都是发给ssserver去处理的。

对于sslocal，on_local_write不会被调用到的。

对于ssserver，也没有看到调用on_local_write。



server的_on_remote_write，是把请求发出去。

server的_on_remote_read，是把网页内容收进来。



跟服务器配置的端口，有哪些交互？

服务器端收到的第一个消息，是什么？



参考资料

1、你也能写个 Shadowsocks

https://segmentfault.com/a/1190000011862912

2、Shadowsocks 源码分析——协议与结构

这篇文章特别好，值得认真研究。这个文章的作者实现了rust版本的ssr。

https://loggerhead.me/posts/shadowsocks-yuan-ma-fen-xi-xie-yi-yu-jie-gou.html

tcprelay分析

https://loggerhead.me/posts/shadowsocks-yuan-ma-fen-xi-tcp-dai-li.html

超时机制分析

https://loggerhead.me/posts/shadowsocks-yuan-ma-fen-xi-chao-shi-chu-li.html