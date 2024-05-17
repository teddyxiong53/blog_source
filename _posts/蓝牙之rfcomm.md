---
title: 蓝牙之rfcomm
date: 2018-11-27 14:59:35
tags:
	- 蓝牙

---

--

经典蓝牙中的数据传输协议是串行仿真协议RFCOMM。

RFCOMM仿真了常见的串口连接。

数据从一端输入，从另一端取出。

经典蓝牙的开发非常简单。

基于串口开发的有线键鼠程序，就可以直接用于RFCOMM连接的无线键鼠。

此外，经典蓝牙可以快速传输数据。

因此，诺基亚N95这样的早期智能手机，也用RFCOMM来互传图片和文件。





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
    rfcommCon('00:1A:7D:DA:71:13',port)
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

bd_addr = "00:1A:7D:DA:71:13 "
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))
sock.send("hello,bt")
sock.close()
```

把上面的程序在我的笔记本上运行。

先安装pybluez。出错了。

```
    bluez/btmodule.h:5:33: fatal error: bluetooth/bluetooth.h: 没有那个文件或目录
    compilation terminated.
    error: command 'i686-linux-gnu-gcc' failed with exit status 1
```

需要安装这个。

```
sudo apt-get install libbluetooth-dev
```

现在server.py运行正常。

但是client.py运行有问题。

```
bluetooth.btcommon.BluetoothError: (113, 'No route to host')
```

我的蓝牙地址就是本机的蓝牙地址。

sudo运行也是一样的错误。



https://bluez-users.narkive.com/6Yl3DOn6/rfcomm-gives-no-route-to-host

这里有个回答说，

```
you can't connect to yourself. This is not possible with Bluetooth.

src = 00:80:37:25:B7:DB	(hci0)
dst = 00:80:37:25:B7:DB (rfcomm0)
```

蓝牙不能连接到自己？



rfcomm的端口号是1到30 。



# 问题

我sdptool add SP之后。没有报错。sdptool browse local也可以看到Serial Port。但是没有生成/dev/rfcomm0这样的设备节点。

在rk3308的板子上，和我的笔记本上（用usb蓝牙）。都是这样的现象。

实际上，是我的操作不对。

设备节点是通过rfcomm bind产生的。

```
scan on
devices
pair XX:XX:XX:XX:XX:XX
trust XX:XX:XX:XX:XX:XX
quit
```

```
sudo rfcomm bind /dev/rfcomm0 XX:XX:XX:XX:XX:XX 1
```

现在可以进行连接了。但是手机这边用蓝牙spp调试助手，一连接，板端这边就出错退出了。

```
root@thinkpad:~# rfcomm bind /dev/rfcomm0 08:D4:6A:78:68:D7 
root@thinkpad:~# rfcomm -h^C
root@thinkpad:~# rfcomm listen /dev/rfcomm0
Waiting for connection on channel 1
Can't create RFCOMM TTY: Address already in use
```



# btstack里的实现

spp_counter这个例子。运行正常。

效果是：Ubuntu上运行spp_counter，手机打开蓝牙spp这个app，连接到电脑。然后电脑这边每秒向手机通过rfcomm发送一个自增的计数值。

看spp_counter的代码。

```
To provide an SPP service, the L2CAP, RFCOMM, and SDP protocol layers 
are required. After setting up an RFCOMM service with channel nubmer
RFCOMM_SERVER_CHANNEL, an SDP record is created and registered with the SDP server.
```

要提供一个spp服务，需要L2CAP，RFCOMM，SDP这3个层被初始化。

表现在代码里，就是：

```
l2cap_init();

    rfcomm_init();
    rfcomm_register_service(packet_handler, RFCOMM_SERVER_CHANNEL, 0xffff);  // reserved channel, mtu limited by l2cap

    // init SDP, create record for SPP and register with SDP
    sdp_init();
```

# bluez-alsa里的rfcomm

这个是用来控制hfp和hsp的。

传输AT指令的。



# 参考资料

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

9、

http://pages.iu.edu/~rwisman/c490/html/pythonandbluetooth.htm

10、rfcomm工具的使用方法 创建/dev/rfcomm0 并检测

https://blog.csdn.net/wang_shuai_ww/article/details/68944430

11、Using /dev/rfcomm0 in raspberry pi

https://raspberrypi.stackexchange.com/questions/78155/using-dev-rfcomm0-in-raspberry-pi

12、Ubuntu14.04 蓝牙适配器的连接

https://www.cnblogs.com/li-yao7758258/p/5577401.html



https://www.cnblogs.com/vamei/p/6753531.html