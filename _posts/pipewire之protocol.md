---
title: pipewire之protocol
date: 2025-05-30 10:21:37
tags:
	- 音频
---

--

# 官方文档protocol.dox文档总结

### PipeWire 原生协议文档翻译总结

本文件描述了 PipeWire 的可插拔客户端/服务器 IPC 协议，参考实现基于 unix 套接字，由 **page_module_protocol_native** 模块实现。以下是文档的翻译总结，保留专有名词术语和图标。

#### 消息头格式 {#native-protocol-message-header}
每个消息包含 16 字节头部和可变长度负载：

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                     Id                                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |    opcode     |                   size                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                         seq                                   |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                         n_fds                                 |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                     payload POD                               |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                     optional footer POD                       |
   .                                                               .
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **Id**：目标 **resource/proxy** 的 ID。
- **opcode**：**resource/proxy** 接口的操作码。
- **size**：消息负载和可选尾部的总大小。
- **seq**：每个消息的递增序列号。
- **n_fds**：消息中包含的文件描述符数量。

消息发送时需附带文件描述符，若文件描述符过多，消息会分片发送。接收方先读取头部以确定消息大小，再处理 **payload POD**（见 **page_spa_pod**）和可选的 **footer POD**。

#### 建立连接 {#native-protocol-making-connection}
客户端连接到默认命名为 **pipewire-0** 的 unix 套接字，搜索路径包括：
- **getenv("PIPEWIRE_RUNTIME_DIR")**
- **getenv("XDG_RUNTIME_DIR")**
- **getenv("USERPROFILE")**

连接后：
1. 客户端分配 ID 0 的 **Core proxy** 和 ID 1 的 **Client proxy**，用于标识远程对象。
2. 服务器分配 ID 0 的 **Core resource**，作为客户端 **proxy** 的对应物。
3. 客户端发送 **Core::Hello** 消息启动通信。
4. 服务器将 ID 1 的 **resource** 绑定到客户端。
5. 客户端发送客户端属性，完成设置，客户端出现在 **registry** 中。

```
   client                                    server
     |---------------------------------------->|
     |            open socket                  |
     |                                         |
     |---------------------------------------->|
     |            Core::Hello(version)         |
     |                                         |
     |---------------------------------------->|
     |       Client::UpdateProperties          |
     .                                         .
```

#### Core 代理/资源 {#native-protocol-core}
**Core** 对象始终为 ID 0。

##### Core 方法
- **Core::Hello (Opcode 1)**：客户端首次发送，包含版本号（当前为 3）。
- **Core::Sync (Opcode 2)**：触发服务器返回 **Done** 事件，确保之前操作完成。
- **Core::Pong (Opcode 3)**：响应服务器的 **Ping** 事件，复制 **id** 和 **seq**。
- **Core::Error (Opcode 4)**：报告客户端对象的错误，包含 **id**、**seq**、错误码和消息。
- **Core::GetRegistry (Opcode 5)**：请求绑定 **registry** 对象，列出服务器可用对象，触发 **Registry::Global** 事件。
- **Core::CreateObject (Opcode 6)**：通过 **factory** 创建新对象，指定 **factory_name**、**type**、**version**、**props** 和 **new_id**。
- **Core::Destroy (Opcode 7)**：销毁指定 **id** 的对象。

##### Core 事件
- **Core::Info (Opcode 0)**：连接时或服务器信息变化时触发，提供服务器信息（如 **cookie**、**user_name**、**version** 等）。
- **Core::Done (Opcode 1)**：响应 **Sync** 方法，确认操作完成。
- **Core::Ping (Opcode 2)**：服务器检查客户端存活或事件处理状态。
- **Core::Error (Opcode 3)**：报告致命错误，包含 **id**、**seq**、错误码和消息。
- **Core::RemoveId (Opcode 4)**：通知客户端对象 ID 已移除，可安全重用。
- **Core::BoundId (Opcode 5)**：通知本地对象 ID 绑定到全局 ID（已弃用，推荐 **BoundProps**）。
- **Core::AddMem (Opcode 6)**：向客户端分配内存（如 **memfd**），包含 **id**、**type**、**fd** 和 **flags**。
- **Core::RemoveMem (Opcode 7)**：移除指定 **id** 的内存。
- **Core::BoundProps (Opcode 8)**：通知本地对象 ID 绑定到全局 ID，包含附加属性。

#### Registry 代理/资源 {#native-protocol-registry}
通过 **Core::GetRegistry** 获取，ID 由 **new_id** 指定。

##### Registry 方法
- **Registry::Bind (Opcode 1)**：绑定到指定全局 **id**，使用 **new_id** 作为代理，指定 **type** 和 **version**。
- **Registry::Destroy (Opcode 2)**：尝试销毁全局对象，可能因权限不足失败。

##### Registry 事件
- **Registry::Global (Opcode 0)**：通知新全局对象，包含 **id**、**permissions**、**type**、**version** 和 **props**。
- **Registry::GlobalRemove (Opcode 1)**：通知全局对象移除。

#### Client 接口 {#native-protocol-client}
表示连接到服务器的客户端，ID 1 用于当前客户端。

##### Client 方法
- **Client::Error (Opcode 1)**：向客户端发送错误。
- **Client::UpdateProperties (Opcode 2)**：更新客户端属性。
- **Client::GetPermissions (Opcode 3)**：获取客户端权限，触发 **Permissions** 事件。
- **Client::UpdatePermissions (Opcode 4)**：更新全局对象的权限。

##### Client 事件
- **Client::Info (Opcode 0)**：提供客户端信息更新，包含 **id**、**change_mask** 和 **props**。
- **Client::Permissions (Opcode 1)**：响应 **GetPermissions**，返回权限列表。

#### Device 接口 {#native-protocol-device}
管理其他 **device** 或 **node**。

##### Device 方法
- **Device::SubscribeParams (Opcode 1)**：订阅参数变化，触发 **Param** 事件。
- **Device::EnumParams (Opcode 2)**：枚举参数值，触发 **Param** 事件。
- **Device::SetParam (Opcode 3)**：设置参数。

##### Device 事件
- **Device::Info (Opcode 0)**：绑定或信息变化时触发，包含 **id**、**change_mask**、**props** 和 **param_info**。
- **Device::Param (Opcode 1)**：响应 **EnumParams** 或 **SubscribeParams**，提供参数值。

#### Factory 接口 {#native-protocol-factory}
用于创建新对象，无方法，仅有 **Factory::Info (Opcode 0)** 事件，提供 **id**、**name**、**type**、**version**、**change_mask** 和 **props**。

#### Link 接口 {#native-protocol-link}
连接两个 **port**，无方法，仅有 **Link::Info (Opcode 0)** 事件，提供 **id**、节点和端口信息、**state**、**error**、**format** 和 **props**。

#### Module 接口 {#native-protocol-module}
提供动态加载功能，无方法，仅有 **Module::Info (Opcode 0)** 事件，提供 **id**、**name**、**filename**、**args**、**change_mask** 和 **props**。

#### Node 接口 {#native-protocol-node}
图中的处理单元。

##### Node 方法
- **Node::SubscribeParams (Opcode 1)**：订阅参数变化。
- **Node::EnumParams (Opcode 2)**：枚举参数值。
- **Node::SetParam (Opcode 3)**：设置参数。
- **Node::SendCommand (Opcode 4)**：发送命令。

##### Node 事件
- **Node::Info (Opcode 0)**：提供节点信息，包含端口数量、**state**、**error**、**props** 和 **param_info**。
- **Node::Param (Opcode 1)**：提供参数值。

#### Port 接口 {#native-protocol-port}
**Node** 的输入/输出接口。

##### Port 方法
- **Port::SubscribeParams (Opcode 1)**：订阅参数变化。
- **Port::EnumParams (Opcode 2)**：枚举参数值。

##### Port 事件
- **Port::Info (Opcode 0)**：提供端口信息，包含 **id**、**direction**、**change_mask**、**props** 和 **param_info**。
- **Port::Param (Opcode 1)**：提供参数值。

#### ClientNode 接口 {#native-protocol-clientnode}
由 **client-node** 工厂创建，允许客户端控制服务器 **Node**，用于 **pw-stream** 和 **pw-filter**。

##### ClientNode 方法
- **ClientNode::GetNode (Opcode 1)**：绑定服务器 **Node**。
- **ClientNode::Update (Opcode 2)**：更新节点参数和信息。
- **ClientNode::PortUpdate (Opcode 3)**：创建、更新或销毁端口。
- **ClientNode::SetActive (Opcode 4)**：设置节点激活状态。
- **ClientNode::Event (Opcode 5)**：触发事件。
- **ClientNode::PortBuffers (Opcode 6)**：通知服务器端口的缓冲区分配。

##### ClientNode 事件
- **ClientNode::Transport (Opcode 0)**：提供激活记录和 **eventfd**。
- **ClientNode::SetParam (Opcode 1)**：设置参数。
- **ClientNode::SetIO (Opcode 2)**：设置 IO 区域。
- **ClientNode::Event (Opcode 3)**：触发事件。
- **ClientNode::Command (Opcode 4)**：发送命令。
- **ClientNode::AddPort (Opcode 5)**：添加端口。
- **ClientNode::RemovePort (Opcode 6)**：移除端口。
- **ClientNode::PortSetParam (Opcode 7)**：设置端口参数。
- **ClientNode::UseBuffers (Opcode 8)**：设置端口缓冲区。
- **ClientNode::PortSetIO (Opcode 9)**：设置端口 IO 区域。
- **ClientNode::SetActivation (Opcode 10)**：通知对等节点的激活记录。
- **ClientNode::PortSetMixInfo (Opcode 11)**：通知混音端口的对等信息。

#### Metadata 接口 {#native-protocol-metadata}
共享设置和属性数据库。

##### Metadata 方法
- **Metadata::SetProperty (Opcode 1)**：设置属性。
- **Metadata::Clear (Opcode 2)**：清空存储。

##### Metadata 事件
- **Metadata::Property (Opcode 0)**：通知属性变化。

#### Profiler 接口 {#native-protocol-profiler}
提供图的性能分析信息，无方法，仅有 **Profiler::Profile (Opcode 0)** 事件，提供 **SPA_TYPE_OBJECT_Profiler** 对象。

#### 消息尾部 {#native-protocol-footer}
消息尾部包含不指向 **Id** 定义目标对象的附加消息，格式为：

```
   Struct(
      Id: opcode1,
      Struct { ... },
      Id: opcode2,
      Struct { ... },
      ...
   )
```

- **Core Generation (Footer Opcode 0)**：服务器通知客户端当前 **registry generation**。
- **Client Generation (Footer Opcode 0)**：客户端通知服务器已处理的最新 **registry generation**。

#### Registry Generation {#native-protocol-registry-generation}
**registry generation** 是服务器 **pw_context** 中的 64 位整数，当分配新全局 **PW_KEY_OBJECT_ID** 时递增。对象以 (**id**, **object generation**) 元组管理，服务器根据元组查找对象，防止异步协议中已销毁对象 ID 的误用。若查找失败，返回 **ESTALE** 错误。客户端使用 **PW_KEY_OBJECT_SERIAL** 唯一标识对象。

总结：PipeWire 原生协议基于 unix 套接字，通过消息头、负载和尾部实现异步通信，支持 **Core**、**Registry**、**Client**、**Device**、**Factory**、**Link**、**Module**、**Node**、**Port**、**ClientNode**、**Metadata** 和 **Profiler** 接口，提供灵活的媒体处理和会话管理功能。
