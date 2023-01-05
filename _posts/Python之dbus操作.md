---
title: Python之dbus操作
date: 2020-06-16 13:46:49
tags:
	- python

---

--

看bluez/test下面的测试脚本，这个是最好的学习材料。

用python2来执行下面的脚本。

```
#coding:utf-8
from __future__ import print_function
import dbus
bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.freedesktop.DBus.ObjectManager")

objects = manager.GetManagedObjects()

# 这个是一个字典
#print(objects)
all_devices = []

for path, interfaces in objects.iteritems():
    if "org.bluez.Device1" in interfaces.keys():
        all_devices.append(str(path))

print(all_devices)

```



参考资料

1、DbusExamples

https://wiki.python.org/moin/DbusExamples

2、dbus-python tutorial

https://dbus.freedesktop.org/doc/dbus-python/tutorial.html