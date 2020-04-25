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



参考资料

1、

https://blog.csdn.net/u012377333/article/details/69397124

2、订阅mosquitto服务器状态各主题

https://blog.csdn.net/qhdcsj/article/details/44630201