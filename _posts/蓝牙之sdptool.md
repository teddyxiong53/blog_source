---
title: 蓝牙之sdptool
date: 2018-12-13 17:42:35
tags:
	- 蓝牙

---



先看看man手册是怎么说的。

**sdp就是设备发现协议。它的重点就是查询机器的信息。**

# sdp协议



**sdptool是控制和查询sdp server的。**

先用hcitool扫描一下附近的蓝牙设备。

```
teddy@teddy-ThinkPad-SL410:~$ sudo hcitool scan
Scanning ...
        44:66:FC:43:40:BC       n/a
        94:87:E0:A3:4F:4B       小米手机
        B4:0B:44:F4:16:8D       xhl_bt
```

xhl_bt就是我的手机。

用sdptool查询我的手机的蓝牙提供的服务。

```
teddy@teddy-ThinkPad-SL410:~$ sdptool browse B4:0B:44:F4:16:8D | grep "Service Name" 
Service Name: Headset Gateway
Service Name: Handsfree Gateway
Service Name: AV Remote Control Target
Service Name: Advanced Audio
Service Name: SIM Access
Service Name: OBEX Phonebook Access Server
Service Name: OBEX Object Push
```



在我的树莓派上安装obexfs。

```
sudo apt-get install obexfs
```



```
Services:                                                                 
        DID SP DUN LAN FAX OPUSH FTP PRINT HS HSAG HF HFAG SAP PBAP MAP   
        NAP GN PANU HCRP HID KEYB WIIMOTE CIP CTP A2SRC A2SNK AVRCT AVRTG 
        UDIUE UDITE SEMCHLA SR1 SYNCML SYNCMLSERV ACTIVESYNC HOTSYNC      
        PALMOS NOKID PCSUITE NFTP NSYNCML NGAGE APPLE IAP ISYNC GATT      
```



sdptool常用命令

B4:0B:44:F4:16:8D这个是我的手机的蓝牙地址。

1、查询指定地址的蓝牙设备的服务。板端执行下面的命令：

```
sdptool browse B4:0B:44:F4:16:8D
```

2、有些设备不支持browse，那么就可以用search来查询。

```
sdptool search --bdaddr B4:0B:44:F4:16:8D HFAG
```

3、查看自己提供的服务的情况。

```
sdptool browse local
```

4、添加A2SNK服务。

```
sdptool add A2SNK
```



# 问题

在rk3308上执行：sdptool browse local。

出错提示：

```
Failed to connect to SDP server on FF:FF:FF:00:00:00:
```

网上查了一下，说是需要用compatible模式来运行bluetoothd。

我恰好是手动启动bluetoothd，没有加上兼容模式的参数。

加上-C选项运行bluetoothd，果然好了。



# 参考资料

1、sdptool 设备服务查找命令使用

https://blog.csdn.net/u014778332/article/details/50654620

2、Bluetooth Hacks

https://www.linuxjournal.com/content/bluetooth-hacks

3、Failed to connect to SDP server on FF:FF:FF:00:00:00: Connection refused问题解决方法

https://blog.csdn.net/wang_shuai_ww/article/details/68927525

4、蓝牙SDP协议概述

https://www.cnblogs.com/libs-liu/p/9498952.html