---
title: avs之event发送
date: 2018-11-07 10:42:24
tags:
	- avs

---





CertifiedSender。

这个只有设置和闹钟的才用这个来发送。主要接口是sendJSONMessage。

内部有个mainLoop来处理消息。容量是50，到25的时候，就会警告了。

消息也不同于不同的MessageRequest，是这个类的子类：CertifiedMessageRequest。

而且消息会存到数据库里。

