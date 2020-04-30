---
title: mqtt之paho.mqtt代码分析
date: 2017-10-17 23:21:42
tags:
	- mqtt
	- iot

---



从代码里的宏看，这套代码兼容了windows、osx、Linux。我们重点关注Linux版本的代码。

从sample目录下的paho_cs_pub.c代码作为分析入口。

对外的接口和结构体都在MQTTClient.h里进行声明。实现都在MQTTClient.c里。



这个库设计的原则就是易于使用，有些接口会阻塞。

例如MQTTClient_connect就会阻塞，如果在timeout时间内没有成功，则返回失败。这个timeout默认是30s。

但是对于移动设备或者其他有图形界面的设备，在gui线程里阻塞会导致界面无法响应。

这个对于用户体验是非常不好的。

所以又增加了新的api，MQTTAsync。在MQTTAsync.c里实现。

异步的方式，不会影响gui，但是增加了复杂性。

对线程比较节省，使用了select的io多路复用。

封装的接口是：Socket_getReadySocket。这个api是线程安全的。



# 对外暴露的数据结构体

1、MQTTClient

这个就是void *的指针。类似一个handle的概念。

**对应的内部结构体是MQTTClients，**这个是一个较大的结构体。

2、MQTTClient_connectOptions

在connect函数里使用。

所有结构体的特点：

都是前面有个struct_id的数组，就是放几个字符：'M'/'Q'/'T'/'C'。这样的。

然后是一个struct_version。就是这个结构体的版本号。



# 对外的接口

1、MQTTClient_create

这个就是得到一个MQTTClients对象。

需要指定url、clientid、是否持久化。

函数分析：

{

1、如果是第一次调用这个函数，则进行一系列的初始化。

​       包括：socket初始化、list初始化。

2、malloc一个MQTTClients，对各个成员进行初始化。有不少链表、sem。

}

2、MQTTClient_connect

连接到mqtt server。

调用层次如下：

```
MQTTClient_connect
	MQTTClient_connectURI
		MQTTClient_connectURIVersion
			MQTTProtocol_connect
				Socket_new：这里进行了connect操作。
				MQTTPacket_send_connect
					MQTTPacket_send
						Socket_writev
```



3、MQTTClient_publish

发布消息。

需要的参数：client handle，topic字符串，payload长度，payload本身，qos，retain标志。

4、MQTTClient_subscribe



5、MQTTClient_receive



