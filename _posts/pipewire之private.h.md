---
title: pipewire之private.h
date: 2025-03-11 11:39:37
tags:
	- 音频
---

--

pipewire/private.h 定义了 PipeWire 内部实现的核心结构体，涵盖了：

- **配置和管理**: settings, pw_context。
- **通信和协议**: pw_protocol, pw_resource, pw_proxy。
- **核心和客户端**: pw_impl_core, pw_core, pw_impl_client。
- **处理图和调度**: pw_impl_node, pw_node_activation, pw_impl_port, pw_impl_link。
- **模块和设备**: pw_impl_module, pw_impl_device。
- **流和扩展**: pw_stream, pw_filter, pw_impl_factory。



`pipewire/private.h` 是 PipeWire 的私有头文件，定义了许多内部使用的结构体和函数，这些内容不属于公开 API，而是 PipeWire 实现的核心组件。以下是对该文件中主要定义的结构体及其作用的详细说明，从全局视角分析它们在 PipeWire 系统中的功能和意义。

---

### 主要结构体及其作用

#### 1. **`struct settings`**
- **作用**: 定义了 PipeWire 的全局设置参数，主要用于配置系统的默认行为和运行时参数。
- **字段**:
  - `log_level`: 日志级别。
  - `clock_rate`, `clock_rates[]`, `n_clock_rates`: 默认和允许的时钟采样率。
  - `clock_quantum`, `clock_min_quantum`, `clock_max_quantum`, `clock_quantum_limit`, `clock_quantum_floor`: 与 "quantum" 相关的参数，控制处理周期的大小。
  - `video_size`, `video_rate`: 默认视频分辨率和帧率。
  - `link_max_buffers`: 链接的最大缓冲区数。
  - 标志位（如 `mem_allow_mlock`, `clock_power_of_two_quantum`）和更新模式（如 `clock_rate_update_mode`）。
- **全局意义**: 这是 PipeWire 的全局配置基础，影响核心调度（`pw_impl_core`）、节点处理（`pw_impl_node`）和客户端行为（`pw_core`）。例如，"quantum" 参数直接影响音频处理的延迟和性能。

---

#### 2. **`struct pw_param`**
- **作用**: 表示一个参数对象，用于存储和管理 SPA（Simple Plugin API）参数（如格式、延迟等），支持参数的添加、更新和清除。
- **字段**:
  - `id`: 参数的标识符。
  - `seq`: 序列号，用于同步。
  - `link`: 链表节点，用于组织参数列表。
  - `param`: 指向 SPA 参数的 POD（Plain Old Data）结构。
- **全局意义**: 在 PipeWire 中，参数是节点、端口等对象配置的核心机制。`pw_param` 提供了动态管理参数的能力，常用于 `pw_impl_node` 和 `pw_impl_port` 的参数协商。

---

#### 3. **`struct pw_protocol`**
- **作用**: 表示 PipeWire 的通信协议（如 `pw_protocol_native`），负责管理客户端和服务器之间的通信。
- **字段**:
  - `context`: 所属上下文。
  - `name`: 协议名称。
  - `marshal_list`, `client_list`, `server_list`: 分别管理协议的序列化器、客户端和服务器实例。
  - `listener_list`: 事件监听器。
  - `implementation`, `extension`: 协议的具体实现和扩展接口。
- **全局意义**: 它是 PipeWire 分布式架构的通信基础，连接 `pw_impl_core` 和 `pw_core`，支持 `pw_resource` 和 `pw_proxy` 的消息传递。

---

#### 4. **`struct pw_impl_core`**
- **作用**: 服务器端的核心实现，表示 PipeWire 实例的核心，管理全局资源和客户端连接。
- **字段**:
  - `context`, `global`, `properties`, `info`, `listener_list`: 与上下文、全局对象、属性和事件的关联。
  - `registered`: 是否注册标志。
- **全局意义**: 它是服务器端的“心脏”，通过 `pw_global` 导出自身，与客户端的 `pw_core` 交互，协调所有资源（如模块、节点）。

---

#### 5. **`struct pw_impl_metadata`**
- **作用**: 表示元数据对象，用于存储和管理系统的元数据（如路由信息、属性）。
- **字段**:
  - `context`, `global`, `properties`: 上下文、全局对象和属性。
  - `metadata`: 元数据接口。
  - `listener_list`: 事件监听器。
- **全局意义**: 提供全局状态的动态更新能力，例如在 LE Audio 中用于管理设备状态，客户端通过 `pw_resource` 访问。

---

#### 6. **`struct pw_impl_client`**
- **作用**: 表示服务器端的一个客户端实例，管理客户端的连接和资源。
- **字段**:
  - `core`, `context`, `global`: 核心、上下文和全局对象。
  - `permission_func`: 权限检查函数。
  - `properties`, `info`: 属性和信息。
  - `core_resource`, `client_resource`: 核心和客户端资源对象。
  - `objects`: 资源对象映射。
  - `protocol`, `recv_seq`, `send_seq`: 协议和序列号。
- **全局意义**: 它是服务器端对客户端的抽象，与 `pw_core` 对应，管理客户端的 `pw_resource` 和通信状态。

---

#### 7. **`struct pw_global`**
- **作用**: 表示一个全局对象，是服务器端资源的统一抽象，用于导出到客户端。
- **字段**:
  - `context`, `id`, `properties`, `type`, `version`: 上下文、ID、属性和接口类型。
  - `func`, `object`: 绑定函数和关联对象。
  - `resource_list`: 绑定到该全局对象的资源列表。
- **全局意义**: 它是 `export` 机制的核心，连接 `pw_impl_core`、`pw_impl_module` 等与客户端的 `pw_proxy`。

---

#### 8. **`struct pw_context`**
- **作用**: 表示 PipeWire 的全局上下文，是服务器端的顶层容器，管理所有对象和资源。
- **字段**:
  - `core`: 核心对象。
  - `conf`, `properties`, `defaults`, `settings`: 配置和运行时参数。
  - 各种列表（如 `core_impl_list`, `module_list`, `node_list`）: 管理核心、模块、节点等。
  - `main_loop`, `work_queue`: 主循环和工作队列。
- **全局意义**: 它是 PipeWire 的运行时环境，所有对象（`pw_impl_core`, `pw_impl_module`, `pw_impl_node` 等）都依赖它。

---

#### 9. **`struct pw_data_loop`**
- **作用**: 表示数据循环，用于处理实时数据（如音频流）。
- **字段**:
  - `loop`: 底层循环对象。
  - `affinity`, `rt_prio`: 线程亲和性和优先级。
  - `thread`, `running`: 线程和运行状态。
- **全局意义**: 它是 PipeWire 数据处理的执行环境，与 `pw_impl_node` 关联，负责 "quantum" 周期内的实时任务。

---

#### 10. **`struct pw_main_loop`**
- **作用**: 表示主循环，用于处理控制任务和事件。
- **字段**:
  - `loop`: 底层循环对象。
  - `running`: 运行状态。
- **全局意义**: 它是 PipeWire 的控制中心，与 `pw_context` 配合，处理非实时任务（如客户端请求）。

---

#### 11. **`struct pw_impl_device`**
- **作用**: 表示一个设备实例（如声卡、蓝牙设备）。
- **字段**:
  - `context`, `global`, `properties`, `info`: 上下文、全局对象和设备信息。
  - `device`: SPA 设备接口。
- **全局意义**: 它是硬件设备的抽象，通过 `pw_global` 导出，与 `pw_impl_node` 协作处理设备数据。

---

#### 12. **`struct pw_impl_module`**
- **作用**: 表示一个模块实例，用于扩展 PipeWire 功能。
- **字段**:
  - `context`, `global`, `properties`, `info`: 上下文、全局对象和模块信息。
- **全局意义**: 它是 PipeWire 可扩展性的基础，通过 `pw_global` 集成到系统中。

---

#### 13. **`struct pw_node_activation`**
- **作用**: 表示节点的激活状态，用于调度和同步节点处理。
- **字段**:
  - `status`: 当前状态（如触发、完成）。
  - `state[]`: 当前和下一状态。
  - `signal_time`, `awake_time`, `finish_time`: 时间戳。
  - `position`: 当前位置和段信息。
- **全局意义**: 它是 PipeWire 处理图（graph）调度的核心，支持 "quantum" 周期内的节点执行。

---

#### 14. **`struct pw_node_target`**
- **作用**: 表示节点的目标，用于调度依赖关系。
- **字段**:
  - `node`, `activation`, `fd`: 节点、激活状态和文件描述符。
  - `trigger`: 触发函数。
- **全局意义**: 它是节点间依赖管理的部分，与 `pw_node_activation` 配合实现图的驱动。

---

#### 15. **`struct pw_node_peer`**
- **作用**: 表示节点之间的对等关系（如输入输出连接）。
- **字段**:
  - `output`, `target`: 输出节点和目标。
- **全局意义**: 它是处理图中节点连接的抽象，与 `pw_impl_link` 相关。

---

#### 16. **`struct pw_impl_node`**
- **作用**: 表示一个节点实例，是 PipeWire 处理图的基本单元。
- **字段**:
  - `context`, `global`, `properties`, `info`: 上下文、全局对象和节点信息。
  - `node`: SPA 节点接口。
  - `input_ports`, `output_ports`: 输入输出端口。
  - `driver`, `target_list`: 驱动和目标。
- **全局意义**: 它是音频/视频处理的核心，通过 `pw_global` 导出，与 `pw_impl_port` 和 `pw_impl_link` 协作。

---

#### 17. **`struct pw_impl_port_mix`**
- **作用**: 表示端口的混合器配置，用于处理多输入/输出。
- **字段**:
  - `p`, `port`: 关联端口。
  - `io`: 输入输出缓冲区。
- **全局意义**: 它是端口数据处理的一部分，与 `pw_impl_port` 配合实现缓冲区协商。

---

#### 18. **`struct pw_impl_port`**
- **作用**: 表示一个端口实例，是节点的数据输入输出接口。
- **字段**:
  - `node`, `global`, `direction`, `port_id`: 节点、全局对象和端口信息。
  - `buffers`, `mix`: 缓冲区和混合器。
- **全局意义**: 它是节点与链接的接口，通过 `pw_global` 导出，支持数据流动。

---

#### 19. **`struct pw_control_link`** 和 **`struct pw_control`**
- **作用**: 表示控制链接和控制对象，用于管理控制数据（如音量）。
- **字段**:
  - `output`, `input`: 输出输入控制端。
  - `context`, `port`: 上下文和端口。
- **全局意义**: 它们是控制流的抽象，与 `pw_impl_port` 关联。

---

#### 20. **`struct pw_impl_link`**
- **作用**: 表示节点之间的链接，连接输入和输出端口。
- **字段**:
  - `context`, `global`, `output`, `input`: 上下文、全局对象和端口。
  - `io`: 输入输出缓冲区。
- **全局意义**: 它是处理图中数据流的连接器，通过 `pw_global` 管理。

---

#### 21. **`struct pw_resource`**
- **作用**: 表示客户端对服务器资源的绑定。
- **字段**:
  - `context`, `global`, `client`, `id`, `bound_id`: 上下文、全局对象和绑定信息。
  - `marshal`: 协议序列化器。
- **全局意义**: 它是客户端与服务器交互的桥梁，与 `pw_proxy` 对应。

---

#### 22. **`struct pw_proxy`**
- **作用**: 表示客户端对服务器资源的代理。
- **字段**:
  - `core`, `id`, `bound_id`: 核心和绑定信息。
  - `marshal`: 协议序列化器。
- **全局意义**: 它是客户端的本地表示，与 `pw_resource` 协作。

---

#### 23. **`struct pw_core`**
- **作用**: 表示客户端侧的核心，与服务器交互。
- **字段**:
  - `proxy`, `context`, `properties`: 代理、上下文和属性。
  - `objects`: 本地对象映射。
- **全局意义**: 它是客户端的“窗口”，连接 `pw_impl_core`。

---

#### 24. **`struct pw_stream`** 和 **`struct pw_filter`**
- **作用**: 表示客户端的流和过滤器，用于处理音频/视频数据。
- **字段**:
  - `core`, `name`, `properties`, `node_id`: 核心、名称和节点信息。
- **全局意义**: 它们是客户端的高级抽象，依赖 `pw_core` 和 `pw_impl_node`。

---

#### 25. **`struct pw_impl_factory`**
- **作用**: 表示工厂，用于创建对象实例。
- **字段**:
  - `context`, `global`, `info`: 上下文、全局对象和信息。
- **全局意义**: 它是对象创建的机制，通过 `pw_global` 导出。

