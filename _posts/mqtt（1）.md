---
title: mqtt了解
date: 2017-09-18 21:49:15
tags:
	- iot
	- mqtt

---



mqtt是Message Queues Telemetry Transport的缩写。表示消息队列遥测传输。

mqtt是和http在同一层的应用层协议。**http协议的请求回答模式对于物联网应用不太适用。mqtt使用的是发布订阅模式。**

http是基于文本的，mqtt是基于二进制的。

mqtt规范很简单，最早是由IBM提出的，很适合低功耗和带宽有限的iot应用场景。

例如：遥感数据、汽车、智能家居等。

mqtt的设计遵循下面的原则：

1、精简，可有可无的东西不要。

2、采用发布订阅模式。

3、**允许用户动态创建主题，零运维成本。**

4、把传输量降到最低。

5、把网络慢、不稳定这些因素充分考虑。

6、支持连续的会话控制。

7、理解客户端的计算能力很低。

8、提供质量服务管理。QoS。

9、假设数据不可知，不强求传输数据的类型与格式，保持灵活性。



在1999年，IBM的两个博士就提出了mqtt协议。**在mqtt出现前，物联网应用里采集传感器数据是靠不断查询传感器。这种方式简单、粗暴，而且很耗电。**

**最早研究这个是为了石油管道和卫星通信的场景。**



OASIS组织在2013年，宣布将mqtt作为新兴的物联网消息传递协议的首选标准。



# 1. 发布/订阅模式

与请求/回答这种同步模式不同，发布/订阅模式解耦了生产者和消费者的关系。

发布订阅模式，就是你把一个消息贴到公布栏一样。你不用关系谁会去看，谁关心谁自己去看。

这是编程中很常见的一种设计模式。带来了下面的好处。

你不需要关心有多少用户。你把消息贴出去就好了。用户也不需要知道谁生产的消息，只需要知道公布栏的位置就好。这对通信的主体带来了很大的解放。



# 2. mqtt协议在协议栈上的位置

是在tcp之上的应用层。

传统上我们网络通信，都是自己基于socket来做。因为这个是一个重复造轮子的过程。mqtt封装了socket操作，帮我们做了很多的工作。直接用比我们自己写要好。



# 3. mqtt的实际应用有哪些？

1、物联网云。

YeeLink是国内最大的物联网云平台之一。

国外的是EvoThings。

2、实时消息推送。

facebook是较早大规模采用mqtt协议的互联网巨头。

云吧也是用mqtt来推送的。



# 4. mqtt的服务端

eclipse为了支持mqtt的发展，建立了一个公共的mqtt服务器：test.mosquitto.org。

也可以自己搭建服务器端。我们可以自己用mosquitto来搭建自己的 服务器。

我们订阅这个服务器的看看，`mosquitto_sub -h test.mosquitto.org -t "#" -v`。会得到很多的信息。

```
home/kitchen/status dead
home/status stopped
home/ESP-2D881F/hum 62.60
home/ESP-2D881F/temp 19.50
home/ESP-2D881F/led 0
home/ESP-2D881F/status connected
home/ESP-2D881F/tau 12.17
home/ESP-2D881F/abshum 12.00 g/m3
home/outside/led 0
home/outside/status connected
home/outside/temp 13.90
home/outside/tau 10.82
home/outside/hum 81.70
home/outside/abshum 11.22 g/m3
home/alarm disarmed
magicblcoks/thenuka/m2mqtt ww
magicblcoks/thenuka/w sdd
```



# 5. mqtt的客户端

paho就是用来做mqtt的客户端的。网上有个用arduino做的基于mqtt的WiFi物联网血压计。用Python做的。

其工作过程是：

1、用户启动血压测量。则血压计把mqtt消息发布到test.mosquitto.org的服务器。

2、只要是订阅相关病人血压主题的医生，都可以及时掌握病人的血压变化。医生的手机像收到微信消息一样，收到了病人的血压数据。



# 6. mqtt的改进方式

如果说改进，那肯定就是因为mqtt有缺点。

mqtt的缺点是什么？

1、是tcp连接的，连接一直存在。如果你的传感器网络大部分时间是要处于休眠状态的，那么可以使用mqtt-s。这个是基于udp的。

2、缺少加密机制。

# 7. 主题

订阅和发布都要以主题为基础。只有订阅了某个主题之后，才能收到相应主题的payload，才能进行通信。

1、主题区分大小写。

2、每个主题至少一个字节。可以包含空格。



主题的分隔符是`/`。可以有多个斜杠来分层。如下：

```
room401/light
room401/tv/control/sensor
```

`#`井号是主题的通配符。就像我们平时一般用星号来通配类型。

`+`加号是单层通配符。

`$`美元符通配一个字符。**正常的用途是用来不被`#`来通配。一般用来做mqtt服务器的保留特性。例如$SYS这种。**



下面是一些主题使用上的建议：

1、不要用'/'开头。这个会导致认为前面有个空的主题。

2、虽然在主题中用空格，但是建议不要用。就如同Linux里的文件名可以加空格，但是用起来麻烦。

3、只用ASCII字符。不要用不可打印的字符。

4、不要订阅`#`。这样消息就太多了。



# 8. utf编码

看到协议里说payload内容是用utf编码的。这句话的内涵是什么？



# 9. mqtt 的心跳

就是ping，客户端定时发给服务端，告诉服务端自己还在呢。



# 10. will的作用

看到协议里提到了will这个东西，有什么用呢？

1、will是在connect报文里发给服务器的。

2、作用是客户端给自己留的遗言，就是自己异常端口的时候会有作用。

3、will的内容是主题加消息。当客户端异常断开时，服务端就会主动把这个will的内容发布出来。



# 11. retain标志的作用

就是要求服务端长期保持这个消息。就是这个消息不仅要发给当前的订阅者，还要发给新来的订阅者。



# 12. dup标志的作用

如果dup被设置为1，则意味着消息的变长头部要有一个message id存在，并且要求回复确认。

这个和qos大于0的值进行配合。



# 13. mqtt的flag分类

我们到目前看到了好些mqtt的flag。有什么规律？

flag分为两种，一种在固定头部里，一种在可变头部里。

## 固定头部里的flag

就是dup、qos、retain这3个。总共占用4个bit。

作用范围是？

## 可变头部里的flag

有username和password的标志。

will的3个：will retain，will qos，will flag。

还有一个bit的clean session。

clean session是0，表示客户端和服务端要建立长久的会话。这个和qos为1和2时进行配合，服务端会保留所有的消息。



# 14 . 持久会话

当一个client连接到一个server的时候，它需要订阅所有感兴趣的主题。再次连接时，之前的主题都不见了，你需要重新订阅，是不是很麻烦？那怎么办？

要做到这个，就要靠可变头部里的clean session这个flag来做。为0的时候，表示要建立的就是持久会话。





# 其他

我在实际使用中，发现这样的实现行为：

我pub了一个消息是，qos为2的，然后启动一个sub。看broker的打印，可以看到broker就马上把之前pub出来的消息发给了这个sub。

```
1532927913: New connection from 127.0.0.1 on port 1883.
1532927913: New client connected from 127.0.0.1 as doss_server (c1, k30).
1532927913: Sending CONNACK to doss_server (0, 0)
1532927914: Received SUBSCRIBE from doss_server
1532927914:     doss/device_info (QoS 0)
1532927914: doss_server 0 doss/device_info
1532927914: Sending SUBACK to doss_server
1532927914: Sending PUBLISH to doss_server (d0, q0, r1, m0, 'doss/device_info', ... (36 bytes))
```

但是实际上sub这边并没有看到。

不过我先启动sub。再启动pub。是可以收到的。



keepalive

这个是用来做心跳间隔的。以秒位单位的。

一个U16的长度，最长就是18个小时。

mqtt_init 默认给的是300秒。

sub程序，需要定时给broker发ping。

对于pub，则没有要求，因为pub可以发一下，就马上退出的。

如果到了应该发ping的时候，broker还没有收到，broker就会认为这个client已经断开了。



**mqtt支持离线，你订阅了某个topic，这个topic之前的消息就会都发过来的。**



# 参考资料

1、MQTT协议笔记之连接和心跳

http://www.blogjava.net/yongboy/archive/2014/02/09/409630.html

2、mqtt协议中文版

https://mcxiaoke.gitbooks.io/mqtt-cn/content/

3、Mqtt Qos 深度解读

https://www.jianshu.com/p/8b0291e8ee02