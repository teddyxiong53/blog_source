---
title: Python之树莓派蓝牙
date: 2018-11-28 09:54:05
tags:
	- 蓝牙

---

--

安装依赖库。

```
sudo apt-get install python-dev libbluetooth-dev
```

```
sudo pip install pybluez
```



```
import bluetooth
print("looking for nearby devices...")
nearby_devices = bluetooth.discover_devices(lookup_names = True)
print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
	print("%s-%s" % (addr,name))

def what_services(addr,name):
	print("%s-%s" % (addr,name))
	for services in bluetooth.find_service(address = addr):
		print("Name: %s" %(services["name"]))
		print("Description: %s" %(services["description"]))
		print("Protocol: %s" %(services["protocol"]))
		print("Provider: %s" %(services["provider"]))
		print("Port: %s" %(services["port"]))
		print("Service id: %s" %(services["service-id"]))
		print("")
		print("")

```



```
sudo pip install gattlib
```

安装出错，需要glib2.0的才行。

```
sudo apt-get install glib-2.0
sudo pip install --upgrade setuptools --user python
```

安装还是出错。错误是一样的。

看网上说，只能通过编译代码段方式来安装了。

# 蓝牙python开发有哪些包和工具可以使用

在Python中进行蓝牙开发时，有一些常用的包和工具可以帮助你进行蓝牙通信和开发，其中一些主要的包和工具包括：

1. **PyBluez**：PyBluez是Python的一个蓝牙库，提供了一系列用于蓝牙通信的API和工具。它支持蓝牙套接字编程、设备发现、连接建立等功能，是进行蓝牙开发的重要工具之一。

2. **lightblue**：lightblue是一个跨平台的Python蓝牙库，提供了一些简单易用的API和工具，用于进行蓝牙设备的发现、连接和数据传输等操作。

3. **bluepy**：bluepy是一个针对蓝牙低功耗（BLE）设备的Python库，它提供了一些用于BLE设备交互的API和工具，包括扫描设备、读写属性等功能。

4. **gattlib**：gattlib是一个用于BLE设备的Python库，它提供了一些高级的API和工具，用于进行BLE设备的发现、连接和数据交互等操作。

5. **bleak**：bleak是一个跨平台的Python库，用于与BLE设备进行通信。它提供了一些简单易用的API和工具，支持BLE设备的发现、连接和数据传输等功能。

这些包和工具提供了丰富的功能和灵活的接口，使得在Python中进行蓝牙开发变得更加方便和简单。根据你的具体需求和应用场景，可以选择合适的包和工具来进行开发。

# pybluez

代码：

https://github.com/pybluez/pybluez

文档：

https://pybluez.readthedocs.io/

已经停止开发了。

# bleak

代码：

https://github.com/hbldh/bleak

文档：

https://bleak.readthedocs.io/en/latest/

Bleak 是低功耗蓝牙平台 Agnostic Klient 的首字母缩写词。

Bleak 是一个 GATT 客户端软件，能够连接到充当 GATT 服务器的 BLE 设备。它旨在提供一个异步、跨平台的 Python API，用于连接和通信，例如传感器。

安装：

```
pip install bleak
```

Bleak 支持读取、写入和接收来自 GATT 服务器的通知，以及用于发现 BLE 设备的功能。



# lightblue



# 参考资料

1、树莓派3 基于Python的pybluez库查询蓝牙

https://blog.csdn.net/Billyran/article/details/60968358

2、pylgbst on RPI3 with Raspbian stretch 

https://github.com/undera/pylgbst/issues/10