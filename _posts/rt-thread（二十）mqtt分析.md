---
title: rt-thread（二十）mqtt分析
date: 2018-02-13 17:40:37
tags:
	- rt-thread
	- mqtt
---



rt-thread里好几个地方都涉及到mqtt。

1、lwip的apps下面。这个是用lwip的raw api实现的。不看。

2、packages里选择的paho mqtt。这个只是用了paho的packet的目录。client是自己封装的。

3、mongoose里也包括了mqtt功能。

我当前的分析，还是以paho的为主。



paho的packet。对外的接口文件就是MQTTPacket.h文件。这个头文件里把其他几个头文件都包含进来了。packet的内容是基本固定的。主要就是协议的格式。

先不看这个。

先看client的内容。

client由2个文件组成。paho_mqtt.h。paho_mqtt_pipe.c。

另外有个example程序：paho_mqtt_app.c。

# paho_mqtt.h

1、定义QoS枚举。3种。0/1/2

2、定义MQTTMessage。

```
1、qos。
2、retained。
3、dup。
4、id。
5、void *payload
6、payload_len。
```

3、定义MessageData结构体。

```
struct {
  MQTTMessage *message;
  MQTTString *topicName;
};
```

4、定义MQTTClient结构体。

```
struct {
  char *host;
  int port;
  int sock;
  MQTTPacket_connectData conData;
  int next_packetid, command_timeout_ms;
  size_t buf_size, readbuf_size;
  char *buf, *readbuf;
  int keepAliveInterval;
  int isconnected;
  u32 tick_ping;
  void (*connect_callback)(MQTTClient*);
  void (*online_callback)(MQTTClient *);
  void (*offline_callback)(MQTTClient *);
  struct MessageHandlers {
    char *topicFilter;
    void (*callback)(MQTTClient *, MessageData *);
  }messageHandlers[1];
  void (*defaultMessageHandler)(MQTTClient*, MessageData *);
  int pub_pipe[2];
  int pub_sock;
  int pub_port;
};
```

5、声明2个函数。

paho_mqtt_start

MQTTPublish。



然后从paho_mqtt_app.c里开始看。

# paho_mqtt_app.c

全局变量：

1、static MQTTClient client; 

入口：

mq_start。这个是msh命令。输入命令就会执行。

1、先把client的数据填好。分配的buf和readbuf都是1024字节。

2、调用paho_mqtt_start。

这个函数在paho_mqtt_pipe.c里。创建了paho_mqtt_thread线程。



# paho_mqtt_thread线程

1、调用pipe函数，建立pub_pipe。

2、回调connect_callback。

3、调用自己封装的net_connect函数。新建一个socket，然后connect到目标服务器上。

4、调用自己封装的MQTTConnect函数。连接到目标服务器。

```
1、调用packet里的MQTTSerialize_connect函数，构造出conn的包。
2、调用自己封装的sendPacket把构造的包发出去。里面就是调用了send函数。
3、调用select等connack的包。
4、等到了包，调用自己封装的MQTTPacket_readPacket解析包的内容。主要是得到包头类型是不是connack。是表示成功。否则返回失败。
```

5、调用自己封装的MQTTSubscribe函数，订阅topic。

也是一个发送、等待、解析判断是否成功的过程。

6、如果上面成功，就等于这个clien就online了。调用一下online_callback。

7、然后就进入到一个死循环。就是select等待服务器的消息，如果一段时间没有等到。就调用MQTTPacket_pingreq进行查询服务器的状态。

如果等到了服务器的消息。

调用自己封装的MQTT_Cycle函数对消息进行解析处理。



上面的那个pipe是为了本地测试，把pub也放在本地。









