---
title: 蓝牙之uuid
date: 2018-12-13 17:18:35
tags:
	- 蓝牙

---

--

每个设备可以包含多个service，每个service对应一个uuid。

概念的层次关系：

```
profile：规范
	service：服务
		characteristic：特征值
```

service和characteristic都需要用uuid来进行标识。

![](../images/蓝牙概念层次.png)

耳机不适合用ble，因为ble适合在数据量非常小的。而耳机的数据量很大。



主机和从机的通信都是通过characteristic来实现。



蓝牙规范执行了两种uuid：

1、基本的uuid。

2、16bit的uuid。（是uuid的简略写法）



有一个共用的基本uuid

```
0x0000xxxx-0000-1000-8000-00805F9B34FB
```

上面这个xxxx，就是16bit的uuid。

例如心率测量就是：2A37，那么完整的就是：

```
0x00002A37-0000-1000-8000-00805F9B34FB
```

对应蓝牙的属性，16bit足够用了。

基本uuid不能用于任何基本定制的属性、服务和特性。

对于定制的uuid，必须使用完整的128位的uuid。



==字符串长度是36。32个是数字，4个是“-”。==

==8-4-4-4-12 。==



蓝牙4.0是以参数来进行数据传输的。

就是说，服务端定义好一个参数，客户端可以对这个参数进行读、写、通知操作。

这个参数，在蓝牙里有个术语，叫特征值。

对特征值进行分类，一组特征值就是一个服务。

每个特征值有属性：

```
长度
权限
值
描述
```



==蓝牙4.0引入了2个核心协议ATT和GATT。==

==主要是为了ble的，但是传统蓝牙也可以用。==



在开发中我们需要获取设备的UUID字段，可以询问硬件工程师，也可以通过蓝牙测试工具查看service UUID 和

characteristic UUID。



# 定义uuid

**可以自定义uuid。有什么约束吗？**

**按格式来就行了。**

service的uuid。可以理解为tcp协议栈里的端口号。

例如80默认是提供http服务的，但是你只要客户端和服务端约定好，用其他的端口号也完全没有问题。

UUID通常以8-4-4-4-12的形式表示，例如：`123e4567-e89b-12d3-a456-426614174000`。

# 常用的uuid

我们只看16bit的。

```
var uuids = {
    "0001": "SDP",
    "0003": "RFCOMM",
    "0005": "TCS-BIN",
    "0007": "ATT",
    "0008": "OBEX",
    "000f": "BNEP",
    "0010": "UPNP",
    "0011": "HIDP",
    "0012": "Hardcopy Control Channel",
    "0014": "Hardcopy Data Channel",
    "0016": "Hardcopy Notification",
后面省略了，太多了。
```

在蓝牙开发中，常用的 UUID 分为两类：**16 位的标准 UUID** 和 **128 位的自定义 UUID**。标准 UUID 由蓝牙 SIG 分配，用于定义常见的服务和特征，而自定义 UUID 则用于特定应用的自定义服务和特征。

### 常用的 16 位标准 UUID

| UUID   | 名称                          | 说明                    |
| ------ | ----------------------------- | ----------------------- |
| 0x1800 | Generic Access                | 通用访问服务            |
| 0x1801 | Generic Attribute             | 通用属性服务            |
| 0x180A | Device Information            | 设备信息服务            |
| 0x180F | Battery Service               | 电池服务                |
| 0x181D | Weight Scale                  | 体重秤服务              |
| 0x181C | User Data                     | 用户数据服务            |
| 0x1805 | Current Time Service          | 当前时间服务            |
| 0x181B | Continuous Glucose Monitoring | 连续血糖监测服务        |
| 0x181E | Bond Management               | 绑定管理服务            |
| 0x1823 | Fitness Machine               | 健身器材服务            |
| 0x1826 | Insulin Delivery              | 胰岛素输送服务          |
| 0x180D | Heart Rate                    | 心率服务                |
| 0x1802 | Immediate Alert               | 即时警报服务            |
| 0x1803 | Link Loss                     | 链接丢失服务            |
| 0x1804 | Tx Power                      | 发送功率服务            |
| 0x1809 | Health Thermometer            | 健康温度计服务          |
| 0x1812 | Human Interface Device        | 人机交互设备服务（HID） |
| 0x1814 | Running Speed and Cadence     | 跑步速度和节奏服务      |
| 0x1816 | Cycling Speed and Cadence     | 自行车速度和节奏服务    |
| 0x1818 | Cycling Power                 | 自行车功率服务          |

### 常用的特征 UUID

| UUID   | 名称                                       | 说明                 |
| ------ | ------------------------------------------ | -------------------- |
| 0x2A00 | Device Name                                | 设备名称             |
| 0x2A01 | Appearance                                 | 外观                 |
| 0x2A04 | Peripheral Preferred Connection Parameters | 外围设备首选连接参数 |
| 0x2A19 | Battery Level                              | 电池电量             |
| 0x2A37 | Heart Rate Measurement                     | 心率测量             |
| 0x2A38 | Body Sensor Location                       | 身体传感器位置       |
| 0x2A39 | Heart Rate Control Point                   | 心率控制点           |
| 0x2A29 | Manufacturer Name String                   | 制造商名称字符串     |
| 0x2A23 | System ID                                  | 系统 ID              |
| 0x2A24 | Model Number String                        | 型号字符串           |
| 0x2A25 | Serial Number String                       | 序列号字符串         |
| 0x2A26 | Firmware Revision String                   | 固件版本字符串       |
| 0x2A27 | Hardware Revision String                   | 硬件版本字符串       |
| 0x2A28 | Software Revision String                   | 软件版本字符串       |
| 0x2A50 | PnP ID                                     | 即插即用 ID          |
| 0x2A2B | Current Time                               | 当前时间             |
| 0x2A2A | Date Time                                  | 日期时间             |
| 0x2A35 | Blood Pressure Measurement                 | 血压测量             |
| 0x2A49 | Blood Pressure Feature                     | 血压特征             |
| 0x2A52 | Glucose Measurement Context                | 血糖测量上下文       |

### 自定义 UUID

如果需要定义自定义服务或特征，可以使用 128 位 UUID。以下是一个示例：

```c
#define CUSTOM_SERVICE_UUID     "12345678-1234-5678-1234-56789abcdef0"
#define CUSTOM_CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"
```

### 使用示例

假设你要实现一个带有电池服务和自定义服务的 BLE 设备，以下是定义和注册服务的示例：

```c
#include <stdint.h>
#include <stdio.h>
#include <string.h>

// 示例：定义电池服务和自定义服务的 UUID
#define BATTERY_SERVICE_UUID            0x180F
#define BATTERY_LEVEL_CHARACTERISTIC_UUID 0x2A19
#define CUSTOM_SERVICE_UUID             "12345678-1234-5678-1234-56789abcdef0"
#define CUSTOM_CHARACTERISTIC_UUID      "12345678-1234-5678-1234-56789abcdef1"

// 示例：定义服务和特征的结构体
typedef struct {
    uint16_t uuid;
    uint8_t value[20];
} gatt_characteristic_t;

typedef struct {
    uint16_t uuid;
    gatt_characteristic_t characteristics[2];
} gatt_service_t;

// 初始化服务和特征
void init_services(gatt_service_t* battery_service, gatt_service_t* custom_service) {
    // 初始化电池服务
    battery_service->uuid = BATTERY_SERVICE_UUID;
    battery_service->characteristics[0].uuid = BATTERY_LEVEL_CHARACTERISTIC_UUID;
    battery_service->characteristics[0].value[0] = 100;  // 假设电池电量为100%

    // 初始化自定义服务
    custom_service->uuid = 0x0000;  // 自定义 UUID 在实际使用中需要处理
    strncpy((char*)custom_service->characteristics[0].value, CUSTOM_SERVICE_UUID, sizeof(custom_service->characteristics[0].value));
    strncpy((char*)custom_service->characteristics[1].value, CUSTOM_CHARACTERISTIC_UUID, sizeof(custom_service->characteristics[1].value));
}

int main() {
    gatt_service_t battery_service;
    gatt_service_t custom_service;

    init_services(&battery_service, &custom_service);

    // 输出服务和特征信息
    printf("Battery Service UUID: 0x%04X\n", battery_service.uuid);
    printf("Battery Level Characteristic UUID: 0x%04X, Value: %d%%\n",
        battery_service.characteristics[0].uuid, battery_service.characteristics[0].value[0]);

    printf("Custom Service UUID: %s\n", custom_service.characteristics[0].value);
    printf("Custom Characteristic UUID: %s\n", custom_service.characteristics[1].value);

    return 0;
}
```

### 总结

了解和使用常用的 BLE UUID 有助于开发和实现符合规范的蓝牙应用。标准 UUID 提供了丰富的预定义服务和特征，而自定义 UUID 则允许你根据具体需求扩展和实现个性化功能。

# uuid换算

128位的和16位、32位的可以有公式进行换算。



sdp协议定义了128bit的uuid的16bit写法。

base uuid

```
00000000-0000-1000-8000-00805F9B34FB
```

其他的uuid都是在这个上面改的。

协议uuid

```
0001:SDP
0002：RESERVED
0003：RFCOMM
0004：tcp
0005：tcs-bin
0006：tcs-at
0007：att
0008：obex
0009：ip
000a：ftp
000c：http
0017：avctp
0019：avdtp
0100：l2cap
```



# 一些uuid分析

## 0x1800

0x1800 是通用属性配置文件（GATT Profile）中定义的一个服务 UUID，称为 **"Generic Access"（通用访问）**。该服务主要用于定义设备的基本连接属性，包括设备名称、外观、连接参数等。这些信息在设备发现和连接过程中非常重要。

### Generic Access Service (通用访问服务)

- **UUID**: 0x1800
- **服务名称**: Generic Access
- **服务描述**: 提供设备的基本连接属性，包括设备名称、外观和首选连接参数等。

### Generic Access Service 中的常见特征

| 特征 UUID | 特征名称                                   | 描述                                                 |
| --------- | ------------------------------------------ | ---------------------------------------------------- |
| 0x2A00    | Device Name                                | 设备名称，提供一个可读的设备名称。                   |
| 0x2A01    | Appearance                                 | 设备外观，描述设备的外观类别。                       |
| 0x2A04    | Peripheral Preferred Connection Parameters | 外围设备首选连接参数，提供连接的首选参数。           |
| 0x2AA6    | Central Address Resolution                 | 中心地址解析，指示设备是否支持地址解析。             |
| 0x2AC9    | Resolvable Private Address Only            | 仅可解析的私有地址，指示设备仅使用可解析的私有地址。 |

### 使用示例

假设你要定义一个带有 Generic Access 服务的 BLE 设备，以下是定义和注册服务的示例：

```c
#include <stdint.h>
#include <stdio.h>
#include <string.h>

// 示例：定义 Generic Access 服务和特征的 UUID
#define GENERIC_ACCESS_SERVICE_UUID             0x1800
#define DEVICE_NAME_CHARACTERISTIC_UUID         0x2A00
#define APPEARANCE_CHARACTERISTIC_UUID          0x2A01
#define PREFERRED_CONN_PARAMS_CHARACTERISTIC_UUID 0x2A04

// 示例设备名称和外观
#define DEVICE_NAME "MyBLEDevice"
#define APPEARANCE_GENERIC 0x0000  // 通用外观

typedef struct {
    uint16_t uuid;
    uint8_t value[20];
} gatt_characteristic_t;

typedef struct {
    uint16_t uuid;
    gatt_characteristic_t characteristics[3];
} gatt_service_t;

// 初始化 Generic Access 服务和特征
void init_generic
```

## 0x2A01

0x2A01 是通用属性配置文件（GATT Profile）中定义的一个特征 UUID，称为 **"Appearance"（外观）**。它用于描述设备的外观类别，便于其他设备识别设备的类型。这个特征的值是一个 16 位的字段，表示设备的外观类别。

### Appearance Characteristic (外观特征)

- **UUID**：0x2A01
- **特征名称**：Appearance
- **特征描述**：描述设备的外观类别，例如手表、心率监测器、电话等。
- **数据类型**：16 位无符号整数（uint16）

### Appearance 值示例

Appearance 特征的值是一个 16 位整数，对应不同类型设备的外观类别。以下是一些常见的 Appearance 值示例：

| 值（十六进制） | 外观类别                  | 描述                    |
| -------------- | ------------------------- | ----------------------- |
| 0x0000         | Unknown                   | 未知                    |
| 0x0040         | Generic Phone             | 通用电话                |
| 0x0080         | Generic Computer          | 通用计算机              |
| 0x00C0         | Generic Watch             | 通用手表                |
| 0x00C1         | Watch: Sports Watch       | 运动手表                |
| 0x0140         | Generic Clock             | 通用时钟                |
| 0x0180         | Generic Display           | 通用显示器              |
| 0x01C0         | Generic Remote Control    | 通用遥控器              |
| 0x0200         | Generic Eye-glasses       | 通用眼镜                |
| 0x0240         | Generic Tag               | 通用标签                |
| 0x0280         | Generic Keyring           | 通用钥匙扣              |
| 0x02C0         | Generic Media Player      | 通用媒体播放器          |
| 0x0300         | Generic Barcode Scanner   | 通用条形码扫描器        |
| 0x0340         | Generic Thermometer       | 通用温度计              |
| 0x0380         | Generic Heart Rate Sensor | 通用心率传感器          |
| 0x03C0         | Generic Blood Pressure    | 通用血压计              |
| 0x0400         | Generic Human Interface   | 通用人机界面设备（HID） |
| 0x0440         | Keyboard                  | 键盘                    |
| 0x0480         | Mouse                     | 鼠标                    |
| 0x04C0         | Joystick                  | 游戏杆                  |
| 0x0500         | Gamepad                   | 游戏手柄                |
| 0x0540         | Digitizer Tablet          | 数字化平板              |
| 0x0580         | Card Reader               | 卡片读取器              |
| 0x05C0         | Digital Pen               | 数字笔                  |
| 0x0600         | Barcode Scanner           | 条形码扫描器            |

### 使用示例

在 GATT 服务中，Appearance 特征通常作为通用访问服务（Generic Access Service, UUID: 0x1800）的一部分被定义。以下是一个 GATT 服务定义示例，其中包含 Appearance 特征：

```c
#include <stdint.h>
#include <stdio.h>

// 示例：定义一个 GATT 服务，包括 Appearance 特征
#define GATT_APPEARANCE_UUID    0x2A01

// 示例外观类别：运动手表 (Sports Watch)
#define APPEARANCE_SPORTS_WATCH 0x00C1

typedef struct {
    uint16_t uuid;
    uint16_t value;
} gatt_characteristic_t;

gatt_characteristic_t appearance_characteristic = {
    .uuid = GATT_APPEARANCE_UUID,
    .value = APPEARANCE_SPORTS_WATCH
};

void print_characteristic(gatt_characteristic_t characteristic) {
    printf("Characteristic UUID: 0x%04X, Value: 0x%04X\n", characteristic.uuid, characteristic.value);
}

int main() {
    print_characteristic(appearance_characteristic);
    return 0;
}
```

### 总结

Appearance 特征（UUID: 0x2A01）用于描述 BLE 设备的外观类别，有助于其他设备识别其类型。通过设置不同的外观值，设备可以提供更多的上下文信息，使配对和连接的设备能够根据设备类型进行适当的处理和交互。

# 参考资料

1、对Android蓝牙UUID的理解

http://dxjia.cn/2016/01/29/android-bluetooth-uuid/

2、蓝牙UUID编码

https://blog.csdn.net/qq_37389133/article/details/79412836

3、蓝牙概念

http://www.cnblogs.com/hshy/p/8268025.html

4、通用属性配置文件（GATT）及其服务，特性与属性介绍

http://blog.chinaunix.net/uid-21411227-id-5750680.html

5、各种通用蓝牙UUID列表

https://blog.csdn.net/qq_15003505/article/details/75315049

6、

https://blog.csdn.net/andry05/article/details/81118383

7、蓝牙UUID及其128位换算

https://blog.csdn.net/zhangjs0322/article/details/39048509

8、【BLE-CC2640】CC2640之使用自定义128bit的UUID

http://www.voidcn.com/article/p-vuyeyimy-eo.html

9、Service Discovery

这里对uuid写得很详细。

https://www.bluetooth.com/specifications/assigned-numbers/service-discovery