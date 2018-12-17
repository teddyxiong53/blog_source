---
title: 蓝牙之Ubuntu串口
date: 2018-12-17 21:00:02
tags:
	- 蓝牙

---



在Ubuntu上进行蓝牙串口通信。

按照这个步骤来。

1、查看当前蓝牙是否已经启动串口服务。

```
teddy@teddy-ThinkPad-SL410:~$ sudo sdptool browse local | grep "Service Name" 
Service Name: Generic Access Profile
Service Name: Generic Attribute Profile
Service Name: AVRCP CT
Service Name: AVRCP TG
Service Name: Audio Source
Service Name: Audio Sink
Service Name: Headset Voice gateway
Service Name: Message Notification
Service Name: Message Access
Service Name: Phone Book Access
Service Name: Synchronization
Service Name: File Transfer
Service Name: Object Push
Service Name: Nokia OBEX PC Suite Services
```

看来没有启动。

2、启动蓝牙串口服务。

```
teddy@teddy-ThinkPad-SL410:~$ sudo sdptool add --channel=22 SP
Serial Port service registered
```

3、运行。

```
teddy@teddy-ThinkPad-SL410:~$ sudo rfcomm listen /dev/rfcomm0 22
Waiting for connection on channel 22
Connection from B4:0B:44:F4:16:8D to /dev/rfcomm0
Press CTRL-C for hangup
Disconnected
teddy@teddy-ThinkPad-SL410:~$ 
```

4、手机上运行蓝牙SPP调试助手。

就可以进行通信了。



# 参考资料

1、How do I connect and send data to a bluetooth serial port on Linux?

https://unix.stackexchange.com/questions/92255/how-do-i-connect-and-send-data-to-a-bluetooth-serial-port-on-linux