---
title: 蓝牙之sdptool
date: 2018-12-13 17:42:35
tags:
	- 蓝牙

---



先看看man手册是怎么说的。

sdptool是控制和查询sdp server的。

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



# 参考资料

1、sdptool 设备服务查找命令使用

https://blog.csdn.net/u014778332/article/details/50654620

2、Bluetooth Hacks

https://www.linuxjournal.com/content/bluetooth-hacks