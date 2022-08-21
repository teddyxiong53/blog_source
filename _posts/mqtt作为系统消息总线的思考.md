---
title: mqtt作为系统消息总线的思考
date: 2022-08-14 11:43:08
tags:
	- mqtt

---

--

我对于使用dbus作为系统总线，觉得非常繁琐复杂。

我希望可以用json格式来组织消息，各个通信组件之间可以自由随意相互发送消息。

我觉得mqtt的订阅发布模式很好。有很大的自由度。

现在看看能不能把它设计成一个可用的嵌入式Linux本地消息总线来使用。

我对于效率的要求没有那么高，通信的数据量也没有那么大。



这个思路是行得通的。

现在就要先找一个嵌入式可用的mqtt broker

看buildroot里已经集成了mosquitto。

这个当然可以用。



所以就是在本地运行一个mosquitto。



在刚才描述的嵌入式系框架设计中，每一个进程都是运行在本地的，所有的消息也都是在系统内进行收发。那么，如果需要把数据传输到云端、或者需要从云端接收一些控制指令，又该如何设计呢?

加入一个 **MQTT Bridge 桥接模块即可**!也就是再增加一个进程，这个进程同时连接到云端的 MQTT Broker 和本地的 MQTT Broker，通信模型如下：

![img](../images/random_name/1603bc52d72a4411ed45ff980c9c6923.jpg)

MQTT Bridge 接收到云端发来的指令时，转发到本地的消息总线上;

MQTT Bridge 接收到本地的消息时，转发到云端的消息总线上。



mqtt bridge用哪个开源的呢？



Mosquitto broker 可以被配置为一个 MQTT bridge 桥，连接着两个 MQTT broker。

通常的做法是连接边缘 MQTT brokers 到一个中心/远程的 MQTT 网络。



当你配置一个 broker 为 bridge 时，它就成为了一个 MQTT 客户，可以订阅/发布消息给另一个broker，并且它自己依赖 **mosquitto.conf** 配置文件。



我把mqtt_msg_bus写完了。

但是想了一下，mqtt方式对于方法调用，然后返回调用的结果支持不是太好。

应该在收到sub消息，处理后，给出pub。

payload里，我就用jsonrpc的格式来做。

那怎么样让调用后阻塞等待执行结果呢？

dbus也并不都是阻塞，也有两套接口，一套sync的，一套异步的。

搜索“mqtt rpc”。

https://blog.csdn.net/yaojiawan/article/details/101282825

这篇文章跟我的想法一样，也是把payload用jsonrpc的格式化。

这个作者是写了这个modular-2 edge的软件。

https://blog.csdn.net/yaojiawan/article/details/100141479



maxim labs 是一个研发iot 技术的公司，过去的两年中，我们开发了基于Arm 公司Mbed OS 的模块化物联网设备modular-2。

modular-2是一台基于cortex-M 系列微处理器为主的模块化微服务器它采用Arm 公司物联网操作系统Mbed OS ， Mbed 的C++ 设备驱动API使程序员基本摆脱了硬件的细节，使应用软件更加模块化，更加清晰和高效率开发。

目前，modular-2 技术包括了三项技术

1. modular-2 micro server 模块化微服务器
2. modular-2 Edge server 模块化边缘服务器
3. modular-2 Cloud server 模块化云服务器

MQTT同步通信（RPC）

https://developer.qiniu.com/linking/6309/mqtt-synchronous-communication

这个是七牛云的产品。直接就有这种应用场景。

mqtt做为⼀个异步PUB/SUB协议在嵌⼊式设备中使⽤很⼴泛，主要⽤户数据上报和从服务端指令下发。这种模式⽆法满⾜IoT中的设备控制功能(需要同步返回设备数据)，Linking平台开发了⼀套**基于mqtt的同步返回机制**，对外提供http的API，⼿机端/应⽤服务端通过API即可同步返回设备端结果。



这个是nodejs版本的实现。

https://github.com/rse/mqtt-json-rpc

这个是mongooseos上的实现。

https://mongoose-os.com/docs/mongoose-os/api/rpc/rpc-mqtt.md

这个是讨论mqtt是否适合做rpc通信。

https://www.quora.com/Is-MQTT-suitable-for-interprocess-communication



ipc和rpc

我现在是需要rpc多过ipc。

rpc还是比较强调要消息的返回结果的。

mqtt做RPC还是不太合适。



# 参考资料

1、

这个系列倒是跟我的想法有些契合。看看。用户是“道哥分享”。

https://iot.ofweek.com/2021-03/ART-132209-11000-30487804.html

这篇非常好，图画得很直观。

https://mp.ofweek.com/iot/a756714071157

这个是道哥的cnblog地址

https://www.cnblogs.com/sewain/

2、mqtt应用于进程间通信实例分享

https://juejin.cn/post/6984070002320080910

3、

https://www.51cto.com/article/645702.html

4、

https://www.wandouip.com/t5i76527/

5、

https://www.cnblogs.com/zhenqichai/p/mosquitto-bridge-configuration.html

6、

https://blog.csdn.net/yaojiawan/article/details/101282825

7、一种基于MQTT的请求/响应模型

https://blog.csdn.net/happen23/article/details/107413922