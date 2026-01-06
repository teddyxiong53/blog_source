---
title: Pipewire之wireplumber
date: 2025-05-23 19:27:17
tags:
	- 音频

---

--

现在主要是靠deepwiki的内容保存。

# autoswitch-to-headset-profile

当 `bluetooth.autoswitch-to-headset-profile` 为 `true` 时：

1. **自动切换到耳机模式**：当检测到音频输入流（如通话、录音）时，蓝牙设备会自动从 A2DP 配置文件切换到 HSP/HFP 配置文件
2. **自动切换回音乐模式**：当输入流结束时，设备会自动切换回 A2DP 配置文件以获得更好的音质

这个功能特别适用于蓝牙耳机用户，可以在通话时自动切换到支持麦克风的配置文件，通话结束后自动切换回高音质的音乐配置文件，提供更好的用户体验。

# monitor.bluez.properties

`monitor.bluez.properties` 是配置 WirePlumber 蓝牙功能的核心配置段，涵盖了从基本的角色和编解码器设置到高级的 Opus Pro Audio 和 LE Audio BAP 服务器能力配置。这些设置直接影响蓝牙设备的连接方式、音质和功能支持。



# 硬件数据库机制

这些功能的启用状态通常由 WirePlumber 的硬件兼容性数据库决定，

该数据库包含了已知设备的兼容性信息。

通过显式设置这些选项，您可以覆盖数据库的默认行为，强制启用或禁用这些功能。

这种基于硬件数据库的自动启用机制确保了最佳的设备兼容性，避免了因功能不兼容导致的连接问题或音质下降。只有在确定设备支持或需要调试时，才建议手动覆盖这些设置。
