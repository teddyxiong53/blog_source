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

作为Python dbus专家，我来为你详细比较`dbus-python`和`pydbus`，从功能、设计、使用场景、优缺点等多个方面进行分析，帮助你选择适合的工具。

---

### 1. **概述**
- **`dbus-python`**：
  - 是Python对D-Bus的官方绑定库，基于底层的libdbus（D-Bus的C实现）。
  - 历史较长，广泛用于早期的Linux桌面应用和系统编程。
  - 当前维护较少，最后一次主要更新在几年前。
- **`pydbus`**：
  - 是一个更现代的D-Bus绑定库，基于GLib和GObject（GIO库）的Python绑定。
  - 由社区驱动，设计更简洁，近年来更活跃。

---

### 2. **底层依赖**
- **`dbus-python`**：
  - 依赖libdbus（D-Bus的低级C库）。
  - 需要安装D-Bus开发库（例如`libdbus-1-dev`），编译时与C代码绑定。
  - 这使得它与D-Bus协议紧密耦合，但也增加了依赖复杂性。
- **`pydbus`**：
  - 依赖GLib和GObject（通过`python-gi`，即PyGObject）。
  - 不直接依赖libdbus，而是通过GLib的高级抽象与D-Bus交互。
  - 依赖更现代化，且与GNOME生态系统集成良好。

---

### 3. **安装**
- **`dbus-python`**：
  ```bash
  pip install dbus-python
  ```
  - 需要系统级的D-Bus支持，可能需要额外的开发包（例如`sudo apt install libdbus-1-dev`）。
  - 在非Linux系统（如Windows）上安装和使用较困难。
- **`pydbus`**：
  ```bash
  pip install pydbus
  ```
  - 需要安装PyGObject（`sudo apt install python3-gi`）。
  - 安装相对简单，但仍主要面向Linux环境。

---

### 4. **API设计**
- **`dbus-python`**：
  - API较为底层，偏向传统的D-Bus概念。
  - 使用`bus.get_object`获取代理对象，再通过`dbus.Interface`指定接口。
  - 示例：
    ```python
    import dbus
    bus = dbus.SessionBus()
    obj = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    interface = dbus.Interface(obj, 'org.freedesktop.Notifications')
    interface.Notify("App", 0, "", "Title", "Message", [], {}, 5000)
    ```
  - 代码较为冗长，手动管理接口。
- **`pydbus`**：
  - API更现代化，基于属性和方法的动态访问。
  - 支持Pythonic的调用方式，直接通过属性访问接口和方法。
  - 示例：
    ```python
    from pydbus import SessionBus
    bus = SessionBus()
    notifications = bus.get('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    notifications.Notify("App", 0, "", "Title", "Message", [], {}, 5000)
    ```
  - 更简洁，减少样板代码。

---

### 5. **功能对比**
| 功能         | `dbus-python`                       | `pydbus`                       |
| ------------ | ----------------------------------- | ------------------------------ |
| **方法调用** | 支持，通过代理对象和接口            | 支持，直接属性访问             |
| **信号监听** | 支持，需要手动添加信号接收器        | 支持，简化为订阅模式           |
| **服务发布** | 支持，但实现较复杂                  | 支持，API更直观                |
| **类型系统** | 强类型，需要手动处理D-Bus类型       | 自动类型转换，更Pythonic       |
| **错误处理** | 抛出`dbus.exceptions.DBusException` | 抛出标准Python异常             |
| **异步支持** | 无原生支持，需配合主循环            | 无原生支持，但与GLib循环集成好 |

- **信号监听示例**：
  - `dbus-python`：
    ```python
    def handle_signal(*args):
        print("信号:", args)
    bus.add_signal_receiver(handle_signal, signal_name="NotificationClosed", 
                            dbus_interface="org.freedesktop.Notifications")
    ```
  - `pydbus`：
    ```python
    def handle_signal(*args):
        print("信号:", args)
    notifications.NotificationClosed.connect(handle_signal)
    ```

---

### 6. **优点**
- **`dbus-python`**：
  - **官方支持**：作为D-Bus官方绑定，文档和兼容性有一定保障。
  - **广泛使用**：在许多遗留项目和系统中已有成熟应用。
  - **低级控制**：提供对D-Bus协议的细粒度控制。
- **`pydbus`**：
  - **简洁性**：API设计更符合Python习惯，代码更少。
  - **活跃维护**：社区更新频繁，修复bug和适配新系统的速度更快。
  - **集成性**：与GLib和GNOME生态兼容性更好。

---

### 7. **缺点**
- **`dbus-python`**：
  - **维护停滞**：近年来更新少，可能存在未修复的bug。
  - **复杂性**：API不够直观，学习曲线较陡。
  - **依赖问题**：对libdbus的依赖可能导致移植性问题。
- **`pydbus`**：
  - **依赖GLib**：需要额外的PyGObject支持，增加了依赖链。
  - **社区驱动**：不像`dbus-python`有官方背书，可能不够权威。
  - **功能限制**：某些低级D-Bus功能可能不如`dbus-python`全面。

---

### 8. **使用场景**
- **`dbus-python`**：
  - 适合需要与传统D-Bus服务深度集成的项目。
  - 适用于维护旧代码或与已有`dbus-python`项目协作。
  - 需要细粒度控制D-Bus协议的场景。
- **`pydbus`**：
  - 适合现代Python项目，尤其是追求简洁代码的开发者。
  - 与GNOME或GLib相关的桌面应用程序开发。
  - 新项目或快速原型开发。

---

### 9. **性能**
- **`dbus-python`**：由于直接绑定libdbus，性能略高，但差别不大。
- **`pydbus`**：通过GLib间接调用，性能稍有开销，但在大多数场景下影响可忽略。

---

### 10. **社区与文档**
- **`dbus-python`**：
  - 文档较全面，但更新较少。
  - 社区活跃度下降，问题可能得不到及时解答。
- **`pydbus`**：
  - 文档简洁但清晰，示例丰富。
  - GitHub上有活跃的社区支持。

---

### 11. **选择建议**
- 如果你在**维护旧项目**或需要与**传统Linux系统服务**深度交互，推荐使用`dbus-python`。
- 如果你在开发**新项目**，追求**简洁性和现代性**，或者与**GNOME生态**集成，推荐使用`pydbus`。
- 如果你需要**跨平台潜力**或**无C依赖**，可以考虑第三个选项`jeepney`（纯Python实现，但功能较新，未在此详细比较）。

---

### 总结
`dbus-python`是老牌选择，稳定但略显过时；`pydbus`是现代替代品，简洁且活跃。选择哪个主要取决于你的项目需求、团队熟悉度和维护性考虑。如果你有具体的使用场景或代码问题，我可以进一步提供针对性的建议和示例！有什么想深入探讨的吗？

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



# dbus.service.Object

作为Python dbus专家，我来为你详细讲解`dbus.service.Object`，它是`dbus-python`库中用于创建D-Bus服务的重要类。通过它，你可以在D-Bus总线上发布自己的服务，供其他应用程序调用方法或监听信号。

---

### 什么是`dbus.service.Object`？
`dbus.service.Object`是`dbus-python`提供的一个基类，用于定义和发布D-Bus服务对象。当你继承这个类并实现方法时，可以将其实例注册到D-Bus总线上，使其成为一个可供其他客户端访问的服务。

- **作用**：
  - 定义D-Bus对象的接口、方法和信号。
  - 将对象绑定到特定的总线名称（bus name）和对象路径（object path）。
- **使用场景**：
  - 创建自定义D-Bus服务，例如系统工具、桌面应用插件等。
  - 与其他进程通信，提供功能或广播事件。

---

### 核心概念
在使用`dbus.service.Object`之前，需要了解几个D-Bus相关概念：
1. **Bus Name**：服务的唯一名称（如`com.example.MyService`），标识总线上的服务。
2. **Object Path**：服务内对象的路径（如`/com/example/MyObject`），类似文件路径。
3. **Interface**：定义方法和信号的命名空间（如`com.example.MyInterface`）。
4. **Method**：客户端可以调用的函数。
5. **Signal**：服务可以广播的事件。

---

### 基本用法
以下是使用`dbus.service.Object`创建D-Bus服务的基本步骤：

#### 示例代码
```python
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

# 设置D-Bus主循环
DBusGMainLoop(set_as_default=True)

# 定义一个D-Bus服务对象
class MyService(dbus.service.Object):
    def __init__(self):
        # 连接到会话总线
        bus = dbus.SessionBus()
        # 请求一个总线名称
        bus_name = dbus.service.BusName('com.example.MyService', bus=bus)
        # 初始化对象并绑定到路径
        dbus.service.Object.__init__(self, bus_name, '/com/example/MyObject')

    # 定义一个方法
    @dbus.service.method('com.example.MyInterface', in_signature='s', out_signature='s')
    def Hello(self, name):
        return f"你好, {name}!"

    # 定义一个信号
    @dbus.service.signal('com.example.MyInterface', signature='s')
    def SignalEmitted(self, message):
        pass

# 启动服务
if __name__ == '__main__':
    # 创建服务实例
    service = MyService()

    # 模拟触发信号
    import time
    time.sleep(2)
    service.SignalEmitted("服务已启动")

    # 运行主循环
    loop = GLib.MainLoop()
    print("服务运行中...")
    loop.run()
```

#### 运行结果
- 服务启动后，其他D-Bus客户端可以通过`com.example.MyService`访问`/com/example/MyObject`对象。
- 客户端可以调用`Hello`方法，或监听`SignalEmitted`信号。

---

### 工作原理
1. **继承`dbus.service.Object`**：
   - 你需要创建一个类，继承`dbus.service.Object`，并在`__init__`中调用父类的初始化方法。
   - 初始化时指定总线名称（`BusName`）和对象路径。

2. **注册服务**：
   - `dbus.service.BusName`请求一个总线名称，将服务注册到D-Bus总线上。
   - 如果名称已被占用，会抛出异常（除非设置`replace_existing=True`）。

3. **定义方法**：
   - 使用`@dbus.service.method`装饰器定义可调用的方法。
   - 参数：
     - `dbus_interface`：接口名称。
     - `in_signature`：输入参数的D-Bus类型签名（如`s`表示字符串）。
     - `out_signature`：返回值类型签名。

4. **定义信号**：
   - 使用`@dbus.service.signal`装饰器定义信号。
   - 参数：
     - `dbus_interface`：接口名称。
     - `signature`：信号参数的类型签名。
   - 调用信号方法时，会向总线广播事件。

5. **主循环**：
   - D-Bus服务需要事件循环（如GLib的`MainLoop`）来处理传入的请求和信号。

---

### 测试服务
你可以用`dbus-send`命令行工具测试服务：
```bash
# 调用方法
dbus-send --session --type=method_call --print-reply \
  --dest=com.example.MyService \
  /com/example/MyObject \
  com.example.MyInterface.Hello \
  string:"Alice"
```
输出类似：
```
method return time=... sender=... -> ... reply_serial=...
   string "你好, Alice!"
```

监听信号可以用`dbus-monitor`：
```bash
dbus-monitor "interface='com.example.MyInterface'"
```

---

### 类型签名（Signature）
D-Bus使用类型签名来定义参数和返回值类型，常见类型包括：
- `s`：字符串
- `i`：整数
- `b`：布尔值
- `a{sv}`：字典（键为字符串，值为任意类型）
- `(ss)`：元组（两个字符串）

例如：
```python
@dbus.service.method('com.example.MyInterface', in_signature='is', out_signature='b')
def CheckAge(self, name, age):
    return age >= 18
```

---

### 注意事项
1. **总线选择**：
   - `SessionBus`用于用户会话，`SystemBus`用于系统服务。
   - 系统总线可能需要权限配置（如`/etc/dbus-1/system.d/`）。
2. **异常处理**：
   - 方法中抛出的异常会通过D-Bus返回给客户端。
   - 示例：
     ```python
     @dbus.service.method('com.example.MyInterface')
     def RaiseError(self):
         raise ValueError("出错了")
     ```
3. **线程安全**：
   - 默认情况下，`dbus-python`不是线程安全的，建议在主线程运行服务。
4. **信号触发**：
   - 调用信号方法（如`SignalEmitted`）会立即广播，不需要客户端显式订阅。

---

### 与`pydbus`的对比
`pydbus`也支持服务发布，API更简洁：
```python
from pydbus import SessionBus
from gi.repository import GLib

class MyService:
    dbus = """
    <node>
        <interface name='com.example.MyInterface'>
            <method name='Hello'>
                <arg type='s' name='name' direction='in'/>
                <arg type='s' name='result' direction='out'/>
            </method>
            <signal name='SignalEmitted'>
                <arg type='s' name='message'/>
            </signal>
        </interface>
    </node>
    """
    def Hello(self, name):
        return f"你好, {name}!"
    def SignalEmitted(self, message):
        pass  # 信号由publish触发

bus = SessionBus()
bus.publish('com.example.MyService', ('/com/example/MyObject', MyService()))
GLib.MainLoop().run()
```
- **区别**：`pydbus`使用XML定义接口，方法和信号更直观，但需要额外依赖PyGObject。

---

### 总结
`dbus.service.Object`是`dbus-python`中创建D-Bus服务的核心工具，通过继承它并使用装饰器，你可以轻松定义方法和信号。它适合需要低级控制或与传统D-Bus系统集成的场景。如果你有具体需求（例如实现复杂服务、调试方法），可以告诉我，我会提供更详细的指导！有什么问题吗？

# 参考资料

1、DbusExamples

https://wiki.python.org/moin/DbusExamples

2、dbus-python tutorial

https://dbus.freedesktop.org/doc/dbus-python/tutorial.html