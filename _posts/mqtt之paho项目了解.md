---
title: mqtt之paho项目了解
date: 2017-10-09 20:23:28
tags:
	- mqtt

---



paho这个项目的总体目标是：提供针对IOT的消息协议。

项目当前的重点就是mqtt的pub和sub程序。后续可能会增加对其他协议的支持。



# 1. 使用paho client

1、创建一个client对象。

2、设置连接到server的option。

3、设置多个回调函数，如果使用异步模式的话。

4、订阅主题。

5、死循环里。处理消息。

6、断开连接，释放资源。

