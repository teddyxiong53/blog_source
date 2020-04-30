---
title: mqtt之3.1.1版本的改进
date: 2020-04-30 09:55:42
tags:
	- mqtt
	- iot

---

1

看到3.1.1这个版本用得比较多，我还是觉得比较奇怪，因为这个版本号显得很不正式。

看看这个版本，相对于之前的版本，做了哪些改进。

相对于它的前一个版本，3.1版本，3.1.1主要有这些改进。

```
/**
 * MQTT version to connect with: 3.1
 */
#define MQTTVERSION_3_1 3
/**
 * MQTT version to connect with: 3.1.1
 */
#define MQTTVERSION_3_1_1 4
```



### session present flag

如果客户端使用持久会话进行连接，

参考资料

1、MQTT 3.1和3.1.1版的区别

https://blog.csdn.net/qq_21842575/article/details/82760457

