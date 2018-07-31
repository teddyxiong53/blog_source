---
title: mqtt之mosquitto使用
date: 2017-10-09 21:23:45
tags:
	- mqtt

---



mosquitto是一个开源的MQTT v3.1 Broker。 这个Broker只有几百k，貌似是MQTT协议的创始人用C写的，非常精简，功能也非常强大。网上有朋友测过，可以承受20000人同时在线。

为了方便理解，mosquitto可以理解为一个sever。sub和pub是两种不同的client。sub主要是接受消息，而pub则主要是发送消息。

最简单的使用场景：

1、先启动一个shell窗口，输入：

```
mosquitto -v
```

这样就启动了一个server。-v表示verbose模式。

2、然后再开一个shell窗口，输入：

```
mosquitto_sub -t "xhliang"
```

表示启动一个订阅的client。订阅了"xhliang"这个主题。

订阅的程序是阻塞的。

3、再开一个shell窗口，输入：

```
mosquitto_pub -t "xhliang" -m "hello"
```

表示启动一个发布的client，发布了xhliang这个主题的消息"hello"。

发布的程序不是阻塞的。



# password设置

默认是可以不用密码的。

如果要加上密码，该怎么弄呢？



