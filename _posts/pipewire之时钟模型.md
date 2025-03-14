---
title: pipewire之时钟模型
date: 2025-03-06 20:37:37
tags:
	- 音频
---

--

# 时钟模型

### PipeWire 的时钟模型简介

- 时钟（Clock）

  ：

  - PipeWire 使用 struct spa_io_clock 表示时钟，包含字段如 rate（采样率）、duration（周期样本数）、position（样本位置）等。
  - 通过 SPA_IO_Clock 接口传递给节点。

- 主时钟（Master Clock）

  ：

  - 图中某个节点（通常是音频源或硬件设备）提供主时钟，其他节点可以选择跟随（following = true）。

- 时钟更新

  ：

  - 主时钟通过 struct spa_io_position（包含 clock）广播给所有节点，驱动数据处理。

**时钟来源**：

- 在你的 BIS source 板子上，pw-play 播放本地文件，作为图的主时钟。
- BIS source（media-sink.c）通过 following = true 跟随 pw-play 的时钟。



# SPA_IO_Position 

它对应于 struct spa_io_position 结构体，用于在 PipeWire 图的节点间传递时钟和位置信息。

SPA_IO_Position 不仅仅是时钟数据，而是为原始时钟时间（raw clock times）赋予了逻辑意义，提供了图周期的起点和流时间的转换机制。

#### 1. **具体含义**

- SPA_IO_Position 是一个接口标识符

  ：

  - 表示节点通过 spa_node_set_io 设置的 struct spa_io_position 数据。
  - 它是 PipeWire 图中所有节点共享的全局时钟和位置信息的载体。

- 内容

  ：

  - **时钟状态**（clock）：由驱动节点（如 pw-play 或 audiotestsrc）提供，表示当前周期的逻辑时间。
  - **运行时间**（offset）：从时钟时间中减去偏移，得到图运行的总时间。
  - **流时间转换**（segments）：将运行时间映射到流的逻辑时间，支持变速、跳跃等。
  - **状态**（state）：反映图的运行状态（如运行、暂停）。

- 逻辑表示

  ：

  - 它是图中所有节点的“时间地图”，定义了当前周期的起点（clock.nsec）和未来的时间线（segments）。



**在 PipeWire 中的作用**：

1. **时钟同步**：广播驱动节点的时钟，确保节点一致。
2. **周期管理**：定义处理节奏（如 21.3ms）。
3. **流时间转换**：支持复杂时间线（如变速）。
4. **状态协调**：管理图的运行状态。
5. **数据驱动**：触发节点处理。
