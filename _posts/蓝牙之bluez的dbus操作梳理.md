---
title: 蓝牙之bluez的dbus操作梳理
date: 2024-07-24 17:12:35
tags:
	- 蓝牙

---



看看怎么使用bluez的dbus接口来实现A2DP的播放功能，实现类似bluez-alsa的功能，但是要更加简单。

首先需要把bluez的所有dbus接口梳理一遍。

在github上有这么一个topic。

https://github.com/topics/bluez-dbus

例如这个，

https://github.com/weliem/bluez_inc

说明里写了：

该库的目标是为 Bluez 提供一个干净的 C 接口，而无需使用 DBus 命令。至少可以说，在 DBus 上使用 Bluez 是相当棘手的，而且这个库在后台完成了所有艰苦的工作。因此，它看起来像一个用于蓝牙的“普通”C 库！

在bluez/doc目录下，执行：`ls org*.rst -lh`

得到这些文件：

```
org.bluez.Adapter.rst
org.bluez.AdminPolicySet.rst
org.bluez.AdminPolicyStatus.rst
org.bluez.AdvertisementMonitorManager.rst
org.bluez.AdvertisementMonitor.rst
org.bluez.AgentManager.rst
org.bluez.Agent.rst
org.bluez.BatteryProviderManager.rst
org.bluez.BatteryProvider.rst
org.bluez.Battery.rst
org.bluez.Device.rst
org.bluez.DeviceSet.rst
org.bluez.GattCharacteristic.rst
org.bluez.GattDescriptor.rst
org.bluez.GattManager.rst
org.bluez.GattProfile.rst
org.bluez.GattService.rst
org.bluez.Input.rst
org.bluez.LEAdvertisement.rst
org.bluez.LEAdvertisingManager.rst
org.bluez.MediaControl.rst
org.bluez.MediaEndpoint.rst
org.bluez.MediaFolder.rst
org.bluez.MediaItem.rst
org.bluez.MediaPlayer.rst
org.bluez.Media.rst
org.bluez.MediaTransport.rst
org.bluez.Network.rst
org.bluez.NetworkServer.rst
org.bluez.obex.AgentManager.rst
org.bluez.obex.Agent.rst
org.bluez.obex.Client.rst
org.bluez.obex.FileTransfer.rst
org.bluez.obex.MessageAccess.rst
org.bluez.obex.Message.rst
org.bluez.obex.ObjectPush.rst
org.bluez.obex.PhonebookAccess.rst
org.bluez.obex.Session.rst
org.bluez.obex.Synchronization.rst
org.bluez.obex.Transfer.rst
org.bluez.ProfileManager.rst
```

这些就是所有的dbus接口了。

obex我不关注。都忽略就好。

# dbus表格

依次梳理一下：

| dbus api                              | 说明                                                         |
| ------------------------------------- | ------------------------------------------------------------ |
| org.bluez.Adapter                     | 蓝牙适配器<br />Interface是：org.bluez.Adapter1<br />Object path：xx/hci0<br />==Methods有==：<br />**StartDiscovery()**：<br />开始扫描session。如果发现设备，则创建对应的device object。<br />可能的错误：NotReady、Failed、InProgress<br />**StopDiscovery()**：<br />停止扫描session。<br />**RemoveDevice(object device)**：<br />移除指定的设备。<br />**SetDiscoveryFilter(dict filter)**:<br />设置device filter。filter的可能取值：<br />* 字符串数组。是多个uuid。<br />* int16 rssi。<br />* uint16 pathloss。<br />* string transport。可能取值：auto（默认）、bredr、le。<br />* bool duplicate ，默认true。<br />**GetDiscoveryFilters()**：返回filters，字符串数组。<br />**ConnectDevice(dict properties)**：<br />这个是实验接口。不经过discovery直接连接设备。<br />==Properties有：==<br />Address：字符串，蓝牙地址<br />AddressType：字符串，取值：public或者random<br /><br />Name：蓝牙的名字。<br />Alias：别名。<br />Class：<br />Powered：<br />PowerState：取值：on、off、off-enabling、on-disabling、off-blocked。<br />Discoverable：<br />Pairable：<br />PairableTimeout：<br />DiscoverableTimeout：<br />Discovering：<br />UUIDs：本地的服务的uuid。<br />Modalias：<br />Roles：支持的role。有：centeral、peripheral、center-peripheral。<br />ExperimentalFeatures：字符串数组。<br />Manufacture：<br />Version： |
| org.bluez.AdminPolicySet              | 管理员策略集<br />                                           |
| org.bluez.AdminPolicyStatus           | 管理员策略状态                                               |
| org.bluez.AdvertisementMonitorManager | 广告监控管理器                                               |
| org.bluez.AdvertisementMonitor        | 广告监控                                                     |
| org.bluez.AgentManager                | 代理管理器                                                   |
| org.bluez.Agent                       | 代理                                                         |
| org.bluez.BatteryProviderManager      | 电池提供者管理器                                             |
| org.bluez.BatteryProvider             | 电池提供者                                                   |
| org.bluez.Battery                     | 电池                                                         |
| org.bluez.Device                      | 设备                                                         |
| org.bluez.DeviceSet                   | 设备集合                                                     |
| org.bluez.GattCharacteristic          | GATT特征                                                     |
| org.bluez.GattDescriptor              | GATT描述符                                                   |
| org.bluez.GattManager                 | GATT管理器                                                   |
| org.bluez.GattProfile                 | GATT配置文件                                                 |
| org.bluez.GattService                 | GATT服务                                                     |
| org.bluez.Input                       | 输入                                                         |
| org.bluez.LEAdvertisement             | 低功耗广告                                                   |
| org.bluez.LEAdvertisingManager        | 低功耗广告管理器                                             |
| org.bluez.MediaControl                | 多媒体控制                                                   |
| org.bluez.MediaEndpoint               | 多媒体端点                                                   |
| org.bluez.MediaFolder                 | 多媒体文件夹                                                 |
| org.bluez.MediaItem                   | 多媒体项                                                     |
| org.bluez.MediaPlayer                 | 多媒体播放器                                                 |
| org.bluez.Media                       | 多媒体                                                       |
| org.bluez.MediaTransport              | 多媒体传输                                                   |
| org.bluez.Network                     | 网络                                                         |
| org.bluez.NetworkServer               | 网络服务器                                                   |
| org.bluez.ProfileManager              | 配置文件管理器                                               |

# org.bluez.Adapter

## 获取所有的属性

测试代码：

```
#include <gio/gio.h>
#include <stdio.h>

int main() {
    GError *error = NULL;
    GDBusConnection *connection;
    GVariant *result;
    const gchar *properties[] = {"Address", "Name", "Alias", "Class", "Powered", "Discoverable", "Pairable", NULL};
    int i;

    // 连接到系统总线
    connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &error);
    if (error != NULL) {
        g_printerr("Error connecting to system bus: %s\n", error->message);
        g_error_free(error);
        return 1;
    }

    // 遍历并获取每个属性
    for (i = 0; properties[i] != NULL; i++) {
        result = g_dbus_connection_call_sync(
            connection,
            "org.bluez",                // 蓝牙服务名称
            "/org/bluez/hci0",          // 适配器对象路径（hci0是第一个适配器）
            "org.freedesktop.DBus.Properties", // DBus Properties 接口
            "Get",                      // Get 方法
            g_variant_new("(ss)", "org.bluez.Adapter1", properties[i]), // 参数
            NULL,                       // 返回值类型
            G_DBUS_CALL_FLAGS_NONE,
            -1,                         // 超时时间
            NULL,
            &error
        );

        if (error != NULL) {
            g_printerr("Error getting property %s: %s\n", properties[i], error->message);
            g_error_free(error);
            error = NULL;
        } else {
            GVariant *value;
            g_variant_get(result, "(v)", &value);
            g_print("Property %s: %s\n", properties[i], g_variant_print(value, TRUE));
            g_variant_unref(value);
            g_variant_unref(result);
        }
    }

    // 清理
    g_object_unref(connection);
    return 0;
}

```

Makefile：

```
CC = gcc
CFLAGS = -Wall -std=c99
LIBS = $(shell pkg-config --cflags --libs gio-2.0)

all: dbus_client

dbus_client: dbus_client.c
	$(CC) $(CFLAGS) -o dbus_client dbus_client.c $(LIBS)

clean:
	rm -f dbus_client
```

执行：

```
./dbus_client
Property Address: '58:00:E3:45:BA:C8'
Property Name: 'amlogic-BAD-INDEX'
Property Alias: 'amlogic-BAD-INDEX'
Property Class: uint32 1835276
Property Powered: true
Property Discoverable: false
Property Pairable: true
```

## StartDiscovery

c文件：

```
#include <gio/gio.h>
#include <stdio.h>

// 设备增加的信号处理函数
static void on_interfaces_added(GDBusConnection *connection,
                                const gchar *sender_name,
                                const gchar *object_path,
                                const gchar *interface_name,
                                const gchar *signal_name,
                                GVariant *parameters,
                                gpointer user_data) {
    GVariantIter *interfaces, *properties;
    const gchar *interface;
    GVariant *prop_value;

    g_variant_get(parameters, "(&oa{sa{sv}})", &object_path, &interfaces);
    while (g_variant_iter_next(interfaces, "{&sa{sv}}", &interface, &properties)) {
        if (g_strcmp0(interface, "org.bluez.Device1") == 0) {
            g_print("Device found: %s\n", object_path);

            while (g_variant_iter_next(properties, "{&sv}", &interface, &prop_value)) {
                gchar *str_val = g_variant_print(prop_value, TRUE);
                g_print("  %s: %s\n", interface, str_val);
                g_free(str_val);
                g_variant_unref(prop_value);
            }
        }
        g_variant_iter_free(properties);
    }
    g_variant_iter_free(interfaces);
}

int main() {
    GError *error = NULL;
    GDBusConnection *connection;
    guint signal_subscription_id;

    // 连接到系统总线
    connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &error);
    if (error != NULL) {
        g_printerr("Error connecting to system bus: %s\n", error->message);
        g_error_free(error);
        return 1;
    }

    // 订阅 InterfacesAdded 信号
    signal_subscription_id = g_dbus_connection_signal_subscribe(
        connection,
        "org.bluez",               // 发送者
        "org.freedesktop.DBus.ObjectManager", // 接口名称
        "InterfacesAdded",         // 信号名称
        NULL,                      // 对象路径
        NULL,                      // 参数匹配
        G_DBUS_SIGNAL_FLAGS_NONE,
        on_interfaces_added,       // 回调函数
        NULL,                      // 用户数据
        NULL                       // 用户数据释放函数
    );

    // 调用 StartDiscovery 方法开始扫描
    g_dbus_connection_call_sync(
        connection,
        "org.bluez",
        "/org/bluez/hci0",          // 适配器对象路径
        "org.bluez.Adapter1",
        "StartDiscovery",
        NULL,
        NULL,
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        &error
    );

    if (error != NULL) {
        g_printerr("Error starting discovery: %s\n", error->message);
        g_error_free(error);
        g_object_unref(connection);
        return 1;
    }

    g_print("Discovery started...\n");

    // 主循环，等待信号
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);

    // 清理
    g_dbus_connection_signal_unsubscribe(connection, signal_subscription_id);
    g_object_unref(connection);
    g_main_loop_unref(loop);

    return 0;
}

```

执行输出的打印，很多条，这个是其中一条的样子：

```
Device found: /org/bluez/hci0/dev_78_66_9D_39_C2_B9
  Address: '78:66:9D:39:C2:B9'
  AddressType: 'public'
  Name: 'TCL 55V8E Pro-6976'
  Alias: 'TCL 55V8E Pro-6976'
  Class: uint32 1704220
  Icon: 'computer'
  Paired: false
  Trusted: false
  Blocked: false
  LegacyPairing: false
  RSSI: int16 -76
  Connected: false
  UUIDs: ['0000110a-0000-1000-8000-00805f9b34fb', '0000110c-0000-1000-8000-00805f9b34fb', '0000110e-0000-1000-8000-00805f9b34fb', '00001200-0000-1000-8000-00805f9b34fb', '00000000-0000-0000-0000-000000000000']
  Adapter: objectpath '/org/bluez/hci0'
  ServicesResolved: false
```

# dbus命令操作Adapter

`org.bluez.Adapter1` 是 BlueZ 中用于表示蓝牙适配器的 D-Bus 接口。它提供了管理蓝牙适配器的能力，包括启动扫描、设置适配器属性等。

以下是与 `org.bluez.Adapter1` 通信的常见操作及实际示例：

------

### **1. 获取适配器对象路径**

适配器对象路径通常是 `/org/bluez/hciX`，其中 `X` 是适配器编号（如 `hci0`）。

命令示例：

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0 org.freedesktop.DBus.Properties.Get \
string:org.bluez.Adapter1 string:Address
```

返回结果：

```text
   variant       string "00:1A:7D:DA:71:13"
```

表示适配器的地址为 `00:1A:7D:DA:71:13`。

------

### **2. 设置适配器属性**

**示例 1：更改适配器名称**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0 org.freedesktop.DBus.Properties.Set \
string:org.bluez.Adapter1 string:Alias variant:string:"MyBluetoothAdapter"
```

**示例 2：启用适配器的发现功能**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0 org.freedesktop.DBus.Properties.Set \
string:org.bluez.Adapter1 string:Discoverable variant:boolean:true
```

------

### **3. 开始扫描设备**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0 org.bluez.Adapter1.StartDiscovery
```

扫描开始后，你可以通过 `org.freedesktop.DBus.ObjectManager` 接口获取发现的设备。

------

### **4. 停止扫描设备**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0 org.bluez.Adapter1.StopDiscovery
```

------

### **5. 示例：启动扫描并获取发现的设备**

1. **启动扫描**：

   ```bash
   dbus-send --system --print-reply --dest=org.bluez \
   /org/bluez/hci0 org.bluez.Adapter1.StartDiscovery
   ```

2. **获取设备列表**： 使用以下命令列出 BlueZ 管理的所有设备：

   ```bash
   dbus-send --system --print-reply --dest=org.bluez \
   / org.freedesktop.DBus.ObjectManager.GetManagedObjects
   ```

   返回结果中类似于 `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX` 的对象路径为发现的设备。

------

### **6. 停用适配器**

如果需要禁用适配器，可以设置 `Powered` 属性为 `false`：

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0 org.freedesktop.DBus.Properties.Set \
string:org.bluez.Adapter1 string:Powered variant:boolean:false
```

------

### **常用 D-Bus 方法汇总**

| **方法**               | **功能**       | **示例命令**                                                 |
| ---------------------- | -------------- | ------------------------------------------------------------ |
| `StartDiscovery`       | 开始扫描设备   | `org.bluez.Adapter1.StartDiscovery`                          |
| `StopDiscovery`        | 停止扫描设备   | `org.bluez.Adapter1.StopDiscovery`                           |
| `RemoveDevice`         | 移除配对的设备 | `org.bluez.Adapter1.RemoveDevice` `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX` |
| `Set` (Properties.Set) | 设置属性值     | 设置发现功能：`Discoverable = true`                          |
| `Get` (Properties.Get) | 获取属性值     | 获取设备地址：`Address`                                      |

------

### **蓝牙适配器主要属性**

| **属性**       | **类型**  | **描述**                                   |
| -------------- | --------- | ------------------------------------------ |
| `Address`      | `string`  | 适配器的蓝牙地址，例如 `00:1A:7D:DA:71:13` |
| `Name`         | `string`  | 蓝牙设备名称                               |
| `Alias`        | `string`  | 用户设置的设备别名                         |
| `Class`        | `uint32`  | 设备类别代码                               |
| `Powered`      | `boolean` | 是否启用适配器                             |
| `Discoverable` | `boolean` | 设备是否可被发现                           |
| `Pairable`     | `boolean` | 是否允许配对                               |

这些命令和方法适用于大部分 BlueZ 环境，用于控制和调试蓝牙适配器及其功能。

# 实现A2DP sink功能

实现 A2DP Sink 功能，即使蓝牙设备充当音频接收器，可以通过 BlueZ 的 D-Bus 接口进行配置。以下是如何通过 BlueZ 的 D-Bus 接口实现 A2DP Sink 功能的基本步骤：

1. **连接到 D-Bus 系统总线**
2. **创建一个音频端点 (A2DP Sink)**
3. **发现并配对音频源设备**
4. **设置音频流的属性**
5. **启动音频流**

以下是实现 A2DP Sink 功能的基本示例代码。注意，这只是一个简化的示例。实际使用中可能需要额外处理错误、权限和配置问题。

### 示例代码

```c
#include <gio/gio.h>
#include <stdio.h>

#define A2DP_SINK_UUID "0000110b-0000-1000-8000-00805f9b34fb" // A2DP Sink UUID

// 回调函数，处理音频流数据
static void on_audio_stream_data(GDBusConnection *connection,
                                 const gchar *sender_name,
                                 const gchar *object_path,
                                 const gchar *interface_name,
                                 const gchar *signal_name,
                                 GVariant *parameters,
                                 gpointer user_data) {
    g_print("Received audio stream data on %s\n", object_path);
}

int main() {
    GError *error = NULL;
    GDBusConnection *connection;
    GVariant *result;
    GVariant *properties;
    guint signal_subscription_id;
    const gchar *adapter_path = "/org/bluez/hci0";
    const gchar *audio_sink_path = "/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX"; // 替换为实际设备路径

    // 连接到系统总线
    connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &error);
    if (error != NULL) {
        g_printerr("Error connecting to system bus: %s\n", error->message);
        g_error_free(error);
        return 1;
    }

    // 创建 A2DP Sink 音频端点
    result = g_dbus_connection_call_sync(
        connection,
        "org.bluez",
        adapter_path,
        "org.bluez.Media1",
        "CreateEndpoint",
        g_variant_new("(s)", A2DP_SINK_UUID),
        NULL,
        G_DBUS_CALL_FLAGS_NONE,
        -1,
        NULL,
        &error
    );

    if (error != NULL) {
        g_printerr("Error creating A2DP Sink endpoint: %s\n", error->message);
        g_error_free(error);
        g_object_unref(connection);
        return 1;
    }

    g_print("A2DP Sink endpoint created.\n");

    // 订阅音频流数据信号
    signal_subscription_id = g_dbus_connection_signal_subscribe(
        connection,
        "org.bluez",
        "org.bluez.Media1",
        "StreamData",
        audio_sink_path,
        NULL,
        G_DBUS_SIGNAL_FLAGS_NONE,
        on_audio_stream_data,
        NULL,
        NULL
    );

    // 发现音频源设备并配对
    // 需要实现配对逻辑，比如使用蓝牙地址找到设备并配对

    // 启动音频流
    // 实际操作可能涉及到更多的配置和流控制

    // 主循环，等待信号
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);

    // 清理
    g_dbus_connection_signal_unsubscribe(connection, signal_subscription_id);
    g_object_unref(connection);
    g_main_loop_unref(loop);

    return 0;
}
```

### 代码解释

1. **连接到 D-Bus 系统总线**:
   - 使用 `g_bus_get_sync()` 连接到系统总线。

2. **创建 A2DP Sink 音频端点**:
   - 使用 `g_dbus_connection_call_sync()` 调用 `CreateEndpoint` 方法来创建 A2DP Sink 音频端点。这里的 UUID 是 A2DP Sink 的标准 UUID。

3. **订阅音频流数据信号**:
   - 使用 `g_dbus_connection_signal_subscribe()` 订阅 `StreamData` 信号，以便接收音频数据。

4. **发现和配对音频源设备**:
   - 需要实现音频源设备的发现和配对逻辑。这部分通常涉及到更多的 D-Bus 调用和蓝牙配对逻辑，具体取决于你的应用程序需求。

5. **启动音频流**:
   - 实际的音频流控制和启动通常涉及到音频流的配置和控制。可以通过 `org.bluez.Media1` 接口进行控制。

### 编译和运行

编译程序：
```bash
gcc -o a2dp_sink a2dp_sink.c `pkg-config --cflags --libs gio-2.0`
```

运行程序：
```bash
sudo ./a2dp_sink
```

### 注意事项

1. **对象路径和设备地址**:
   - 替换 `audio_sink_path` 为实际的设备对象路径。在实际应用中，你可能需要通过蓝牙扫描和配对逻辑找到设备路径。

2. **音频流处理**:
   - 示例中 `on_audio_stream_data` 函数是处理音频数据的回调，你需要根据实际需求实现音频数据的处理逻辑。

3. **权限和配置**:
   - 确保你有足够的权限来访问 D-Bus 和蓝牙设备，且系统中已配置并启用 BlueZ 服务。

4. **蓝牙设备兼容性**:
   - 确保蓝牙设备支持 A2DP Sink 功能，并正确配置了相关参数。

# org.bluez.Agent1 有哪些方法和属性

`org.bluez.Agent1` 接口是 BlueZ 的 D-Bus 接口之一，用于处理蓝牙配对和配对代理。它提供了配对时的用户交互功能，比如请求配对确认、用户输入等。

### `org.bluez.Agent1` 接口方法和属性

#### 1. **方法 (Methods)**

| Method Name            | Description                | Parameters                                      |
| ---------------------- | -------------------------- | ----------------------------------------------- |
| `Release`              | 释放代理对象。             | 无                                              |
| `RequestPinCode`       | 请求用户输入配对 PIN 码。  | `Device1` (object path) <br> `Request` (string) |
| `RequestPasskey`       | 请求用户输入配对 Passkey。 | `Device1` (object path) <br> `Request` (uint32) |
| `RequestConfirmation`  | 请求用户确认配对。         | `Device1` (object path) <br> `Request` (uint32) |
| `RequestAuthorization` | 请求用户授权设备。         | `Device1` (object path)                         |
| `RequestAuthorization` | 请求用户授权设备。         | `Device1` (object path)                         |

#### 2. **属性 (Properties)**

`org.bluez.Agent1` 没有定义具体的属性。此接口主要是通过方法处理蓝牙配对和授权过程。

### 详细解释

- **方法**

  - **Release**: 通常在配对过程完成后调用，用于释放代理对象并清理资源。

  - **RequestPinCode**: 在配对过程中，设备会请求用户输入 PIN 码以完成配对。这个方法在代理中被调用时，会传递设备对象路径和请求 PIN 码的提示。

  - **RequestPasskey**: 在需要输入 Passkey（通常是数字密码）时调用。它会要求用户输入一个数字（`Request`）来完成配对。

  - **RequestConfirmation**: 用于请求用户确认配对请求。会传递设备对象路径和 Passkey。

  - **RequestAuthorization**: 请求用户授权某个设备访问配对。

### 使用示例

以下是一个如何实现 `org.bluez.Agent1` 接口的简单示例：

```c
#include <gio/gio.h>
#include <stdio.h>

static void on_request_pin_code(GDBusConnection *connection,
                                const gchar *sender_name,
                                const gchar *object_path,
                                const gchar *interface_name,
                                const gchar *signal_name,
                                GVariant *parameters,
                                gpointer user_data) {
    g_print("Request PIN Code from device: %s\n", object_path);
    // 发送 PIN 码到设备
    // g_dbus_connection_emit_signal(connection, ...)
}

static void on_request_passkey(GDBusConnection *connection,
                               const gchar *sender_name,
                               const gchar *object_path,
                               const gchar *interface_name,
                               const gchar *signal_name,
                               GVariant *parameters,
                               gpointer user_data) {
    g_print("Request Passkey from device: %s\n", object_path);
    // 发送 Passkey 到设备
    // g_dbus_connection_emit_signal(connection, ...)
}

static void on_request_confirmation(GDBusConnection *connection,
                                     const gchar *sender_name,
                                     const gchar *object_path,
                                     const gchar *interface_name,
                                     const gchar *signal_name,
                                     GVariant *parameters,
                                     gpointer user_data) {
    g_print("Request Confirmation from device: %s\n", object_path);
    // 发送确认请求到设备
    // g_dbus_connection_emit_signal(connection, ...)
}

static void on_request_authorization(GDBusConnection *connection,
                                     const gchar *sender_name,
                                     const gchar *object_path,
                                     const gchar *interface_name,
                                     const gchar *signal_name,
                                     GVariant *parameters,
                                     gpointer user_data) {
    g_print("Request Authorization from device: %s\n", object_path);
    // 发送授权请求到设备
    // g_dbus_connection_emit_signal(connection, ...)
}

int main() {
    GError *error = NULL;
    GDBusConnection *connection;

    // 连接到系统总线
    connection = g_bus_get_sync(G_BUS_TYPE_SYSTEM, NULL, &error);
    if (error != NULL) {
        g_printerr("Error connecting to system bus: %s\n", error->message);
        g_error_free(error);
        return 1;
    }

    // 订阅代理请求信号
    g_dbus_connection_signal_subscribe(
        connection,
        "org.bluez",
        "org.bluez.Agent1",
        "RequestPinCode",
        NULL,
        NULL,
        G_DBUS_SIGNAL_FLAGS_NONE,
        on_request_pin_code,
        NULL,
        NULL
    );

    g_dbus_connection_signal_subscribe(
        connection,
        "org.bluez",
        "org.bluez.Agent1",
        "RequestPasskey",
        NULL,
        NULL,
        G_DBUS_SIGNAL_FLAGS_NONE,
        on_request_passkey,
        NULL,
        NULL
    );

    g_dbus_connection_signal_subscribe(
        connection,
        "org.bluez",
        "org.bluez.Agent1",
        "RequestConfirmation",
        NULL,
        NULL,
        G_DBUS_SIGNAL_FLAGS_NONE,
        on_request_confirmation,
        NULL,
        NULL
    );

    g_dbus_connection_signal_subscribe(
        connection,
        "org.bluez",
        "org.bluez.Agent1",
        "RequestAuthorization",
        NULL,
        NULL,
        G_DBUS_SIGNAL_FLAGS_NONE,
        on_request_authorization,
        NULL,
        NULL
    );

    // 主循环，等待信号
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);

    // 清理
    g_object_unref(connection);
    g_main_loop_unref(loop);

    return 0;
}
```

### 编译和运行

编译代码：
```bash
gcc -o agent agent.c `pkg-config --cflags --libs gio-2.0`
```

运行程序：
```bash
sudo ./agent
```

### 注意事项

1. **接口实现**: 实际使用时，你可能需要实现所有的信号处理函数，并正确响应配对请求。
2. **权限和配置**: 确保你有足够的权限来访问 D-Bus 和蓝牙设备，并且 BlueZ 服务已启动和配置。
3. **D-Bus 路径和接口**: 确保在实际应用中使用正确的 D-Bus 对象路径和接口名称。

通过实现 `org.bluez.Agent1` 接口，你可以自定义和处理蓝牙配对过程中的用户交互。

# dbus命令操作Agent

`org.bluez.Agent` 是 BlueZ 用于处理设备配对过程的 D-Bus 接口。Agent（代理）在蓝牙配对时负责用户交互，例如 PIN 码输入、确认配对请求等。

以下是与 `org.bluez.Agent` 接口相关的 D-Bus 操作及实际示例：

------

### **1. 注册代理 (Agent)**

通过 `org.bluez.AgentManager1.RegisterAgent` 方法注册一个代理。代理对象通常由用户程序实现，负责处理配对过程。

**命令示例：**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez org.bluez.AgentManager1.RegisterAgent \
object:/my/agent string:NoInputNoOutput
```

| **参数**                 | **说明**                                              |
| ------------------------ | ----------------------------------------------------- |
| `object:/my/agent`       | 代理对象路径，由程序实现。                            |
| `string:NoInputNoOutput` | 代理功能类型（Capability），定义交互能力：            |
|                          | - `DisplayOnly`: 仅显示 PIN 码；                      |
|                          | - `DisplayYesNo`: 显示确认提示；                      |
|                          | - `KeyboardOnly`: 用户输入 PIN 码；                   |
|                          | - `NoInputNoOutput`: 无交互功能（常用于嵌入式设备）； |
|                          | - `KeyboardDisplay`: 允许输入 PIN 和显示 PIN。        |

**结果：** 代理注册后，蓝牙堆栈将通过此代理处理配对过程。

------

### **2. 设置默认代理**

通过 `org.bluez.AgentManager1.RequestDefaultAgent` 方法，将代理设置为默认代理。

**命令示例：**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez org.bluez.AgentManager1.RequestDefaultAgent \
object:/my/agent
```

**说明：** 一旦设置为默认代理，所有蓝牙配对请求将默认由此代理处理。

------

### **3. 实现代理方法**

代理需要实现以下关键方法：

| **方法**              | **功能**                                          |
| --------------------- | ------------------------------------------------- |
| `Release`             | 在代理被注销时调用，执行清理操作。                |
| `RequestPinCode`      | 请求用户输入 PIN 码。                             |
| `DisplayPinCode`      | 显示 PIN 码给用户。                               |
| `RequestPasskey`      | 请求用户输入 Passkey（数值）。                    |
| `DisplayPasskey`      | 显示 Passkey 并同步显示当前按键状态（键盘输入）。 |
| `RequestConfirmation` | 请求用户确认配对是否继续（通常是 Yes/No）。       |
| `AuthorizeService`    | 请求用户授权设备访问特定服务。                    |
| `Cancel`              | 当配对被取消时调用。                              |

------

### **4. 示例：处理配对事件**

假设代理路径为 `/my/agent`，以下是常见交互的模拟命令：

#### **用户输入 PIN 码**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/my/agent org.bluez.Agent1.RequestPinCode \
object:/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX
```

返回示例：

```text
   string "1234"
```

#### **确认配对**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/my/agent org.bluez.Agent1.RequestConfirmation \
object:/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX uint32:123456
```

用户可以根据显示的 Passkey `123456` 进行确认。

返回示例：

- 确认：正常退出；
- 拒绝：返回错误。

#### **取消配对**

当配对取消时，代理会收到 `Cancel` 方法调用：

```bash
dbus-send --system --print-reply --dest=org.bluez \
/my/agent org.bluez.Agent1.Cancel
```

------

### **5. 注销代理**

通过 `org.bluez.AgentManager1.UnregisterAgent` 方法注销代理。

**命令示例：**

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez org.bluez.AgentManager1.UnregisterAgent \
object:/my/agent
```

------

### **6. 完整的配对流程**

1. **启动代理服务**：注册代理并设置为默认代理。
2. **用户接受配对请求**：通过代理实现 `RequestPinCode` 或 `RequestConfirmation`。
3. **完成配对**：代理方法完成后，设备完成配对并授权服务。

------

### **配对场景能力示例**

| **能力**          | **描述**                       | **适用设备**                 |
| ----------------- | ------------------------------ | ---------------------------- |
| `DisplayOnly`     | 显示 PIN，用户输入到对方设备   | 仅显示设备（如数字显示屏）。 |
| `DisplayYesNo`    | 显示 Passkey，用户选择确认     | 交互式设备（如手机）。       |
| `KeyboardOnly`    | 用户输入 PIN 到设备            | 支持键盘的设备（如电脑）。   |
| `NoInputNoOutput` | 无用户交互，配对自动完成       | 嵌入式设备、IoT 设备。       |
| `KeyboardDisplay` | 同时支持输入和显示 PIN/Passkey | 高级交互设备（如智能手表）。 |

使用 `org.bluez.Agent`，可以灵活处理配对过程，适配各种使用场景。

# org.bluez.Profile1

`org.bluez.Profile1` 是 BlueZ 中定义的 D-Bus 接口，用于管理蓝牙配置文件（Bluetooth profiles）。在蓝牙通信中，配置文件定义了设备之间通信的规范和协议。通过 `org.bluez.Profile1` 接口，可以实现对蓝牙配置文件的注册、管理和通信。

### 主要作用和功能：

1. **管理蓝牙配置文件**：
   - `org.bluez.Profile1` 接口==用于管理蓝牙配置文件==，包括注册、激活和注销配置文件。

2. **通信协议**：
   - 通过配置文件，设备可以定义支持的蓝牙通信协议和特性，如音频传输、文件传输等。

3. **实现蓝牙功能**：
   - 通过实现 `org.bluez.Profile1` 接口，可以为设备添加特定的蓝牙功能和服务，使其能够与其他设备进行通信。

4. **提供服务**：
   - 蓝牙配置文件允许设备作为服务器提供特定的服务，如音频播放、键盘输入等。

### 示例代码：

以下是一个简单的示例，演示如何使用 `org.bluez.Profile1` 接口在 BlueZ 中注册蓝牙配置文件：

```python
import dbus
from gi.repository import GLib

bus = dbus.SystemBus()
bluez = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1")

class MyProfile(dbus.service.Object):
    @dbus.service.method("org.bluez.Profile1",
                         in_signature="oha{sv}",
                         out_signature="o")
    def Release(self):
        print("Profile Released")
        mainloop.quit()

profile = MyProfile(bus, "/org/bluez/myprofile")

options = {
    "Name": "MyProfile",
    "Role": "server",
    "Channel": dbus.UInt16(22),
    "ServiceRecord": """
    (...)
    """  # ServiceRecord 可以是一个描述蓝牙服务的字符串
}

bluez.RegisterProfile("/org/bluez/myprofile", "00001101-0000-1000-8000-00805f9b34fb", options)

mainloop = GLib.MainLoop()
mainloop.run()
```

在这个示例中，通过注册一个实现 `org.bluez.Profile1` 接口的蓝牙配置文件，可以向蓝牙系统添加新的功能和服务。通过 `RegisterProfile` 方法注册配置文件，然后实现 `Release` 方法来处理配置文件的释放。这样就可以在蓝牙设备上提供自定义的蓝牙功能和服务。

# SetConfiguration和SelectConfiguration

## 触发的时机

`MediaEndpoint.SetConfiguration` 和 `MediaEndpoint.SelectConfiguration` 是 D-Bus 接口中与蓝牙音频配置相关的方法。它们的触发时机及作用如下：

### 1. **MediaEndpoint.SetConfiguration**

- **触发时机**：
  - 当音频端点需要设置或更新其配置时，例如在连接过程中或配置变化时。

- **作用**：
  - 用于设置音频端点的具体配置，包括编码方式、通道数等。
  - 这通常在设备连接后由媒体协议栈（如 A2DP）调用，以确保音频流的正确传输。

### 2. **MediaEndpoint.SelectConfiguration**

- **触发时机**：
  - 在建立连接时，蓝牙设备需要选择适合的音频配置，如选择支持的编码格式。

- **作用**：
  - 用于选择适合当前传输的配置。
  - 这一步骤通常在设备协商音频流配置时发生，确保两端设备达成一致，以便顺利传输音频数据。

### 总结

- **SetConfiguration**：用于设置或更新端点的具体配置。
- **SelectConfiguration**：用于选择合适的音频配置以进行传输。

这两个方法在蓝牙音频传输的建立和配置过程中扮演着关键角色。

## 假如我手机上播放单声道音频变为播放双声道音频时，SetConfiguration会触发吗

是的，当你从播放单声道音频切换到双声道音频时，`MediaEndpoint.SetConfiguration` 方法会被触发。这是因为设备需要更新其音频配置，以适应新的音频流设置。

### 触发情况

- **切换音频格式**：在这种情况下，音频配置（如通道数、编码方式等）会发生变化，因此需要调用 `SetConfiguration` 来设置新的配置。

### 作用

- **更新配置**：确保音频端点能够正确处理新的双声道音频流，确保音频质量和传输的正确性。

### 总结

在音频格式变化时，`SetConfiguration` 方法通常会被调用，以便更新端点的配置并适应新的音频需求。



# org.bluez.DeviceSet1用途

`org.bluez.DeviceSet1` 是 BlueZ 提供的一个 D-Bus 接口，主要用于管理设备集合（Device Set）。设备集合通常用来表示多个设备的逻辑分组，便于应用程序对其进行批量管理或标识特定的上下文场景。

------

### **主要用途**

| **功能**                 | **说明**                                                     |
| ------------------------ | ------------------------------------------------------------ |
| 逻辑分组设备             | 将多个蓝牙设备组织成一个集合，表示它们属于同一个场景或应用需求。 |
| 批量操作                 | 可以针对设备集合执行批量操作（如连接、断开或配对）。         |
| 描述设备集合的属性和状态 | 通过 D-Bus 属性查询和描述集合内的设备及其状态。              |

------

### **关键属性**

以下是 `org.bluez.DeviceSet1` 的常用属性：

| **属性**  | **类型**        | **说明**                                             |
| --------- | --------------- | ---------------------------------------------------- |
| `Devices` | `array[object]` | 集合内的设备对象路径列表。                           |
| `Name`    | `string`        | 设备集合的名称，用于标识集合。                       |
| `Type`    | `string`        | 集合类型，例如 `audio`, `input` 等，表示集合的用途。 |

------

### **常见方法**

| **方法**       | **说明**                 |
| -------------- | ------------------------ |
| `AddDevice`    | 将指定设备添加到集合中。 |
| `RemoveDevice` | 将指定设备从集合中移除。 |

------

### **D-Bus 示例操作**

#### **1. 查询设备集合的属性**

查询某个设备集合的所有属性。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/DeviceSet1 org.freedesktop.DBus.Properties.GetAll \
string:org.bluez.DeviceSet1
```

**返回示例：**

```text
array [
    dict entry(
        string "Devices"
        variant array [
            object "/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX"
            object "/org/bluez/hci0/dev_YY_YY_YY_YY_YY_YY"
        ]
    )
    dict entry(
        string "Name"
        variant string "AudioGroup1"
    )
    dict entry(
        string "Type"
        variant string "audio"
    )
]
```

------

#### **2. 添加设备到集合**

将设备 `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX` 添加到设备集合。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/DeviceSet1 org.bluez.DeviceSet1.AddDevice \
object:/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX
```

------

#### **3. 从集合中移除设备**

从设备集合中移除设备 `/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX`。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/DeviceSet1 org.bluez.DeviceSet1.RemoveDevice \
object:/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX
```

------

### **场景示例**

#### **1. 音频组管理**

对于支持 LE Audio 或其他多设备音频场景，可以创建一个 `audio` 类型的设备集合，将所有相关设备（如耳机、麦克风等）加入集合中。通过集合，可以统一管理这些设备的连接、断开等操作。

#### **2. 多输入设备管理**

如果一个应用需要同时使用多个输入设备（如鼠标和键盘），可以将它们归入一个 `input` 类型的集合。

------

`org.bluez.DeviceSet1` 提供了一种管理多个设备的高级抽象接口，对于复杂场景（如 LE Audio 群组管理）尤其有用，便于开发者通过逻辑分组简化设备操作。



# org.bluez.MediaEndpoint1用途



`org.bluez.MediaEndpoint1` 是 BlueZ 中用于蓝牙音频传输的 D-Bus 接口，主要用于描述和管理音频流的终端（Media Endpoint）。它涉及到蓝牙音频流的建立、管理和控制，特别是在支持音频协议（如 A2DP 或 HFP）的设备之间传输音频数据。

### **主要用途**

1. **音频流管理**： `org.bluez.MediaEndpoint1` 允许应用程序通过 D-Bus 接口管理音频流的终端，例如设置音频终端的配置、打开和关闭音频流等。
2. **音频协议支持**： 该接口用于支持 A2DP（高级音频分发协议）和 HFP（免提协议）等音频协议的数据传输。
3. **终端连接与控制**： 可以用来连接到音频设备的媒体终端，并通过该接口控制音频流的打开、暂停或关闭等操作。
4. **配置音频特性**： 通过该接口，蓝牙音频终端的音频特性（如音频编码方式、音量控制、媒体类型等）可以进行配置。

------

### **关键属性**

| **属性**    | **类型** | **说明**                                                     |
| ----------- | -------- | ------------------------------------------------------------ |
| `UUID`      | `string` | 媒体终端的唯一标识符（通常为音频服务的 UUID）。              |
| `Transport` | `object` | 关联的传输对象路径，通常为传输音频流的 `AudioTransport` 对象。 |
| `Codec`     | `string` | 媒体终端使用的音频编解码器，例如 SBC、AAC 等。               |
| `State`     | `string` | 媒体终端的状态（如 `idle`、`active`）。                      |
| `Role`      | `string` | 音频流的角色（如 `source` 或 `sink`），用于标识终端是音频源还是音频接收端。 |

------

### **常见方法**

| **方法**              | **说明**                                                 |
| --------------------- | -------------------------------------------------------- |
| `SetConfiguration`    | 设置音频终端的配置，例如编码、传输方式等。               |
| `Release`             | 释放音频终端，停止音频流并解除连接。                     |
| `Open`                | 打开音频终端，开始音频数据流的传输。                     |
| `Close`               | 关闭音频终端，停止音频数据流的传输。                     |
| `SelectConfiguration` | 选择某个配置（例如选择合适的编码格式和传输方式）并应用。 |

------

### **D-Bus 示例操作**

#### **1. 查询媒体终端的属性**

查询 `org.bluez.MediaEndpoint1` 对象的所有属性。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/endpoint_1 \
org.freedesktop.DBus.Properties.GetAll \
string:org.bluez.MediaEndpoint1
```

**返回示例：**

```text
array [
    dict entry(
        string "UUID"
        variant string "0000110A-0000-1000-8000-00805F9B34FB"
    )
    dict entry(
        string "State"
        variant string "active"
    )
    dict entry(
        string "Codec"
        variant string "SBC"
    )
    dict entry(
        string "Role"
        variant string "sink"
    )
]
```

------

#### **2. 设置媒体终端配置**

通过 `SetConfiguration` 方法设置媒体终端的音频编码和传输配置。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/endpoint_1 \
org.bluez.MediaEndpoint1.SetConfiguration \
dict:string:variant \
    string:"Codec" variant:string:"SBC" \
    string:"Transport" variant:object:"/org/bluez/hci0/transport_1"
```

**说明**：

- 设置媒体终端的音频编码为 SBC。
- 设置传输方式为某个指定的音频传输对象。

------

#### **3. 打开音频终端**

通过 `Open` 方法打开音频终端，开始音频数据流传输。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/endpoint_1 \
org.bluez.MediaEndpoint1.Open
```

------

#### **4. 关闭音频终端**

通过 `Close` 方法关闭音频终端，停止音频数据流的传输。

```bash
dbus-send --system --print-reply --dest=org.bluez \
/org/bluez/hci0/dev_XX_XX_XX_XX_XX_XX/endpoint_1 \
org.bluez.MediaEndpoint1.Close
```

------

### **场景示例**

#### **1. A2DP 音频流（音频源）**

如果您有一个设备（如手机或计算机）作为 A2DP 音频源（`source` 角色），您可以通过 `org.bluez.MediaEndpoint1` 接口设置合适的编码（如 SBC 或 AAC），并打开媒体终端，以便开始向蓝牙耳机或其他音频接收设备发送音频数据。

#### **2. 音频接收设备（音频接收端）**

如果设备作为音频接收端（`sink` 角色），则可以通过 `org.bluez.MediaEndpoint1` 接口配置并接收来自音频源的音频流，并控制音频流的开始和结束。

------

### **总结**

`org.bluez.MediaEndpoint1` 接口是 BlueZ 蓝牙堆栈中用于管理音频流终端的关键组件。它提供了打开、关闭、配置和管理蓝牙音频流的功能，适用于 A2DP、HFP 等音频协议的设备间音频数据传输。通过该接口，应用程序能够控制音频终端的状态、配置以及传输过程。