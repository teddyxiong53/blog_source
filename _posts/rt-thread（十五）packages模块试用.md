---
title: rt-thread（十五）packages模块试用
date: 2018-02-06 13:47:30
tags:
	- rt-thread

---



rt-thread的3.0版本，已经加入了很多的第三方的package。但是经过我初步使用，很多模块还是有问题的。

本文就把各个package打开看看使用情况。

安装menuconfig里看到的层次关系，是这样的：

```
system packages
	lwext4：轻量级的ext2/3/4文件系统。
	partition：分区工具。
	sqlite：sqlite数据库。用不起来。也没有文档支持。
	rt-thread insight。调试工具。
IOT ：物联网相关的包。
	paho mqtt：mqtt协议支持。
	webclient：
	mongoose：这个是一个web server。还有一个同名的rtos。
	webterminal：
	cjson：
	ljson：
	ezxml：
	nanopb：protocol buffer。
	gagent：
	wifi：进去是勾选驱动。
	coap：
	nopoll：
security：
	mbedtls：
	libsodium：
	tinycrypt：
language：
	Jerryscript
	MicroPython
MultiMedia：
	openmv
tools：
	cmbacktrace。给CortexM用的。
	easylogger。
	systemview：
	iperf。
misc：
	fastlz：压缩。
	minilzo：
	hello：

```

为了控制变量，我们采取单个引入的方式，除非相互依赖了。

我们先把所有的都勾选了。然后在bsp/qemu-vexpress-a9目录下。

有2个模块有点小问题。ljson的配置有点问题，改了可以继续。SystemView的有问题，我暂时不用这个了。

# hello

hello是一个简单的示例。我们分析一下，看看package的构成。

目录下就一个hello.c和一个SConscript。

hello里就定义一个类似main函数的函数。然后用MSH命令输出。

```
#include <rtthread.h>
#include <finsh.h>

int hello_func(int argc, char** argv)
{
    rt_kprintf("Hello RT-Thread!\n");
    return 0;
}
MSH_CMD_EXPORT(hello_func, say hello);

```



system的package当前就不管了。

从iot的开始看。

lwip协议关闭对ipv6的支持。把所有我还不是很清楚的配置都关闭掉。



# IOT



## paho mqtt

只选择mqtt和它的sample。

在bsp/qemu-vexpress-a9/packages下下载了pahomqtt目录。

```
├── example
│   └── paho_mqtt_app.c
├── LICENSE
├── MQTTClient-RT
│   ├── paho_mqtt.h
│   ├── paho_mqtt_pipe.c：编译这个。
│   └── paho_mqtt_udp.c：这个不用。
├── MQTTPacket
│   └── src
│       ├── MQTTConnectClient.c
│       ├── MQTTConnect.h
│       ├── MQTTConnectServer.c
│       ├── MQTTDeserializePublish.c
│       ├── MQTTFormat.c
│       ├── MQTTFormat.h
│       ├── MQTTPacket.c
│       ├── MQTTPacket.h
│       ├── MQTTPublish.h
│       ├── MQTTSerializePublish.c
│       ├── MQTTSubscribeClient.c
│       ├── MQTTSubscribe.h
│       ├── MQTTSubscribeServer.c
│       ├── MQTTUnsubscribeClient.c
│       ├── MQTTUnsubscribe.h
│       ├── MQTTUnsubscribeServer.c
│       └── StackTrace.h
├── README.md
└── SConscript
```

运行起来看看。

提供了mq_start、mq_pub这两条命令。

mq_start对应client。默认是要访问iot.eclipse.org。我的qemu连不了外网。我在本地搭建一个mqtt服务。

总之比较难用。我先放着。代码可以后续读一读。



## webclient



## webterminal

这个对于嵌入式意义不大。

看到需要c99的支持。先不要了。

而且这个引入了问题，我没有选择这个模块的时候，会进行编译。

不过我可以把对应目录下的SConscript改个名字，就不会编译了。

##cjson

解析cjson的文件。我另外写了一篇文章进行实验。



# security



## libsodium



## tinycrypt



# MultiMedia



## openmv

