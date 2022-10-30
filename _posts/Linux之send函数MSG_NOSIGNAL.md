---
title: Linux之send函数MSG_NOSIGNAL
date: 2022-10-27 13:18:33
tags:
	- Linux

---

--

linux下当连接断开，还发数据的时候，不仅send()的返回值会有反映，而且还会向系统发送一个异常消息，

如果不作处理，系统会出BrokePipe，程序会退出，**（为什么不直接给应用设置忽略pipe信号呢？）**

这对于服务器提供稳定的服务将造成巨大的灾难。

为此，send()函数的最后一个参数可以设MSG_NOSIGNAL，禁止send()函数向系统发送异常消息



参考资料

1、

https://blog.csdn.net/yuanchunsi/article/details/79745619