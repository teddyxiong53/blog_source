---
title: 蓝牙之bluez_inc库分析
date: 2024-07-25 11:17:35
tags:
	- 蓝牙
---

--

# 基本信息

该库的目标是为 Bluez 提供一个干净的 C 接口，而无需使用 DBus 命令。

至少可以说，在 DBus 上使用 Bluez 是相当棘手的，而且这个库在后台完成了所有艰苦的工作。

因此，它看起来像一个用于蓝牙的“普通”C 库！

该库专注于 BLE，并支持中心和外围角色。一些有趣的事实包括：

- 同时管理/连接多个外围设备
- 支持粘接
- 简化的编程接口，便于编码
- 可配置的日志记录，具有广泛的调试可能性

该库使用 GLib 2.0。

# 编译运行

下载代码：

```
git clone https://github.com/weliem/bluez_inc
```

编译：

```
mkdir build
cd build
cmake ../
make
```

运行：

```
cd examples
./peripheral/peripheral 
./central/central 
```

centeral的日志：

```
./central/central 
2024-07-25 11:15:20:306 DEBUG [Adapter] finding adapters
2024-07-25 11:15:20:311 DEBUG [Adapter] found device /org/bluez/hci0/dev_BE_EF_BE_EF_BC_8F 'AmlSoundBar-1b98'
2024-07-25 11:15:20:311 DEBUG [Adapter] found 1 adapter
2024-07-25 11:15:20:311 INFO [Main] using adapter 'hci0'
2024-07-25 11:15:20:318 DEBUG [Main] discovery 'starting' (/org/bluez/hci0)
2024-07-25 11:15:20:757 DEBUG [Main] discovery 'started' (/org/bluez/hci0)
2024-07-25 11:16:20:739 DEBUG [Device] freeing /org/bluez/hci0/dev_BE_EF_BE_EF_BC_8F
```

peripheral的日志：

```
./peripheral/peripheral 
2024-07-25 11:15:35:550 DEBUG [Adapter] finding adapters
2024-07-25 11:15:35:551 DEBUG [Adapter] found device /org/bluez/hci0/dev_BE_EF_BE_EF_BC_8F 'AmlSoundBar-1b98'
2024-07-25 11:15:35:551 DEBUG [Adapter] found 1 adapter
2024-07-25 11:15:35:551 DEBUG [Main] using default_adapter '/org/bluez/hci0'
2024-07-25 11:15:35:552 DEBUG [Application] successfully published application
2024-07-25 11:15:35:552 DEBUG [Application] successfully published local service 00001809-0000-1000-8000-00805f9b34fb
2024-07-25 11:15:35:552 DEBUG [Application] successfully published local characteristic 00002a1c-0000-1000-8000-00805f9b34fb
2024-07-25 11:15:35:552 DEBUG [Application] successfully published local descriptor 00002901-0000-1000-8000-00805f9b34fb
2024-07-25 11:15:35:552 DEBUG [Application] set value <68656c6c6f20746865726500> to <00002901-0000-1000-8000-00805f9b34fb>
2024-07-25 11:15:35:554 DEBUG [Application] adding /org/bluez/bincapplication/service0
2024-07-25 11:15:35:554 DEBUG [Application] adding /org/bluez/bincapplication/service0/char0
2024-07-25 11:15:35:554 DEBUG [Application] adding /org/bluez/bincapplication/service0/char0/desc0
2024-07-25 11:15:35:557 DEBUG [Adapter] successfully registered application
2024-07-25 11:15:35:561 DEBUG [Adapter] started advertising (58:00:E3:45:BA:C8)
```

# centeral代码流程

首先是拿到adapter，在dbus连接后，binc_adapter_get_default拿到adapter。

然后是设置adapter的discovery的回调。设置discovery的filter。

然后启动discovery。

discovery的回调函数，一般行为是这样：

```c
void on_scan_result(Adapter *default_adapter, Device *device) {
    char *name = binc_device_get_name(device);
    if (name != NULL && g_str_has_prefix(name, "xxx")) {
        //找到了我们要的device了。
        //停止扫描。
        binc_adapter_stop_discovery(default_adapter);
        //然后就是配置device的回调函数
        binc_device_set_connection_state_changed_cb(devcie, &on_connection_state_changed);
        binc_device_set_services_resolved_cb(device,xx);
        binc_device_set_read_char_cb(device, xx);
        binc_device_set_write_char_cb(device, xx);
        binc_device_set_notify_char_cb(device, xx);
        //连接device
        binc_device_connect(device);
    }
}
```

在调用了binc_device_connect函数后，

会依次发生这些事情：

* 首先connection_state变变为connecting
* 当状态变为connected后，你注册的回调被调用。但是这个时候，还不能使用该设备，因为服务发现还没有完成。
* 然后bluez会自动启动服务发现。这一步完成后，会调用我们上面注册的services_resolved回调。在这个回调里，你可以读写特性和启动通知。

连接状态变化的回调一般是这样：

```c
void on_connection_state_changed(Device *device, ConnectionState state, GError *error) {
    if (error != NULL) {
        log_debug(TAG, "(dis)connect fail (error:%d :%s)", error->code, error->message);
        return;
    }
    log_debug(TAG, "%s (%s) state :%s (%d)", binc_device_get_name(device), );
    if (state == BINC_DISCONNECTED && binc_device_get_bonding_state(device) != BINC_BONDED) {
        binc_adapter_remove_device(default_adapter, device);
    }
}
```

对特性进行read/write操作

一旦服务发现完成，我们就会开始使用特性。

一般会read一些特征。

例如型号和vendor。

```c
void on_services_resolved(Device *device) {
    Characteristic *manufacturer = binc_device_get_characteristic(device, DIS_SERVICE, DIS_MANUFACTURER);
    if (manufacturer != NULL) {
        binc_characteristic_read(manufacturer);
    }
    binc_device_read_char(device, DIS_SERVICE, DIS_MODEL_CHAR);
}
```

所有的ble操作都是异步的。

所以要借助回调来完成。

```c
void on_read(Device *device, Characteristic *ch, GByteArray *byteArray, GError *error) {
    char *uuid= binc_characteristic_get_uuid(ch);
    if (error != NULL) {
        return;
    }
    if (byteArray == NULL) {
        return;
    }
    if (g_str_equal(uuid, DIS_MANUFACTURER_CHAR) {
        log_debug(TAG, "manufacturer = %s", byteArray->data);
    }
}
```

在on_services_resolved回调函数里还可以进行write和notify操作。

```c
void on_services_resolved(Device *device) {
	Characteristic *current_time = binc_device_get_characteristic(device, CTS_SERVICE, CURRENT_TIME_CHAR);
	if (current_time != NULL) {
		if (binc_characteristic_supports_write(current_time, WITH_RESPONSE)) {
			GByteArray *timeBytes = binc_get_current_time();
            binc_characteristic_write(current_time, timeBytes, WITH_RESPONSE);
            g_byte_array_free(timeBytes, TRUE);
		}
	}
}
```

# peripheral代码流程

使用binc来创建一个外围设备。

也就是进行广播，并实现service和char。

创建广播，然后开始广播。

```c
GPtrArray *uuids = g_ptr_array_new();
g_ptr_array_add(uuids, HTS_SERVICE_UUID);
g_ptr_array_add(uuids, BLP_SERVICE_UUDI);
//创建广播
adv = binc_advertisement_create();
binc_advertisement_set_local_name(adv, "BINC2");
binc_advertisement_set_services(adv, uuids);
//开始广播
binc_adapter_start_advertising(default_adapter, adv);
g_ptr_array_free(uuids, TRUE);
```

为了让外围设备支持工作，需要创建一个app。

步骤是这样：

* 创建app
* 添加一个或多个service
* 添加一个或多个char
* 实现char的read/write/notify

下面的对应的代码：

```c
app = binc_create_application(default_adapter);
binc_application_add_service(app, HIS_SERVICE_UUID);
binc_application_add_characteristic(app, HIS_SERVICE_UUID,
                                   TEMPERATURE_CHAR_UUID,
                                   READ|INDICATE|WRITE);
//设置read和write的回调
binc_application_set_char_read_cb(app, xx);
binc_application_set_char_write_cb(app, xx);
//注册app
binc_adapter_register_application(default_adapter, app);
```

# log初始化和打印

```c
log_eanbled(TRUE);
log_set_level(LOG_DEBUG);

log_set_filename("mylog.log", 655356, 10);

log_debug("MyTag", "hello %s", "world");
```



