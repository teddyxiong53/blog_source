---
title: websocketpp
date: 2018-11-05 09:39:21
tags:
	- 网络

---



基于asio。可以是boost里带的，也可以是单独安装的asio。

手册在在这里。

http://docs.websocketpp.org/



什么是websocket？

它为什么会出现？为了解决什么问题？

基于tcp的协议。

实现了浏览器和服务器的全双工通信。允许服务器主动给浏览器发送信息。

在websocket出现之前，是靠浏览器不断发起http request来模拟双工的。这样效率非常低。

有什么限制条件？目前主要有哪些应用场景？

使用单个tcp连接。

所有主流浏览器都支持了websocket。

社交聊天、弹幕、协同编辑、股票实时刷新、体育直播、视频会议、智能家居。这些场景都可以应用。

是html5里的协议。



一个服务器程序是websocketd。



参考资料

1、百度百科

https://baike.baidu.com/item/WebSocket/1953845?fr=aladdin

2、WebSocket 教程

http://www.ruanyifeng.com/blog/2017/05/websocket.html