---
title: BTstack（1）
date: 2018-12-11 19:17:12
tags:
	- 蓝牙

---



--

# 基本信息

需要的目标板提供这些东西就可以工作：

1、串口。

2、CPU。

3、clock实现。



有几个缩写要先明确一下：

1、H2，是HCI USB 。

2、H4 。是HCI UART

3、H5。三线UART 。

我现在只管usb的。



手册章节

```
1、welcome信息。
2、quick start
	通用工具
	从github下载btstack代码
	开始
3、btstack架构
	单线程设计
	不阻塞
	不人为限制buffer
	静态内存
4、怎样配置btstack
	在btstack_config.h里配置
	HAVE_XX宏
	ENABLE_XX宏
	HCI控制器
	内存配置指令
	nvm指令
	源代码结构
	运行loop配置
	HCI传输配置
	服务
	packet handle配置
	蓝牙HCI包日志
5、协议
	HCI
	L2CAP
	RFCOMM
	SDP
	BNEP
	ATT
	SMP
6、profile
	GAP
	SPP
	PAN
	HSP
	HFP
	GAP LE
	GATT
7、实现GATT服务
8、嵌入式example
	一大堆的例子
9、HCI接口
10、移植到其他平台
```





在我的Ubuntu笔记本上运行。

需要先安装libusb。

```
sudo apt-get install gcc git libusb-1.0 pkg-config
```

然后在btstack/port/libusb目录下，make。

这个会自动把所有的example都编译的，并且把二进制生成到当前目录下。

运行其中一个例子：

```
teddy@teddy-ThinkPad-SL410:~/work/bt/btstack/port/libusb$ sudo ./le_counter 
Packet Log: /tmp/hci_dump.pklg
BTstack counter 0001
USB Path: 01
BTstack up and running on 00:1A:7D:DA:71:13.
```

可以看到可以正常运行。

我的蓝牙适配器是CSR的。

我们看看这个le_counter的代码是怎么写的。

main函数是在libus/main.c里。这里面调用了btstack_main这个函数在每个example里。



看看libusb目录下的btstack_config.h的内容：

```
HAVE_XX宏有4个：
1、有malloc。
2、有posix file no
3、有btstack stdin
4、有posix time
ENABLE_XX宏有：
1、使能ble。
2、使能经典蓝牙。
3、使能hfp 
4、
```

HAVE_PORTAUDIO这个有效。

当前btstack_memory_init这个函数相当于空的。里面的多个宏都没有生效。

可以通过gdb调试看到。



运行a2dp_sink_demo的例子。在手机上可以搜索到一个A2DP Sink Demo的蓝牙名字，可以连接上来。

然后播放歌曲。打印如下。当然实际上没有声音播放出来。这个不管。

```
teddy@teddy-ThinkPad-SL410:~/work/bt/btstack/port/libusb$ sudo ./a2dp_sink_demo 
Packet Log: /tmp/hci_dump.pklg
Starting BTstack ...
USB Path: 01
BTstack up and running on 00:1A:7D:DA:71:13.
A2DP Sink demo: received SBC codec configuration.
Received SBC configuration:
    - num_channels: 2
    - sampling_frequency: 48000
    - channel_mode: 1
    - block_length: 16
    - subbands: 8
    - allocation_method: 1
    - bitpool_value [2, 51] 

A2DP_SUBEVENT_STREAM_ESTABLISHED 86, 0 
A2DP Sink demo: streaming connection is established, address B4:0B:44:F4:16:8D, a2dp cid 0x56, local_seid 1
A2DP Sink demo: stream started, a2dp cid 0x56, local_seid 1
A2DP Sink demo: stream paused, a2dp cid 0x56, local_seid 1
WAV Writer: Decoding done. Processed totaly 5410 frames:
 - 5410 good
 - 0 bad
WAV Writer: Written 5410 frames to wav file: avdtp_sink.wav
```

这个例子的内容比较多。

最后hci的发送，调用的是usb_send_packet。这个跟每个平台有关系了。

最后调用libusb_submit_transfer。

# a2dp_sink_register_packet_handler 和a2dp_sink_register_media_handler 这2个处理函数的用途

`a2dp_sink_register_packet_handler` 和 `a2dp_sink_register_media_handler` 是 **BTstack** 蓝牙协议栈中用于注册回调函数的函数。这两个函数主要用于 **A2DP Sink**（音频接收端）的功能实现。

1. **`a2dp_sink_register_packet_handler`：**
   
   - 用途：注册处理 A2DP Sink 相关事件的回调函数。
   - 工作原理：当 BTstack 接收到与 A2DP Sink 相关的事件时，会调用注册的回调函数来处理这些事件。
   - 例如，当 A2DP Sink 收到音频数据包时，注册的 `a2dp_sink_register_packet_handler` 回调函数会被 BTstack 调用，从而可以在回调函数中处理接收到的音频数据包。

2. **`a2dp_sink_register_media_handler`：**
   
   - 用途：注册处理 A2DP Sink 媒体数据的回调函数。
   - 工作原理：用于处理音频流的数据，例如解码、播放等。
   - 当 A2DP Sink 收到音频流时，注册的 `a2dp_sink_register_media_handler` 回调函数会被调用，以便对接收到的音频数据进行进一步的处理，如解码和播放。

这两个函数的作用是将应用程序中定义的回调函数注册到 BTstack 中，以便在特定事件发生时得到通知并处理相应的数据。通过这种机制，开发者可以自定义处理 A2DP Sink 相关事件和音频数据的行为，实现音频接收端的功能。

# hci_stack_t

这个可以算是蓝牙协议栈hci内涵的直观体现了。

```
btstack_packet_handler_t 类型的处理函数
	acl_packet_handler
	sco_packet_handler
	iso_packet_handler
	event_handlers
一些链表：
	iso_streams
	le_audio_bigs
```



# l2cap_acl_handler

```c
    if (conn->address_type == BD_ADDR_TYPE_ACL){
        l2cap_acl_classic_handler(handle, packet, size);
    } else {
        l2cap_acl_le_handler(handle, packet, size);
    }
```

从这里也可以看出，acl有经典蓝牙和ble这2种。

# inquiry mode

### 三种模式的对比

| 模式                      | 返回信息                | 规范版本 | 复杂度 | 典型应用场景                 |
| ------------------------- | ----------------------- | -------- | ------ | ---------------------------- |
| INQUIRY_MODE_STANDARD     | BD_ADDR, CoD            | 1.1+     | 最低   | 简单设备发现                 |
| INQUIRY_MODE_RSSI         | BD_ADDR, CoD, RSSI      | 2.0+     | 中等   | 距离感知的设备选择           |
| INQUIRY_MODE_RSSI_AND_EIR | BD_ADDR, CoD, RSSI, EIR | 2.1+     | 最高   | 丰富信息的设备发现（如名称） |

# page scan

作为一个蓝牙软件专家，我来为你详细解释 `page_scan_type_t` 枚举类型中定义的两种模式：`PAGE_SCAN_MODE_STANDARD` 和 `PAGE_SCAN_MODE_INTERLACED`。这两种模式与蓝牙经典（BR/EDR）的 **Page Scan** 过程相关，决定了设备如何监听来自其他设备的连接请求（Paging）。以下是逐一说明：

---

### 背景：蓝牙 Page 和 Page Scan 过程
在蓝牙经典（BR/EDR）中，设备之间的连接建立分为两个角色：
- **Paging 设备**：主动发起连接的设备，发送 Paging 请求以寻找目标设备。
- **Page Scanning 设备**：处于可连接状态的设备，定期监听 Paging 请求。

Page Scan 是被发现设备的一种工作模式，设备在特定频率上监听其他设备的连接请求。`page_scan_type_t` 定义了 Page Scan 的扫描方式，影响设备的可发现速度和功耗。以下是两种模式的含义和区别。

---

### 1. `PAGE_SCAN_MODE_STANDARD` (值为 0)
- **含义**：标准 Page Scan 模式。
- **功能**：
  - 这是蓝牙中最基本的 Page Scan 方式，设备按照标准的时间间隔和频率顺序监听 Paging 请求。
  - 设备在每个扫描窗口内只监听一个频率（从 32 个可能的跳频通道中选择）。
- **工作原理**：
  - Page Scan 使用蓝牙跳频机制，基于设备的时钟（Clock）和地址（BD_ADDR）计算跳频序列。
  - 在标准模式下，设备按顺序扫描这些频率，每次扫描一个固定的时间窗口（通常为 11.25 毫秒，对应 R0 模式）。
  - 扫描间隔（Page Scan Interval）和窗口大小（Page Scan Window）由 GAP（Generic Access Profile）参数控制，例如默认值为 1.28 秒间隔和 11.25 毫秒窗口。
- **蓝牙规范支持**：
  - 从 Bluetooth 1.1 开始支持，是最原始的 Page Scan 模式。
- **特点**：
  - **简单性**：实现简单，功耗较低，因为每次只监听一个频率。
  - **连接时间较长**：由于频率逐一扫描，Paging 设备可能需要多次尝试才能与 Page Scan 设备的频率对齐。
- **适用场景**：
  - 低功耗优先的设备，例如不需要快速建立连接的场景。
  - 兼容性要求高的应用，因为所有蓝牙设备都支持标准模式。
- **BTstack 中的实现**：
  - 在 `src/hci.c` 或 `src/gap.c` 中，通过 `gap_set_page_scan_type(PAGE_SCAN_MODE_STANDARD)` 设置。
  - 对应的 HCI 命令为 `HCI_OP_WRITE_PAGE_SCAN_TYPE`，参数值为 `0x00`。
  - 事件处理中，标准模式不涉及额外的频率切换逻辑。

---

### 2. `PAGE_SCAN_MODE_INTERLACED` (值为 1)
- **含义**：交错式 Page Scan 模式（Interlaced Page Scan）。
- **功能**：
  - 这是一种增强的 Page Scan 方式，设备在每个扫描窗口内监听两个频率，而不是一个。
  - 通过交错扫描（Interlaced Scanning），提高 Paging 设备与 Page Scan 设备频率对齐的概率，从而加快连接建立速度。
- **工作原理**：
  
  - 在交错模式下，设备基于跳频序列选择两个连续的频率（例如 f(k) 和 f(k+1)），并在同一扫描窗口内快速切换监听这两者。
  - 扫描窗口大小通常需要稍大（例如 22.5 毫秒），以容纳两次频率扫描。
  - Paging 设备发送的 ID 数据包（用于 Paging 的初始握手）更容易被捕获，因为扫描频率覆盖范围更广。
- **蓝牙规范支持**：
  - 在 Bluetooth 2.0 中引入，作为对连接性能的优化。
- **特点**：
  - **更快连接**：交错扫描将频率对齐时间平均减少一半，显著缩短连接建立延迟。
  - **功耗稍高**：由于需要监听两个频率并快速切换，功耗和硬件要求略高于标准模式。
  - **硬件依赖**：需要蓝牙控制器支持交错扫描功能（部分老旧芯片可能不支持）。
- **适用场景**：
  - 对连接速度敏感的应用，例如音频设备（耳机、音箱）或需要快速重连的场景。
  - 在密集设备环境中，提高连接成功率。
- **BTstack 中的实现**：
  - 通过 `gap_set_page_scan_type(PAGE_SCAN_MODE_INTERLACED)` 设置。
  - 对应的 HCI 命令为 `HCI_OP_WRITE_PAGE_SCAN_TYPE`，参数值为 `0x01`。
  - 在支持交错模式的控制器上，BTstack 会配置更大的扫描窗口，并处理交错频率的响应。例如：
    ```c
    gap_set_page_scan_type(PAGE_SCAN_MODE_INTERLACED);
    gap_set_page_scan_activity(0x0800, 0x0012); // 1.28s 间隔，22.5ms 窗口
    ```

---

### 两种模式的对比

| 特性           | `PAGE_SCAN_MODE_STANDARD` | `PAGE_SCAN_MODE_INTERLACED` |
| -------------- | ------------------------- | --------------------------- |
| **扫描频率数** | 每次 1 个频率             | 每次 2 个频率               |
| **连接速度**   | 较慢                      | 较快                        |
| **功耗**       | 较低                      | 稍高                        |
| **规范版本**   | 1.1+                      | 2.0+                        |
| **硬件要求**   | 所有设备支持              | 需要控制器支持              |
| **典型应用**   | 低功耗简单设备            | 高性能快速连接设备          |

---

### 在 BTstack 中的使用
在 BTstack 中，`page_scan_type_t` 通常与 GAP（Generic Access Profile）相关的函数一起使用，用于配置设备的可连接性。例如：
```c
// 设置为交错模式以加快连接
gap_set_page_scan_type(PAGE_SCAN_MODE_INTERLACED);
gap_connectable(1); // 开启 Page Scan
```
- **事件处理**：Page Scan 模式本身不直接影响事件类型，但会影响连接建立的时间和成功率。连接成功后，`HCI_EVENT_CONNECTION_COMPLETE` 事件会被触发。
- **硬件依赖**：文档中的“Supported Chipsets”表明，部分芯片（如 TI CC256x、Broadcom BCM 系列）支持交错模式，而低端芯片（如 STM STLC2500D）可能仅支持标准模式。

---

### 总结
- **`PAGE_SCAN_MODE_STANDARD`**：基本的单频率扫描模式，功耗低但连接较慢，适合简单、低功耗场景。
- **`PAGE_SCAN_MODE_INTERLACED`**：交错双频率扫描模式，连接更快但功耗稍高，适合对连接速度敏感的应用。

# hci包类型

### 五种 HCI 包类型的对比

| 类型                    | 值   | 方向        | 用途         | 典型场景        |
| ----------------------- | ---- | ----------- | ------------ | --------------- |
| HCI_COMMAND_DATA_PACKET | 0x01 | Host → Ctrl | 发送命令     | 配置、控制设备  |
| HCI_ACL_DATA_PACKET     | 0x02 | 双向        | 异步数据传输 | GATT、SPP、A2DP |
| HCI_SCO_DATA_PACKET     | 0x03 | 双向        | 同步语音数据 | HFP、HSP 语音   |
| HCI_EVENT_PACKET        | 0x04 | Ctrl → Host | 事件通知     | 状态更新、响应  |
| HCI_ISO_DATA_PACKET     | 0x05 | 双向        | 等时音频数据 | LE Audio        |

# acl和sco包类型

作为一个蓝牙软件专家，我来为你详细解释这些宏定义中涉及的 HCI 数据包类型（`DM`、`DH`、`EV` 等）及其名称的含义。这些宏定义了不同类型 ACL（Asynchronous Connection-Less）和 SCO（Synchronous Connection-Oriented）数据包的最大有效载荷（Payload）大小，单位是字节。这些名称来源于蓝牙核心规范，用于描述数据包的编码方式、带宽效率和纠错能力。以下逐一解析：

---

### 背景：ACL 和 SCO 数据包
- **ACL 数据包**：用于异步数据传输（如 GATT、SPP、A2DP），支持多种编码类型，分为 DM、DH、2DH、3DH 等。
- **SCO 数据包**：用于同步数据传输（如语音），分为 HV 和 EV 类型。
这些类型的命名反映了数据包的调制方式（Modulation）、纠错机制（Error Correction）和带宽利用率。

---

### 1. ACL 数据包类型（DM、DH、2DH、3DH）
ACL 数据包支持多种编码格式，名称中的字母和数字有以下含义：
- **D**：表示数据包（Data Packet）。
- **M**：Medium Rate（中等速率），带前向纠错（FEC）。
- **H**：High Rate（高速率），不带前向纠错，最大化数据吞吐量。
- **2** 或 **3**：表示增强数据率（EDR，Enhanced Data Rate），分别对应 2 Mbps（π/4-DQPSK 调制）和 3 Mbps（8DPSK 调制）。
- **1、3、5**：表示数据包长度（占用的时隙数），分别为 1 时隙、3 时隙、5 时隙。

#### 具体类型解释：
- **`HCI_ACL_DM1_SIZE` (17 字节)**：
  - **DM1**：中等速率，1 时隙，带 2/3 FEC（前向纠错）。
  - 带宽较低，但可靠性高，适合嘈杂环境。
- **`HCI_ACL_DH1_SIZE` (27 字节)**：
  - **DH1**：高速率，1 时隙，无 FEC。
  - 比 DM1 载荷大，适用于干净信道。
- **`HCI_ACL_DM3_SIZE` (121 字节)**：
  - **DM3**：中等速率，3 时隙，带 FEC。
  - 占用 3 个时隙（3.75 ms），载荷增加。
- **`HCI_ACL_DH3_SIZE` (183 字节)**：
  - **DH3**：高速率，3 时隙，无 FEC。
  - 更高吞吐量，适合大数据传输。
- **`HCI_ACL_DM5_SIZE` (224 字节)**：
  - **DM5**：中等速率，5 时隙，带 FEC。
  - 占用 5 个时隙（6.25 ms），可靠性高。
- **`HCI_ACL_DH5_SIZE` (339 字节)**：
  - **DH5**：高速率，5 时隙，无 FEC。
  - 最大化吞吐量，适合高速应用。
- **`HCI_ACL_2DH1_SIZE` (54 字节)**：
  - **2DH1**：EDR 2 Mbps，1 时隙，无 FEC。
  - 使用 π/4-DQPSK 调制，带宽翻倍。
- **`HCI_ACL_3DH1_SIZE` (83 字节)**：
  - **3DH1**：EDR 3 Mbps，1 时隙，无 FEC。
  - 使用 8DPSK 调制，带宽更高。
- **`HCI_ACL_2DH3_SIZE` (367 字节)**：
  - **2DH3**：EDR 2 Mbps，3 时隙，无 FEC。
- **`HCI_ACL_3DH3_SIZE` (552 字节)**：
  - **3DH3**：EDR 3 Mbps，3 时隙，无 FEC。
- **`HCI_ACL_2DH5_SIZE` (679 字节)**：
  - **2DH5**：EDR 2 Mbps，5 时隙，无 FEC。
- **`HCI_ACL_3DH5_SIZE` (1021 字节)**：
  - **3DH5**：EDR 3 Mbps，5 时隙，无 FEC。
  - ACL 中最大的数据包，适合高带宽应用（如 A2DP）。

#### ACL 类型总结：
- **DM vs DH**：DM 带纠错，适合不可靠信道；DH 无纠错，载荷更大。
- **1/3/5**：时隙数越多，数据包越大，但延迟也增加。
- **2DH/3DH**：EDR 模式（Bluetooth 2.0+），通过高级调制提升带宽。

---

### 2. SCO 数据包类型（HV、EV）
SCO 数据包用于同步语音传输，名称中的字母和数字含义如下：
- **H**：High Quality（高质量语音）。
- **V**：Voice（语音）。
- **E**：Enhanced（增强型），支持更高带宽或不同编码。
- **1、2、3、5**：表示不同的语音编码方案或时隙占用。
- **2EV/3EV**：增强型 SCO（eSCO，Bluetooth 2.0+），支持更高带宽。

#### 具体类型解释：
- **`HCI_SCO_HV1_SIZE` (10 字节)**：
  - **HV1**：高质量语音，1 时隙，带 1/3 FEC。
  - 每 1.25 ms 发送 10 字节，64 kbps 带宽（PCM 编码）。
- **`HCI_SCO_HV2_SIZE` (20 字节)**：
  - **HV2**：高质量语音，2 时隙，带 2/3 FEC。
  - 每 2.5 ms 发送 20 字节，同样 64 kbps。
- **`HCI_SCO_HV3_SIZE` (30 字节)**：
  - **HV3**：高质量语音，3 时隙，无 FEC。
  - 每 3.75 ms 发送 30 字节，64 kbps。
- **`HCI_SCO_EV3_SIZE` (30 字节)**：
  - **EV3**：增强型 SCO，3 时隙，无 FEC。
  - 与 HV3 类似，但支持重传，提高可靠性。
- **`HCI_SCO_EV4_SIZE` (120 字节)**：
  - **EV4**：增强型 SCO，带 FEC。
  - 支持更高带宽（如 128 kbps），用于宽带语音。
- **`HCI_SCO_EV5_SIZE` (180 字节)**：
  - **EV5**：增强型 SCO，无 FEC。
  - 最大 288 kbps，适合高质量语音。
- **`HCI_SCO_2EV3_SIZE` (60 字节)**：
  - **2EV3**：EDR 2 Mbps，增强型 SCO。
  - 使用 π/4-DQPSK 调制，提升带宽。
- **`HCI_SCO_2EV5_SIZE` (360 字节)**：
  - **2EV5**：EDR 2 Mbps，增强型 SCO。
  - 高带宽语音传输。
- **`HCI_SCO_3EV3_SIZE` (90 字节)**：
  - **3EV3**：EDR 3 Mbps，增强型 SCO。
  - 使用 8DPSK 调制。
- **`HCI_SCO_3EV5_SIZE` (540 字节)**：
  - **3EV5**：EDR 3 Mbps，增强型 SCO。
  - SCO 中最大的数据包，适合高质量音频。

#### SCO 类型总结：
- **HV**：传统 SCO（Bluetooth 1.1），固定 64 kbps，带或不带 FEC。
- **EV**：增强型 SCO（Bluetooth 2.0+），支持重传和更高带宽。
- **2EV/3EV**：结合 EDR 调制，进一步提升带宽。

---

### 在 BTstack 中的使用
- **ACL 数据包**：
  - 在 `src/hci.c` 中，`hci_send_acl_packet` 根据连接类型选择合适的包类型。
  - 例如，发送大数据时优先使用 `DH5` 或 `3DH5`，由控制器协商。
- **SCO 数据包**：
  - 在支持 SCO 的芯片上，`hci_send_sco_packet` 处理语音数据。
  - 示例：HFP 使用 `HV3` 或 `EV3` 传输语音。
- **硬件依赖**：
  - EDR（2DH/3DH、2EV/3EV）需要 Bluetooth 2.0+ 芯片支持。
  - SCO 支持取决于芯片（如 TI CC256x 支持，Nordic nRF 不支持）。

---

### 总结
- **DM/DH**：ACL 中等/高速率包，带或不带纠错。
- **2DH/3DH**：EDR ACL 包，提升带宽。
- **HV**：传统 SCO 语音包，64 kbps。
- **EV**：增强型 SCO，支持重传和高带宽。
- **2EV/3EV**：EDR SCO 包，进一步优化语音传输。

这些定义帮助开发者选择合适的数据包类型，平衡带宽、延迟和可靠性。如果你想深入某个类型的实现细节或应用场景，可以告诉我，我会进一步分析！

# 逐层解包分析

作为一个蓝牙软件专家，我来为你详细分析蓝牙经典（BR/EDR）中 A2DP（Advanced Audio Distribution Profile）Sink 端连接和播放过程的典型数据包示例，并逐层解包分析。A2DP 是用于单向音频流传输的配置文件，Sink 端（如蓝牙耳机或音箱）接收音频数据并播放。以下示例基于 BTstack 的实现，结合蓝牙核心规范，逐步从 HCI 层到应用层解包。

---

### 背景：A2DP Sink 的工作流程
1. **连接建立**：通过 SDP（服务发现协议）协商 A2DP 服务，创建 L2CAP 信道。
2. **信令协商**：通过 AVDTP（Audio/Video Distribution Transport Protocol）配置音频流参数（如编解码器）。
3. **音频传输**：建立 A2DP 数据流，传输压缩音频（如 SBC 或 AAC）。
4. **播放控制**：通过 AVRCP（Audio/Video Remote Control Profile，可选）控制播放。

我们将重点分析以下三个典型阶段的 HCI 数据包：
1. **HCI 连接建立**。
2. **AVDTP 信令配置**。
3. **A2DP 音频数据传输**。

---

### 1. HCI 连接建立
#### 示例场景
A2DP Source（手机）发起与 Sink（耳机）的连接，Sink 已处于可连接状态（Page Scan）。

#### HCI 数据包示例：连接请求
- **类型**：`HCI_COMMAND_DATA_PACKET (0x01)`（主机 → 控制器）
- **命令**：`HCI_OP_CREATE_CONNECTION`（Opcode: 0x0405）
- **数据包**：
  ```
  0x01 0x05 0x04 0x0D 0x11 0x22 0x33 0x44 0x55 0x66 0x18 0x00 0x00 0x00 0x01 0x00 0x00
  ```
- **解包分析**：
  - `0x01`：包类型（命令包）。
  - `0x05 0x04`：Opcode（创建连接）。
  - `0x0D`：参数长度（13 字节）。
  - `0x11 0x22 0x33 0x44 0x55 0x66`：目标设备地址（BD_ADDR，例如 66:55:44:33:22:11）。
  - `0x18 0x00 0x00`：支持的包类型（DM1, DH1 等）。
  - `0x00`：Page Scan 重复模式。
  - `0x01`：允许角色切换（1 = 允许）。
  - `0x00 0x00`：时钟偏移（未知时为 0）。

#### HCI 数据包示例：连接完成事件
- **类型**：`HCI_EVENT_PACKET (0x04)`
- **事件**：`HCI_EVENT_CONNECTION_COMPLETE`（Event Code: 0x03）
- **数据包**：
  ```
  0x04 0x03 0x0B 0x00 0x40 0x00 0x11 0x22 0x33 0x44 0x55 0x66 0x01 0x00
  ```
- **解包分析**：
  - `0x04`：包类型（事件包）。
  - `0x03`：事件码（连接完成）。
  - `0x0B`：参数长度（11 字节）。
  - `0x00`：状态（0 = 成功）。
  - `0x40 0x00`：连接句柄（例如 0x0040）。
  - `0x11 0x22 0x33 0x44 0x55 0x66`：目标设备地址。
  - `0x01`：链接类型（1 = ACL）。
  - `0x00`：加密模式（0 = 未加密）。

#### 上层解析
- **GAP 层**：完成物理连接后，进入服务发现阶段。
- **SDP 层**：Sink 通过 SDP 查询 Source 的 A2DP 服务（UUID: 0x110B），建立 L2CAP 信道（PSM: 0x0019）。

---

### 2. AVDTP 信令配置
#### 示例场景
连接建立后，Source 和 Sink 通过 AVDTP 协商音频流参数（如使用 SBC 编解码器）。

#### HCI 数据包示例：AVDTP 配置请求
- **类型**：`HCI_ACL_DATA_PACKET (0x02)`（主机 → 控制器）
- **数据包**：
  ```
  0x02 0x40 0x20 0x0E 0x00 0x0A 0x00 0x19 0x00 0x06 0x04 0x01 0x00 0x01 0x02 0x08 0x22
  ```
- **解包分析**：
  - **HCI 层**：
    - `0x02`：包类型（ACL 数据包）。
    - `0x40 0x20`：连接句柄（0x0040）+ PB Flag（2 = 第一个非分片包）。
    - `0x0E 0x00`：数据总长度（14 字节）。
  - **L2CAP 层**：
    - `0x0A 0x00`：L2CAP 数据长度（10 字节）。
    - `0x19 0x00`：信道 ID（PSM: 0x0019，AVDTP）。
  - **AVDTP 层**：
    - `0x06`：信号标识（0x06 = Set Configuration）。
    - `0x04`：ACP（Sink）端事务标签（Transaction Label）+ 包类型（0 = 单包）。
    - `0x01 0x00`：服务类别（0x01 = 媒体传输）+ LOSC（Length of Service Capability，2 字节）。
    - `0x01 0x02`：SBC 编解码器（0x01）+ 参数（0x02，如采样率 44.1 kHz）。
    - `0x08 0x22`：媒体类型（0x08 = 音频）+ 配置参数（0x22，如立体声）。

#### HCI 数据包示例：AVDTP 配置响应
- **类型**：`HCI_ACL_DATA_PACKET (0x02)`（控制器 → 主机）
- **数据包**：
  ```
  0x02 0x40 0x20 0x08 0x00 0x04 0x00 0x19 0x06 0x04 0x00
  ```
- **解包分析**：
  - **HCI 层**：
    - `0x02`：包类型。
    - `0x40 0x20`：连接句柄 + PB Flag。
    - `0x08 0x00`：数据长度（8 字节）。
  - **L2CAP 层**：
    - `0x04 0x00`：L2CAP 数据长度（4 字节）。
    - `0x19 0x00`：信道 ID（AVDTP）。
  - **AVDTP 层**：
    - `0x06`：信号标识（Set Configuration 响应）。
    - `0x04`：事务标签 + 包类型。
    - `0x00`：状态（0 = 成功）。

#### 上层解析
- **AVDTP 层**：协商完成后，Source 和 Sink 同意使用 SBC 编解码器，准备开始流传输。
- **A2DP 层**：建立媒体传输信道，状态变为“OPEN”。

---

### 3. A2DP 音频数据传输
#### 示例场景
Source 开始向 Sink 发送 SBC 编码的音频数据，Sink 接收并解码播放。

#### HCI 数据包示例：音频数据传输
- **类型**：`HCI_ACL_DATA_PACKET (0x02)`（主机 → 控制器）
- **数据包**：
  ```
  0x02 0x40 0x20 0x24 0x00 0x20 0x00 0x19 0x00 0x01 0x01 0x0C [SBC 数据 20 字节]
  ```
- **解包分析**：
  - **HCI 层**：
    - `0x02`：包类型。
    - `0x40 0x20`：连接句柄 + PB Flag。
    - `0x24 0x00`：数据总长度（36 字节）。
  - **L2CAP 层**：
    - `0x20 0x00`：L2CAP 数据长度（32 字节）。
    - `0x19 0x00`：信道 ID（AVDTP 媒体信道）。
  - **AVDTP 层**：
    - `0x00`：事务标签（媒体数据无信令）。
    - `0x01`：包类型（单包）。
    - `0x01`：SBC 数据流标识。
    - `0x0C`：媒体头（Payload Header，例如序列号、时间戳）。
    - `[SBC 数据 20 字节]`：实际音频数据（SBC 编码）。
- **后续包**：连续发送类似数据包，构成音频流。

#### 上层解析
- **A2DP 层**：Sink 接收 AVDTP 数据包，提取 SBC 有效载荷。
- **应用层**：解码 SBC 数据，转换为 PCM 格式，通过 DAC 输出到扬声器。

---

### 数据包逐层总结
| 层级      | 连接建立（HCI Command/Event） | AVDTP 配置（ACL）    | A2DP 数据（ACL）     |
| --------- | ----------------------------- | -------------------- | -------------------- |
| **HCI**   | 0x01 (Cmd), 0x04 (Event)      | 0x02 (ACL)           | 0x02 (ACL)           |
| **L2CAP** | -                             | PSM 0x0019, 信令数据 | PSM 0x0019, 媒体数据 |
| **AVDTP** | -                             | 配置信令（SBC 参数） | 媒体流（SBC 数据）   |
| **A2DP**  | SDP 服务发现                  | 协商编解码器         | 音频流传输           |
| **应用**  | -                             | -                    | 解码播放             |

---

### 在 BTstack 中的实现
- **连接**：`gap_connect` 发起连接，`hci_event_callback` 处理事件。
- **AVDTP**：`avdtp_sink.c` 实现信令和数据流，`a2dp_sink.c` 封装 A2DP 逻辑。
- **数据处理**：`packet_handler` 解析 ACL 数据，调用 `avdtp_packet_handler`。

---

### 总结
1. **连接**：HCI 命令和事件建立 ACL 链接。
2. **配置**：AVDTP 通过 ACL 协商 SBC 参数。
3. **传输**：A2DP 使用 ACL 发送音频流，Sink 解码播放。

如果你需要更详细的某层分析或代码示例，可以告诉我，我会深入讲解！

# hci dump log格式

作为一个蓝牙软件专家，我来为你详细解释 `hci_dump_format_t` 枚举类型中定义的四种 HCI 数据包转储（Dump）格式：`HCI_DUMP_INVALID`、`HCI_DUMP_BLUEZ`、`HCI_DUMP_PACKETLOGGER` 和 `HCI_DUMP_BTSNOOP`。这些格式用于记录和分析 BTstack 中主机（Host）和控制器（Controller）之间的 HCI 数据包，用于调试和协议分析。以下是它们的区别和用途：

---

### 背景：HCI 数据包转储
在蓝牙开发中，HCI 数据包转储是将主机和控制器之间的通信（命令、事件、ACL/SCO 数据）记录到文件的功能。这些记录可以用于：
- 调试协议栈问题。
- 分析连接或数据传输行为。
- 与标准工具（如 Wireshark）集成。

BTstack 支持多种转储格式，每种格式对应不同的文件结构和工具兼容性，由 `hci_dump_format_t` 枚举指定。

---

### 1. `HCI_DUMP_INVALID` (0)
- **含义**：无效格式。
- **功能**：
  - 表示未指定或不支持的转储格式。
  - 通常作为默认值或错误状态，禁用数据包转储功能。
- **文件结构**：
  - 无输出文件生成。
- **用途**：
  - 初始化时的占位符，或关闭转储功能。
- **兼容工具**：
  - 无（不生成任何数据）。
- **BTstack 中的实现**：
  - 在 `src/hci_dump.c` 中，若格式设置为 `HCI_DUMP_INVALID`，则 `hci_dump_packet` 函数不执行任何操作。

---

### 2. `HCI_DUMP_BLUEZ` (1)
- **含义**：BlueZ 格式。
- **功能**：
  - 模仿 Linux BlueZ 协议栈的 HCI 日志格式。
  - BlueZ 是 Linux 系统上的开源蓝牙协议栈，其日志格式被广泛用于嵌入式和桌面开发。
- **文件结构**：
  - 纯文本格式，每行记录一个 HCI 数据包。
  - 每行包含时间戳、方向（发送/接收）和数据包内容（十六进制）。
  - 示例：
    ```
    > 2025-03-11 10:00:00.123 HCI Command: 01 03 0C 00
    < 2025-03-11 10:00:00.124 HCI Event: 04 0E 04 01 03 0C 00
    ```
    - `>` 表示主机发送，`<` 表示控制器返回。
- **用途**：
  - 与 BlueZ 生态兼容，便于 Linux 开发者分析。
  - 适合手动阅读或简单脚本解析。
- **兼容工具**：
  - 可直接阅读，或用文本编辑器查看。
  - 不直接支持 Wireshark，需要转换。
- **BTstack 中的实现**：
  - 在 `hci_dump_posix_bluez.c` 中实现，记录为 ASCII 文本。

---

### 3. `HCI_DUMP_PACKETLOGGER` (2)
- **含义**：Apple PacketLogger 格式。
- **功能**：
  - 专为苹果的 PacketLogger 工具设计的二进制格式，用于 macOS 上的蓝牙调试。
  - PacketLogger 是苹果提供的蓝牙分析工具，广泛用于 iOS/macOS 开发。
- **文件结构**：
  - 二进制文件，扩展名通常为 `.pklg`。
  - 包含头部和多个数据包记录：
    - 头部：文件标识、版本号等。
    - 数据包：时间戳、类型（命令/事件/数据）、方向、内容。
  - 示例（概念性）：
    ```
    [Header: "PKLG" + Version]
    [Packet: TS=123456789, Type=0x01, Dir=Host->Ctrl, Data=01 03 0C 00]
    ```
- **用途**：
  - 在 macOS 环境中调试 BTstack 应用。
  - 分析 iOS 设备与 BTstack 的交互。
- **兼容工具**：
  - Apple PacketLogger（macOS 内置工具）。
  - 不直接兼容 Wireshark，但可通过工具转换。
- **BTstack 中的实现**：
  - 在 `hci_dump_posix_packetlogger.c` 中实现，生成 `.pklg` 文件。

---

### 4. `HCI_DUMP_BTSNOOP` (3)
- **含义**：btsnoop 格式。
- **功能**：
  - 基于 libpcap 的二进制格式，广泛用于蓝牙数据包捕获。
  - 最初由 Android 平台采用，现已成为跨平台标准。
- **文件结构**：
  - 二进制文件，扩展名通常为 `.btsnoop` 或 `.cfa`。
  - 包含全局头部和数据包记录：
    - 头部：文件标识（"btsnoop"）、版本号、数据链路类型（通常为 1002，表示 HCI）。
    - 数据包：时间戳（微秒）、长度、标志（方向）、数据。
  - 示例（概念性）：
    ```
    [Header: "btsnoop\0\0\0\0\1\0\0\3\0\0\0\0"]
    [Packet: TS=123456789012, Len=4, Flags=0x00, Data=01 03 0C 00]
    ```
    - 方向标志：0x00（主机→控制器），0x01（控制器→主机）。
- **用途**：
  - 跨平台蓝牙调试，记录完整通信过程。
  - 与多种分析工具无缝集成。
- **兼容工具**：
  - **Wireshark**：直接打开 `.btsnoop` 文件，解析 HCI、L2CAP 等层。
  - Android 的 btsnoop Viewer。
  - Ellisys Bluetooth Analyzer 等。
- **BTstack 中的实现**：
  - 在 `hci_dump_posix_btsnoop.c` 中实现，生成 Wireshark 可读的 `.btsnoop` 文件。

---

### 四种格式的对比

| 格式           | 值   | 文件类型 | 输出格式 | 主要用途   | 兼容工具                     |
| -------------- | ---- | -------- | -------- | ---------- | ---------------------------- |
| `INVALID`      | 0    | 无       | 无       | 禁用转储   | 无                           |
| `BLUEZ`        | 1    | 文本     | ASCII    | Linux 调试 | 文本编辑器，需转换至其他工具 |
| `PACKETLOGGER` | 2    | 二进制   | .pklg    | macOS 调试 | Apple PacketLogger           |
| `BTSNOOP`      | 3    | 二进制   | .btsnoop | 跨平台分析 | Wireshark、Android 等        |

---

### 在 BTstack 中的使用
- **配置方式**：
  - 在程序启动时通过 `hci_dump_open` 指定格式：
    ```c
    hci_dump_open("hci_dump.btsnoop", HCI_DUMP_BTSNOOP);
    ```
  - 或在编译时通过宏定义启用特定格式。
- **记录数据**：
  - `hci_dump_packet` 函数根据格式记录数据：
    ```c
    hci_dump_packet(HCI_COMMAND_DATA_PACKET, 0, packet, size); // 主机发送
    hci_dump_packet(HCI_EVENT_PACKET, 1, packet, size);       // 控制器返回
    ```
- **平台适配**：
  - `hci_dump_posix.c` 和相关文件根据目标平台（如 POSIX、嵌入式）实现不同格式。

---

### 选择建议
- **调试简单问题**：用 `HCI_DUMP_BLUEZ`，便于手动查看。
- **macOS 开发**：用 `HCI_DUMP_PACKETLOGGER`，与苹果工具集成。
- **全面分析**：用 `HCI_DUMP_BTSNOOP`，兼容 Wireshark，功能最强大。

---

### 总结
- **`INVALID`**：无转储，占位符。
- **`BLUEZ`**：文本格式，适合 Linux 和手动分析。
- **`PACKETLOGGER`**：苹果专用，macOS 调试首选。
- **`BTSNOOP`**：通用二进制格式，跨平台最佳选择。

如果你需要具体格式的生成示例或工具使用指南，可以告诉我，我会进一步展开！

# 参考资料

1、libusb安装

https://github.com/bluekitchen/btstack/tree/master/port/libusb

2、第06节-开源蓝牙协议BTStack框架分析

这个作者总结了韦东山的蓝牙视频笔记。挺好的。

https://www.cnblogs.com/-glb/p/11617659.html

3、

https://blog.csdn.net/happygrilclh/article/details/100743580