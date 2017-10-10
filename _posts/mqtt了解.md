---
title: mqtt了解
date: 2017-09-18 21:49:15
tags:
	- iot
	- mqtt

---



mqtt是Message Queues Telemetry Transport的缩写。表示消息队列遥测传输。

mqtt是和http在同一层的应用层协议。http协议的请求回答模式对于物联网应用不太适用。mqtt使用的是发布订阅模式。

http是基于文本的，mqtt是基于二进制的。

mqtt规范很简单，最早是由IBM提出的，很适合低功耗和带宽有限的iot应用场景。

例如：遥感数据、汽车、智能家居等。

mqtt的设计遵循下面的原则：

1、精简，可有可无的东西不要。

2、采用发布订阅模式。

3、允许用户动态创建主题，零运维成本。

4、把传输量降到最低。

5、把网络慢、不稳定这些因素充分考虑。

6、支持连续的会话控制。

7、理解客户端的计算能力很低。

8、提供质量服务管理。QoS。

9、假设数据不可知，不强求传输数据的类型与格式，保持灵活性。



在1999年，IBM的两个博士就提出了mqtt协议。在mqtt出现前，物联网应用里采集传感器数据是靠不断查询传感器。这种方式简单、粗暴，而且很耗电。

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

国内有家创业公司，叫云吧，在做相关的工作。例如集成在某些App里的聊天功能，App的消息推送。



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

主题的分隔符是`/`。可以有多个斜杠来分层。如下：

```
room401/light
room401/tv/control/sensor
```

`#`井号是主题的通配符。就像我们平时一般用星号来通配类型。

`+`加号是单层通配符。

`$`美元符通配一个字符。



# 8. utf编码

看到协议里说payload内容是用utf编码的。这句话的内涵是什么？

