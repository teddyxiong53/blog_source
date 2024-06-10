---
title: 蓝牙之ble
date: 2018-07-23 22:28:29
tags:
	- 蓝牙

---

--

# 什么是ble

低功耗蓝牙（Bluetooth Low Energy，简称BLE），也称为蓝牙4.0及更高版本，是一种通信技术，旨在实现低能耗、短距离通信。它是经典蓝牙（Classic Bluetooth）的一种扩展，专门设计用于低功耗应用和物联网（IoT）设备连接。

BLE的主要特点包括：

1. **低功耗：** BLE专为电池供电设备设计，其工作方式和协议结构经过优化，以实现尽可能低的能耗。这使得BLE非常适合需要长时间运行的设备，如可穿戴设备、传感器、健康监测设备等。

2. **短距离通信：** BLE适用于短距离通信，通常在几米到十数米范围内。这有助于减少干扰和提高通信的安全性。

3. **快速连接：** BLE设备可以在非常短的时间内建立连接，以减少连接延迟，适用于需要快速响应的应用场景。

4. **多设备连接：** BLE支持多设备并行连接，这对于物联网环境中的设备互联非常重要。

5. **简化的协议栈：** BLE的协议栈相对较轻量，适用于资源受限的设备。这有助于减少开发成本和功耗。

6. **广播和扫描：** BLE设备可以通过广播发送数据，其他设备可以通过扫描接收广播数据。这种方式适用于一对多通信，如室内定位。

7. **异步数据传输：** BLE支持异步数据传输，适合断断续续的低频数据传输。

由于BLE的低功耗特性和适用范围广泛的特点，它在健康监测、智能家居、可穿戴设备、物联网、工业自动化等领域得到了广泛应用。

# ble优点

1、高可靠性
对于无线通信而言，由于电磁波在传输过程中容易受很多因素的干扰，例如，障碍物的阻挡、天气状况等，因此，无线通信系统在数据传输过程中具有内在的不可靠性。蓝牙技术联盟 SIG 在指定蓝牙 4.0 规范时已经考虑到了这种数据传输过程中的内在的不确定性，在射频，基带协议，链路管理协议中采用可靠性措施，包括：差错检测和矫正，进行数据编解码，数据降噪等，极大地提高了蓝牙无线数据传输的可靠性，另外，使用自适应调频技术，能最大程度地减少和其他 2.4G 无线电波的串扰。

2、低成本、低功耗
低功耗蓝牙支持两种部署方式：双模式和单模式，一般智能机上采用双模式，外设一般采用 BLE 单模。

低功耗设计：蓝牙 4.0 版本强化了蓝牙在数据传输上的低功耗性能，功耗较传统蓝牙降低了 90%。

传统蓝牙设备的待机耗电量一直是其缺陷之一，这与传统蓝牙技术采用16至32个频道进行广播有很大关系，而低功耗蓝牙仅适用 3 个广播通道，且每次广播时射频的开启时间也有传统的 22.5ms 减少到 0.6~1.2ms，这两个协议规范的改变，大幅降低了因为广播数据导致的待机功耗。

低功耗蓝牙设计用深度睡眠状态来替换传统蓝牙的空闲状态，在深度睡眠状态下，主机 Host 长时间处于超低的负载循环 Duty Cycle 状态，只在需要运作时由控制器来启动，由于主机较控制器消耗的能源更多，因此这样的设计也节省了更多的能源。

3、快速启动/瞬间连接
此前蓝牙版本的启动速度非常缓慢，2.1 版本的蓝牙启动连接需要 6s 时间，而蓝牙4.0版本仅需要3ms 即可完成。

4、传输距离增强
传统蓝牙传输距离一般为 2-10 米，而蓝牙4.0的有效传输距离可以达到 60~100米，传输距离大大提高，极好的开拓了蓝牙技术的应用前景。

# le audio是基于ble吗

是的，LE Audio（Low Energy Audio）是基于低功耗蓝牙（BLE）技术的一项扩展，旨在为蓝牙设备提供更强大的音频功能。LE Audio扩展了BLE技术，使其能够支持高质量的音频传输和更广泛的音频应用。

传统的低功耗蓝牙（BLE）在音频传输方面有一些限制，因为其设计主要是为了低功耗通信，而不是高质量的音频传输。LE Audio的引入旨在弥补这些限制，为蓝牙设备提供更好的音频体验。

LE Audio引入了以下一些新的功能：

1. **LC3编解码器：** LE Audio引入了更高效的音频编解码器，称为LC3（Low Complexity Communication Codec）。LC3编解码器可以在相对低的比特率下提供高质量的音频传输，从而实现更好的音频效果。

2. **多流传输：** LE Audio支持多个音频流同时传输，这对于多个听者之间共享音频或实现多个音频设备的协同工作非常有用。

3. **广播音频：** LE Audio引入了支持广播音频的功能，这意味着BLE设备可以广播音频流，其他设备可以扫描并连接以接收音频流，这有助于实现一对多的音频广播。

4. **声学共享：** LE Audio引入了声学共享功能，允许多个用户共享同一音频源，例如在公共场所或公共交通工具中。

总之，LE Audio是基于BLE技术的一项扩展，旨在提供更好的音频体验和更广泛的音频应用。它使BLE设备能够支持高质量的音频传输，从而扩展了BLE的应用范围。

https://shumeipai.nxez.com/2023/08/07/bluetooth-protocol-capture-based-on-raspberry-pi.html



# le audio的包结构

LE Audio的包结构是指在蓝牙低功耗音频（LE Audio）传输中，数据在传输过程中如何组织和封装。LE Audio引入了新的数据包结构以支持音频传输。以下是LE Audio的包结构概述：

在LE Audio中，音频数据通过一系列的音频数据包进行传输。每个音频数据包包含了一定数量的音频采样数据。音频数据包通常会通过BLE连接从发送端传输到接收端。

LE Audio的包结构如下：

1. **头部（Header）：** 每个音频数据包的开头包含一个头部，其中包含了一些控制信息，如数据包类型和流标识等。

2. **音频采样数据（Audio Samples）：** 在头部之后是音频采样数据。这部分包含了音频信号的采样值。数据包的大小和数据传输速率决定了每个数据包中包含的音频样本数量。

3. **纠错检验（Error Correction）：** 为了提高传输的可靠性，一些音频数据包可能包含纠错检验信息。这有助于在数据传输过程中检测和纠正错误。

4. **标识和同步（Identification and Synchronization）：** 在BLE连接中，数据包同步和识别非常重要。数据包中通常包含了标识和同步信息，以确保接收端可以正确解析数据包。

5. **连接维护信息（Connection Maintenance）：** LE Audio在数据包中还包含了一些连接维护信息，以确保数据的连续传输。

需要注意的是，LE Audio的包结构可能会因不同的音频编码、数据传输速率、连接参数等而有所不同。具体的包结构会根据实际应用和配置进行调整。这只是一个一般的概述，详细的包结构可以在LE Audio相关的蓝牙规范文档中找到。

# le audio一个包的大小

LE Audio的一个音频数据包的大小可以根据具体的配置和使用情况而有所不同。然而，LE Audio的一个典型音频数据包的大小通常在几十字节到一百多字节之间。

具体的包大小取决于以下因素：

1. **音频编码：** 使用不同的音频编码器（如LC3）会影响一个数据包中包含的音频样本数量，从而影响包的大小。

2. **采样率：** 音频数据的采样率（每秒采样次数）也会影响一个数据包中包含的音频样本数量。

3. **数据传输速率：** 数据传输速率决定了每个数据包中可用的比特数，进而影响包的大小。

4. **连接参数：** 蓝牙连接参数，如连接间隔和数据包长度等，也会影响一个数据包的大小。

5. **纠错码：** 数据包中是否包含纠错码信息以及纠错码的类型也会影响包的大小。

一般情况下，LE Audio的音频数据包大小在20字节到100字节之间。这个范围可以用于传输高质量音频，同时保持较低的延迟和功耗。

如果您在特定应用中需要精确的数据包大小，请参考相关的蓝牙规范和技术文档，这些文档会详细描述LE Audio的包结构和参数配置。

# 当前的导游讲解器是基于什么技术

当前的导游讲解器通常基于无线通信技术，其中常用的技术之一是无线语音传输技术。这些导游讲解器使用无线通信技术来实现导游和游客之间的实时语音传输，以便在旅游景点、博物馆、展览等场所提供有声导览和讲解服务。

以下是一些可能用于导游讲解器的无线通信技术：

1. **无线电频率通信：** 这是较早期使用的无线技术，通常基于无线电频率的传输。导游和游客使用不同的频率来进行语音传输，类似于对讲机的原理。

2. **蓝牙技术：** 低功耗蓝牙（BLE）可以用于导游讲解器，它可以在短距离范围内实现实时的语音传输，同时具备较低的功耗。

3. **Wi-Fi技术：** Wi-Fi技术可以用于实现更远距离的语音传输，但通常需要更多的功耗。导游和游客可以通过连接到相同的Wi-Fi网络来进行语音交流。

4. **RFID技术：** 射频识别（RFID）技术可以用于在特定区域内触发语音播放。游客带着携带RFID标签的设备，在接近特定位置时，设备会自动播放相应的讲解内容。

这些技术可以根据实际需求和场景选择。导游讲解器的设计要考虑到语音传输的稳定性、实时性、通信范围、功耗以及用户友好性等因素。不同的技术有不同的优势和限制，选择合适的技术取决于特定的应用需求。

# 基本信息

经典蓝牙bt。1.0到2.0到3.0，都是。其中1.0和2.0，叫传统蓝牙，3.0叫高速蓝牙。

低功耗蓝牙ble。4.0是。



CC2540是ble单模芯片。是不兼容传统蓝牙的。

安卓要4.3以上版本才能支持ble。



常说的蓝牙4.0一般就是指ble。

**ble默认不能传输音乐。**

**ble就是用来传输少量数据的。**



大家可以理解为service就是java里的class，characteristic是class里的public方法。所以我们应该先找到class，再调用其方法。

再往下想，写和读肯定是两个方法，所以也会是两个characteristic。

service和characteristic的uuid都是通信之前双方约定好的。android端在上文说的discoverService之后，查看有没有对应的uuid，如果有，就可以发起通信了。





![v4f6bxnfb3](../images/random_name/v4f6bxnfb3.jpeg)



# 规范

参考资料

1、

https://www.cnblogs.com/xiaorenwu702/p/4304378.html

# ble地址类型

BLE（蓝牙低功耗）设备的地址类型分为以下几种，每种地址类型有不同的用途和特性。理解这些地址类型有助于更好地管理和开发 BLE 设备。

### BLE 地址类型

1. **Public Device Address (公共设备地址)**
   - **特征**：固定且全球唯一，由蓝牙设备地址 (BD_ADDR) 组成，包含一个 24 位公司标识符（OUI）和一个 24 位设备标识符。
   - **用途**：用于需要唯一标识的设备，如手机或笔记本电脑。

2. **Random Device Address (随机设备地址)**
   - **分类**：
     1. **Static Random Address (静态随机地址)**
        - **特征**：设备启动时生成，除非设备重启或电池更换，否则不会改变。静态地址的最高两个位设置为 11。
        - **用途**：提供稳定性，适用于隐私要求较低的设备。
     2. **Private Random Address (私有随机地址)**
        - **进一步分类**：
          - **Resolvable Private Address (可解析的私有地址)**
            - **特征**：使用一个由设备和配对设备共享的密钥生成，定期更改以提供隐私保护。配对设备可以解析地址以识别设备。
            - **用途**：隐私保护，适用于定期广播的设备，如健身追踪器。
          - **Non-Resolvable Private Address (不可解析的私有地址)**
            - **特征**：随机生成且短时间内使用，不包含可用于识别设备的持久信息。
            - **用途**：提供最高级别的隐私保护，适用于短时间广播的设备。

### 地址类型的具体表示

每种 BLE 地址类型在数据包中都有相应的表示方法。

| 地址类型               | 表示方法 | 说明               |
| ---------------------- | -------- | ------------------ |
| Public                 | 0x00     | 公共设备地址       |
| Random Static          | 0x01     | 静态随机地址       |
| Private Resolvable     | 0x02     | 可解析的私有地址   |
| Private Non-Resolvable | 0x03     | 不可解析的私有地址 |

### 地址生成和使用示例

1. **生成和使用公共设备地址**
   公共设备地址由设备制造商分配，通常在设备出厂时已固定。

2. **生成静态随机地址**
   静态随机地址在设备首次启动时生成，并存储在设备的非易失性存储器中。
   
   ```c
   // 生成静态随机地址示例（伪代码）
   uint8_t random_address[6];
   random_address[0] = random_byte();
   random_address[1] = random_byte();
   random_address[2] = random_byte();
   random_address[3] = random_byte();
   random_address[4] = random_byte();
   random_address[5] = (random_byte() & 0x3F) | 0xC0;  // 设置最高两位为11
```
   
3. **生成可解析的私有地址**
   可解析的私有地址使用设备和配对设备共享的 IRK（Identity Resolving Key）生成。蓝牙协议栈通常会处理这个过程。

### 使用示例

假设你要实现一个 BLE 设备，并希望支持多种地址类型。以下是如何在代码中实现地址选择的示例：

```c
#include <stdio.h>
#include <stdint.h>

// 生成一个随机字节的示例函数
uint8_t random_byte() {
    return rand() % 256;
}

// 生成静态随机地址的函数
void generate_static_random_address(uint8_t address[6]) {
    for (int i = 0; i < 5; ++i) {
        address[i] = random_byte();
    }
    address[5] = (random_byte() & 0x3F) | 0xC0;  // 设置最高两位为11
}

// 打印地址
void print_address(const char *label, uint8_t address[6]) {
    printf("%s: %02X:%02X:%02X:%02X:%02X:%02X\n", label, address[5], address[4], address[3], address[2], address[1], address[0]);
}

int main() {
    uint8_t static_random_address[6];
    generate_static_random_address(static_random_address);
    print_address("Static Random Address", static_random_address);

    // 其他地址类型的生成和使用可以类似实现
    return 0;
}
```

### 总结

不同类型的 BLE 地址在不同的应用场景下有各自的优势和适用性。理解这些地址类型及其特性，可以帮助开发者更好地设计和实现 BLE 设备的通信和隐私保护功能。



# BLE 标准的配对和绑定过程

BLE（低能耗蓝牙）标准的配对和绑定过程涉及设备发现、密钥交换、身份验证和加密等多个步骤。以下是详细步骤：

### 1. 设备发现

在配对过程开始之前，两个 BLE 设备需要相互发现对方。

- **扫描设备**：一个设备（通常是中心设备，如手机）会扫描周围的设备。
- **广播设备**：另一个设备（通常是外围设备，如智能手环）会广播其存在。

### 2. 配对过程

配对过程包括密钥交换和身份验证，用于建立加密链接。配对过程有三种主要方法，分别是“Just Works”、“Passkey Entry”和“Numeric Comparison”。

1. **Just Works**：不需要用户输入任何信息，适用于低安全性需求的场景。
2. **Passkey Entry**：一方输入另一个设备显示的6位数密码，用于中等安全性需求。
3. **Numeric Comparison**：双方显示6位数数字，用户确认数字是否相同，用于高安全性需求。

### 3. 密钥分配

配对过程中，设备会生成和交换密钥，用于保护后续的数据传输。

1. **临时密钥（TK）**：用于生成短期会话密钥的临时密钥。
2. **短期会话密钥（STK）**：配对过程中生成的会话密钥。
3. **长时间密钥（LTK）**：生成并存储用于后续连接的长期密钥。
4. **身份信息**：设备可能会交换身份信息（IRK，Identity Resolving Key）和设备地址。

### 4. 加密链接的建立

配对过程成功后，设备会使用生成的会话密钥来加密传输链路。

### 5. 绑定过程

绑定是指设备在配对后保存密钥，以便后续连接时能够快速建立加密链路。绑定过程确保了设备在断开连接后重新连接时能够安全地通信。

### 配对示例代码

以下是一个简化的示例代码，展示了如何在嵌入式系统中使用 BLE 堆栈进行配对和绑定过程。注意，这是一个伪代码示例，实际实现将依赖于具体的 BLE 堆栈和硬件平台。

```c
#include <ble.h>

// 初始化BLE配对
void init_ble_pairing() {
    // 设置配对参数
    ble_gap_sec_params_t sec_params;
    memset(&sec_params, 0, sizeof(sec_params));
    sec_params.bond = 1; // 启用绑定
    sec_params.mitm = 0; // 关闭MITM保护
    sec_params.io_caps = BLE_GAP_IO_CAPS_NONE; // 配对方式
    sec_params.min_key_size = 7; // 最小密钥长度
    sec_params.max_key_size = 16; // 最大密钥长度

    // 启动配对过程
    sd_ble_gap_sec_params_reply(conn_handle, BLE_GAP_SEC_STATUS_SUCCESS, &sec_params, NULL);
}

// 处理配对请求
void on_ble_gap_evt_sec_params_request(ble_gap_evt_sec_params_request_t *p_sec_params_request) {
    // 回复安全参数请求
    ble_gap_sec_keyset_t sec_keyset;
    memset(&sec_keyset, 0, sizeof(sec_keyset));
    sec_keyset.keys_periph.ltk_len = 16;

    sd_ble_gap_sec_params_reply(conn_handle, BLE_GAP_SEC_STATUS_SUCCESS, &sec_params, &sec_keyset);
}

// 处理加密状态变化
void on_ble_gap_evt_auth_status(ble_gap_evt_auth_status_t *p_auth_status) {
    if (p_auth_status->auth_status == BLE_GAP_SEC_STATUS_SUCCESS) {
        // 配对和加密成功
    } else {
        // 配对或加密失败
    }
}

int main() {
    // 初始化BLE堆栈
    ble_stack_init();

    // 初始化配对过程
    init_ble_pairing();

    // 主循环
    while (1) {
        // 处理BLE事件
        ble_evt_t evt;
        if (ble_evt_get(&evt)) {
            switch (evt.header.evt_id) {
                case BLE_GAP_EVT_SEC_PARAMS_REQUEST:
                    on_ble_gap_evt_sec_params_request(&evt.evt.gap_evt.params.sec_params_request);
                    break;
                case BLE_GAP_EVT_AUTH_STATUS:
                    on_ble_gap_evt_auth_status(&evt.evt.gap_evt.params.auth_status);
                    break;
                default:
                    break;
            }
        }
    }

    return 0;
}
```

这个示例展示了如何初始化配对过程、处理配对请求和处理加密状态变化。实际实现中需要处理更多的事件和错误，并根据具体的 BLE 堆栈和硬件平台进行调整。

# 使用bluez的api，让板子作为ble server，手机可以搜索并连接到ble server上

以下是一个简单的示例代码，展示如何使用BlueZ的API将嵌入式Linux设备作为BLE Server，使手机可以搜索并连接到该BLE Server。

**步骤1：安装BlueZ**
确保你的板子上已经安装了BlueZ。可以通过以下命令安装：

```sh
sudo apt-get update
sudo apt-get install bluez
```

**步骤2：编写BLE Server代码**

下面是一个Python示例代码，使用`pydbus`库（BlueZ的DBus接口）来创建一个BLE Server。

```python
from gi.repository import GLib
from pydbus import SystemBus
import dbus
import dbus.service
import dbus.mainloop.glib

# 定义BLE服务UUID和特征UUID
SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0'
CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1'

class BLEAdvertisement(dbus.service.Object):
    PATH = '/org/bluez/example/advertisement'

    def __init__(self, bus):
        self.path = self.PATH
        self.bus = bus
        self.ad_type = 'peripheral'
        self.service_uuid = SERVICE_UUID
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        return {
            'Type': self.ad_type,
            'ServiceUUIDs': [self.service_uuid]
        }

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ss', out_signature='v')
    def Get(self, interface, property):
        return self.GetAll(interface)[property]

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ssv')
    def Set(self, interface, property, value):
        pass

    @dbus.service.method('org.freedesktop.DBus.ObjectManager', out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        return {
            self.path: {
                'org.freedesktop.DBus.Properties': {
                    'Type': self.ad_type,
                    'ServiceUUIDs': [self.service_uuid]
                }
            }
        }

class BLEApplication(dbus.service.Object):
    PATH = '/org/bluez/example/service'

    def __init__(self, bus):
        self.path = self.PATH
        self.bus = bus
        self.service = None
        self.characteristic = None
        dbus.service.Object.__init__(self, bus, self.path)

        self.add_service()
        self.add_characteristic()

    def add_service(self):
        self.service = BLEService(self.bus, self.path, 0, SERVICE_UUID, True)
        self.bus.register_object(self.service)

    def add_characteristic(self):
        self.characteristic = BLECharacteristic(self.bus, self.service.path, 0, CHARACTERISTIC_UUID, ['read', 'write'])
        self.bus.register_object(self.characteristic)

class BLEService(dbus.service.Object):
    def __init__(self, bus, path, index, uuid, primary):
        self.path = f"{path}/service{index}"
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        return {
            'UUID': self.uuid,
            'Primary': self.primary
        }

class BLECharacteristic(dbus.service.Object):
    def __init__(self, bus, path, index, uuid, flags):
        self.path = f"{path}/char{index}"
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        return {
            'UUID': self.uuid,
            'Flags': self.flags
        }

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ss', out_signature='v')
    def Get(self, interface, property):
        return self.GetAll(interface)[property]

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ssv')
    def Set(self, interface, property, value):
        pass

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = SystemBus()

ad_manager = bus.get("org.bluez", "/org/bluez/hci0")
ad_manager.RegisterAdvertisement(BLEAdvertisement(bus), {}, reply_handler=print("Advertisement registered"), error_handler=print("Advertisement register failed"))

app = BLEApplication(bus)
mainloop = GLib.MainLoop()
mainloop.run()
```

**步骤3：运行BLE Server**

```sh
sudo python3 ble_server.py
```

**说明：**

1. **BLEAdvertisement**类负责BLE广告。
2. **BLEApplication**类负责管理BLE服务和特征。
3. **BLEService**类表示一个BLE服务。
4. **BLECharacteristic**类表示一个BLE特征。

运行代码后，你的设备将成为一个BLE Server，可以被手机搜索到并连接。

**注意：**
你可能需要修改`SERVICE_UUID`和`CHARACTERISTIC_UUID`以适应你的需求。这些UUID应当是符合BLE规范的128位UUID。

# 板端做le audio cis sink

为了将板子配置为LE Audio CIS（Connected Isochronous Stream）Sink，以下是如何使用BlueZ API实现的步骤和示例代码。请注意，LE Audio和CIS是蓝牙5.2及以上版本的新特性，可能需要更新的BlueZ版本和内核支持。

### 步骤1：确保系统支持

1. **内核**：确保使用支持蓝牙5.2及以上的内核。
2. **BlueZ**：安装最新版本的BlueZ。可以从源码编译安装。

### 步骤2：安装必要的依赖

确保安装了必要的Python包：

```sh
sudo apt-get install python3-dbus
sudo apt-get install python3-gi
sudo pip3 install pydbus
```

### 步骤3：编写CIS Sink示例代码

以下Python代码展示了如何设置LE Audio CIS Sink：

```python
from gi.repository import GLib
from pydbus import SystemBus
import dbus
import dbus.service
import dbus.mainloop.glib

# 定义LE Audio服务UUID和特征UUID
LE_AUDIO_SERVICE_UUID = '00001850-0000-1000-8000-00805f9b34fb'
LE_AUDIO_CHARACTERISTIC_UUID = '00002bb1-0000-1000-8000-00805f9b34fb'

class LEAudioAdvertisement(dbus.service.Object):
    PATH = '/org/bluez/example/advertisement'

    def __init__(self, bus):
        self.path = self.PATH
        self.bus = bus
        self.ad_type = 'peripheral'
        self.service_uuid = LE_AUDIO_SERVICE_UUID
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        return {
            'Type': self.ad_type,
            'ServiceUUIDs': [self.service_uuid]
        }

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ss', out_signature='v')
    def Get(self, interface, property):
        return self.GetAll(interface)[property]

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ssv')
    def Set(self, interface, property, value):
        pass

    @dbus.service.method('org.freedesktop.DBus.ObjectManager', out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        return {
            self.path: {
                'org.freedesktop.DBus.Properties': {
                    'Type': self.ad_type,
                    'ServiceUUIDs': [self.service_uuid]
                }
            }
        }

class LEAudioApplication(dbus.service.Object):
    PATH = '/org/bluez/example/service'

    def __init__(self, bus):
        self.path = self.PATH
        self.bus = bus
        self.service = None
        self.characteristic = None
        dbus.service.Object.__init__(self, bus, self.path)

        self.add_service()
        self.add_characteristic()

    def add_service(self):
        self.service = LEAudioService(self.bus, self.path, 0, LE_AUDIO_SERVICE_UUID, True)
        self.bus.register_object(self.service)

    def add_characteristic(self):
        self.characteristic = LEAudioCharacteristic(self.bus, self.service.path, 0, LE_AUDIO_CHARACTERISTIC_UUID, ['read', 'notify'])
        self.bus.register_object(self.characteristic)

class LEAudioService(dbus.service.Object):
    def __init__(self, bus, path, index, uuid, primary):
        self.path = f"{path}/service{index}"
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        return {
            'UUID': self.uuid,
            'Primary': self.primary
        }

class LEAudioCharacteristic(dbus.service.Object):
    def __init__(self, bus, path, index, uuid, flags):
        self.path = f"{path}/char{index}"
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        dbus.service.Object.__init__(self, bus, self.path)

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface):
        return {
            'UUID': self.uuid,
            'Flags': self.flags
        }

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ss', out_signature='v')
    def Get(self, interface, property):
        return self.GetAll(interface)[property]

    @dbus.service.method('org.freedesktop.DBus.Properties', in_signature='ssv')
    def Set(self, interface, property, value):
        pass

    @dbus.service.method('org.bluez.GattCharacteristic1', in_signature='', out_signature='ay')
    def ReadValue(self):
        return dbus.ByteArray(b'\x01')

    @dbus.service.method('org.bluez.GattCharacteristic1', in_signature='ay')
    def WriteValue(self, value):
        print(f"Received value: {value}")

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = SystemBus()

ad_manager = bus.get("org.bluez", "/org/bluez/hci0")
ad_manager.RegisterAdvertisement(LEAudioAdvertisement(bus), {}, reply_handler=print("Advertisement registered"), error_handler=print("Advertisement register failed"))

app = LEAudioApplication(bus)
mainloop = GLib.MainLoop()
mainloop.run()
```

### 步骤4：运行LE Audio CIS Sink服务

```sh
sudo python3 le_audio_cis_sink.py
```

### 说明

1. **LEAudioAdvertisement**类负责LE Audio广告。
2. **LEAudioApplication**类管理LE Audio服务和特征。
3. **LEAudioService**类表示一个LE Audio服务。
4. **LEAudioCharacteristic**类表示一个LE Audio特征。

这段代码将把你的设备设置为一个LE Audio CIS Sink，允许手机搜索和连接。你可以根据需求修改UUID和特征值。请确保BlueZ和内核支持LE Audio特性。

**注意：**
LE Audio和CIS是相对较新的特性，实际实现过程中可能需要调整配置和调试。确保你的设备固件和驱动程序支持这些特性。

# bluetoothctl控制ble



# 参考资料

1、普及一下什么是蓝牙和BLE，看完让你秒懂

https://www.sohu.com/a/167206747_404276

2、ESP32必杀技 - 蓝牙配网篇

http://club.gizwits.com/thread-4966-1-1.html

3、蓝牙4.0 BLE与传统蓝牙之间的兼容性

http://blog.51cto.com/cto521/1638654

4、请问，蓝牙4.0协议能不能传音频或文件? 

https://bbs.csdn.net/topics/391493417?page=1

5、Android BLE4.0(蓝牙通信)

https://www.jianshu.com/p/2b4620c52d47

6、

https://e2echina.ti.com/question_answer/wireless_connectivity/bluetooth/f/103/t/111227

7、Android蓝牙通信过程详解

https://cloud.tencent.com/developer/news/216558

8、

https://blog.csdn.net/zzfenglin/article/details/51304084