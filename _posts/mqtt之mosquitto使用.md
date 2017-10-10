---
title: mqtt之mosquitto使用
date: 2017-10-09 21:23:45
tags:
	- mqtt

---



mosquitto是一个开源的MQTT v3.1 Broker。 这个Broker只有几百k，貌似是MQTT协议的创始人用C写的，非常精简，功能也非常强大。网上有朋友测过，可以承受20000人同时在线。

为了方便理解，mosquitto可以理解为一个sever。sub和pub是两种不同的client。sub主要是接受消息，而pub则主要是发送消息。



[1] 发布者客户端运行命令示例：

```
mosquitto_pub -h 192.168.6.243 -p 1883 -t "111" -m "this is jason.hou" -u 111 -P 111
```



[2] 订阅者客户端运行命令示例:

```
mosquitto_sub -h 192.168.6.243 -i 111 -p 1883 -t 111 -k 60 -d -c -u hjx -P hjx
```

[3] mosquitto服务器端运行命令示例：

```
mosquitto -v
```



