---
title: Python之树莓派蓝牙
date: 2018-11-28 09:54:05
tags:
	- 蓝牙

---



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



参考资料

1、树莓派3 基于Python的pybluez库查询蓝牙

https://blog.csdn.net/Billyran/article/details/60968358

2、pylgbst on RPI3 with Raspbian stretch 

https://github.com/undera/pylgbst/issues/10