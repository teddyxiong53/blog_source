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

# pydbus和dbus-python对比

`pydbus` 和 `dbus-python` 是两个用于与 D-Bus 交互的 Python 库，它们各有优缺点。以下是它们的对比：

### 1. **易用性**

- **pydbus**：
  - 更加简洁和直观，使用起来相对简单。
  - 支持通过简单的属性访问和方法调用来与 D-Bus 对象交互。

- **dbus-python**：
  - 功能强大，但 API 相对复杂，学习曲线较陡峭。
  - 需要更多的代码来实现相同的功能。

### 2. **功能**

- **pydbus**：
  - 提供了对 D-Bus 的高层次封装，适合快速开发和原型制作。
  - 支持异步调用，但不如 `dbus-python` 灵活。

- **dbus-python**：
  - 提供了更全面的功能，适合复杂的应用程序。
  - 支持信号处理、异步调用等高级功能。

### 3. **性能**

- **pydbus**：
  - 性能良好，但在某些高负载场景下可能不如 `dbus-python`。

- **dbus-python**：
  - 性能较高，适合对性能要求严格的应用。

### 4. **社区和支持**

- **pydbus**：
  - 社区活跃，文档相对完善，适合入门。

- **dbus-python**：
  - 更成熟，广泛使用于许多项目中，文档和示例丰富。

### 5. **适用场景**

- **pydbus**：
  - 适合快速开发、简单的 D-Bus 应用。

- **dbus-python**：
  - 适合需要复杂 D-Bus 交互的应用程序。

### 总结

选择哪个库取决于你的需求。如果你需要快速开发和简单的 API，可以选择 `pydbus`。如果你需要更强大的功能和灵活性，则可以考虑使用 `dbus-python`。

# dbus-python官方文档总结

## 连接到总线

有两种方式，一种是连接到session bus，一种是连接到systembus。

```python
import dbus
# session bus
session_bus = dbus.SessionBus()
# system bus
system_bus = dbus.SystemBus()
```

你在一个程序里可以同时连接两种bus。

## 进行method call

一个dbus应用程序可以导出对象给其他程序使用。

你要使用的话，需要知道：

* bus name。这个一般是泛域名的写法，就像java package那样的方式。
* object path。一个app可以导出多个object。例如一个文本处理程序，它可以导出一个表示程序本身的object，还可以导出针对每个文档的object，还可以为文本的每个段落导出object。要决定跟哪个对象进行交互，你就需要提供object path。这个path是以/ 切分的字符串。例如/document/123 这样。

你跟object交互的方式，就是调用object的method。

### proxy object

你要跟远程对象进行交互。

一个比较方式的方式是通过proxy object来进行。

通过proxy object来统一负责跟远程对象的交互。这样就比较清晰简单。

要拿到一个proxy object，需要调用bus的get_object方式。

举例：

```python
import dbus
bus = dbus.SystemBus()
proxy = bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager/Devices/eth0")
```

### interface & method

dbus使用interface来给method提供命名空间。

interface包含多个method和signal。

interface的名字也是反写域名的方式。后面会多跟一些内容。

例如：

```
org.freedesktop.NetworkManager.Devices
这个接口，有
getProperties 这个方法。
```

调用interface的方法是在proxy object上调用。

```python
import dbus
bus = SystemBus()
eth0 = bus.get_object('org.freedesktop.NetworkManager', '/org/freedesktop/NetworkManager/Devices/eth0')
props = eth0.getProperties(dbus_interface='org.freedesktop.NetworkManager.Devices')
```

有一种简便方法，就是通过dbus.Interface来构造一个interface对象。这样调用就可以少写一点代码。

```
eth0_dev_iface = dbus.Interface(eth0, dbus_interface='org.freedesktop.NetworkManager.Devices')
pros = eth0_dev_iface.getProperties()
```

### 数据类型

跟python不同，dbus是静态数据类型的。

每一个method都一个特性的签名字符串来表示参数的类型。

dbus有一个内省机制。

dbus-python使用它来发现正确的数据类型。

如果成功，python类型就会自动转换为dbus的类型。

如果失败，则触发TypeError。

| python类型                                                | dbus类型签名 | 说明 |
| --------------------------------------------------------- | ------------ | ---- |
| proxy object<br />dbus.Interface<br />dbus.service.Object | 'o'          |      |
| dbus.Boolean                                              | 'b'          |      |
| dbus.Byte                                                 | 'y'          |      |
| dbus.Int16                                                | 'n'          |      |
| dbus.UInt16                                               | 'q'          |      |
| dbus.Int32                                                | 'i'          |      |
| dbus.UInt32                                               | 'u'          |      |
| dbus.Int64                                                | x            |      |
| dbus.UInt64                                               | 't'          |      |
| dbus.Double                                               | 'd'          |      |
| dbus.ObjectPath                                           | 'o'          |      |
| dbus.Signature                                            | 'g'          |      |
| dbus.String                                               | 's'          |      |
| dbus.UTF8String                                           | 's'          |      |
| bool                                                      | 'b'          |      |

## async method call

异步方法调用运行多个method同时被调用。

并运行在等待结果的时候同时执行其他任务。

async的前提是有一个event loop。

### 设置event loop

dbus-python目前唯一支持的loop 是glib的loop。

有一个全局是默认主循环。

这个是最简单的使用方法。

方法是：

```python
from dbus.mainloop.glib import DBusMainLoop

DBusMainLoop(set_as_default=True) # 这一步应该在连接到dbus之前设置。
```

### 进行异步调用

就是要设置2个参数：

* reply_handler
* error_handler

作为成功时的处理和失败时的处理回调函数。

## signal处理

### signal matching

## export object

这个是当你想对外提供object的时候需要做的事情。

### 继承dbus.service.Object

### 使用dbus.service.method导出方法

### 使用dbus.service.signal导出信号



# 参考资料

1、DbusExamples

https://wiki.python.org/moin/DbusExamples

2、dbus-python tutorial

https://dbus.freedesktop.org/doc/dbus-python/tutorial.html