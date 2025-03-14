---
title: pipewire之native protocol分析
date: 2025-03-11 14:58:37
tags:
	- 音频
---

--

# protocol-native.c总结

这份代码是 PipeWire 的协议实现文件，

定义了 PipeWire 原生协议（`pw_protocol_native`）的序列化（marshal）

和反序列化（demarshal）逻辑，

用于客户端和服务器之间的通信。

代码主要集中在如何将 PipeWire 的核心对象（如 `pw_core`、`pw_registry`、`pw_node` 等）的方法和事件编码为 POD（Plain Old Data）结构，

以及如何解析接收到的 POD 数据并触发相应的事件或方法调用。



---

### 1. 代码功能概述
这份代码实现了 PipeWire 原生协议（`pw_protocol_native`）的通信机制，主要包括：
- **序列化（Marshal）**：
  - 将客户端调用（如 `pw_core_hello`）或服务器事件（如 `pw_core_event_info`）编码为 POD 数据，发送给对端。
- **反序列化（Demarshal）**：
  - 解析接收到的 POD 数据，触发相应的事件或方法（如 `core_event_demarshal_done`）。
- **协议注册**：
  - 在 `pw_protocol_native_init` 中注册各种对象的序列化和反序列化方法。

#### 适用对象
协议支持以下 PipeWire 对象：
- `pw_core`：核心对象，用于建立连接和同步。
- `pw_registry`：注册表，用于发现全局对象。
- `pw_node`：节点（如 `bluez_input` 和 ALSA sink）。
- `pw_port`：端口。
- `pw_link`：链接。
- `pw_client`：客户端。
- `pw_device`：设备。
- `pw_factory`：工厂。
- `pw_module`：模块。
- `pw_security_context`：安全上下文。

#### 通信机制
- 使用 `spa_pod_builder` 和 `spa_pod_parser` 构建和解析 POD 数据。
- 通过 `pw_protocol_native_begin_proxy` 和 `pw_protocol_native_end_proxy` 发送消息。
- 支持异步操作（如 `SPA_RESULT_RETURN_ASYNC`）。

---

### 2. 主要结构体和函数

#### 2.1. 核心结构体
以下结构体在代码中起到关键作用：
- **`struct pw_proxy`**：
  - 表示代理对象，用于客户端与服务器通信。
  - 方法如 `pw_proxy_add_object_listener` 和 `pw_proxy_notify` 用于事件监听和通知。
- **`struct pw_resource`**：
  - 表示服务器端的资源对象。
  - 方法如 `pw_resource_notify` 用于触发客户端方法。
- **`struct spa_pod_builder`** 和 **`struct spa_pod_parser`**：
  - 用于构建和解析 POD 数据。
  - 提供 `spa_pod_builder_add_struct` 和 `spa_pod_parser_get_struct` 等方法。
- **`struct pw_protocol_native_message`**：
  - 表示协议消息，包含序列号（`seq`）和数据（`data`）。
- **`struct spa_dict`** 和 **`struct spa_dict_item`**：
  - 用于存储键值对（如节点的属性）。
  - `push_dict` 和 `parse_dict` 函数处理字典的序列化和反序列化。

#### 2.2. 事件和方法结构体
每种 PipeWire 对象都有对应的事件和方法结构体，例如：
- **`struct pw_core_methods`** 和 **`struct pw_core_events`**：
  - 定义核心方法（如 `hello`、`sync`）和事件（如 `info`、`done`）。
- **`struct pw_node_methods`** 和 **`struct pw_node_events`**：
  - 定义节点方法（如 `set_param`）和事件（如 `info`）。
- **`struct pw_protocol_marshal`**：
  - 定义协议的序列化和反序列化方法：
    ```c
    struct pw_protocol_marshal {
        const char *type;               // 对象类型（如 PW_TYPE_INTERFACE_Node）
        uint32_t version;               // 版本号
        uint32_t flags;                 // 标志
        uint32_t n_methods;             // 方法数量
        uint32_t n_events;              // 事件数量
        const void *client_marshal;     // 客户端序列化方法
        const struct pw_protocol_native_demarshal *server_demarshal; // 服务器反序列化
        const void *server_marshal;     // 服务器序列化
        const struct pw_protocol_native_demarshal *client_demarshal; // 客户端反序列化
    };
    ```

#### 2.3. 关键函数
- **序列化函数**（如 `core_method_marshal_hello`）：
  - 使用 `spa_pod_builder` 构建 POD 数据。
  - 示例：
    ```c
    static int core_method_marshal_hello(void *object, uint32_t version) {
        struct pw_proxy *proxy = object;
        struct spa_pod_builder *b;
        b = pw_protocol_native_begin_proxy(proxy, PW_CORE_METHOD_HELLO, NULL);
        spa_pod_builder_add_struct(b, SPA_POD_Int(version));
        return pw_protocol_native_end_proxy(proxy, b);
    }
    ```
- **反序列化函数**（如 `core_event_demarshal_info`）：
  - 使用 `spa_pod_parser` 解析 POD 数据。
  - 示例：
    ```c
    static int core_event_demarshal_info(void *data, const struct pw_protocol_native_message *msg) {
        struct pw_proxy *proxy = data;
        struct spa_dict props = SPA_DICT_INIT(NULL, 0);
        struct pw_core_info info = { .props = &props };
        struct spa_pod_parser prs;
        spa_pod_parser_init(&prs, msg->data, msg->size);
        // 解析字段
        if (spa_pod_parser_get(&prs,
                SPA_POD_Int(&info.id),
                SPA_POD_String(&info.user_name), /* ... */) < 0)
            return -EINVAL;
        parse_dict_struct(&prs, &f[1], &props);
        return pw_proxy_notify(proxy, struct pw_core_events, info, 0, &info);
    }
    ```
- **辅助函数**：
  - `push_dict` 和 `parse_dict`：处理字典。
  - `push_params` 和 `parse_params_struct`：处理参数列表。
  - `pw_protocol_native_begin_proxy` 和 `pw_protocol_native_end_proxy`：开始和结束消息发送。

#### 2.4. 协议初始化
- **`pw_protocol_native_init`**：
  - 注册所有对象的序列化和反序列化方法：
    ```c
    void pw_protocol_native_init(struct pw_protocol *protocol) {
        pw_protocol_add_marshal(protocol, &pw_protocol_native_core_marshal);
        pw_protocol_add_marshal(protocol, &pw_protocol_native_node_marshal);
        // 其他对象...
    }
    ```

---

### 3. 协议通信流程

#### 3.1. 客户端到服务器（方法调用）
1. **客户端调用方法**：
   - 例如，客户端调用 `pw_core_hello`：
     ```c
     pw_core_hello(core, PW_VERSION_CORE);
     ```
2. **序列化**：
   - `core_method_marshal_hello` 将 `version` 编码为 POD 数据。
   - 使用 `pw_protocol_native_begin_proxy` 和 `pw_protocol_native_end_proxy` 发送。
3. **服务器解析**：
   - 服务器接收消息，使用 `core_method_demarshal_hello` 解析。
   - 调用 `pw_resource_notify` 触发 `hello` 方法。

#### 3.2. 服务器到客户端（事件通知）
1. **服务器触发事件**：
   - 例如，服务器发送 `info` 事件：
     ```c
     core_event_marshal_info(resource, info);
     ```
2. **序列化**：
   - 使用 `spa_pod_builder` 构建 POD 数据，发送给客户端。
3. **客户端解析**：
   - 客户端使用 `core_event_demarshal_info` 解析 POD 数据。
   - 调用 `pw_proxy_notify` 触发 `info` 事件回调。

#### 3.3. 异步操作
- 方法如 `sync` 和 `enum_params` 使用 `SPA_RESULT_RETURN_ASYNC` 返回异步序列号：
  ```c
  spa_pod_builder_add_struct(b,
      SPA_POD_Int(SPA_RESULT_RETURN_ASYNC(msg->seq)),
      SPA_POD_Id(id), /* ... */);
  ```
- 服务器通过 `done` 事件通知完成：
  ```c
  core_event_marshal_done(resource, id, seq);
  ```

---

### 4. 与你的场景的关联

#### 4.1. 丢帧问题
- **节点通信**：
  - `bluez_input` 和 ALSA sink 的 `pw_node` 通过 `pw_protocol_native_node_marshal` 通信。
  - 方法如 `set_param`（`node_marshal_set_param`）可调整节点的延迟：
    ```c
    node_marshal_set_param(proxy, SPA_PARAM_Latency, 0, latency_pod);
    ```
  - 如果延迟设置不当，可能导致 `bluez_input` 的 `underrun samples:11`。
- **事件通知**：
  - `node_marshal_info` 传递 `pw_node_info`，包括 `state` 和 `error`。
  - 你的日志显示 `node_ready` 检测到 XRun，可能通过 `info` 事件通知客户端。

#### 4.2. 波形变形
- **缓冲区管理**：
  - `core_event_marshal_add_mem` 和 `remove_mem` 管理共享内存。
  - `bluez_input` 的缓冲区不足可能通过 `add_mem` 分配，但未及时填充。
- **参数调整**：
  - `node_marshal_enum_params` 和 `set_param` 可调整缓冲区参数。
  - 增大缓冲区可能减少填 0 行为，缓解波形跳变。

#### 4.3. 协议效率
- 协议使用 POD 数据，效率较高，但如果 `bluez_input` 的数据流未及时同步（例如 `sync` 方法延迟），可能导致调度滞后。

---

### 5. 优化建议

#### 5.1. 增大缓冲区
- 使用 `node_marshal_set_param` 调整 `bluez_input` 的延迟：
  ```c
  struct spa_pod_builder b = SPA_POD_BUILDER_INIT(buffer, sizeof(buffer));
  struct spa_pod *latency_pod = spa_pod_builder_add_object(&b,
      SPA_TYPE_OBJECT_ParamLatency, SPA_PARAM_Latency,
      SPA_POD_Fraction(&SPA_FRACTION(256, 48000)));
  pw_node_set_param(node, SPA_PARAM_Latency, 0, latency_pod);
  ```

#### 5.2. 监控 XRun
- 监听 `node_marshal_info` 事件，检查 `state` 和 `error`：
  ```c
  static void on_node_info(void *data, const struct pw_node_info *info) {
      if (info->state == PW_NODE_STATE_ERROR) {
          printf("Node error: %s\n", info->error);
      }
  }
  ```

#### 5.3. 改进协议
- 如果协议通信延迟影响实时性，可以优化 `pw_protocol_native` 的消息处理，减少序列化和反序列化的开销。

---

### 6. 总结
- **功能**：
  - 代码实现了 PipeWire 原生协议的序列化和反序列化，支持核心对象通信。
- **关键结构体**：
  - `pw_proxy`、`pw_resource`、`spa_pod_builder`、`spa_pod_parser`。
- **你的场景**：
  - `bluez_input` 的丢帧可能与缓冲区不足或调度延迟有关，可通过 `set_param` 调整。
  - 波形变形源于填 0，需优化 `process_buffering` 或增大缓冲区。

如果需要更详细的协议分析或客户端代码实现，我可以进一步协助！有什么想补充的吗？

# 官方文档总结

以下是对 PipeWire 1.2.7 版本“Native Protocol”文档（来源于 `https://docs.pipewire.org/page_native_protocol.html`）的详细分析和总结。该文档描述了 PipeWire 的原生客户端/服务器 IPC 协议，基于 Unix 域套接字实现，定义了消息格式、连接流程以及核心对象（如 Core、Registry、Node 等）的通信方法和事件。以下从结构、核心机制、对象接口和设计意义四个方面进行分析，并总结其特点。

---

### 一、文档结构与概述

#### 1. **目的**
- **描述**: 定义 PipeWire 的原生协议（Protocol Native），用于客户端与服务器间的通信。
- **实现**: 使用 Unix 域套接字，支持可插拔协议。

#### 2. **主要部分**
- **消息头**: 统一的消息格式。
- **连接流程**: 建立客户端与服务器连接。
- **核心对象接口**: Core、Registry、Client、Device、Node 等的方法和事件。
- **消息脚注（Footer）**: 额外的元数据（如注册表生成号）。
- **注册表生成（Registry Generation）**: 处理异步 ID 管理的机制。

#### 3. **版本与状态**
- **版本**: PipeWire 1.2.7。
- **日期**: 当前为 2025 年 3 月 10 日，可能落后于最新版本（如 1.4.x）。

---

### 二、核心机制分析

#### 1. **消息头格式**
- **结构**:
  ```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  | Id                                                            |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  | opcode                | size                                  |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  | seq                                                           |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  | n_fds                                                         |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  | payload POD                                                   |
  .                                                               .
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  | optional footer POD                                           |
  .                                                               .
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  ```
- **字段**:
  - `Id`: 目标资源/代理 ID。
  - `opcode`: 操作码，定义消息类型。
  - `size`: 负载和脚注的总大小。
  - `seq`: 递增的序列号。
  - `n_fds`: 文件描述符数量。
- **负载**: 单 POD（Plain Old Data），基于 SPA POD 格式。
- **脚注**: 可选 POD，附加信息。
- **特点**: 支持文件描述符传递，分片处理大消息。

#### 2. **连接流程**
- **套接字**: 默认名为 `pipewire-0`，在环境变量（如 `PIPEWIRE_RUNTIME_DIR`）中查找。
- **步骤**:
  1. 客户端打开套接字，分配 Core 代理（ID 0）和 Client 代理（ID 1）。
  2. 服务器分配 Core 资源（ID 0），绑定 Client 资源（ID 1）。
  3. 客户端发送 `Core::Hello` 开始通信。
  4. 客户端发送 `Client::UpdateProperties` 更新属性。
- **图示**:
  ```
  Client                  Server
  |------------------------>|
  | open socket            |
  |------------------------>|
  | Core::Hello(version)   |
  |------------------------>|
  | Client::UpdateProperties|
  ```
- **意义**: 建立双向通信，初始化代理和资源映射。

#### 3. **注册表生成（Registry Generation）**
- **机制**:
  - 服务器维护 64 位生成号（`registry_generation`），分配新全局 ID 时递增。
  - 全局 ID 作为 `(id, object_generation)` 元组存储。
  - 客户端跟踪最新处理生成号（`client_generation`）。
- **流程**:
  1. 服务器通过脚注发送 `Core Generation`。
  2. 客户端通过脚注回复 `Client Generation`。
  3. 服务器根据客户端生成号验证 ID。
- **错误处理**: 若生成号过旧，返回 `ESTALE` 错误。
- **意义**: 解决异步协议中 ID 重用问题。

---

### 三、核心对象接口分析

#### 1. **Core (ID 0)**
- **方法**:
  - `Hello`: 初始化通信，携带版本号（3）。
  - `Sync`: 请求同步，返回 `Done` 事件。
  - `GetRegistry`: 获取注册表对象。
  - `CreateObject`: 从工厂创建对象。
- **事件**:
  - `Info`: 服务器信息。
  - `Done`: 同步完成。
  - `Error`: 致命错误。
- **作用**: 核心通信入口，管理全局操作。

#### 2. **Registry**
- **方法**:
  - `Bind`: 绑定全局对象。
  - `Destroy`: 销毁全局对象。
- **事件**:
  - `Global`: 新全局对象通知。
  - `GlobalRemove`: 全局对象移除。
- **作用**: 提供全局对象目录。

#### 3. **Client (ID 1)**
- **方法**:
  - `UpdateProperties`: 更新客户端属性。
  - `GetPermissions`: 获取权限。
- **事件**:
  - `Info`: 客户端信息更新。
- **作用**: 管理客户端状态和权限。

#### 4. **Node**
- **方法**:
  - `EnumParams`: 枚举参数。
  - `SetParam`: 设置参数。
  - `SendCommand`: 发送命令。
- **事件**:
  - `Info`: 节点信息。
  - `Param`: 参数更新。
- **作用**: 图中的处理单元。

#### 5. **ClientNode**
- **方法**:
  - `GetNode`: 获取关联节点。
  - `PortBuffers`: 设置端口缓冲区。
- **事件**:
  - `Transport`: 传输激活记录和事件 FD。
- **作用**: 客户端控制的服务器节点，与 `pw_stream` 相关。

---

### 四、设计特点与意义

#### 1. **高效性**
- **共享内存**: 通过 `memfd` 和 `eventfd` 传递数据和信号。
- **实时支持**: `ClientNode::Transport` 提供 RT 调度支持。

#### 2. **灵活性**
- **可插拔**: 支持扩展协议。
- **对象化**: 通过代理和资源抽象远程对象。

#### 3. **健壮性**
- **序列号**: `seq` 确保消息顺序。
- **生成号**: 解决 ID 重用冲突。

#### 4. **与代码关联**
- **实现**: `pipewire/protocol-native.c`。
- **示例**: `export-spa-node.c` 使用 `Core::CreateObject` 创建节点。

---

### 五、总结

PipeWire 的原生协议基于 Unix 套接字，提供高效、灵活的 IPC 机制。其消息格式支持负载和脚注，连接流程简洁，核心对象接口覆盖全局管理（Core）、对象发现（Registry）和媒体处理（Node、ClientNode）。注册表生成机制增强了异步通信的可靠性。该协议是 PipeWire 系统（如 `pw_stream` 和图调度）的通信基础，适合实时多媒体应用。建议关注最新版本文档以获取可能的更新。

如需更深入分析（如具体方法的实现），请进一步指示！
