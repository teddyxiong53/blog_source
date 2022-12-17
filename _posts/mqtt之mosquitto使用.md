---
title: mqtt之mosquitto使用
date: 2017-10-09 21:23:45
tags:
	- mqtt

---



mosquitto是一个开源的MQTT v3.1 Broker。 这个Broker只有几百k，貌似是MQTT协议的创始人用C写的，非常精简，功能也非常强大。网上有朋友测过，可以承受20000人同时在线。

为了方便理解，mosquitto可以理解为一个sever。sub和pub是两种不同的client。sub主要是接受消息，而pub则主要是发送消息。

最简单的使用场景：

1、先启动一个shell窗口，输入：

```
mosquitto -v
```

这样就启动了一个server。-v表示verbose模式。

2、然后再开一个shell窗口，输入：

```
mosquitto_sub -t "xhliang"
```

表示启动一个订阅的client。订阅了"xhliang"这个主题。

订阅的程序是阻塞的。

3、再开一个shell窗口，输入：

```
mosquitto_pub -t "xhliang" -m "hello"
```

表示启动一个发布的client，发布了xhliang这个主题的消息"hello"。

发布的程序不是阻塞的。



# 默认的消息

我当前用Python的pahotoolkit写了一个简单的测试程序。

运行后，看到有大量的这种打印。

说明mosquitto默认在不停发布一些消息。这些消息都是在$SYS下面的。

```
[85607 - 123145446297600 - client - _on_message] [WARNING] Unhandled message, $SYS/broker/uptime: b'44 seconds'
[85607 - 123145446297600 - client - _on_message] [WARNING] Unhandled message, $SYS/broker/load/messages/received/1min: b'2.53'
[85607 - 123145446297600 - client - _on_message] [WARNING] Unhandled message, $SYS/broker/load/messages/sent/1min: b'87.05'
[85607 - 123145446297600 - client - _on_message] [WARNING] Unhandled message, $SYS/broker/load/publish/sent/1min: b'84.52'
```

这些消息有什么规律？分析一下。

这些消息，是用来让客户端获取mosquitto的姿态信息的。

标记为static的主题，对于每一次订阅只发布一次。

其他的所有主题，都是每隔sys_interval间隔（这个在配置文件里进行配置）就发布一次。

如果想要关闭这个定时发布，那么就把这个值配置为0就好了。



# python写测试代码

新建一个server.py。内容如下。另外同目录下新建一个my_settings.py。定义下面引用的变量。

```
import time
from paho.mqtt.client import Client
from pahotoolkit import init, start_async, stop_async, subscribe, json_message, on_connect


from my_settings import HOST, PORT, USERNAME, PASSWORD


@subscribe("/temperature")
def handle_temperature(client :  Client, userdata, message):
    print(f'get {message}')

@subscribe("/my/topic")
@json_message()
def listen_my_topic(payload: dict, *args, **kwargs):
    pass


@on_connect()
def client_connected(client : Client, *args, **kwargs):
    print("xhl -- connect to server")
    client.publish('/clients', 'paho mqtt toolkit message')
    print("xhl -- after publish ")

def main():
    client:Client = start_async(host=HOST, port=PORT, initialize=False)
    init(client)
    while True:
        time.sleep(1)

main()
```



# password设置

默认是可以不用密码的。

如果要加上密码，该怎么弄呢？

默认的配置目录是这样：

```
.
├── ca_certificates
│   └── README
├── certs
│   └── README
├── conf.d
│   └── README
└── mosquitto.conf
```

mosquitto.conf默认内容。

```
pid_file /var/run/mosquitto.pid

persistence true
persistence_location /var/lib/mosquitto/

log_dest file /var/log/mosquitto/mosquitto.log

include_dir /etc/mosquitto/conf.d
```

我们就在conf.d目录下，新建一个my.conf文件。

在这里面加入我们的修改。

```
mosquitto_passwd -c /etc/mosquitto/pwfile chisj
```

# libmosquitto API

当前版本是v2.0.15的。

实现了mqtt协议5.0、3.1.1、3.1.

有4个头文件

```
mosquitto.h
mosquitto_broker.h
mosquitto_plugin.h
mqtt_protocol.h
```

我们只需要使用mosquitto.h这一个头文件就可以。

只需要链接libmosquitto这一个库。

提供的接口是线程安全的。

只有mosquitto_lib_init这个一个函数不是线程安全的。

函数可以分为下面这些：

```
lib的版本、初始化、清理
	3个函数：
	xx_lib_version
	xx_lib_init
	xx_lib_cleanup
client的创建
	xx_new
	xx_destroy
	xx_reinitialize
will相关
	xx_will_set
	xx_will_set_v5
	xx_will_clear
用户名和密码
	xx_username_pw_set
连接、重连和断开
	xx_connect
	xx_connect_bind
	xx_connect_bind_v5
	xx_connect_async
	xx_connect_bind_async
	xx_connect_srv
	xx_reconnect
	xx_disconnect
	
pub、sub、unsub
	xx_publish
	xx_subscribe
	xx_subscribe_multiple
	xx_unsubscribe
	xx_unsubscribe_multiple
mosquitto_message helper函数
	xx_message_copy
	xx_message_free
	xx_message_free_contents
	
网络循环
	xx_loop_forever
	xx_loop_start
	xx_loop_stop
	xx_loop
在其他的loop里使用
	xx_loop_read
	xx_loop_write
	xx_misc
loop帮助函数
	xx_socket
	xx_want_write
	xx_threaded_set
	
client options设置
	xx_opts_set
	xx_int_option
	xx_string_option
	xx_void_option
	xx_reconnect_delay_set
	xx_user_data_set 设置data
	xx_userdata 获取data

回调函数
	xx_connect_callback_set
	xx_disconnect_callback_set
	xx_pulish_callback_set
	xx_subscribe_callback_set
	xx_unsubscribe_callback_set
	xx_log_callback_set
	
工具函数
	
```

mosquitto的代码也还可以，没有多到令人发指的长度。

代码风格也是我喜欢的朴实风格。可以读一读。以这个来掌握mqtt。



**客户端标识符（Client Identifier）**

将被 Broker 用于唯一标识客户端以及客户端的当前状态，例如客户端的订阅列表，报文收发状态等。客户端断开重连时，Broker 将根据 Client ID 来完成会话的恢复。





参考资料

1、官方文档

https://mosquitto.org/api/files/mosquitto-h.html

2、

https://mosquitto.org/documentation/

# 代码分析

Eclipse Mosquitto 提供了 MQTT 协议的轻量级服务器实现，

适用于从全功率机器到嵌入式和低功率机器的所有情况。

传感器和执行器通常是 MQTT 消息的来源和目的地，

它们可能非常小且功率不足。

这也适用于它们所连接的嵌入式机器，这是可以运行 Mosquitto 的地方。



通常，Mosquitto 的当前实现有一个大约 120kB 的可执行文件，

在连接 1000 个客户端时消耗大约 3MB RAM。

已有 100,000 个已连接客户端以适中的消息速率成功进行测试的报告。



除了接受来自 MQTT 客户端应用程序的连接外，Mosquitto 还有一个桥接器，允许它连接到其他 MQTT 服务器，包括其他 Mosquitto 实例。

这允许构建 MQTT 服务器网络，将 MQTT 消息从网络中的任何位置传递到任何其他位置，具体取决于网桥的配置。



Mosquitto 是 Eclipse Streamsheets 项目的核心组件，

它提供了一个易于使用的实时电子表格界面，

允许非开发人员处理来自 MQTT、OPC-UA、REST 和其他协议的传入数据，以生成仪表板、控制进程，或者任何需要多协议输入和输出的东西。



作者信息：

https://projects.eclipse.org/content/roger-light-project-lead-mosquitto

看loop居然是用的select？

lib\loop.c

# 持久化

只需要设置这个：

```
# =================================================================
# Persistence
# =================================================================

# 消息自动保存的间隔时间
#autosave_interval 1800

# 消息自动保存功能的开关
#autosave_on_changes false

# 持久化功能的开关
persistence true

# 持久化DB文件
#persistence_file mosquitto.db

# 持久化DB文件目录
#persistence_location /var/lib/mosquitto/
```



通常，当 MQTT 代理收到消息时，

它会立即将消息传递给所有具有匹配订阅的客户端。

如果没有订阅者，消息将不会被传递到任何地方。

然而，在某些情况下，将消息保存在代理中并在客户端重新上线时传递它是有意义的。

这可以通过在连接时使用**cleansession**标志来解决。

如果在客户端连接时**cleansession**标志设置为**false**，代理将创建一个持久会话。

当客户端在线时，所有消息都正常传递。

但是，如果具有持久会话的客户端断开连接，代理将保留有关其订阅的信息并将服务质量 1 和 2 消息排队，

直到客户端再次连接，然后传递排队的消息。

Mosquitto 将这些队列存储在内存中。

那么如果代理被关闭会发生什么？使用 Mosquitto，排队的消息将丢失，除非已配置持久存储。



例如，嵌入式设备可以使用[Mosquitto 作为本地 MQTT 代理](https://pagefault.blog/2017/03/02/using-local-mqtt-broker-for-cloud-and-interprocess-communication/)，

使用 MQTT 桥从设备建立单一传出连接，

同时在本地拥有多个通信应用程序。

这对于 Azure IoT-HUB 非常有用，它只允许每个客户端 ID 建立一个连接。

在这样的架构中，经常需要即使设备向外的连接不稳定，也要传递所有的消息，并且设备也可能关机或掉电。

在这种情况下，持久性还将简化应用程序设计，因为各个应用程序可以使用可靠的本地主机连接发送消息，而代理将处理消息的存储和向云的传递。

## mosquitto.db

这个是一个非标的文件，不是sqlite数据库文件。

需要用mosquitto自带的db_dump工具来查看内容。

https://stackoverflow.com/questions/14018386/read-db-file-in-mosquitto

## 参考资料

1、

https://blog.csdn.net/yiluang/article/details/106237149

2、消息接收+数据持久化：Mosquitto+MQTT+MySQL笔记

https://www.cnblogs.com/zkwarrior/p/14807741.html

3、mqtt离线消息的实现

https://www.jianshu.com/p/e85cdaae65bd

# 插件系统

plugins目录下放的一些插件。

src\plugin.c 这个来载入插件。是通过动态库的方式载入的。

有这几个：

```
auth-by-ip
	只给指定的ip地址授权。
消息时间戳
payload修改
都是一些简单的。函数都只有几十行。
```



# 参考资料

1、

https://blog.csdn.net/u012377333/article/details/69397124

2、订阅mosquitto服务器状态各主题

https://blog.csdn.net/qhdcsj/article/details/44630201