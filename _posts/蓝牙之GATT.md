---
title: 蓝牙之GATT
date: 2018-12-13 16:33:35
tags:
	- 蓝牙

---

--

在BLE中，GATT客户端发现服务端服务的过程与经典蓝牙不同，

经典蓝牙会有专门的SDP协议来完成。

==而BLE中，这个过程会直接在GATT层完成。==

直接在GATT层完成服务和特征的发现。



看ble，就看到GATT这个东西，GATT和ble是什么关系？

什么是GATT？

**GATT是在蓝牙连接的基础上，收发很短小的数据段的规范。**这些短小的数据段，被称为属性（Attribute）。

要讨论GATT，需要先看看GAP的概念。

**GAP是所有蓝牙设备都必须有的。**

**GATT是ble设备特有的。**

GATT有服务端和客户端这2种角色。

ATT协议为所有基于ble link的应用提供了一个底层的框架。

ATT协议对应GATT profile。

GATT profile定义地更加具体。

1、一组通用的att类型。例如primary service（基础服务）、secondary service（二级服务）。

# GATT和ATT是什么关系？

蓝牙4.0引入了2个核心协议：GATT和ATT。

GATT是Generic ATTribute protocol。

ATT是ATTribute protocol。

GATT基于ATT。

**所有的ble profile一定是基于GATT。**

也就是说所有的ble服务都是用**ATT作为应用协议。**

GATT 就是使用了 ATT（Attribute Protocol）协议，ATT 协议把 Service, Characteristic遗迹对应的数据保存在一个查找表中，查找表使用 16 bit ID 作为每一项的索引。

一旦两个设备建立起了连接，GATT 就开始起作用了，这也意味着，你必需完成前面的 GAP 协议。这里需要说明的是，GATT 连接，必需先经过 GAP 协议。

GATT 连接需要特别注意的是：**GATT 连接是独占的**。也就是一个 BLE 外设同时只能被一个中心设备连接。一旦外设被连接，它就会马上停止广播，这样它就对其他设备不可见了。当设备断开，它又开始广播。



==中心设备和外设需要双向通信的话，唯一的方式就是建立 GATT 连接。==

GATT 通信的双方是 C/S 关系。外设作为 GATT 服务端（Server），它维持了 ATT 的查找表以及 service 和 characteristic 的定义。中心设备是 GATT 客户端（Client），它向 Server 发起请求。需要注意的是，所有的通信事件，都是由客户端（也叫主设备，Master）发起，并且接收服务端（也叫从设备，Slave）的响应。



Service 是把数据分成一个个的独立逻辑项，它包含一个或者多个 Characteristic。每个 Service 有一个 UUID 唯一标识。 UUID 有 16 bit 的，或者 128 bit 的。**16 bit 的 UUID 是官方通过认证的，需要花钱购买**，128 bit 是自定义的，这个就可以自己随便设置。

在 GATT 事务中的最低界别的是 Characteristic，Characteristic 是最小的逻辑数据单元，当然它可能包含一个组关联的数据，例如加速度计的 X/Y/Z 三轴值。



与 Service 类似，每个 Characteristic 用 16 bit 或者 128 bit 的 UUID 唯一标识。你可以免费使用 Bluetooth SIG 官方定义的[标准 Characteristic](https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicsHome.aspx)，使用官方定义的，可以确保 BLE 的软件和硬件能相互理解。当然，你可以自定义 Characteristic，这样的话，就只有你自己的软件和外设能够相互理解。



实际上，和 BLE 外设打交道，主要是通过 Characteristic。

你可以从 Characteristic 读取数据，也可以往 Characteristic 写数据。

这样就实现了双向的通信。

**所以你可以自己实现一个类似串口（UART）的 Sevice，这个 Service 中包含两个 Characteristic，一个被配置只读的通道（RX），另一个配置为只写的通道（TX）。**



# GAP

GAP是Generic Access Profile的缩写。

**GAP用来控制设备连接和广播。决定了你的设备是否可以跟其他设备交互，以及怎样交互。**

例如Beacon设备，就只能向外发送广播，不支持连接。

## 设备角色

GAP给设备分配了角色，主要就2个：

1、外围设备。例如手环。

2、中心设备。例如手机。

## 广播数据

外围设备通过两种方式向外广播数据：

1、广播数据。Advertising Data Payload。

2、扫描回复。Scan Response Data Payload。

第一种是必须的，因为外围设备必须不停地向外广播，让中心设备知道它存在。

扫描回复是可选的。是由中心设备发起。

广播间隔越长越省电。

# GATT

讨论了GAP之后，我们回到GATT 的主题上来。

GATT可以叫做普通属性协议。

它规定了2个ble设备，通过两种机制进行通信：

1、Service。

2、Characteristic。

一旦2个设备建立了连接，GATT就开始起作用了。

**GATT是独占的。ble设备连接后，就停止广播了。其他设备就看不到它了。**





# HRP

以HRP这个为例，心率profile。

文档20页左右。描述还比较简单。

## 配置

定义了2个角色：sensor和collector。

sensor相当于server，collector相当于client。

这个只能在ble传输层上走。





**GATT层是真正传输数据所在的层。**

一个GATT 服务器通过**一个属性表的表格来组织数据。**

一个属性包括：

1、句柄。属性在GATT表里的索引。

2、uuid（类型）

3、值。



# gatt_server和gatt_client实现举例

我将以BlueZ专家的身份，为您详细讲解如何基于BlueZ使用Python实现一个GATT Server和对应的GATT Client。我会从原理开始，然后描述交互流程，最后提供具体的代码实现。

---

### 原理

BlueZ是Linux上用于处理Bluetooth协议栈的开源框架，支持低功耗蓝牙（BLE）的GATT（Generic Attribute Profile）。GATT是BLE的核心，用于定义设备之间的数据交换方式。

- **GATT Server**: 提供服务（Services）和特性（Characteristics），存储数据并响应客户端的请求（如读写操作）。
- **GATT Client**: 连接到GATT Server，发现服务和特性，并与之交互（如读取或写入数据）。

在BlueZ中，GATT Server通过D-Bus接口实现，Python可以通过`dbus-python`库与BlueZ交互。GATT Client则通过扫描、连接和操作远程设备的特性来完成通信。

---

### 交互流程

1. **GATT Server端**:
   - 注册一个应用程序（Application），包含服务（Service）、特性（Characteristic）和描述符（Descriptor）。
   - 通过BlueZ的D-Bus接口发布服务。
   - 等待客户端连接并处理读/写请求。

2. **GATT Client端**:
   - 扫描附近的BLE设备，找到目标设备（通过服务UUID或设备地址）。
   - 连接到目标设备，发现其服务和特性。
   - 对特性执行读/写操作。

3. **交互示例**:
   - Client扫描并连接到Server。
   - Client读取Server的某个特性值。
   - Client写入数据到Server的某个特性，Server处理并返回响应。

---

### Python代码实现

以下是基于BlueZ的GATT Server和GATT Client的Python实现示例。假设我们创建一个简单的服务，包含一个可读写的特性，用于传输字符串数据。

#### 前置条件
- 确保系统安装了BlueZ（`sudo apt install bluez`）。
- 安装Python依赖：`pip install dbus-python pybluez`。
- 示例需要root权限运行（如`sudo`），因为BlueZ需要访问Bluetooth设备。

---

#### GATT Server代码

```python
import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

# GATT相关常量
GATT_MANAGER_IFACE = "org.bluez.GattManager1"
GATT_SERVICE_IFACE = "org.bluez.GattService1"
GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"

# UUIDs
SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

class Characteristic(dbus.service.Object):
    def __init__(self, bus, index, service):
        self.path = f"/org/bluez/example/service{index}/char0"
        dbus.service.Object.__init__(self, bus, self.path)
        self.bus = bus
        self.service = service
        self.value = bytearray("Hello, GATT!".encode("utf-8"))

    @dbus.service.method(GATT_CHRC_IFACE, in_signature="", out_signature="ay")
    def ReadValue(self, options):
        print("ReadValue called")
        return self.value

    @dbus.service.method(GATT_CHRC_IFACE, in_signature="ay", out_signature="")
    def WriteValue(self, value, options):
        print(f"WriteValue called with: {value}")
        self.value = value

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature="ss", out_signature="v")
    def Get(self, interface, prop):
        if prop == "UUID":
            return CHAR_UUID
        elif prop == "Service":
            return self.service.path
        elif prop == "Flags":
            return ["read", "write"]
        return None

class Service(dbus.service.Object):
    def __init__(self, bus, index):
        self.path = f"/org/bluez/example/service{index}"
        dbus.service.Object.__init__(self, bus, self.path)
        self.bus = bus
        self.characteristics = []

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature="ss", out_signature="v")
    def Get(self, interface, prop):
        if prop == "UUID":
            return SERVICE_UUID
        return None

class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = "/"
        dbus.service.Object.__init__(self, bus, self.path)
        self.services = []

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(dbus.INTROSPECTABLE_IFACE, out_signature="s")
    def Introspect(self):
        return ""

def register_app_cb():
    print("GATT application registered")

def register_app_error_cb(error):
    print(f"Failed to register application: {error}")
    mainloop.quit()

def main():
    global mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    # 创建服务和特性
    app = Application(bus)
    service = Service(bus, 0)
    char = Characteristic(bus, 0, service)
    service.characteristics.append(char)
    app.add_service(service)

    # 获取GATT Manager
    adapter = bus.get_object("org.bluez", "/org/bluez/hci0")
    gatt_manager = dbus.Interface(adapter, GATT_MANAGER_IFACE)

    # 注册应用程序
    mainloop = GLib.MainLoop()
    gatt_manager.RegisterApplication(
        app.path,
        {},
        reply_handler=register_app_cb,
        error_handler=register_app_error_cb
    )

    print("GATT Server running...")
    mainloop.run()

if __name__ == "__main__":
    main()
```

**说明**:
- 定义了一个服务（UUID: `SERVICE_UUID`）和一个特性（UUID: `CHAR_UUID`）。
- 特性支持读写操作，初始值为`"Hello, GATT!"`。
- 通过D-Bus将服务注册到BlueZ。

运行方法：`sudo python3 gatt_server.py`

---

#### GATT Client代码

```python
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import time

# BlueZ相关常量
ADAPTER_IFACE = "org.bluez.Adapter1"
DEVICE_IFACE = "org.bluez.Device1"
GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHAR_UUID = "12345678-1234-5678-1234-56789abcdef1"

class GattClient:
    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.mainloop = GLib.MainLoop()
        self.device_path = None
        self.char_path = None

    def find_device(self):
        adapter = self.bus.get_object("org.bluez", "/org/bluez/hci0")
        adapter_iface = dbus.Interface(adapter, ADAPTER_IFACE)
        adapter_iface.StartDiscovery()

        print("Scanning for devices...")
        time.sleep(5)  # 扫描5秒

        objects = self.bus.get_object("org.bluez", "/").GetManagedObjects(
            dbus_interface="org.freedesktop.DBus.ObjectManager"
        )

        for path, interfaces in objects.items():
            if DEVICE_IFACE in interfaces:
                device = self.bus.get_object("org.bluez", path)
                props = dbus.Interface(device, "org.freedesktop.DBus.Properties")
                uuids = props.Get(DEVICE_IFACE, "UUIDs")
                if SERVICE_UUID in uuids:
                    self.device_path = path
                    print(f"Found device: {path}")
                    break

        adapter_iface.StopDiscovery()
        if not self.device_path:
            print("Target device not found")
            exit(1)

    def connect_device(self):
        device = self.bus.get_object("org.bluez", self.device_path)
        device_iface = dbus.Interface(device, DEVICE_IFACE)
        device_iface.Connect()
        print("Connecting to device...")
        time.sleep(2)  # 等待连接完成

    def find_characteristic(self):
        objects = self.bus.get_object("org.bluez", "/").GetManagedObjects(
            dbus_interface="org.freedesktop.DBus.ObjectManager"
        )
        for path, interfaces in objects.items():
            if GATT_CHRC_IFACE in interfaces and path.startswith(self.device_path):
                props = interfaces[GATT_CHRC_IFACE]
                if props["UUID"] == CHAR_UUID:
                    self.char_path = path
                    print(f"Found characteristic: {path}")
                    break

        if not self.char_path:
            print("Target characteristic not found")
            exit(1)

    def read_value(self):
        char = self.bus.get_object("org.bluez", self.char_path)
        char_iface = dbus.Interface(char, GATT_CHRC_IFACE)
        value = char_iface.ReadValue({})
        print(f"Read value: {bytes(value).decode('utf-8')}")

    def write_value(self, value):
        char = self.bus.get_object("org.bluez", self.char_path)
        char_iface = dbus.Interface(char, GATT_CHRC_IFACE)
        char_iface.WriteValue(value.encode("utf-8"), {})
        print(f"Wrote value: {value}")

    def run(self):
        self.find_device()
        self.connect_device()
        self.find_characteristic()
        self.read_value()
        self.write_value("Hello from Client!")
        time.sleep(1)
        self.read_value()
        self.mainloop.run()

if __name__ == "__main__":
    client = GattClient()
    client.run()
```

**说明**:
- 扫描设备并找到提供目标服务的设备。
- 连接后查找目标特性，并执行读写操作。
- 写入`"Hello from Client!"`后再次读取验证。

运行方法：`sudo python3 gatt_client.py`

---

### 测试步骤
1. 在一台设备上运行`gatt_server.py`。
2. 在另一台设备上运行`gatt_client.py`（或同一设备，使用不同终端）。
3. 观察Server端的输出，确认读写操作被正确处理。

---

### 注意事项
- **权限**: 确保以root权限运行，因为BlueZ需要访问Bluetooth硬件。
- **UUID**: 示例中的UUID是随机生成的，实际使用时可根据需要自定义。
- **异常处理**: 生产环境中需添加更多错误处理逻辑。

如果您有具体需求（如添加更多特性、通知功能等），请告诉我，我可以进一步扩展代码！

# 参考资料

1、GATT Profile 简介

https://www.race604.com/gatt-profile-intro/

2、gatt官网profile列表

https://www.bluetooth.com/specifications/gatt

3、通用属性配置文件（GATT）及其服务，特性与属性介绍

http://blog.chinaunix.net/uid-21411227-id-5750680.html

4、BLE GATT 介绍

https://www.cnblogs.com/smart-mutouren/p/5937990.html

5、Bluetooth GATT Profile Spec 解读

这个非常好。

https://blog.csdn.net/utadalight/article/details/80057032

6、蓝牙低功耗profile：ATT和GATT

https://blog.csdn.net/bxqs001/article/details/37967145

7、BLE协议--ATT、GATT

https://www.jianshu.com/p/d5e65cbb6b73

8、BLE安全入门及实战（1）

蓝牙的安全问题，的确值得关注。

https://www.secpulse.com/archives/75756.html

9、实战智能门锁

https://zhuanlan.zhihu.com/p/30393145

10、Bluetooth: ATT and GATT

https://epxx.co/artigos/bluetooth_gatt.html

11、BLE中GATT的服务和特征发现机制

https://www.cnblogs.com/simpleGao/p/17630670.html