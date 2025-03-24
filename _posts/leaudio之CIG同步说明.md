---
title: leaudio之CIG同步说明
date: 2025-03-18 11:19:37
tags:
	- 蓝牙
---

--

# 举例分析

好的，我将通过一个具体的 TWS（真无线立体声）耳机场景，详细说明 **CIG（Connected Isochronous Group，连接等时组）** 如何实现同步和重传机制，并用具体的数字示例来说明。假设我们有一对 TWS 耳机（左耳机和右耳机）与手机配对，使用蓝牙 LE Audio 传输立体声音频。

---

### 场景设定
- **设备**：
  - 中央设备（Central）：手机。
  - 外围设备（Peripheral）：左耳机（CIS 0）、右耳机（CIS 1）。
- **音频需求**：
  - 使用 LC3 编解码器，采样率 48 kHz，码率 96 kbps，每声道每 10 毫秒生成一个 120 字节的音频帧（SDU）。
- **CIG 配置**：
  - **ISO_Interval**：10 毫秒（音频帧周期）。
  - **Sub_Interval**：2.5 毫秒（每个子事件之间的间隔）。
  - **BN（Burst Number）**：2（每个 CIS 在一个子事件中最多发送 2 个 PDU）。
  - **FT（Flush Timeout）**：2（允许重传的 ISO_Interval 数，即 20 毫秒）。
  - **Presentation Delay**：20 毫秒（从发送到播放的延迟）。
  - **SDU_Interval**：10 毫秒（上层音频帧生成周期）。
  - **CIS PDU 大小**：最大负载 64 字节（假设分段后每个 PDU 承载部分音频数据）。

---

### CIG 的时间线和同步过程
假设 CIG 的第一个事件从时间 **T = 0 ms** 开始，手机与左右耳机建立了一个包含两个 CIS 的 CIG：

#### **CIG 事件 0（T = 0 ms 到 T = 10 ms）**
1. **子事件 0（T = 0 ms 到 T = 2.5 ms）**：
   - 手机向左耳机（CIS 0）发送第一个音频帧的两个 CIS PDU：
     - **PDU 0**：SN = 0，负载 64 字节（音频帧前半部分）。
     - **PDU 1**：SN = 1，负载 56 字节（音频帧后半部分，120 - 64 = 56）。
   - 左耳机响应：
     - 返回 CIS PDU（SN = 0，NESN = 1），表示成功接收 PDU 0，期望下一个 SN = 1。
     - 返回 CIS PDU（SN = 1，NESN = 0），表示成功接收 PDU 1。

2. **子事件 1（T = 2.5 ms 到 T = 5 ms）**：
   - 手机向右耳机（CIS 1）发送第一个音频帧的两个 CIS PDU：
     - **PDU 0**：SN = 0，负载 64 字节。
     - **PDU 1**：SN = 1，负载 56 字节。
   - 右耳机响应：
     - 返回 CIS PDU（SN = 0，NESN = 1）。
     - 返回 CIS PDU（SN = 1，NESN = 0）。

3. **同步点**：
   - 两个耳机通过 ISOAL 重组各自的 120 字节 SDU，并根据时间戳和 Presentation Delay（20 ms）在 **T = 20 ms** 同时播放第一个音频帧。

#### **结果**：
- 左耳机和右耳机在 T = 20 ms 精确同步播放第一个音频帧，因为它们共享相同的 ISO_Interval（10 ms）和时间锚点（T = 0 ms）。

---

### 重传场景：右耳机丢包
假设在 **CIG 事件 1（T = 10 ms 到 T = 20 ms）** 中，右耳机因干扰未能正确接收数据。

#### **CIG 事件 1（T = 10 ms 到 T = 20 ms）**
1. **子事件 0（T = 10 ms 到 T = 12.5 ms）**：
   - 手机向左耳机（CIS 0）发送第二个音频帧：
     - **PDU 0**：SN = 0，64 字节。
     - **PDU 1**：SN = 1，56 字节。
   - 左耳机成功接收，返回 NESN = 0（ACK）。

2. **子事件 1（T = 12.5 ms 到 T = 15 ms）**：
   - 手机向右耳机（CIS 1）发送第二个音频帧：
     - **PDU 0**：SN = 0，64 字节。
     - **PDU 1**：SN = 1，56 字节。
   - 右耳机只接收到 PDU 1，未接收到 PDU 0（丢包），返回：
     - CIS PDU（NESN = 0），表示未收到 SN = 0 的数据（NACK）。

3. **重传处理**：
   - 手机检测到右耳机的 NESN = 0，与上次的 SN = 1 不匹配，触发重传。

#### **CIG 事件 2（T = 20 ms 到 T = 30 ms）**
1. **子事件 0（T = 20 ms 到 T = 22.5 ms）**：
   - 手机向左耳机发送第三个音频帧（正常传输）：
     - PDU 0（SN = 0），PDU 1（SN = 1）。
   - 左耳机响应 NESN = 0（ACK）。

2. **子事件 1（T = 22.5 ms 到 T = 25 ms）**：
   - 手机向右耳机重传第二个音频帧的 PDU 0：
     - **PDU 0**：SN = 0，64 字节。
   - 右耳机成功接收，返回 NESN = 1（ACK）。
   - 手机继续发送第二个音频帧的 PDU 1（SN = 1），右耳机也成功接收。

3. **同步点**：
   - 左耳机在 T = 30 ms 播放第二个音频帧（Presentation Delay = 20 ms）。
   - 右耳机在 T = 30 ms 播放第二个音频帧（重组后与左耳机对齐）。

#### **结果**：
- 由于 FT = 2（20 ms），右耳机在丢包后通过重传及时恢复数据，依然在 T = 30 ms 与左耳机同步播放第二个音频帧。

---

### 同步失败的边界情况
假设干扰持续，右耳机在 CIG 事件 2 中仍未收到重传的 PDU 0：
- **CIG 事件 3（T = 30 ms 到 T = 40 ms）**：
  - ==FT 窗口（20 ms）已过，第二个音频帧被“冲洗”（Flush），右耳机丢弃未完成的重传。==
  - 手机开始发送第三个音频帧，右耳机尝试与左耳机在 T = 40 ms 同步播放第三个音频帧。

#### **结果**：
- 右耳机丢失了第二个音频帧，==但通过 FT 机制避免了累积延迟，保持与左耳机的长期同步。==

---

### 数字示例中的关键点
1. **时间对齐**：
   - ISO_Interval = 10 ms 确保每个音频帧按周期传输。
   - Sub_Interval = 2.5 ms 保证左右耳机的子事件不冲突。
2. **同步精度**：
   - Presentation Delay = 20 ms 提供缓冲，确保左右耳机同时播放。
3. **重传容错**：
   - BN = 2 和 FT = 2 允许在 20 ms 内最多重传两次，保证数据完整性或及时放弃。
4. **数据分段**：
   - 120 字节 SDU 分成 64 字节 + 56 字节的 PDU，由 ISOAL 重组。

---

### 总结
在这个 TWS 耳机场景中，CIG 通过以下方式实现同步和重传：
- **同步**：统一的 ISO_Interval（10 ms）、子事件调度（2.5 ms 间隔）和 Presentation Delay（20 ms）确保左右耳机在 T = 20 ms、T = 30 ms 等时间点同时播放。
- **重传**：SN/NESN 机制检测丢包，FT = 2（20 ms）限制重传窗口，避免延迟累积。

这种设计在无线干扰下仍能保持音频流的连续性和同步性，非常适合 TWS 耳机的实时音频需求。如果需要更深入的细节（比如跳频如何影响重传），随时告诉我！

# Presentation Delay是人为设置的吗？

是的，**Presentation Delay（呈现延迟）** 在蓝牙 LE Audio 中通常是由系统或应用开发者人为设置的，但它的具体值并不是完全随意选择的，而是基于实际应用需求、硬件能力和协议配置来确定的。

下面我将详细解释它的设置来源和作用，并结合 TWS 耳机的场景说明。

---

### 1. **Presentation Delay 的定义**
Presentation Delay 是指从数据（如音频帧）被发送（通常以时间戳为基准）到它在接收端被呈现（例如耳机播放声音）之间的时间延迟。

它由蓝牙核心规范中的 **Isochronous Data Streams** 机制支持，旨在确保多个设备（如左右耳机）能够同步呈现数据。

- 在蓝牙协议中，Presentation Delay 通常通过上层协议（如 A2DP 或 LE Audio 配置文件）或应用层传递给设备。
- 它的单位通常是微秒（µs）或毫秒（ms），具体值由系统设计者根据场景需求配置。

---

### 2. **是否人为设置**
**是的，Presentation Delay 是人为设置的，但受限于以下因素：**
- **应用需求**：例如，TWS 耳机需要低延迟以提供实时音频体验，而多人音频共享可能需要更大的延迟以确保同步。
- **硬件能力**：接收设备的处理速度（如解码和缓冲能力）会影响最小可接受的延迟。
- **协议参数**：如 ISO_Interval、BN（Burst Number）、FT（Flush Timeout）等，它们共同决定数据传输的节奏和可靠性。
- **环境因素**：无线干扰可能要求更大的延迟作为缓冲，以容忍重传。

在实际实现中，Presentation Delay 通常由以下角色决定：
1. **设备制造商**：在固件或驱动中预设一个默认值。
2. **应用开发者**：通过蓝牙 API（如 HCI 命令或配置文件）动态调整。
3. **用户**：在某些高级设备中，用户可能通过设置间接影响延迟（例如选择“低延迟模式”或“高音质模式”）。

---

### 3. **如何设置 Presentation Delay**
在蓝牙 LE Audio 中，Presentation Delay 的设置通常通过以下步骤完成：
1. **协商阶段**：
   - 在建立 CIG（Connected Isochronous Group）或 BIG（Broadcast Isochronous Group）时，中央设备（Central）会通过控制消息（如 HCI 配置命令）指定 Presentation Delay。
   - 外围设备（Peripheral）根据自身能力接受或调整这个值。
2. **上层协议传递**：
   - Presentation Delay 可以嵌入 SDU（服务数据单元）的时间戳中，或通过单独的控制信道（如 ACL 连接）通知接收端。
3. **动态调整**：
   - 在传输过程中，系统可能根据丢包率或同步偏差动态优化延迟（需要支持高级算法的实现）。

例如，在 HCI 命令 `LE_Set_CIG_Parameters` 中，中央设备可以为每个 CIS 指定与延迟相关的参数，而 Presentation Delay 通常由上层应用（如音频流管理器）进一步细化。

---

### 4. **TWS 耳机场景中的示例**
让我们回到 TWS 耳机的具体场景，假设：
- **ISO_Interval**：10 ms。
- **SDU_Interval**：10 ms（每 10 ms 生成一个音频帧）。
- **传输时间**：假设每个 CIS PDU 传输和确认需要 1 ms。
- **解码时间**：耳机解码一个 120 字节音频帧需要 5 ms。

#### **人为设置的过程**：
1. **最低延迟需求**：
   - 数据从手机发送到耳机需要 1 ms（传输时间）。
   - 耳机解码需要 5 ms。
   - 理论最小延迟 = 1 ms + 5 ms = 6 ms。
2. **同步和容错考虑**：
   - 为确保左右耳机同步并应对可能的丢包，增加缓冲时间。
   - 假设 FT = 2（20 ms），可能需要一次重传，因此延迟应至少覆盖一个 ISO_Interval（10 ms）。
3. **人为选择**：
   - 开发者选择 Presentation Delay = 20 ms，作为一个折中值：
     - 足以覆盖传输（1 ms）、解码（5 ms）和一次重传（10 ms）。
     - 提供额外的缓冲（4 ms）以确保同步稳定性。

#### **结果**：
- 在 T = 0 ms，手机发送第一个音频帧。
- 在 T = 20 ms，左右耳机同时播放该帧。
- Presentation Delay = 20 ms 是人为设置的，但基于硬件能力和协议参数计算得出。

---

### 5. **人为设置的灵活性与限制**
- **灵活性**：
  - 开发者可以根据应用场景调整。例如，低延迟游戏模式可能设为 10 ms，高音质音乐模式可能设为 50 ms。
  - ==在广播场景（如 BIG），Presentation Delay 可能更大（例如 100 ms），以支持更多设备同步。==
- **限制**：
  - 不能低于硬件和传输的最小需求（例如上述的 6 ms）。
  - 过大则会增加感知延迟，影响用户体验（如唇音不同步）。

---

### 6. **实际中的体现**
在现实产品中：
- **默认值**：TWS 耳机厂商（如苹果 AirPods 或索尼 WF-1000XM5）通常在固件中预设 Presentation Delay（例如 20-50 ms），用户无法直接修改。
- **动态调整**：高端设备可能通过自适应算法根据丢包率调整延迟，但这仍基于初始的人为设计。

---

### 总结
Presentation Delay 是人为设置的，但不是随意决定的。它由开发者或制造商根据应用需求（如同步性、实时性）、硬件能力（如解码速度）和协议参数（如 ISO_Interval）综合计算得出。在 TWS 耳机中，典型值可能是 20-50 ms，既保证左右耳机同步，又留出重传和处理的余地。如果你想深入探讨如何通过 HCI 命令具体设置它，我可以进一步展开！

# 创建CIG的交互流程

下面我将详细描述在蓝牙 LE Audio 中创建 **CIG（Connected Isochronous Group，连接等时组）** 的交互流程，以 TWS 耳机为例，说明中央设备（手机）与外围设备（左耳机和右耳机）之间的步骤。这个流程涵盖了从初始连接到 CIG 建立的完整交互，包括主机（Host）和控制器（Controller）之间的通信，以及设备间的协议交互。我会尽量清晰、系统地列出每一步，并附上必要的参数示例。

---

### 场景假设
- **设备**：
  - 中央设备（Central）：手机。
  - 外围设备（Peripheral）：左耳机（CIS 0）、右耳机（CIS 1）。
- **目标**：
  - 创建一个 CIG，包含两个 CIS，用于传输左右声道音频。
- **参数**：
  - **ISO_Interval**：10 ms。
  - **Sub_Interval**：2.5 ms。
  - **BN（Burst Number）**：2。
  - **FT（Flush Timeout）**：2。
  - **Presentation Delay**：20 ms。
  - **SDU_Interval**：10 ms。

---

### 创建 CIG 的交互流程

#### **步骤 1：建立 ACL 连接**
在创建 CIG 之前，手机和耳机需要先建立异步无连接链路（ACL，Asynchronous Connection-Less）作为控制通道。
1. **手机扫描并发现设备**：
   - 手机进入扫描模式（LE Scanning），检测左耳机和右耳机的广播（Advertising）。
   - 左耳机和右耳机以可连接模式广播（ADV_IND）。
2. **发起连接**：
   - 手机向左耳机发送 `CONNECT_IND`，建立 ACL 连接（连接句柄：ACL_Handle_1）。
   - 手机向右耳机发送 `CONNECT_IND`，建立 ACL 连接（连接句柄：ACL_Handle_2）。
3. **结果**：
   - 手机与左右耳机分别建立 ACL 连接，用于后续控制消息传输。

---

#### **步骤 2：主机配置 CIG 参数**
手机的主机（Host）通过 HCI（Host Controller Interface）向控制器（Controller）发送命令，配置 CIG 参数。
1. **主机发送 HCI 命令：LE_Set_CIG_Parameters**：
   - **命令格式**：
     ```
     Opcode: 0x2062 (LE_Set_CIG_Parameters)
     Parameters:
     - CIG_ID: 0x01 (标识这个 CIG，范围 0x00-0xEF)
     - SDU_Interval: 10000 µs (10 ms)
     - FT_Central: 2 (中央设备 Flush Timeout)
     - FT_Peripheral: 2 (外围设备 Flush Timeout)
     - ISO_Interval: 8 (10 ms / 1.25 ms = 8 个时隙)
     - Packing: 0 (顺序打包)
     - Framing: 0 (未分帧)
     - Number_of_CIS: 2 (两个 CIS)
     - CIS_Config:
       - CIS_ID_0: 0x00, Max_SDU_C_to_P: 120 bytes, Max_SDU_P_to_C: 0 bytes
       - CIS_ID_1: 0x01, Max_SDU_C_to_P: 120 bytes, Max_SDU_P_to_C: 0 bytes
     ```
   - 说明：
     - CIG_ID 是 CIG 的唯一标识符。
     - SDU_Interval 定义上层数据生成周期。
     - ISO_Interval 以 1.25 ms 为单位（10 ms = 8 个时隙）。
     - CIS_ID_0 和 CIS_ID_1 分别对应左耳机和右耳机。
2. **控制器响应**：
   - 返回 `Command Complete` 事件：
     ```
     Event: Command Complete
     Parameters:
     - Status: 0x00 (成功)
     - CIG_ID: 0x01
     - Num_Handles: 2
     - Conn_Handle_0: 0x0100 (CIS 0 的连接句柄)
     - Conn_Handle_1: 0x0101 (CIS 1 的连接句柄)
     ```
   - 控制器分配两个连接句柄（Conn_Handle），后续用于标识 CIS。

---

#### **步骤 3：建立 CIS 连接**
手机通过已有的 ACL 连接，请求与耳机建立 CIS 连接。
1. **主机发送 HCI 命令：LE_Create_CIS**：
   - **命令格式**：
     ```
     Opcode: 0x2064 (LE_Create_CIS)
     Parameters:
     - Num_CIS: 2
     - CIS_Config:
       - CIS_Conn_Handle_0: 0x0100, ACL_Conn_Handle_0: ACL_Handle_1
       - CIS_Conn_Handle_1: 0x0101, ACL_Conn_Handle_1: ACL_Handle_2
     ```
   - 说明：
     - 将 CIS 连接绑定到对应的 ACL 连接。
2. **控制器发起 CIS 建立**：
   - 手机的控制器通过 ACL 通道向左耳机发送 `LE_CIS_Request`：
     ```
     CIS_ID: 0x00
     CIG_ID: 0x01
     ```
   - 向右耳机发送 `LE_CIS_Request`：
     ```
     CIS_ID: 0x01
     CIG_ID: 0x01
     ```
3. **耳机响应**：
   - 左耳机控制器接受请求，返回 `LE_CIS_Rsp`（接受）。
   - 右耳机控制器接受请求，返回 `LE_CIS_Rsp`（接受）。
4. **CIS 连接建立完成**：
   
   - 手机控制器收到耳机的响应后，发送 `LE_CIS_Established` 事件给主机：
     ```
     Event: LE_CIS_Established
     Parameters (CIS 0):
     - Status: 0x00 (成功)
     - Conn_Handle: 0x0100
     - CIG_Sync_Delay: 2000 µs (2 ms)
     - CIS_Sync_Delay: 2500 µs (2.5 ms)
     - Presentation_Delay: 20000 µs (20 ms)
     Parameters (CIS 1):
     - Status: 0x00 (成功)
     - Conn_Handle: 0x0101
     - CIG_Sync_Delay: 2000 µs (2 ms)
     - CIS_Sync_Delay: 5000 µs (5 ms)
     - Presentation_Delay: 20000 µs (20 ms)
     ```
   - 说明：
     - CIG_Sync_Delay：CIG 事件开始到第一个子事件的延迟。
     - CIS_Sync_Delay：CIS 数据开始传输的延迟（因子事件顺序不同）。

---

#### **步骤 4：同步和数据传输**
CIG 创建完成后，手机和耳机开始按照协商的参数传输数据。
1. **时间锚点对齐**：
   - 手机控制器设定第一个 CIG 事件的锚点（T = 0 ms）。
   - 子事件 0（CIS 0，左耳机）：T = 0 ms 到 2.5 ms。
   - 子事件 1（CIS 1，右耳机）：T = 2.5 ms 到 5 ms。
2. **数据发送**：
   - 在 T = 0 ms，手机向左耳机发送 CIS PDU（音频数据）。
   - 在 T = 2.5 ms，手机向右耳机发送 CIS PDU。
3. **同步播放**：
   - 根据 Presentation_Delay = 20 ms，左右耳机在 T = 20 ms 同时播放第一个音频帧。

---

### 交互流程图
```
手机(Host)        手机(Controller)       左耳机           右耳机
   |                   |                  |                |
1. |--ACL Connect-->  |--CONNECT_IND-->  |                |
   |<--Connected----  |<--Connected----- |                |
   |                   |                  |                |
2. |--ACL Connect-->  |--CONNECT_IND-->  |                |--CONNECT_IND-->|
   |<--Connected----  |<--Connected----- |                |<--Connected----|
   |                   |                  |                |
3. |--LE_Set_CIG_Parameters-->           |                |
   |<--Command Complete---------------   |                |
   |                   |                  |                |
4. |--LE_Create_CIS-->|                  |                |
   |                   |--LE_CIS_Request-->|               |
   |                   |<--LE_CIS_Rsp-----|               |
   |                   |--LE_CIS_Request----------------->|
   |                   |<--LE_CIS_Rsp--------------------|
   |<--LE_CIS_Established---------------|               |
   |                   |                  |                |
5. |                   |--CIS PDU------->|               |
   |                   |--CIS PDU----------------------->|
   |                   |                  |                |
   |                   |  T = 20 ms: 左右耳机同步播放    |
```

---

### 关键点说明
1. **ACL 连接**：作为控制基础，确保设备间通信。
2. **CIG 参数配置**：由手机主机定义，控制器分配句柄。
3. **CIS 建立**：通过 ACL 通道协商，绑定 CIG 和 CIS。
4. **同步传输**：CIG 事件按 ISO_Interval（10 ms）周期性发生，子事件按顺序调度。

---

### 总结
创建 CIG 的交互流程从 ACL 连接开始，通过 HCI 命令配置参数，再经由 CIS 建立过程完成。最终，手机与左右耳机形成一个同步的 CIG，数据传输和播放严格遵循时间基准（如 Presentation Delay = 20 ms）。如果你需要更具体的 HCI 命令细节或某个步骤的深入分析，请告诉我！

# 创建CIG是必须的吗？如果只有一个CIS，是否需要创建CIG？

在蓝牙 LE Audio 中，创建 **CIG（Connected Isochronous Group，连接等时组）** 并不是绝对必须的，但它与 **CIS（Connected Isochronous Stream，连接等时流）** 的使用场景和协议设计密切相关。是否需要创建 CIG，取决于具体应用需求和设备数量。下面我将详细解答你的问题，特别是针对只有一个 CIS 的情况，分析是否需要 CIG。

---

### 1. **CIG 的作用和定义**
CIG 是蓝牙核心规范 5.2 中引入的概念，用于将一个或多个 CIS 组织成一个逻辑组。它的主要作用是：
- **时间同步**：确保组内所有 CIS 共享相同的 **ISO_Interval** 和时间锚点（Anchor Point），实现多个数据流之间的协调。
- **资源管理**：通过统一的配置（如 ISO_Interval、FT、BN 等），优化控制器对多个 CIS 的调度。
- **典型场景**：支持多设备同步，例如 TWS 耳机（左右耳机各一个 CIS）或多声道音频系统。

CIG 的本质是一个“容器”，可以包含一个或多个 CIS。如果有多个 CIS，CIG 的作用尤为明显，因为它能保证这些 CIS 在时间上的对齐和一致性。

---

### 2. **只有一个 CIS 的情况**
如果应用场景中只需要一个 CIS（例如手机与单个耳机建立点对点音频流），==理论上可以不显式创建 CIG，==而是直接建立一个独立的 CIS。==然而，蓝牙协议的实现方式和实际操作中，CIG 仍然是推荐甚至是必要的框架==。原因如下：

#### **协议设计上的依赖**
- **HCI 命令的结构**：
  - 在蓝牙控制器中，创建 CIS 的流程通常依赖于 CIG 的上下文。例如，HCI 命令 `LE_Set_CIG_Parameters` 是用来配置 CIG 并分配 CIS 连接句柄的，即使只有一个 CIS，也需要通过这个命令指定参数。
  - ==即使只有一个 CIS，协议仍要求将其放入一个 CIG（Number_of_CIS = 1）==，以保持一致的配置和管理逻辑。
- **CIS 的建立**：
  - `LE_Create_CIS` 命令需要引用 CIG_ID 和 CIS_ID，这些标识符是在 `LE_Set_CIG_Parameters` 中定义的。没有 CIG，控制器无法正确初始化 CIS 的时间参数和连接句柄。

#### **实际实现中的要求**
- 大多数蓝牙控制器和协议栈实现（例如基于蓝牙核心规范的芯片）==都假设 CIS 必须属于某个 CIG，即使这个 CIG 只包含一个 CIS。这是为了简化控制器的调度逻辑和未来的扩展性。==
- 规范中没有提供直接创建“独立 CIS”而不涉及 CIG 的明确流程。

#### **参数示例（单个 CIS 的 CIG）**
假设手机与单个耳机建立一个 CIS：
- **LE_Set_CIG_Parameters**：
  
  ```
  CIG_ID: 0x01
  ISO_Interval: 10 ms (8 个时隙)
  Number_of_CIS: 1
  CIS_ID_0: 0x00
  Max_SDU_C_to_P: 120 bytes
  ```
- 控制器返回一个连接句柄（例如 0x0100），后续通过 `LE_Create_CIS` 建立这个 CIS。
- 结果：CIG 只包含一个 CIS，但仍需通过 CIG 框架配置。

---

### 3. **不创建 CIG 的可能性**
从理论上看，如果蓝牙协议栈和控制器支持一种“独立 CIS”模式（不依赖 CIG），是可以避免创建 CIG 的。但目前的核心规范（截至 5.4 版本）和大多数商用实现中，没有这样的机制。原因包括：
- **一致性**：CIG 提供了一个统一的框架，无论是单个 CIS 还是多个 CIS，都能使用相同的配置和管理流程。
- **扩展性**：即使当前只有一个 CIS，未来可能需要添加更多 CIS（例如从单耳机升级到双耳机），CIG 提供了灵活性。
- **时间管理**：CIS 的等时特性（ISO_Interval、子事件调度等）依赖于 CIG 的事件结构，即使只有一个 CIS，这些参数也需要通过 CIG 定义。

因此，在现有规范下，即使只有一个 CIS，创建 CIG 是必须的，至少在形式上是这样。

---

### 4. **只有一个 CIS 时 CIG 的简化**
当 CIG 中只有一个 CIS 时，它的复杂性会大大降低：
- **子事件调度**：只有一个 CIS，无需多个子事件（Subevent），整个 ISO_Interval 都用于该 CIS 的数据传输。
- **同步需求**：没有其他 CIS 需要同步，CIG 的作用退化为单纯的配置容器。
- **示例时间线**：
  - ISO_Interval = 10 ms。
  - T = 0 ms：手机发送 CIS PDU。
  - T = 20 ms：耳机根据 Presentation Delay 播放。
  - 没有额外的 CIS，流程非常简单。

尽管如此，CIG 的创建步骤（例如通过 `LE_Set_CIG_Parameters` 和 `LE_Create_CIS`）仍然不可省略。

---

### 5. **对比广播场景（BIG）**
为了更全面理解，可以对比广播等时组（BIG，Broadcast Isochronous Group）：
- BIG 用于广播场景（如一对多音频共享），可以包含多个 BIS（Broadcast Isochronous Stream）。
- 如果只有一个 BIS，BIG 仍然是必须的，类似 CIG 的逻辑。
- 这进一步说明蓝牙 LE Audio 的设计倾向于使用组（CIG 或 BIG）来管理等时流，而不是直接操作单个流。

---

### 6. **回答你的问题**
- **创建 CIG 是必须的吗？**
  - 在当前蓝牙 LE Audio 规范和实现中，是的，即使只有一个 CIS，也需要创建 CIG。这是协议设计和控制器实现的要求。
- **如果只有一个 CIS，是否需要创建 CIG？**
  - 是的，CIG 是 CIS 的必要容器，即使只有一个 CIS，也必须通过 CIG 的流程配置和建立。没有独立的“裸 CIS”创建路径。

---

### 总结
创建 CIG 是蓝牙 LE Audio 中使用 CIS 的标准流程，即使只有一个 CIS，也无法绕过 CIG 的创建。这是因为 CIG 提供了时间基准、参数管理和扩展性的基础。即使在单 CIS 场景中，CIG 的作用可能显得冗余，但它是协议栈的强制性部分。实际操作中，你仍然需要调用 `LE_Set_CIG_Parameters` 并指定 Number_of_CIS = 1。如果你对协议的某个具体命令或实现细节有疑问，可以进一步告诉我，我会深入解答！

# CIS的分帧是什么

在蓝牙 LE Audio 中，**CIS（Connected Isochronous Stream，连接等时流）** 的“分帧”（Framing）是指在传输等时数据（如音频流）时，如何将上层生成的 **SDU（Service Data Unit，服务数据单元）** 组织并映射到 **CIS PDU（Protocol Data Unit，协议数据单元）** 的过程。

分帧的概念与数据的分段、打包以及时间对齐密切相关，旨在优化传输效率和满足实时性要求。

下面我将详细解释 CIS 分帧的含义、机制和实际应用，并结合具体场景说明。

---

### 1. **分帧的定义**
分帧（Framing）是蓝牙核心规范中用于描述 SDU 如何被处理并放入 CIS PDU 的术语。它由 **ISOAL（Isochronous Adaptation Layer，等时适配层）** 负责实现，分为两种模式：
- **未分帧（Unframed）**：每个 SDU 被完整地映射到一个或多个 CIS PDU，不强制与 ISO_Interval 边界对齐。
- **分帧（Framed）**：SDU 被分割并严格按照 ISO_Interval 的时间边界打包，通常用于需要更高时间精度的场景。

分帧的设置通过 HCI 命令（如 `LE_Set_CIG_Parameters`）中的 **Framing 参数** 指定：
- `Framing = 0`：未分帧模式。
- `Framing = 1`：分帧模式。

---

### 2. **未分帧（Unframed）模式**
#### **机制**
- 在未分帧模式下，ISOAL 将 SDU 视为一个整体，尽量保持其完整性。
- 如果 SDU 大小超过单个 CIS PDU 的最大负载（Max_SDU，例如 251 字节），ISOAL 会将其分段为多个 CIS PDU，但这些 PDU 不一定与 ISO_Interval 的时间边界对齐。
- 传输时，CIS PDU 的发送时机由链路层的调度决定，可能跨越多个 ISO_Interval。

#### **特点**
- **灵活性**：适合数据大小不固定或不需要严格时间对齐的场景。
- **效率**：减少填充（padding），充分利用 PDU 容量。
- **延迟**：可能因分段和传输跨越多个周期而增加轻微延迟。

#### **示例**
- **场景**：手机向耳机传输一个 300 字节的音频 SDU。
- **参数**：
  - Max_SDU = 120 字节。
  - ISO_Interval = 10 ms。
  - BN（Burst Number） = 2（每个 ISO_Interval 最多发送 2 个 PDU）。
- **分帧过程**：
  1. ISOAL 将 300 字节 SDU 分段：
     - PDU 1：120 字节。
     - PDU 2：120 字节。
     - PDU 3：60 字节。
  2. 在第一个 ISO_Interval（T = 0 ms 到 10 ms）：
     - 发送 PDU 1 和 PDU 2（BN = 2）。
  3. 在第二个 ISO_Interval（T = 10 ms 到 20 ms）：
     - 发送 PDU 3。
- **结果**：接收端重组后得到完整的 300 字节 SDU，传输时间跨两个周期（20 ms）。

---

### 3. **分帧（Framed）模式**
#### **机制**
- 在分帧模式下，ISOAL 强制将 SDU 与 ISO_Interval 的时间边界对齐。
- 每个 ISO_Interval 传输一个完整的 SDU（或其分段），并且通常在该周期内完成传输。
- 如果 SDU 较大，ISOAL 会将其分段，但每个分段都被视为一个独立的“帧”，与时间周期绑定。

#### **特点**
- **时间精度**：每个 SDU（或分段）与 ISO_Interval 严格同步，适合实时性要求高的场景（如音频流）。
- **一致性**：便于接收端按周期处理数据。
- **填充开销**：==如果 SDU 小于 PDU 容量，可能需要填充字节。==

#### **示例**
- **场景**：手机向耳机传输连续的音频流，每 10 ms 生成一个 120 字节 SDU。
- **参数**：
  - Max_SDU = 120 字节。
  - ISO_Interval = 10 ms。
  - BN = 1（每个 ISO_Interval 发送 1 个 PDU）。
- **分帧过程**：
  1. 在 T = 0 ms，生成第一个 120 字节 SDU：
     - ISOAL 打包为一个 CIS PDU（120 字节）。
     - 发送时间：T = 0 ms 到 10 ms。
  2. 在 T = 10 ms，生成第二个 120 字节 SDU：
     - ISOAL 打包为一个 CIS PDU（120 字节）。
     - 发送时间：T = 10 ms 到 20 ms。
- **结果**：每个 SDU 作为一个“帧”，与 10 ms 的 ISO_Interval 对齐，接收端每 10 ms 处理一个完整的音频帧。

#### **大 SDU 的分帧**
- 如果 SDU = 300 字节，Max_SDU = 120 字节：
  1. ISOAL 分段：
     - Frame 1：120 字节（T = 0 ms）。
     - Frame 2：120 字节（T = 10 ms）。
     - Frame 3：60 字节（T = 20 ms）。
  2. 每个帧与 ISO_Interval 对齐，确保时间一致性。

---

### 4. **分帧与未分帧的对比**
| 特性         | 未分帧 (Unframed)          | 分帧 (Framed)            |
| ------------ | -------------------------- | ------------------------ |
| **时间对齐** | 不强制与 ISO_Interval 对齐 | 强制与 ISO_Interval 对齐 |
| **分段方式** | 按 PDU 容量分段            | 按周期分段               |
| **适用场景** | 数据大小不固定             | 实时性要求高（如音频）   |
| **传输效率** | 高（少填充）               | 可能有填充开销           |
| **延迟**     | 可能跨周期                 | 通常单周期内完成         |

---

### 5. **分帧在 CIS 中的实际应用**
- **TWS 耳机**：
  - 通常使用分帧模式，确保左右耳机的音频帧与 ISO_Interval 对齐，实现同步播放。
  - 例如，左右声道各 120 字节 SDU，每 10 ms 发送一个帧。
- **单声道耳机**：
  - 如果数据量较小，可能使用未分帧模式以减少开销；但音频流仍倾向于分帧模式以保持节奏。

---

### 6. **分帧的配置**
分帧模式通过 HCI 命令设置，例如：
- **LE_Set_CIG_Parameters**：
  
  ```
  Framing: 1 (分帧模式)
  ISO_Interval: 10 ms
  SDU_Interval: 10 ms
  ```
- 控制器根据 Framing 参数调整 ISOAL 的行为。

---

### 总结
CIS 的分帧是指 ISOAL 如何将 SDU 组织为 CIS PDU 并与时间周期对齐的过程：
- **未分帧**：灵活分段，适合非严格实时场景。
- **分帧**：周期对齐，适合音频等实时应用。
在 TWS 耳机等典型 LE Audio 场景中，分帧模式更常见，因为它能确保数据与 ISO_Interval 的同步，从而保证左右耳机的播放一致性。如果你想深入探讨分帧的实现细节或某个具体场景的例子，请告诉我！

# 用于CIS的HCI命令有哪些

在蓝牙 LE Audio 中，**CIS（Connected Isochronous Stream，连接等时流）** 的创建、管理和终止依赖于一系列 **HCI（Host Controller Interface）命令** 和 **事件**。

这些命令由主机（Host）发送给控制器（Controller），用于配置和管理 CIS 以及其所属的 **CIG（Connected Isochronous Group，连接等时组）**。

以下是我整理的与 CIS 直接相关的 HCI 命令和事件清单，基于蓝牙核心规范（截至版本 5.4），并附上功能说明和典型参数示例。

---

### 1. **用于创建和管理 CIS 的 HCI 命令**
以下命令主要用于 CIS 的配置、建立和参数调整：

#### **1.1 LE_Set_CIG_Parameters**
- **功能**：配置 CIG 的参数并分配 CIS 的连接句柄，为后续 CIS 建立做准备。
- **Opcode**：`0x2062`
- **参数**：
  
  - `CIG_ID`（1 字节）：CIG 的标识符（0x00–0xEF）。
  - `SDU_Interval_C_To_P`（3 字节）：中央到外围的 SDU 间隔（µs）。
  - `SDU_Interval_P_To_C`（3 字节）：外围到中央的 SDU 间隔（µs）。
  - `FT_Central`（1 字节）：中央设备的 Flush Timeout。
  - `FT_Peripheral`（1 字节）：外围设备的 Flush Timeout。
  - `ISO_Interval`（2 字节）：等时间隔（以 1.25 ms 为单位，例如 10 ms = 8）。
  - `Packing`（1 字节）：打包方式（0 = 顺序，1 = 交错）。
  - `Framing`（1 字节）：分帧模式（0 = 未分帧，1 = 分帧）。
  - `Num_CIS`（1 字节）：CIS 数量。
  - `CIS_Config`（每个 CIS 的配置）：
    - `CIS_ID`（1 字节）：CIS 标识符。
    - `Max_SDU_C_To_P`（2 字节）：中央到外围的最大 SDU 大小。
    - `Max_SDU_P_To_C`（2 字节）：外围到中央的最大 SDU 大小。
- **返回**：
  - `Status`：成功（0x00）或错误码。
  - `CIG_ID`：确认的 CIG 标识符。
  - `Num_Handles`：分配的连接句柄数量。
  - `Conn_Handle[]`：每个 CIS 的连接句柄。
- **示例**：
  ```
  CIG_ID: 0x01
  SDU_Interval: 10000 µs (10 ms)
  ISO_Interval: 8 (10 ms)
  Framing: 1 (分帧)
  Num_CIS: 2
  CIS_ID_0: 0x00, Max_SDU: 120 bytes
  CIS_ID_1: 0x01, Max_SDU: 120 bytes
  ```

#### **1.2 LE_Create_CIS**
- **功能**：请求建立一个或多个 CIS 连接。
- **Opcode**：`0x2064`
- **参数**：
  - `Num_CIS`（1 字节）：要建立的 CIS 数量。
  - `CIS_Config`（每个 CIS 的配置）：
    - `CIS_Conn_Handle`（2 字节）：CIS 的连接句柄（从 LE_Set_CIG_Parameters 获取）。
    - `ACL_Conn_Handle`（2 字节）：关联的 ACL 连接句柄。
- **返回**：无直接返回值，成功与否通过事件反馈。
- **示例**：
  ```
  Num_CIS: 2
  CIS_Conn_Handle_0: 0x0100, ACL_Conn_Handle_0: 0x0001
  CIS_Conn_Handle_1: 0x0101, ACL_Conn_Handle_1: 0x0002
  ```

#### **1.3 LE_Remove_CIG**
- **功能**：删除指定的 CIG 及其所有关联的 CIS。
- **Opcode**：`0x2065`
- **参数**：
  - `CIG_ID`（1 字节）：要删除的 CIG 标识符。
- **返回**：
  - `Status`：成功（0x00）或错误码。
  - `CIG_ID`：确认删除的 CIG。
- **示例**：
  ```
  CIG_ID: 0x01
  ```

#### **1.4 LE_Accept_CIS_Request**
- **功能**：外围设备接受中央设备发起的 CIS 连接请求。
- **Opcode**：`0x2066`
- **参数**：
  - `Conn_Handle`（2 字节）：CIS 的连接句柄。
- **返回**：无直接返回值，通过事件反馈。
- **说明**：通常由外围设备的主机调用，响应中央设备的 `LE_CIS_Request`。

#### **1.5 LE_Reject_CIS_Request**
- **功能**：外围设备拒绝中央设备发起的 CIS 连接请求。
- **Opcode**：`0x2067`
- **参数**：
  - `Conn_Handle`（2 字节）：CIS 的连接句柄。
  - `Reason`（1 字节）：拒绝原因（如 0x0D = Connection Rejected）。
- **返回**：无直接返回值，通过事件反馈。

#### **1.6 LE_Terminate_CIS**
- **功能**：终止指定的 CIS 连接。
- **Opcode**：`0x206B`
- **参数**：
  - `Conn_Handle`（2 字节）：要终止的 CIS 连接句柄。
  - `Reason`（1 字节）：终止原因（如 0x16 = Remote User Terminated）。
- **返回**：通过事件反馈终止状态。

---

### 2. **与 CIS 相关的 HCI 事件**
这些事件由控制器返回给主机，用于通知 CIS 的状态变化。

#### **2.1 LE_CIS_Established**
- **功能**：通知 CIS 连接已成功建立。
- **Event Code**：`0x19`
- **参数**：
  - `Status`：成功（0x00）或错误码。
  - `Conn_Handle`：CIS 的连接句柄。
  - `CIG_Sync_Delay`（3 字节）：CIG 同步延迟（µs）。
  - `CIS_Sync_Delay`（3 字节）：CIS 同步延迟（µs）。
  - `Latency_C_To_P`（3 字节）：中央到外围的延迟。
  - `Latency_P_To_C`（3 字节）：外围到中央的延迟。
  - `PHY_C_To_P`（1 字节）：使用的 PHY。
  - `PHY_P_To_C`（1 字节）：使用的 PHY。
  - `Presentation_Delay`（3 字节）：呈现延迟（µs）。
- **示例**：
  ```
  Conn_Handle: 0x0100
  CIG_Sync_Delay: 2000 µs
  CIS_Sync_Delay: 2500 µs
  Presentation_Delay: 20000 µs
  ```

#### **2.2 LE_CIS_Request**
- **功能**：通知主机收到来自对端设备的 CIS 连接请求（通常由外围设备接收）。
- **Event Code**：`0x1A`
- **参数**：
  - `ACL_Conn_Handle`：关联的 ACL 连接句柄。
  - `CIS_Conn_Handle`：分配的 CIS 连接句柄。
  - `CIG_ID`：CIG 标识符。
  - `CIS_ID`：CIS 标识符。
- **说明**：主机需响应 `LE_Accept_CIS_Request` 或 `LE_Reject_CIS_Request`。

#### **2.3 LE_Connection_Complete**（间接相关）
- **功能**：通知 ACL 连接建立成功，为后续 CIS 创建提供基础。
- **Event Code**：`0x03`
- **参数**：包括 `Conn_Handle` 等。

#### **2.4 LE_Connection_Terminated**（间接相关）
- **功能**：通知 CIS 或 ACL 连接终止。
- **Event Code**：`0x08`
- **参数**：
  - `Conn_Handle`：终止的连接句柄。
  - `Reason`：终止原因。

---

### 3. **典型交互流程中的 HCI 命令**
以手机与 TWS 耳机创建 CIG（包含两个 CIS）为例：
1. **建立 ACL 连接**：
   - 主机发送 `LE_Create_Connection`。
   - 控制器返回 `LE_Connection_Complete`。
2. **配置 CIG**：
   - 主机发送 `LE_Set_CIG_Parameters`。
   - 控制器返回 `Command Complete`。
3. **建立 CIS**：
   - 主机发送 `LE_Create_CIS`。
   - 控制器向耳机发送 `LE_CIS_Request`，耳机响应后返回 `LE_CIS_Established`。
4. **终止 CIS**：
   - 主机发送 `LE_Terminate_CIS`。
   - 控制器返回 `LE_Connection_Terminated`。

---

### 4. **总结**
用于 CIS 的 HCI 命令主要包括：
- **创建和管理**：`LE_Set_CIG_Parameters`、`LE_Create_CIS`、`LE_Remove_CIG`。
- **外围设备响应**：`LE_Accept_CIS_Request`、`LE_Reject_CIS_Request`。
- **终止**：`LE_Terminate_CIS`。
- **相关事件**：`LE_CIS_Established`、`LE_CIS_Request` 等。

这些命令和事件共同支持 CIS 的生命周期管理，从配置、建立到终止。如果需要某个命令的更详细参数说明或具体实现示例，请告诉我，我可以进一步展开！
