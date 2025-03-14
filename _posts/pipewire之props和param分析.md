---
title: pipewire之props和param分析
date: 2025-03-07 11:05:37
tags:
	- 音频
---

--

在 PipeWire 中，props（属性）和 param（参数）是两个核心概念，

用于配置和管理设备（device）、节点（node）和端口（port）。

它们在功能和使用场景上有明显的区别，同时又相互关联。

props 是通过 struct spa_dict（键值对集合）定义的静态配置，通常表示节点的固有属性或运行时可调整的特性。

param 是通过 struct spa_pod 定义的动态参数，用于描述节点或端口的配置、状态或能力（如格式、缓冲区）。

####  **关系对比**

| **方面**     | **props**                           | **param**                                         |
| ------------ | ----------------------------------- | ------------------------------------------------- |
| **数据结构** | struct spa_dict（键值对）           | struct spa_pod（POD 对象）                        |
| **类型标识** | SPA_PARAM_Props                     | 多种（如 SPA_PARAM_Format、SPA_PARAM_Latency）    |
| **作用范围** | 节点或设备级别                      | 节点和端口级别                                    |
| **动态性**   | 较静态，初始化时设置，可部分调整    | 动态，运行时协商                                  |
| **用途**     | 配置固有属性（如设备名、音量）      | 定义能力或状态（如格式、缓冲区）                  |
| **访问方式** | spa_node_set_param(SPA_PARAM_Props) | spa_node_port_enum_params 或 spa_node_enum_params |

**联系**：

- props 是一种特殊的 param（SPA_PARAM_Props），通过 spa_node_set_param 设置。
- param 包含 props，但还包括其他类型（如格式、延迟），功能更广。

**区别**：

- props 是节点级别的“配置表”，param 是节点和端口的“能力描述”。



### Device、Node、Port 的参数对比

| **对象**   | **典型 props**          | **典型 param**                   | **访问方式**              |
| ---------- | ----------------------- | -------------------------------- | ------------------------- |
| **Device** | device, minLatency      | Props, EnumFormat                | spa_device_enum_params    |
| **Node**   | live, volume, frequency | PropInfo, Props, IO, Latency     | spa_node_enum_params      |
| **Port**   | 无（继承节点的 props）  | EnumFormat, Buffers, IO, Latency | spa_node_port_enum_params |

- **Device**：关注硬件配置。
- **Node**：管理整体行为和属性。
- **Port**：处理数据流和格式。
