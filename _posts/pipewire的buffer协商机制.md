---
title: pipewire的buffer协商机制
date: 2025-03-04 11:36:37
tags:
	- 音频
---

--

假设一个音频流：

- 客户端提议：48kHz、2 通道、1024 字节缓冲区。
- 服务器支持：48kHz、2 通道，但要求 2048 字节缓冲区。
- 协商结果：48kHz、2 通道、2048 字节缓冲区。

代码执行：

1. 客户端调用 pw_stream_connect，发送 SPA_PARAM_EnumFormat。
2. 服务器回复匹配的 SPA_PARAM_Format 和调整后的 SPA_PARAM_Buffers。
3. 客户端收到 param_changed 事件，更新流参数，开始传输。
