---
title: mqtt之libemqtt
date: 2018-07-30 09:28:29
tags:
	- 物联网

---



libemqtt是一个简单小巧的库。只有一个头文件和一个C文件。

默认提供了一个sub和一个pub的例子。



emqtt怎么知道连上来的client是同一个呢？

连接的时候，需要设置一个clientid，这个id可以不设置，如果不设置，在emqtt服务端会自动产生一个唯一的id，如果你要用到session，必须有一个唯一个id，你可以用imei。如果你一定要收到离线消息的话，就必须使用确定的id了。



#参考资料

