---
title: Python之dbus操作
date: 2020-06-16 13:46:49
tags:
	- python

---

--

# Python的dbus包说明

https://pypi.org/project/dbus-python/

dbus-python 是 dbus 的原始 Python 绑定，是 D-Bus 协议的参考实现。

下面是关于Python的`dbus`包的一些简要说明：

| 功能           | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| 连接到DBus会话 | 使用`dbus.SessionBus()`方法连接到当前用户的DBus会话总线。    |
| 连接到系统DBus | 使用`dbus.SystemBus()`方法连接到系统DBus总线。               |
| 发送消息       | 使用`bus.get_object()`方法获取要调用的对象，然后使用其方法发送消息。 |
| 接收消息       | 使用`bus.add_signal_receiver()`方法注册信号接收器，以便在接收到指定信号时触发回调函数。 |
| 导出对象       | 使用`dbus.service.Object`类创建DBus服务对象，并通过`export()`方法将其导出。 |
| 调用方法       | 通过获取DBus对象并调用其方法来调用其他应用程序的DBus方法。   |

你可以在一个程序里同时连接SessionBus和SystemBus。

这个是自由的。

为了进行连接并进行方法调用，你需要这些东西：

1、bus名字。也就是你要连接的应用。是一个反写的域名。典型的例如org.bluez。表示你要跟bluez通信。

2、object path。在bluez里有很多个对象你可以进行通信的，例如Device、MediaPlayer，所以你需要指定你想跟谁进行通信。这个是用斜杠划分的。



代理对象

你想要跟远程对象通信的时候，你可以使用代理对象，代理对象就是远程对象的替身。你跟它说话，就等价于跟远程对象说话。

怎么拿到一个远程对象的代理？这样：

```
bus = dbus.SystemBus()
proxy = bus.get_object('org.bluez', '/xx/yy')
```

这里的proxy的类型是：dbus.proxies.ProxyObject

dbus这里的接口和方法的关系：

就类似面向对象编程里的接口和方法的关系：接口是给方法提供命名空间的。

接口里包括了方法和信号。

接口跟path有点像，只是写法是点分反写域名的方式。

接口举例：org.freedesktop.NetworkManager.Devices，它里面有个方法getProperties。

调用接口上的方法：

```
dbus = dbus.SystemBus()
eth0 = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Devices/eth0")
props = eth.getProperties(dbus_interface='org.freedesktop.NetworkManger.Devices')
```

可以看到，上面的写法是有些繁琐的。

有个快捷方式的写法：

就是使用同一个接口调用多个方法，可以构造一个dbus.Interface对象。

然后直接在这个接口对象上调用方法，而不用多次指定。

如下：

```
dbus = dbus.SystemBus()
eth0 = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Devices/eth0")
eth0_dev_iface = dbus.Interface(eth0, dbus_interface='org.freedesktop.NetworkManger.Devices')
props = eth0_dev_iface.getProperties()
```

## 进行异步方法调用

异步调用首先需要一个事件循环。

dbus-python当前唯一支持的事件循环是GLib的。

```
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_de)
```



https://dbus.freedesktop.org/doc/dbus-python/tutorial.html

# 客户端和服务器的例子

好的，下面是一个简单的示例，演示了如何创建一个DBus服务器和一个DBus客户端进行通信。

**DBus服务器端：**

```python
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
import gobject

class ExampleService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('com.example.ExampleService', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/com/example/ExampleService')

    @dbus.service.method('com.example.ExampleService', in_signature='s', out_signature='s')
    def Echo(self, message):
        print("Server received:", message)
        return "Echo from server: " + message

DBusGMainLoop(set_as_default=True)
loop = gobject.MainLoop()
ExampleService()
loop.run()
```

**DBus客户端：**

```python
import dbus

session_bus = dbus.SessionBus()
remote_object = session_bus.get_object('com.example.ExampleService', '/com/example/ExampleService')
interface = dbus.Interface(remote_object, 'com.example.ExampleService')

response = interface.Echo('Hello from client!')
print("Client received:", response)
```

这个示例中，DBus服务器定义了一个服务名为`com.example.ExampleService`，对象路径为`/com/example/ExampleService`。服务器端提供了一个名为`Echo`的方法，该方法接收一个字符串参数并返回相同的字符串前缀加上一段特定文本。DBus客户端连接到了相同的服务名和对象路径，并调用了服务器端的`Echo`方法，然后打印出返回的结果。

要运行这个示例，您需要确保已经安装了DBus，并且安装了Python的`dbus-python`库。





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



# 参考资料

1、DbusExamples

https://wiki.python.org/moin/DbusExamples

2、dbus-python tutorial

https://dbus.freedesktop.org/doc/dbus-python/tutorial.html