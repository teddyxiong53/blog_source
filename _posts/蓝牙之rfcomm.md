---
title: 蓝牙之rfcomm
date: 2018-11-27 14:59:35
tags:
	- 蓝牙

---



看蓝牙相关资料，看到rfcomm这个东西。了解一下。

rfcomm是蓝牙协议栈里的一个协议。

这个协议很简单，是在无线上模拟了RS232协议。

rfcomm可以支持2个蓝牙模块之间同时进行60路通信。

```
/* ---- RFCOMM sockets ---- */
struct sockaddr_rc {
	sa_family_t	rc_family;
	bdaddr_t	rc_bdaddr;
	u8		rc_channel;
};
```

```
#define BTPROTO_L2CAP	0
#define BTPROTO_HCI	1
#define BTPROTO_SCO	2
#define BTPROTO_RFCOMM	3
#define BTPROTO_BNEP	4
#define BTPROTO_CMTP	5
#define BTPROTO_HIDP	6
#define BTPROTO_AVDTP	7
```



查看自己安装的bluez的版本。

```
teddy@teddy-ThinkPad-SL410:/etc/bluetooth$ dpkg -s bluez |grep ^Version
Version: 5.37-0ubuntu5.1
```



基于rfcomm，可以实现拨号上网、ftp功能等。

基于rfcomm的编程，跟基于socket的编程一样，只是ip地址变成了蓝牙地址，端口号变成了channel。

也可以写服务端和客户端。



在linux/socket.h里，

AF_INET是2 ，AF_BLUETOOTH是31 。它们是一个层级的东西。

蓝牙协议栈里的协议有：

```
#define BTPROTO_L2CAP	0
#define BTPROTO_HCI	1
#define BTPROTO_SCO	2
#define BTPROTO_RFCOMM	3
#define BTPROTO_BNEP	4
#define BTPROTO_CMTP	5
#define BTPROTO_HIDP	6
#define BTPROTO_AVDTP	7
```

协议层选项：

```
#define SOL_HCI		0
#define SOL_L2CAP	6
#define SOL_SCO		17
#define SOL_RFCOMM	18
```



# rfcomm具体可以做什么

说了那么多，从用户的角度看，rfcomm可以帮我们做什么？

是通过在蓝牙L2CAP协议的基础上模拟RS232串口。

用户可以在其他设备上连接到这个蓝牙，对这个蓝牙进行操作。

```
#!/usr/bin/env python
#--*--coding=utf-8--*--
#P191
#sudo pip install pybluez
 
import time
from bluetooth import *
def rfcommCon(addr,port):
    sock = BluetoothSocket(RFCOMM)
    try:
        sock.connect((addr,port))
        print "[+] RFCOMM port : " +str(port)+' open'
        sock.close()
    except Exception,e:
        print '[-] RFCOMM port :' +str(port)+' closed'
 
for port in range(1,30):
    rfcommCon('FE:XX:XX:XX:XX:57',port)
```



参考mit网站上的例子。

rfcomm服务器端。

```
import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1
server_sock.bind(("", port))
server_sock.listen(1)
client_sock,address = server_sock.accept()
print "accept conn from ", address

data = client_sock.recv(1024)
print "reveived:[%s]" % data

client_sock.close()
server_sock.close()
```

rfcomm客户端

```
import bluetooth

bd_addr = "01:23:34:67:89:ab"
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))
sock.send("hello,bt")
sock.close()
```



#参考资料

1、RFCOMM

https://www.cnblogs.com/fbli/p/5930383.html

2、蓝牙RFCOMM剖析（一）

https://blog.csdn.net/xiaoxiaopengbo/article/details/51446171

3、Bluetooth RFCOMM介绍

https://www.cnblogs.com/hzl6255/p/3811013.html

4、如何查看Ubuntu 蓝牙bluez 软件版本

https://blog.csdn.net/u014778332/article/details/50663887

5、在Linux系统中使用蓝牙功能的基本方法

https://www.cnblogs.com/askDing/p/5111405.html

6、bluetooth开发（二）------基于rfcomm通信编程之服务器端

https://blog.csdn.net/wang_zheng_kai/article/details/23330329

7、python — 扫描蓝牙RFCOMM信道

https://blog.csdn.net/u012611644/article/details/79411369

8、Communicating with RFCOMM

https://people.csail.mit.edu/albert/bluez-intro/x232.html