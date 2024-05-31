---
title: 蓝牙之LE Audio
date: 2023-08-02 19:35:11
tags:
	- 蓝牙
---

--

在今年的在美国消费电子展（Consumer Electronics Show，CES 2020）上，蓝牙技术联盟（Bluetooth Special Interest Group，Bluetooth SIG）公开了即将应用在音频方面的下一代蓝牙技术标准“LE Audio”（Low Energy Audio，低功耗音频），这不同于一般的蓝牙格式，如蓝牙5（Bluetooth 5），这是蓝牙音频的新标准。

也就是说，未来蓝牙音频将支持两种工作模式。最新推出的LE Audio将基于低功耗蓝牙无线通信(Bluetooth Low Energy)，而Classic Audio将基于经典蓝牙无线通信(Bluetooth Classic)。

# 资源收集

stm32官网这篇文章很好，对各个usecase描述简单清晰。

https://wiki.st.com/stm32mcu/wiki/Connectivity:Introduction_to_Bluetooth_LE_Audio

# 简介

下面是关于蓝牙LE Audio的简介：

| 名称     | 蓝牙LE Audio                                                 |
| -------- | ------------------------------------------------------------ |
| 发布日期 | 2020年1月                                                    |
| 概述     | 蓝牙LE Audio是蓝牙技术联盟推出的新一代蓝牙音频标准。它建立在蓝牙低功耗（LE）技术之上，旨在提供更好的音频质量、更低的功耗和更丰富的功能。 |
| 主要特点 | - 支持多流音频传输（Multistream Audio）  <br />- 低能耗语音（Low Energy Voice） <br /> - 支持更好的音频编解码器（Codec Support）<br /> - 提供更好的听力辅助功能（Hearing Aid Support） |
| 应用领域 | - 无线耳机（Wireless Earbuds） <br />- 便携式音箱（Portable Speakers） <br />- 汽车音频系统（Automotive Audio Systems）<br /> - 耳聋助听器（Hearing Aids）等。 |

LE Audio标准的推出为蓝牙音频设备带来了许多新的机会和功能，使得蓝牙技术在音频领域有了更广泛的应用。

# 我应该怎么学习leaudio的开发

学习LE Audio的开发可以通过以下步骤进行：

1. **了解基础知识**：首先，你需要了解蓝牙技术的基础知识，包括蓝牙低功耗（LE）技术的原理、蓝牙协议栈以及蓝牙音频的相关概念。

2. **学习LE Audio标准**：深入研究蓝牙技术联盟发布的LE Audio标准文档，了解其架构、协议、特性和规范要求。

3. **掌握开发工具**：熟悉并掌握用于LE Audio开发的工具和平台，例如蓝牙开发套件、蓝牙调试工具等。

4. **参考示例代码**：查阅蓝牙技术联盟或其他相关资源中的LE Audio示例代码，理解其实现原理和代码结构。

5. **开发和调试**：根据学习的知识和参考资料，开始自己的LE Audio开发项目，并通过调试工具和设备进行验证和调试。

6. **持续学习和更新**：由于技术不断更新和演进，保持学习和了解最新的LE Audio技术发展和更新，以便不断提升自己的开发能力。

通过以上步骤，你可以逐步掌握LE Audio的开发技能，并在实践中不断提升自己的能力。

# LE Audio标准文档内容概要

LE Audio 标准文档的内容概要通常包括以下主题：

1. **介绍和背景**：LE Audio 标准文档通常会介绍 LE Audio 的背景、发展历程以及主要的技术目标。这一部分通常会概述 LE Audio 相对于传统蓝牙音频的优势和特点。

2. **架构和协议**：LE Audio 标准文档会详细介绍 LE Audio 的架构和协议设计。这包括了多流音频传输、低能耗语音、新的音频编解码器支持等方面的内容。文档可能会提供协议栈的层级结构图以及各层之间的通信协议描述。

3. **特性和功能**：LE Audio 标准文档会列举 LE Audio 提供的特性和功能，例如多流音频传输、低功耗语音、听力辅助功能支持等。这部分通常会详细说明每个特性的实现原理和使用场景。

4. **编解码器支持**：LE Audio 标准文档会介绍 LE Audio 支持的音频编解码器，包括新的低能耗编解码器和高质量编解码器的特点和性能比较。

5. **应用场景和用例**：LE Audio 标准文档会列举一些 LE Audio 的应用场景和典型用例，例如无线耳机、便携式音箱、汽车音频系统和听力辅助器等。

6. **测试和认证**：最后，LE Audio 标准文档可能会提供与 LE Audio 相关的测试要求和认证流程，以确保产品符合标准并能够顺利通过认证。

以上是 LE Audio 标准文档可能包含的主要内容概要。具体的文档内容可能会根据不同版本和发布时间有所变化，建议查阅最新版本的文档以获取最准确的信息。

# 哪些芯片支持了le audio

目前，支持 LE Audio 的芯片厂商和型号可能在不断增加，但以下是一些主要的芯片厂商和型号，它们已经或者可能会支持 LE Audio：

| 厂商         | 芯片型号            | 备注                                                         |
| ------------ | ------------------- | ------------------------------------------------------------ |
| Qualcomm     | QCC514x、QCC305x 等 | Qualcomm 的蓝牙芯片通常会支持最新的蓝牙标准，因此 QCC514x 和 QCC305x 等型号有望支持 LE Audio。 |
| Nordic       | nRF52 系列          | Nordic Semiconductor 的 nRF52 系列芯片在蓝牙低功耗领域具有较高的知名度，有望支持 LE Audio。 |
| Cypress      | PSoC 6 系列         | Cypress 的 PSoC 6 系列芯片具有较强的蓝牙功能，可能会支持 LE Audio。 |
| Dialog       | DA1469x 系列        | Dialog Semiconductor 的 DA1469x 系列芯片支持蓝牙 5.1 标准，有望支持 LE Audio。 |
| Silicon Labs | EFR32 系列          | Silicon Labs 的 EFR32 系列芯片在蓝牙领域有一定的市场份额，可能会支持 LE Audio。 |
| MediaTek     | MT2511 等           | MediaTek 的一些蓝牙芯片型号，如 MT2511，可能会支持 LE Audio。 |
| TI           | CC26xx、CC13xx 等   | 德州仪器（TI）的一些蓝牙芯片型号，如 CC26xx 和 CC13xx 等，可能会支持 LE Audio。 |

请注意，以上列出的芯片型号仅是一些主要厂商和型号，实际上可能还有其他厂商和型号的芯片也支持 LE Audio。建议在选择芯片时，查阅厂商提供的最新文档，以确认其是否支持 LE Audio。

# 支持LEAudio的手机

安卓 13 系统虽然原生支持蓝牙 LE Audio，但是 Pixel 7 系列并未提供该功能。而 **Xperia 1 IV 和 Xperia 5 IV 两款手机将会通过更新率先支持蓝牙 LE Audio。**



Xperia 1 V 和 Xperia 5 V 两款机型支持蓝牙 LE Audio 后，可以使用低复杂性通信编解码器（LC3）。LC3 具有像 aptX Adaptive 这样的动态音频缩放功能。

从理论上讲，蓝牙 LE Audio 和 LC3 比其他主流蓝牙技术消耗更少的功率并提供更大的范围，同时还提供更小的延迟。

https://m.ithome.com/html/673535.htm

# pipewire对leaudio的支持

截至2024年，PipeWire 已经开始对 LE Audio（低功耗音频）提供支持。以下是关于 PipeWire 支持 LE Audio 的一些关键点：

| 特性       | 详情                                       |
| ---------- | ------------------------------------------ |
| 支持协议   | 支持 LE Audio 协议，包括 LC3 编解码器      |
| 低功耗     | 利用低功耗蓝牙技术，延长设备电池寿命       |
| 多音频流   | 支持多路音频流，实现更灵活的音频处理       |
| 高质量音频 | 提供高质量音频传输，满足更高的音频体验需求 |
| 兼容性     | 与现有蓝牙音频设备的兼容性正在逐步完善     |

### 具体功能
1. **LC3 编解码器**：LC3（低复杂度通信编解码器）是 LE Audio 的核心，提供高效的音频压缩和解压缩。
2. **多路音频流**：支持同时传输多个独立的音频流，适用于不同的音频设备。
3. **低延迟**：优化延迟性能，适合实时音频应用，例如游戏和视频通话。

### 当前状态
PipeWire 的 LE Audio 支持还在持续开发和完善中。开发者社区正积极贡献代码，解决兼容性和性能问题。

### 如何使用
要使用 PipeWire 的 LE Audio 支持，可以：
1. 确保系统中安装了最新版本的 PipeWire。
2. 配置蓝牙设备，并确保支持 LE Audio。
3. 使用 PipeWire 的配置工具进行必要的设置和调试。

有关详细的配置和使用指南，可以参考 PipeWire 的官方文档和社区资源。

# BAP

从版本 5.66 开始，添加了对 BAP（基本音频配置文件）的初始支持，BAP 是负责流控制的 LE Audio 的重要组成部分。

该插件被认为是实验性的，依赖于 ISO 套接字才能工作，因此需要更改以下设置才能启用它：

```
Experimental = true

# Enables kernel experimental features, alternatively a list of UUIDs
# can be given.
# a6695ace-ee7f-4fb9-881a-5fac66c629af (BlueZ Experimental Offload Codecs)
# 6fbaf188-05e0-496a-9885-d6ddfdb4e03e (BlueZ Experimental ISO socket)
# Defaults to false.
KernelExperimental = 6fbaf188-05e0-496a-9885-d6ddfdb4e03e
```



虽然对 PulseAudio 和 Pipewire 等的适当支持仍在进行中，但可以通过以下命令使用 bluetoothctl 进行测试：



https://www.bluez.org/le-audio-support/



蓝牙® 低功耗音频还基于蓝牙® 5.2 可选功能：同步通道。

这是链路层功能。

此功能允许通过新连接传输流：同步流。

有两种类型的同步流：

* 连接同步流 (CIS)：使用户能够通过蓝牙® 连接获得音频流。这是处理蓝牙低功耗音频的经典方法（一台设备一个连接，例如耳机）。通过两个 CIS，用户可以将同步音频流传输到两个不同的设备（用于耳塞或助听器）

* 广播等时流 (BIS)：使用户能够向任何能够接收该音频流的接收器广播一个或两个音频流。它不需要连接，这意味着可以有无限数量的接收器。

这两种类型的同步流为蓝牙®低功耗添加了新功能：

* 它定义了整个流媒体时间的系统延迟（没有任何漂移）。该延迟低于经典蓝牙®音频）。

* 同时它还定义了重传。应用程序可以请求优先考虑尽可能低的延迟的系统（这可能会导致由于最小重传而丢失一些数据包），或者优先考虑更好的质量的系统（这确保接收所有数据包，但可能导致更高的延迟）。

|                           HFP/HSP                            |                             A2DP                             |     Bluetooth® LE Audio with BAP 带 BAP 的蓝牙® LE 音频      |
| :----------------------------------------------------------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
| Data is sent over SCO (Synchronous Connection Oriented) 数据通过 SCO（面向同步连接）发送 | Data is sent over ACL (Asynchronous Connection Oriented) 数据通过 ACL（面向异步连接）发送 | Data is sent over Isochronous data stream (CIS or BIS) 数据通过同步数据流（CIS 或 BIS）发送 |
|               Data is continuous 数据是连续的                |               Data is continuous 数据是连续的                |     Data is synchronized on a timestamp 数据按时间戳同步     |
|       There is no retransmission in SCO SCO中没有重传        | All packets are transmitted, leading to an infinity of retransmissions if the link has bad quality 所有数据包都会被传输，如果链路质量较差，则会导致无限重传 | Data can be retransmitted, but has a validity in time, becoming obsolete after a certain time 数据可以重传，但有时间有效性，过了一定时间就过时了 |
| Latency is always the same but is not defined 延迟始终相同但未定义 | Latency is not defined and can have some lags or drifts. 延迟未定义，可能会有一些滞后或漂移。 | Latency is always defined in the system and cannot change during the stream. 延迟始终在系统中定义，并且在流传输期间不能更改。 |

# zephyr的leaudio实现

现在就是相关资料太少，无论哪个系统的，我都要看一看。

https://docs.zephyrproject.org/latest/connectivity/bluetooth/api/audio/bluetooth-le-audio-arch.html

# LE audio BIS 音频播放

使用 BlueZ 实现 BLE Audio Broadcast Isochronous Stream (BIS) 的音频播放涉及一些特定步骤。由于 BLE Audio BIS 是一个相对较新的蓝牙功能，BlueZ 可能需要特定版本支持这些功能。在开始之前，请确保您的 BlueZ 版本支持 BLE Audio 规范，特别是 ISOchronous Channels (ISO)。

### 前提条件

1. **确保系统环境**：
   - 一个支持 BLE Audio 的蓝牙适配器。
   - BlueZ 和内核版本支持 ISOchronous Channels。

2. **安装所需库**：
   - `pybluez` 和 `dbus-python` 用于蓝牙操作和 D-Bus 交互。
   - GStreamer 或其他音频播放库。

```bash
pip install pybluez dbus-python
sudo apt-get install gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good
```

### BLE Audio BIS 实现步骤

#### 1. 设置 BLE 广播

要设置 BLE 广播，我们需要定义广播参数，并将音频数据传输到广播通道。以下是一个简单的 Python 示例代码，用于初始化 BLE 广播并设置 BIS。

#### 2. 初始化蓝牙和 D-Bus

```python
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

def setup_dbus():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    return bus

def register_broadcast(bus):
    adapter_path = "/org/bluez/hci0"
    adapter = dbus.Interface(bus.get_object("org.bluez", adapter_path), "org.freedesktop.DBus.Properties")
    adapter.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"),
                             "org.bluez.BassManager1")
    
    broadcast_params = {
        "Interval": dbus.UInt16(10),
        "Latency": dbus.UInt16(30),
        "PHY": dbus.UInt16(1),
        "ChannelMap": dbus.UInt16(0x07),
        "TxPower": dbus.Int16(0)
    }
    
    manager.RegisterBroadcast(broadcast_params)

def main():
    bus = setup_dbus()
    register_broadcast(bus)

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
```

#### 3. 使用 GStreamer 播放音频

要将音频数据流传输到 BLE 广播通道，可以使用 GStreamer 从文件或麦克风获取音频数据，并通过蓝牙发送。以下是一个简单的 GStreamer 管道示例：

```bash
gst-launch-1.0 filesrc location=your_audio_file.mp3 ! decodebin ! audioconvert ! audioresample ! autoaudiosink
```

将其整合到 Python 脚本中：

```python
import subprocess

def start_audio_stream(file_path):
    gst_command = [
        "gst-launch-1.0", "filesrc", f"location={file_path}", "!", "decodebin", "!", "audioconvert", "!", 
        "audioresample", "!", "autoaudiosink"
    ]
    subprocess.run(gst_command)

if __name__ == "__main__":
    audio_file = "your_audio_file.mp3"
    start_audio_stream(audio_file)
```

### 完整的代码整合

以下是将 BLE 广播和音频播放整合在一起的完整示例代码：

```python
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import subprocess

def setup_dbus():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    return bus

def register_broadcast(bus):
    adapter_path = "/org/bluez/hci0"
    adapter = dbus.Interface(bus.get_object("org.bluez", adapter_path), "org.freedesktop.DBus.Properties")
    adapter.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"),
                             "org.bluez.BassManager1")
    
    broadcast_params = {
        "Interval": dbus.UInt16(10),
        "Latency": dbus.UInt16(30),
        "PHY": dbus.UInt16(1),
        "ChannelMap": dbus.UInt16(0x07),
        "TxPower": dbus.Int16(0)
    }
    
    manager.RegisterBroadcast(broadcast_params)

def start_audio_stream(file_path):
    gst_command = [
        "gst-launch-1.0", "filesrc", f"location={file_path}", "!", "decodebin", "!", "audioconvert", "!", 
        "audioresample", "!", "autoaudiosink"
    ]
    subprocess.run(gst_command)

def main():
    bus = setup_dbus()
    register_broadcast(bus)

    audio_file = "your_audio_file.mp3"
    start_audio_stream(audio_file)

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
```

### 总结

通过上述步骤和代码示例，你可以使用 Python 和 BlueZ 实现 BLE Audio BIS 音频播放功能。确保使用支持 BLE Audio 的设备和 BlueZ 版本，调整配置以匹配具体的应用需求。

# 安卓手机怎么进行leaudio连接？手机怎么决定是使用A2DP还是leaudio

在安卓手机上进行LE Audio连接，需要确保手机的蓝牙堆栈和硬件支持蓝牙5.2及以上版本，同时安卓操作系统要支持LE Audio功能。以下是步骤和关键点：

**1. 确认设备支持**
- **硬件支持**：确保你的安卓手机硬件支持蓝牙5.2及以上版本。
- **软件支持**：安卓系统版本需要支持LE Audio，通常是Android 13及以上版本。

**2. 配对和连接LE Audio设备**
在安卓设备上，配对和连接LE Audio设备的步骤与经典蓝牙设备相似：

1. **打开蓝牙**：
   - 进入设置 > 连接 > 蓝牙，确保蓝牙已打开。

2. **扫描设备**：
   - 系统会自动扫描附近的蓝牙设备，找到你的LE Audio设备。

3. **配对设备**：
   - 选择你的LE Audio设备进行配对。配对过程中，设备可能会要求输入PIN码或确认配对请求。

**3. 决定使用A2DP还是LE Audio**
安卓设备自动选择合适的音频协议（A2DP或LE Audio）取决于以下因素：

1. **设备能力**：设备广播的蓝牙服务和配置文件决定了连接的类型。支持LE Audio的设备会广播支持LE Audio的服务。
2. **优先级和用户设置**：如果设备同时支持A2DP和LE Audio，系统可能基于优先级和用户设置选择协议。
3. **应用需求**：某些应用程序可能会指定使用哪种音频协议。

**4. 检查连接协议**
- 在安卓系统中，通常无法直接查看使用的是A2DP还是LE Audio。但是，如果连接的是LE Audio设备，系统会优先选择LE Audio协议，因为它在功耗和音质方面更具优势。
- 一些第三方应用程序可以显示详细的蓝牙连接信息，例如`Bluetooth Scanner`或`BLE Scanner`，这些应用程序可以帮助你查看设备连接的具体细节。

**5. 配置LE Audio**
- LE Audio设备可能会有专门的应用程序，用于管理设备和音频设置。下载并安装这些应用程序，可以帮助你更好地配置和管理LE Audio连接。

以下是简要步骤的Markdown表格：

| 步骤                     | 详细操作                                   |
| ------------------------ | ------------------------------------------ |
| 确认设备支持             | 确保手机和音频设备支持蓝牙5.2及以上版本    |
| 打开蓝牙                 | 设置 > 连接 > 蓝牙，确保蓝牙已打开         |
| 扫描设备                 | 自动扫描附近的蓝牙设备                     |
| 配对设备                 | 选择LE Audio设备进行配对，确认配对请求     |
| 决定使用A2DP还是LE Audio | 系统自动选择，优先使用LE Audio             |
| 检查连接协议             | 使用第三方应用查看详细连接信息（可选）     |
| 配置LE Audio             | 使用专用应用程序管理设备和音频设置（可选） |

**注意事项**：

- 确保设备固件和操作系统都是最新版本，以支持最新的蓝牙功能。
- 某些功能可能需要设备制造商提供的软件支持，例如固件更新或专用管理应用程序。

# android leaudio

https://developer.android.com/develop/connectivity/bluetooth/ble-audio/overview?hl=zh-cn

蓝牙低功耗音频 (LEA) 可确保用户能够接收高保真音频，而不会牺牲电池续航时间，并可让用户在不同的使用情形之间无缝切换。Android 13（API 级别 33）包含对 LEA 的内置支持。

在 LEA 源设备市场份额不断扩大之前，

大多数 LEA 耳机都将采用双模式。

用户应该能够在其双模式耳机上配对和设置这两种传输方式。

# stm32 leaudio

https://wiki.st.com/stm32mcu/wiki/Connectivity:Introduction_to_Bluetooth_LE_Audio



音频框架的基础是音频流管理，由基本音频配置文件 (BAP) [[7\]](https://wiki.st.com/stm32mcu/wiki/Connectivity:Introduction_to_Bluetooth_LE_Audio#cite_note-bap-7) 定义。它是蓝牙®低功耗音频的强制性配置文件。它定义了流类型、配置、功能、质量、延迟等。


BAP 与三种服务一起使用：

- 发布的音频功能服务 (PACS)：用于公开设备的音频功能。
- 音频流控制服务（ASCS）：启用配置单播流。
- 广播音频扫描服务（BASS）：允许请求客户端代表服务器扫描广播音频流。


BAP 定义了两种类型的流：单播和广播，

## 单播

单播是基于连接的同步流 (CIS) 的连接音频流。

这意味着通过单播，您可以通过 CIS 创建连接的音频流。

==要创建单播流，首先需要一个 ACL 连接来通过 GATT 和 LLCP 交换所有有用信息。==

单播分为两个角色：

单播客户端：建立与单播服务器的连接，发现其功能并配置音频流。该角色由智能手机、笔记本电脑、电视等使用。

单播服务器：通告其角色，公开其功能，接受单播服务器配置音频流。耳机、扬声器、某些助听器、某些耳塞甚至麦克风都可以使用此角色。

此外，单播客户端可以同步流式传输到两个单播服务器。

为了通过 ACL 连接启动单播音频流，单播客户端和服务器交换有关流质量、重传、音频通道数量（单声道/立体声）和延迟的信息。

stream可以是：

1、单向的（用于音乐），双向的（用于通话）。这个是client根据server列出的服务里挑选执行。

2、低质量的，也可以是高质量的。

3、低延迟，或者高可靠。

主要的usecase是：

1、一个手机连接到一个耳机。

![Figure 5.1 Unicast with a headphone](images/random_name/800px-Connectivity_introduction_ble_audio_unicast_headphone.png)

2、一个手机连接到2个耳机。

![Figure 5.2 Unicast with some earbuds](images/random_name/800px-Connectivity_introduction_ble_audio_unicast_earbuds.png)

## 广播

广播是一种非连接的stream。

发送方通过BIS广播音频数据。

通过扩展广告和定期广告来发布广播信息。

任何可以扫描到这个stream的设备都可以收听。

这个是一个新的usecase，允许的接收设备数量无限。

这个stream一般是没有加密的，但是你可以加密。

只能是单向传播。

因为广播是没有连接的，用户需要一种方式来同步到stream的状态。

而耳机这类设备一般是没有屏幕的。

所以蓝牙协议在这里增加了一个新的role。

这个role被叫做广播助理。

这个role一般是手机来实现。

手机来扫描发现广播stream，并把它发送到耳机上。

广播定义了4种角色。

1、广播源。发出广播的设备。

2、广播接收器。接收广播的设备，一般是耳机。

3、扫描委托者。暴露一些信息，等待广播助手。

4、广播助手，一般是手机。



主要是usecase是：

1、一个手机或者电脑把音频发送给多个设备。

2、在公共场所发布公告。

3、翻译。



# 参考资料

1、

https://www.eet-china.com/news/202001081019.html

2、

https://wiki.archlinux.org/title/bluetooth_headset