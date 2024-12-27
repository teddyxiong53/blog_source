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



# bluez rfcomm命令用法

把板端作为rfcomm 服务端，让手机上的rfcomm客户端连接过去

要在板子上使用BlueZ的`rfcomm`命令创建一个RFCOMM服务器，并让手机作为RFCOMM客户端连接，下面是详细的步骤和示例：

### 步骤1：配置蓝牙设备

确保蓝牙适配器已启用并处于可发现模式：

```sh
sudo hciconfig hci0 up
sudo hciconfig hci0 piscan
```

### 步骤2：创建RFCOMM服务

使用`rfcomm`命令创建一个RFCOMM服务器。这可以通过以下步骤完成：

1. **启动`bluetoothd`守护进程**：
    确保`bluetoothd`正在运行，可以通过以下命令启动：

    ```sh
    sudo systemctl start bluetooth
    ```

2. **创建RFCOMM服务**：

    使用`sdptool`添加一个RFCOMM通道。这里我们将服务名称设为`rfcomm-server`，并使用通道1：

    ```sh
    sudo sdptool add --channel=1 SP
    ```

3. **启动RFCOMM服务器**：

    使用`rfcomm`命令在指定的通道上绑定RFCOMM服务器：

    ```sh
    sudo rfcomm listen /dev/rfcomm0 1
    ```

### 步骤3：配置手机连接

确保手机的蓝牙已启用，并且可以发现你的蓝牙设备。然后使用一个支持RFCOMM连接的应用程序（如`BlueTerm`或自定义的应用）来连接到蓝牙设备的RFCOMM服务器。

### 示例：完整过程

以下是一个完整的过程示例：

1. **在板子上执行以下命令**：

    ```sh
    sudo hciconfig hci0 up
    sudo hciconfig hci0 piscan
    sudo sdptool add --channel=1 SP
    sudo rfcomm listen /dev/rfcomm0 1
    ```

2. **在手机上**：

    - 打开蓝牙并搜索设备。
    - 找到并连接到板子的蓝牙设备。
    - 使用RFCOMM客户端应用程序（如`BlueTerm`）连接到通道1。
    - 连接成功后，你应该能够在手机和板子之间进行数据传输。

### 注意事项

- **权限**：某些命令可能需要root权限，确保你以`sudo`运行。
- **兼容性**：确保你的设备和手机支持RFCOMM协议。
- **调试**：如果遇到连接问题，可以查看板子的系统日志以获取更多信息：

    ```sh
    sudo journalctl -u bluetooth -f
    ```

### 小结

以下是一个表格，总结了关键步骤和命令：

| 步骤             | 命令                                |
| ---------------- | ----------------------------------- |
| 启用蓝牙适配器   | `sudo hciconfig hci0 up`            |
| 设置蓝牙可发现   | `sudo hciconfig hci0 piscan`        |
| 添加RFCOMM服务   | `sudo sdptool add --channel=1 SP`   |
| 启动RFCOMM服务器 | `sudo rfcomm listen /dev/rfcomm0 1` |

通过这些步骤和命令，你可以成功地将板子设置为RFCOMM服务器，并让手机连接到它，从而实现数据通信。

# 通道

在蓝牙协议栈中，RFCOMM 是一个模拟串口通信的协议层，用于实现设备间的点对点通信。RFCOMM 通道（Channel）是蓝牙设备之间建立通信的重要资源，因为只有 1 到 31 的有限数量。为了避免设备间通信发生冲突，蓝牙标准和社区对这些通道进行了预分配，绑定了常见的蓝牙功能或服务（Profile）。

### 关键解释：

1. **有限性**：RFCOMM 通道范围为 1-31，每个通道都能承载一个服务。因此，为避免服务冲突，对常见服务预分配了固定通道号。
2. **服务和通道对应关系**：服务（Profile）表示蓝牙设备提供的功能，例如传输数据、访问电话簿、文件传输等。分配的通道号保证这些功能在设备间能快速且一致地发现和使用。

### 常见服务及通道分配：

| **Profile**       | **Channel** | **描述**                                                     |
| ----------------- | ----------- | ------------------------------------------------------------ |
| **DUN**           | 1           | Dial-Up Networking，用于调制解调器拨号网络。                 |
| **SPP**           | 3           | Serial Port Profile，用于仿真串口的无线数据通信。            |
| **HSP HS**        | 6           | Headset Profile (Headset Side)，耳机侧的通道，用于音频通信。 |
| **HFP HF**        | 7           | Hands-Free Profile (Hands-Free Side)，免提设备的通道。       |
| **OPP**           | 9           | Object Push Profile，用于推送对象（如名片或图片）。          |
| **FTP**           | 10          | File Transfer Profile，用于文件传输。                        |
| **BIP**           | 11          | Basic Imaging Profile，用于图片传输。                        |
| **HSP AG**        | 12          | Headset Profile (Audio Gateway Side)，音频网关侧的通道。     |
| **HFP AG**        | 13          | Hands-Free Profile (Audio Gateway Side)，音频网关的通道。    |
| **SYNCH (IrMC)**  | 14          | Synchronization Profile，用于同步（如联系人）。              |
| **PBAP**          | 15          | Phone Book Access Profile，用于访问电话簿。                  |
| **MAP MAS**       | 16          | Message Access Profile (Message Access Server)，消息访问服务端。 |
| **MAP MNS**       | 17          | Message Access Profile (Message Notification Server)，消息通知端。 |
| **SyncEvolution** | 19          | Linux SyncEvolution工具专用，用于同步。                      |
| **PC/Ovi Suite**  | 24          | 用于PC套件或Nokia Ovi Suite。                                |
| **SyncML Client** | 25          | SyncML协议客户端，用于数据同步。                             |
| **SyncML Server** | 26          | SyncML协议服务端，用于数据同步。                             |

### 使用场景：

设备需要实现某种服务时，会在 SDP（服务发现协议）中注册对应通道号，客户端通过 SDP 查询服务时，能快速定位服务对应的 RFCOMM 通道号。

### 注意事项：

- 如果设备需要自定义服务，必须选择未被预分配的通道号。
- 某些情况下，服务可能动态分配通道，但需避免与上述通道冲突。

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