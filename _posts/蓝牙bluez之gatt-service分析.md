---
title: 蓝牙bluez之gatt-service分析
date: 2020-03-27 16:24:11
tags:
	- 蓝牙

---

--

# gatt-service.c

## IAS_UUID			

`IAS_UUID` 是 Immediate Alert Service (IAS) 的 UUID，它在蓝牙低能耗（BLE）协议中被用来标识即时警报服务。Immediate Alert Service 是一种用于触发警报的 BLE 服务，常用于定位和安全等应用场景。例如，当某个设备（如智能手表或钥匙链）离开特定范围时，智能手机可以使用这个服务触发警报。

### 作用
Immediate Alert Service 主要用于以下功能：

1. **定位**：
   - 通过触发警报声或震动，帮助用户找到丢失的设备。例如，如果你找不到你的智能手表，可以通过手机应用程序触发手表的警报声。

2. **安全**：
   - 当设备离开预设范围时，触发警报以提醒用户。这在防丢应用中很常见，确保用户不会丢失他们的重要物品。

### UUID 的具体含义
`"00001802-0000-1000-8000-00805f9b34fb"` 是 Immediate Alert Service 的标准 UUID，由 Bluetooth SIG 分配，用于标识这一服务。BLE 服务和特征都有唯一的 UUID，这些 UUID 确保了不同服务和特征在全世界范围内都是唯一的。

### 使用场景
以下是如何使用 Immediate Alert Service 的一个示例：

1. **扫描设备**：首先，使用蓝牙扫描工具扫描可用设备。
2. **连接设备**：找到支持 Immediate Alert Service 的设备并连接。
3. **发现服务**：发现设备上的所有服务，检查是否有 Immediate Alert Service。
4. **触发警报**：写入特定值到 Immediate Alert Service 的特征中，以触发警报。

### 示例代码

以下是一个简单的 Python 示例，使用 `pybluez` 和 `bluepy` 库来扫描设备并触发 Immediate Alert Service：

```python
from bluepy.btle import Scanner, Peripheral, UUID

IAS_UUID = UUID("00001802-0000-1000-8000-00805f9b34fb")
IAS_ALERT_LEVEL_UUID = UUID("00002a06-0000-1000-8000-00805f9b34fb")

def scan_and_connect():
    scanner = Scanner()
    devices = scanner.scan(10.0)

    for dev in devices:
        for adtype, desc, value in dev.getScanData():
            if adtype == 7 and value == str(IAS_UUID):
                print("Found device with Immediate Alert Service: %s" % dev.addr)
                return dev.addr
    return None

def trigger_alert(device_addr):
    try:
        peripheral = Peripheral(device_addr)
        service = peripheral.getServiceByUUID(IAS_UUID)
        alert_level = service.getCharacteristics(IAS_ALERT_LEVEL_UUID)[0]
        
        # Set alert level to high (value 2)
        alert_level.write(b'\x02')
        print("Alert triggered.")
    except Exception as e:
        print("Failed to trigger alert: %s" % e)

if __name__ == "__main__":
    device_addr = scan_and_connect()
    if device_addr:
        trigger_alert(device_addr)
    else:
        print("No device with Immediate Alert Service found.")
```

### 总结
`IAS_UUID` 是 Immediate Alert Service 的 UUID，用于在蓝牙低能耗设备之间触发即时警报。它广泛用于定位和安全应用，通过蓝牙协议与设备通信，触发警报音或震动，帮助用户找到设备或防止丢失。

## org.bluez.GattManager1 

`org.bluez.GattManager1` 是 BlueZ 中的一个 D-Bus 接口，用于管理 Bluetooth LE（Low Energy）设备上的 GATT（Generic Attribute Profile）服务。它提供了注册、注销 GATT 服务的方法，使应用程序能够在 BLE 设备上创建和管理 GATT 服务和特性。

以下是 `org.bluez.GattManager1` 接口的详细说明，包括如何使用 `dbus-send` 命令与其交互：

### 方法

1. **RegisterApplication**

   注册一个 GATT 应用程序，应用程序包含多个 GATT 服务。

   ```plaintext
   void RegisterApplication(object application, dict options)
   ```

   - `application`: 包含 GATT 服务的对象路径。
   - `options`: 附加的选项，目前未使用，传递空字典即可。

2. **UnregisterApplication**

   注销一个已注册的 GATT 应用程序。

   ```plaintext
   void UnregisterApplication(object application)
   ```

   - `application`: 要注销的 GATT 应用程序的对象路径。

### 示例

#### 使用 `dbus-send` 命令注册一个 GATT 应用程序

假设你已经编写了一个 GATT 应用程序，并且它的对象路径是 `/com/example/GattApplication`，你可以使用以下命令注册它：

```bash
dbus-send --system --dest=org.bluez --print-reply /org/bluez org.bluez.GattManager1.RegisterApplication \
    objectpath:/com/example/GattApplication \
    dict:string:string:""
```

#### 使用 `dbus-send` 命令注销一个 GATT 应用程序

注销已经注册的 GATT 应用程序：

```bash
dbus-send --system --dest=org.bluez --print-reply /org/bluez org.bluez.GattManager1.UnregisterApplication \
    objectpath:/com/example/GattApplication
```

### 代码示例

以下是一个 Python 示例，展示如何使用 `dbus-python` 注册和注销 GATT 应用程序：

```python
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

class GattApplication:
    def __init__(self, bus):
        self.path = '/com/example/GattApplication'
        self.services = []
        self.bus = bus

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    def get_properties(self):
        return {
            'org.freedesktop.DBus.ObjectManager': {}
        }

    def get_managed_objects(self):
        response = {}
        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
                descs = chrc.get_descriptors()
                for desc in descs:
                    response[desc.get_path()] = desc.get_properties()
        return response

class GattService:
    def __init__(self, index, uuid, primary):
        self.path = f'/com/example/service{index}'
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def get_properties(self):
        return {
            'org.bluez.GattService1': {
                'UUID': self.uuid,
                'Primary': self.primary,
                'Characteristics': dbus.Array(
                    [chrc.get_path() for chrc in self.characteristics],
                    signature='o'
                )
            }
        }

    def get_characteristics(self):
        return self.characteristics

# Initialize the main loop
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()

# Create GATT application
app = GattApplication(bus)
service = GattService(0, '12345678-1234-5678-1234-56789abcdef0', True)
app.add_service(service)

# Register application
manager = dbus.Interface(bus.get_object('org.bluez', '/org/bluez'),
                         'org.bluez.GattManager1')
manager.RegisterApplication(app.get_path(), {})

# Run the main loop
loop = GLib.MainLoop()
loop.run()
```

### 总结

`org.bluez.GattManager1` 接口用于管理 BLE 设备上的 GATT 服务，通过注册和注销 GATT 应用程序，允许应用程序在 BLE 设备上创建和管理 GATT 服务和特性。通过使用 `dbus-send` 命令或 `dbus-python` 库，你可以与 `org.bluez.GattManager1` 接口进行交互，从而实现对 BLE GATT 服务的管理。

# gdbus目录

bluez代码下有一个gdbus目录。

下面有5个C文件和一个头文件。

头文件是gdbus.h。里面定义了：

```
1、引用了2个头文件。
	#include <dbus/dbus.h>
	#include <glib.h>
	感觉这个模块也就是把dbus和glib进行包装使用。
2、定义了5个结构体。
	GDBusArgInfo
	GDBusMethodTable
	GDBusSignalTable
	GDBusPropertyTable
	GDBusSecurityTable
		就是4个表。方法表、信号表、属性表、安全表。
	结构体定义，都是GDBus开头。
	函数定义，都是 g_dbus开头。
	
```

5个C文件

```
client.c
	g_dbus_client_new 创建一个GDBusClient
	
mainloop.c
	//创建一个dbus的connection的方法。
	connection = g_dbus_setup_bus(DBUS_BUS_SYSTEM, NULL, NULL);
```



基于dbus技术的编程框架有4种：

1、glib-dbus。

2、gdbus。

3、qtdbus。最简单。

4、dbus-python。

gdbus和glib-dbus都是gnu开发的。

gdbus可以认为是glib-dbus的升级版本。

所以我们就看看gdbus的用法。





# 参考资料

1、基于GDBus技术的IPC通信编程详解(1)

https://blog.csdn.net/adlindary/article/details/80167840