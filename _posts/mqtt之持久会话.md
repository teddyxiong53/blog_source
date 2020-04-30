---
title: mqtt之持久会话
date: 2020-04-30 10:01:42
tags:
	- mqtt
	- iot

---

1

当一个mqtt client连接到broker的时候，它需要订阅所有它感兴趣的topic。

当client从broker断开后，已订阅的主题会丢失，client需要重新订阅一次。

有些client订阅的topic特别多，上万条这种量级的话，订阅就会是一个很大的负担。

所以，引入了持久会话的概念，broker会保留这个client的信息。

client的标记，由clientid来唯一标记。



持久会话是从mqtt协议3.1.1版本开始引入的。



持久会话，会保存哪些信息呢？

```
1、所有订阅消息。
2、所有还没有被client确认的，且qos为1和2的消息。
3、所有因为client离线而没有收到的，且qos为1和2的消息。
4、所有客户端已经疏导，但是尚未确认的qos为2的消息。
```



怎样启动和关闭持久会话？

是在client连接broker的时候指定的。

以paho mqtt的代码为例。MQTTCLIENT_PERSISTENCE_NONE 表示不建立持久会话。

```
MQTTClient_create(&m_client, url, clientid, MQTTCLIENT_PERSISTENCE_NONE, NULL)
```

实际上是把cleansession这个标志位置位为0。

broker在connack里，会包含当前的会话标志。



要建立这个持久会话，client也有义务保留一部分的信息。





参考资料

1、MQTT Part 7 持久会话和消息队列

https://www.jianshu.com/p/379b5dbb6233