---
title: http之keep-alive
date: 2020-08-05 14:22:47
tags:
	- http

---

1

# 使用HTTP建立长连接

当需要建立 HTTP 长连接时，HTTP 请求头将包含如下内容：
 `Connection: Keep-Alive`
 如果服务端同意建立长连接，HTTP 响应头也将包含如下内容：
 `Connection: Keep-Alive`
 当需要关闭连接时，HTTP 头中会包含如下内容：
 `Connection: Close`



HTTP 1.1支持只发送header信息(不带任何body信息)，

如果服务器认为客户端有权限请求服务器，则返回100，否则返回401。

客户端如果接受到100，才开始把请求body发送到服务器。

这样当服务器返回401的时候，客户端就可以不用发送请求body了，节约了带宽。



由上面的示例可以看到里面的请求头部和响应头部都有一个key-value `Connection: Keep-Alive`，

这个键值对的作用是让HTTP保持连接状态，

因为HTTP 协议采用“请求-应答”模式，当使用普通模式，即非 Keep-Alive 模式时，

每个请求/应答客户和服务器都要新建一个连接，完成之后立即断开连接（HTTP 协议为无连接的协议）；

当使用 Keep-Alive 模式时，Keep-Alive 功能使客户端到服务器端的连接持续有效。

**在HTTP 1.1版本后，默认都开启Keep-Alive模式，**

只有加入加入 `Connection: close`才关闭连接，

当然也可以设置Keep-Alive模式的属性，例如 `Keep-Alive: timeout=5, max=100`，

表示这个TCP通道可以保持5秒，max=100，表示这个长连接最多接收100次请求就断开。



现在我虽然客户端设置了keep-alive，但是感觉很快就被服务端关闭了连接。

我设置timeout=1800看看。

没用的。这个要服务端设置。算了。



参考资料

1、HTTP协议的Keep-Alive 模式

https://www.jianshu.com/p/49551bda6619

2、nginx keepalive_timeout 设置策略问题分析

https://blog.csdn.net/zilaike/article/details/82112803