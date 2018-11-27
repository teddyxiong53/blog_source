---
title: 蓝牙之hciconfig
date: 2018-11-27 16:36:35
tags:
	- 蓝牙

---



bluez协议栈在安装完成后，会提供2个工具。

hcitool和gattool。

使用工具的前提是以root方式运行。

首先是查看当前有的蓝牙设备。

hciconfig，类似ifconfig。只是操作对象不是网卡，而是蓝牙设备而已。



```
root@raspberrypi:~# hciconfig 
hci0:   Type: BR/EDR  Bus: UART
        BD Address: B8:27:EB:AA:E4:60  ACL MTU: 1021:8  SCO MTU: 64:1
        UP RUNNING PSCAN 
        RX bytes:42850 acl:96 sco:0 events:805 errors:0
        TX bytes:8222 acl:96 sco:0 commands:208 errors:0
```

打开和关闭。

```
hciconfig hci0 down
hciconfig hci0 up
```

打开蓝牙设备后，就可以使用hcitool工具集对蓝牙进行控制。

工具集分为2部分，一个传统蓝牙的，一个是ble的。

