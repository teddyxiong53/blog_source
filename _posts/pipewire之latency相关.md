---
title: pipewire之latency相关
date: 2025-02-28 17:23:37
tags:
	- 音频
---

--

# `SPA_PARAM_Latency` 和 `SPA_PARAM_ProcessLatency`

`SPA_PARAM_Latency` 和 `SPA_PARAM_ProcessLatency` 都与 **音频处理的延迟（latency）** 相关，但它们的作用和应用场景不同。

------

## **1. `SPA_PARAM_Latency`**

- **作用**：用于报告 **设备（source/sink）端的 I/O 延迟**。

- **类型**：`SPA_TYPE_OBJECT_ParamLatency`

- **应用场景**：

  - 用于 **音频设备**（例如声卡、麦克风、扬声器等）报告 **输入/输出延迟**。
  - 主要用于 **流（streaming）** 计算，确保不同设备之间的 **同步**。
  - 例如，在 PipeWire 中，蓝牙、USB 声卡等 **都会提供这个参数**，用于 **延迟补偿**。

- **示例**

  ```c
  struct spa_pod *latency_pod = spa_pod_builder_add_object(&b,
      SPA_TYPE_OBJECT_ParamLatency, SPA_PARAM_Latency,
      SPA_LATENCY_QUANTUM, SPA_POD_Fraction(1, 48000),  // 采样率 48kHz
      SPA_LATENCY_MIN, SPA_POD_Int(256),  // 最小 buffer size
      SPA_LATENCY_MAX, SPA_POD_Int(1024)  // 最大 buffer size
  );
  ```

  这个 POD 定义了 **采样率为 48kHz 时的延迟范围**（`256 - 1024` 个样本）。

------

## **2. `SPA_PARAM_ProcessLatency`**

- **作用**：用于报告 **软件/处理流程的延迟**，而不是设备的 I/O 延迟。

- **类型**：`SPA_TYPE_OBJECT_ParamProcessLatency`

- **应用场景**：

  - 适用于 **音频处理节点（nodes）**，用于报告 **内部 DSP、混音、音效处理等的延迟**。
  - **不用于设备端，而是用于音频处理 pipeline 里的组件**（例如 LADSPA 插件、EQ 处理、回声消除等）。
  - 这对于 **低延迟应用（如实时音频）** 非常重要，需要精确补偿 DSP 处理时间。

- **示例**

  ```c
  struct spa_pod *proc_latency_pod = spa_pod_builder_add_object(&b,
      SPA_TYPE_OBJECT_ParamProcessLatency, SPA_PARAM_ProcessLatency,
      SPA_LATENCY_QUANTUM, SPA_POD_Fraction(1, 48000),
      SPA_LATENCY_MIN, SPA_POD_Int(128),  // 处理延迟最小 128 个样本
      SPA_LATENCY_MAX, SPA_POD_Int(256)   // 处理延迟最大 256 个样本
  );
  ```

  这个 POD 表示 **音频处理节点（比如 DSP 插件）** 需要 **128 到 256 个样本的延迟**。

------

## **区别总结**

| 参数                       | 作用              | 适用范围                                    | 影响的延迟类型           |
| -------------------------- | ----------------- | ------------------------------------------- | ------------------------ |
| `SPA_PARAM_Latency`        | **设备 I/O 延迟** | **音频设备（source/sink）**，如麦克风、声卡 | **采样 buffer 传输延迟** |
| `SPA_PARAM_ProcessLatency` | **软件处理延迟**  | **音频处理节点（nodes）**，如 DSP、EQ、混音 | **内部处理时间延迟**     |

**简单来说**：

- `SPA_PARAM_Latency` 主要用于 **硬件设备**（声卡、蓝牙、USB Audio）报告延迟。
- `SPA_PARAM_ProcessLatency` 主要用于 **软件处理**（DSP、滤波、混音）报告延迟。

如果你在 **调整音频同步**，一般关注 `SPA_PARAM_Latency`。
 如果你在 **开发音频插件**（如 LADSPA 插件）或 **调试 DSP 延迟**，关注 `SPA_PARAM_ProcessLatency`。

# 相关的概念

### 对比分析

| **概念**          | **定义**           | **单位** | **来源**                   | **作用**                     | **与 BIS 的关系**                 |
| ----------------- | ------------------ | -------- | -------------------------- | ---------------------------- | --------------------------------- |
| minLatency        | 节点的最小缓冲延迟 | 样本数   | 节点属性 (Props)           | 确保硬件或节点的最小缓冲需求 | 影响下游 sink，可能导致积压       |
| quantum           | 图的调度单位       | 样本数   | 配置或命令行               | 控制处理周期，平衡延迟与开销 | 不匹配 ISO 间隔可能导致 err       |
| clock.duration    | 当前周期的样本数   | 样本数   | 驱动节点的 SPA_IO_Position | 定义图的节奏，驱动数据处理   | 若与 10ms 不符，影响 process_time |
| SPA_PARAM_Latency | 节点的固有延迟     | 纳秒     | 节点参数 (Latency)         | 报告延迟，优化图同步         | 可设置 10ms，优化 BIS 同步        |
| delay             | 时钟的偏差         | 样本数   | 时钟状态 (SPA_IO_Clock)    | 调整时钟同步，反映漂移       | 间接影响 err，反映时间偏差        |

# io.h里的结构体

**spa_io_buffers**：缓冲区交换。

**spa_io_clock**：节点时钟，驱动同步。

**spa_io_position**：图全局位置，包含 clock。

**spa_io_sequence**：控制消息。

**spa_io_rate_match**：速率匹配。

**未使用**：spa_io_memory、spa_io_range、spa_io_latency。

**与 BIS 的关系**：

- clock 和 position 是核心，驱动 media_iso_pull。
- rate_match 可优化同步。



就是定义的结构体很多没有使用。

要么是给未来预留的，要么就是废弃的。



# SPA_PROP_latencyOffsetNsec 

**SPA_PROP_latencyOffsetNsec 的核心作用**：

- 表示节点引入的额外延迟偏移（可以是正值或负值），用于调整 PipeWire 图中音频或数据的同步。
- 它允许用户或应用手动校正节点的延迟，以补偿硬件、驱动或其他处理环节引入的时间偏差。



# 对bluez_input的node.latency没有作用

### 1. node.latency 的作用

在 PipeWire 中，node.latency 是一个属性（PW_KEY_NODE_LATENCY），==用于指定节点的期望延迟==，通常格式为 "样本数/采样率"（如 "128/48000" 表示 128 样本在 48kHz，约 2.67ms）。它的主要作用是：

- **控制缓冲区大小**：影响节点处理数据的周期长度。
- **调整延迟**：在实时音频处理中平衡延迟和稳定性。
- **影响调度**：驱动节点通过此参数决定图的量子大小（quantum size）。

#### 关键点

- node.latency ==通常对 **驱动节点（driver node）** 生效，因为驱动节点控制整个图的时钟和调度。==
- 对于 **从节点（follower node）**，如 bluez_input，它的作用取决于具体实现和上下文。

### 2. bluez_input 的角色

bluez_input 是 PipeWire 的蓝牙输入节点（source），它的特点：

- **从节点**：通常不直接驱动图，而是跟随驱动节点（如 ALSA sink）的调度。
- **数据来源**：从蓝牙协议栈（BlueZ）接收音频数据（A2DP 或 LE Audio 的 CIS）。
- **实时性**：==依赖蓝牙传输的实时性，数据到达时间可能不稳定。==

#### 与 ALSA Sink 的关系

- 在你的场景中，bluez_input 输出数据到本地 ALSA sink（驱动节点）。
- ALSA sink 控制图的时钟和缓冲区大小，bluez_input 提供数据并跟随其节奏。
