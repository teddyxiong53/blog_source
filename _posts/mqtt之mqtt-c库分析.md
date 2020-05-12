---
title: mqtt之mqtt-c库分析
date: 2020-05-08 13:26:08
tags:
	- mqtt

---

1

代码在这里：

https://github.com/LiamBindle/MQTT-C

我是因为paho-mqtt-c跟我gmrender放在一个代码里进行编译，会冲突，导致gmrender出现无法连接的问题。

所以才去寻找其他的mqtt方案。

libemqtt太简单，功能太弱，难以满足要求。

mqtt-c这个似乎还可以。

从代码看，对多平台都做了兼容，可见用心。

代码是C89标准写的，兼容性很好。

编译需要依赖libcmocka-dev。这个是一个单元测试的库。

```
sudo apt-get install libcmocka-dev
```

默认编译了例子。

```
./simple_publisher 
```

这个每回车一次，就往外publish一个当前时间的消息。

```
./simple_subscriber 
```

这个则订阅了这个时间消息。

```
listening for 'datetime' messages.
```

这样就可以进行简单的验证。

代码文件就2个mqtt.c和mqtt_pal.c。

pal是platform abstraction level平台抽象层的意思。这里做了对不同系统的兼容。

mqtt.c，大概1700行。

看文档里，这个项目是一个大学的课程作业。

```
Authors
MQTT-C was initially developed as a CMPT 434 (Winter Term, 2018) final project at the University of Saskatchewan by:

Liam Bindle
Demilade Adeoye
```

mqtt.h里罗列了对外的接口。

```
struct mqtt_client 

mqtt_sync
	同步发送，会等待回复内容的。
mqtt_init
mqtt_init_reconnect
mqtt_reinit
mqtt_connect
mqtt_publish
mqtt_subscribe
mqtt_unsubscribe
mqtt_ping
mqtt_disconnect
```



有一个队列来存放消息。

```
struct mqtt_message_queue
```

配套的函数：

```
mqtt_mq_init
mqtt_mq_clean
mqtt_mq_register
mqtt_mq_find
mqtt_mq_get
mqtt_mq_length
mqtt_mq_currsz
```



mqtt_mq_init

```
参数1：
	是输出参数，主要就是用这个函数来填充mqtt_client结构体。
参数2：
	sockfd。socket需要用户自己创建，然后传递进去。
参数3/4/5/6：
	send buf和recv buf及长度。
参数7；
	一个回调函数。是在收到数据的时候调用。
	我们在这个里面接收处理数据。
处理逻辑：
	很简单，就是填充结构体。
```

mqtt_connect

```
参数：
	有9个。主要是username这种，没有什么特别的。
```

构造一个message，都是这种模式。

```
/* try to pack the message */
    MQTT_CLIENT_TRY_PACK(rv, msg, client, 
        mqtt_pack_connection_request(
            client->mq.curr, client->mq.curr_sz,
            client_id, will_topic, will_message, 
            will_message_size,user_name, password, 
            connect_flags, keep_alive
        ), 
        1
    );
```



参考资料

1、

