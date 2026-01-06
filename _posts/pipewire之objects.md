---
title: pipewire之objects
date: 2025-05-30 10:12:37
tags:
	- 音频
---

--

# 官方文档objects.dox文档总结

### PipeWire 对象设计文档翻译总结

本文件是 PipeWire 媒体和会话管理图中各种对象的参考设计，解释对象的定义、使用方式以及与子系统或其他库的关联。

#### 媒体图
媒体图描述 PipeWire daemon 内部及与客户端之间的媒体流，包含以下核心对象：
- **Node**：媒体处理单元，负责消费或生成包含音频、视频等数据的缓冲区。可运行于 daemon 或客户端进程中，客户端通过 PipeWire 协议传输媒体。类比 GStreamer 的 **element**（但不完全等同）。
- **Port**：依附于 **node** 的接口，用于媒体输入（**sink**）或输出（**source**）。一个 **node** 可有多个 **port**，每个 **port** 有明确方向（输入或输出）。类比 GStreamer 的 **pad**。
- **Link**：连接相反方向的两个 **port**（输出到输入），实现媒体流传输。

#### 会话管理图
会话管理图是媒体流的高级虚拟表示，由会话管理器创建，仅通过会话管理器的操作影响媒体图。用于简化用户和策略管理代码的复杂性，包含以下对象：
- **Endpoint**：表示用户可感知的媒体路由起点或终点，如硬件（笔记本扬声器、USB 摄像头、蓝牙耳机麦克风）或软件（桌面捕获、媒体播放器）。**Endpoint** 通常映射到媒体图的 **node**，但也可能对应多个 **node** 或无 **node**（如直接连接硬件的 CD 播放器）。**Endpoint** 可包含互斥的 **target**（如笔记本的扬声器和耳机插孔共享同一 ALSA PCM 设备）。
- **Endpoint Stream**：依附于 **endpoint**，表示到达该 **endpoint** 的逻辑路径，通常与特定用例相关。例如，汽车扬声器放大器的 **endpoint** 可能有：
  - **Music**：播放音乐，输出到所有扬声器。
  - **Voice**：播放导航或语音助手消息，仅输出到前排扬声器，降低音乐音量。
  - **Emergency**：播放紧急音，输出到所有扬声器，必要时提高音量并静音其他流。
  **Endpoint Stream** 可互斥或同时使用，实现方式包括添加额外的 **node**、使用不同设备 **node** 或触发硬件开关。
- **Endpoint Link**：连接两个 **endpoint** 的 **stream**，表示逻辑媒体流。可通过媒体图中的 **link** 或硬件资源配置实现。构建 **endpoint link** 需源 **stream** 提供连接信息，接收 **stream** 确认兼容性并完成连接。

#### 其他相关对象
- **Device**：表示底层 API 的句柄，用于创建高级对象（如 **node** 或其他 **device**）。常见 **device** 包括：
  - **alsa.pcm.device**：ALSA 声卡（如 `hw:0`）。
  - **alsa.seq.device**：ALSA MIDI 设备。
  - **v4l2.device**：V4L2 设备（如 `/dev/video0`）。
  - **jack.device**：JACK 客户端，允许 PipeWire 作为 JACK 的从属设备。
  **Device** 具有 **profile**，支持多种配置或关闭设备。
- **Session**：表示会话管理器，管理全局属性和方法，如默认设备 **endpoint**（模拟 PulseAudio 行为，供用户在 UI 中选择默认音频输出）。多会话支持尚未明确定义。

#### 与底层子系统的映射
- **ALSA UCM**（建议方案）：
  - ALSA 声卡 → **device**。
  - UCM verb → **device profile**。
  - UCM device → **endpoint**（冲突设备可分组为同一 **endpoint** 的 **target**）。
  - UCM modifier → **endpoint stream**。
  - PCM stream → **node**。
  激活 **profile**（UCM verb）创建 PCM 流对应的 **node** 和每个 UCM device 的 **endpoint**，UCM modifier 作为 **stream**。
- **ALSA Fallback**（无 UCM 时）：
  - ALSA 声卡 → **device**（仅 on/off 两种 **profile**）。
  - PCM stream → **node** + **endpoint**（仅默认 **stream**，可由会话管理器扩展）。
- **V4L2**：
  - V4L2 设备 → **device** + **node**（待完善）。

#### 与其他 API 的关系
- **PulseAudio**：
  - **PipeWire → PulseAudio**：
    - **device** → **card**。
    - **device profile** → **card profile**。
    - **endpoint**（关联设备）→ **sink/source**。
    - **endpoint**（关联客户端）→ **sink-input/source-output**。
    - **endpoint target** → **port**。
    - **endpoint stream** → 无对应（PulseAudio 客户端限于默认 **stream**）。
  - **PulseAudio → PipeWire**：
    - **stream** → **client** + **node** + **endpoint**（无 **target**，仅默认 **stream**）。
- **JACK**（JACK 客户端通过兼容库连接 PipeWire）：
  - **PipeWire → JACK**：
    - **node** → **client**。
    - **port** → **port**。
    - **device/endpoint** → 无对应。
  - **JACK → PipeWire**：
    - **client** → **client** + **node**。
    - **port** → **port**。
    JACK 客户端不创建 **endpoint**，需会话管理器支持直接 **node** 链接。

总结来说，PipeWire 的媒体图（**node**、**port**、**link**）处理实际媒体流，会话管理图（**endpoint**、**endpoint stream**、**endpoint link**）提供高级抽象，简化用户交互和策略管理。**Device** 和 **session** 提供底层支持和全局管理，与 ALSA、V4L2、PulseAudio 和 JACK 等系统兼容。
