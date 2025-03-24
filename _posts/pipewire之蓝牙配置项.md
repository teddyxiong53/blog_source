---
title: pipewire之蓝牙配置项
date: 2025-03-21 16:18:37
tags:
	- 音频
---

--

# api.bluez5.connection-info

具体来说：

- **启用时（true）**：PipeWire 会尝试通过 BlueZ 的 D-Bus 接口获取并更新设备的连接状态，并在节点或设备的属性中反映这些信息。这对于需要实时监控蓝牙设备状态的应用（例如 GUI 音频管理工具）非常有用。
- **禁用时（false）**：PipeWire 可能不会主动获取或报告这些连接细节，减少开销，但也可能限制某些功能的可用性。

# bluez5.dummy-avrcp-player

它用于控制是否在 PipeWire 的蓝牙模块中注册一个“虚拟的 AVRCP 播放器”（dummy AVRCP player）。

### bluez5.dummy-avrcp-player 的作用

AVRCP（Audio/Video Remote Control Profile）是蓝牙协议中的一个配置文件，用于远程控制音频/视频设备，例如播放、暂停、音量调整等。bluez5.dummy-avrcp-player 的主要作用是：

- **解决设备兼容性问题**：某些蓝牙设备（例如 Bose Mini Soundlink II 或其他耳机）在未检测到 AVRCP 播放器时，可能无法正确启用音量控制或其他 AVRCP 功能。通过注册一个虚拟的 AVRCP 播放器，PipeWire 可以“欺骗”这些设备，使其认为系统中存在一个播放器，从而激活相关功能。
- 布尔值配置
  - true：启用虚拟 AVRCP 播放器。
  - false：禁用虚拟播放器，默认情况下不注册。

默认值在 PipeWire 的不同版本或发行版中可能有所不同，但在较新版本中通常默认为 true，以确保更广泛的设备兼容性。
