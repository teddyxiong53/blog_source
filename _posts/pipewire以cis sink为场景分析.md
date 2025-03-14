---
title: pipewire以cis sink为场景分析
date: 2025-03-06 13:34:37
tags:
	- 音频
---

--

# 过程分析

BlueZ 将接收到的 CIS 数据通过文件描述符（fd）或共享内存传递给 PipeWire。

PipeWire 的 spa_node（通常是一个蓝牙源节点，media.class = Audio/Source）负责从 BlueZ 获取数据。

数据接收是通过事件触发完成的：

当 BlueZ 有新数据时，会通过 socket 或其他 IPC 机制通知 PipeWire，触发 spa_node_process()。



#### 2. **数据处理**

- 解码与格式转换

  ：

  - 接收到的 CIS 数据通常是 LC3 编码的音频流。PipeWire 使用 SPA 插件（如 spa/plugins/audioconvert 或专门的 LC3 解码器）将数据解码为 PCM 格式。
  - 解码后的数据会被放入缓冲区（buffer），供下游节点（如 ALSA sink）使用。

- 缓冲与同步

  ：

  - PipeWire 使用环形缓冲区（ring buffer）管理数据流，确保接收和处理之间的平滑过渡。
  - 数据处理由节点的 spa_node_process() 函数完成，该函数在每次有新数据或定时器触发时被调用。

- 输出到 sink

  ：

  - 解码后的 PCM 数据通过 PipeWire 图传递给目标 sink（例如 ALSA sink）。
  - sink 节点将数据写入硬件缓冲区，最终输出到声卡。



####  **运转的核心机制**

PipeWire 的数据流动依赖于两个主要循环：

- **Main Loop**：处理控制事件（如节点状态更新、命令发送），基于事件驱动。
- **Data Loop**：处理实时数据流，基于定时器或事件触发。 对于 CIS sink，数据接收和处理主要发生在 **data-loop** 中，而这个循环的运转确实依赖定时器。



### 数据传递的时序示例

假设 CIS 的 ISO 间隔为 10ms，采样率为 48kHz：

1. **0ms**：BlueZ 接收一个 10ms 的 LC3 帧（480 样本），通知 PipeWire。
2. **~1ms**：蓝牙源节点的 spa_node_process() 将 LC3 数据写入 spa_buffer。
3. **~2ms**：解码器节点接收 spa_buffer，解码为 PCM，生成新的 spa_buffer。
4. **~3ms**：ALSA sink 节点接收 PCM spa_buffer，写入硬件缓冲区。
5. **10ms**：下一帧数据到达，重复上述过程。
