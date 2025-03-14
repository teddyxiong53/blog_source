---
title: pipewire之pw_proxy和pw_resource
date: 2025-03-13 18:57:37
tags:
	- 音频
---

--

# 1

我将基于你提供的 `pw_resource.h` 和其实现文件，

详细分析 `pw_resource` 在 PipeWire 中的用途、设计目标及其功能。

`pw_resource` 是 PipeWire 中一个核心概念，

==用于管理客户端拥有的资源（resources），==

在客户端与服务端交互中起关键作用。

以下是逐步解析：

---

### 1. **什么是 `pw_resource`？**
- **定义**：
  - `pw_resource` 表示一个客户端（`pw_impl_client`）拥有的资源对象。
  - 它是客户端与 PipeWire 服务端之间交互的基本单元，通常对应于服务端的一个全局对象（如节点、设备、模块）或客户端创建的本地对象。
- **来源**：
  - 通过绑定到服务端的全局对象（global object）创建，例如通过 `pw_registry_bind`。
  - 通过客户端调用 API 创建，例如 `pw_core_create_object`。
- **生命周期**：
  - 当客户端断开连接或绑定的全局对象被销毁时，资源会被销毁。

- **文档描述**：
  - “Resources represent objects owned by a client. They are the result of binding to a global resource or by calling API that creates client-owned objects.”

---

### 2. **主要用途**
`pw_resource` 在 PipeWire 中有以下核心用途：

#### **1. 客户端与服务端通信的桥梁**
- **代理（Proxy）关联**：
  - 客户端通常通过 `pw_proxy`（代理对象）与 `pw_resource` 交互，`pw_proxy` 是客户端对资源的本地表示。
  - 服务端通过 `pw_resource` 向客户端发送事件或响应客户端的请求。
- **协议支持**：
  - `pw_resource` 通过 `pw_protocol_marshal` 实现与特定协议的绑定，支持序列化和反序列化消息。

#### **2. 表示和管理资源**
- **类型与版本**：
  - 每个资源有唯一的类型（`type`，如 `PW_TYPE_INTERFACE_Node`）和版本（`version`），确保客户端和服务端接口兼容。
- **权限控制**：
  - `permissions` 字段定义客户端对资源的访问权限（如读、写、执行）。
- **全局绑定**：
  - 通过 `pw_resource_set_bound_id` 关联到服务端的全局 ID（`global_id`），表示资源对应的服务端对象。

#### **3. 事件与方法的双向通信**
- **事件通知**：
  - 服务端通过 `pw_resource` 向客户端发送事件（如 `destroy`、`error`）。
- **方法调用**：
  - 客户端通过 `pw_resource_call` 调用服务端资源的方法。

#### **4. 用户数据支持**
- 提供额外的用户数据存储（`user_data`），方便客户端扩展功能。

---

### 3. **核心结构体与功能**

#### **结构体定义**
```c
struct pw_resource {
    int refcount;                    // 引用计数
    struct pw_context *context;      // 所属上下文
    struct pw_impl_client *client;   // 拥有资源的客户端
    uint32_t id;                     // 客户端内唯一 ID
    uint32_t permissions;            // 权限标志
    const char *type;                // 资源类型
    uint32_t version;                // 资源版本
    uint32_t bound_id;               // 绑定的全局 ID
    struct spa_hook_list listener_list; // 资源事件监听器
    struct spa_hook_list object_listener_list; // 对象方法监听器
    const struct pw_protocol_marshal *marshal; // 协议序列化器
    void *user_data;                 // 用户数据
    struct spa_interface impl;       // 服务端实现接口
    bool destroyed;                  // 销毁标志
    bool removed;                    // 移除标志
    struct spa_list link;            // 全局资源链表
    struct pw_global *global;        // 关联的全局对象
};
```

#### **关键函数**
1. **创建资源**：
   - `pw_resource_new`：
     ```c
     struct pw_resource *pw_resource_new(struct pw_impl_client *client, uint32_t id,
                                         uint32_t permissions, const char *type,
                                         uint32_t version, size_t user_data_size);
     ```
     - 创建一个新资源，分配用户数据空间并绑定到客户端。

2. **销毁资源**：
   - `pw_resource_destroy`：
     - 销毁资源，触发 `destroy` 事件，清理监听器并释放内存。
   - `pw_resource_remove`：
     - 类似 `destroy`，但不发送 `remove_id` 消息给客户端。

3. **事件监听**：
   - `pw_resource_add_listener`：
     - 添加资源事件监听器（如 `destroy`、`pong`、`error`）。
   - `pw_resource_add_object_listener`：
     - 添加对象方法监听器，用于处理服务端调用。

4. **通信支持**：
   - `pw_resource_ping`：
     - 发送 ping 请求，返回序列号，等待 pong 响应。
   - `pw_resource_error` / `pw_resource_errorf`：
     - 向客户端发送错误消息。

5. **全局绑定**：
   - `pw_resource_set_bound_id`：
     - 设置资源的全局 ID，并通知客户端绑定属性。
   - `pw_resource_get_bound_id`：
     - 获取绑定的全局 ID。

6. **引用计数**：
   - `pw_resource_ref` / `pw_resource_unref`：
     - 管理资源的生命周期，引用计数为 0 时释放。

---

### 4. **工作原理**
- **创建流程**：
  1. 客户端通过 `pw_registry_bind` 或其他 API 创建资源。
  2. 服务端分配一个 `pw_resource`，并将其加入客户端的资源表（`client->objects`）。
  3. 通过 `pw_resource_install_marshal` 设置协议序列化器。

- **通信流程**：
  1. 服务端调用 `pw_resource_notify` 发送事件给客户端。
  2. 客户端通过 `pw_resource_call` 调用服务端方法。
  3. 协议层（`pw_protocol`）处理消息的序列化和传输。

- **销毁流程**：
  1. 客户端断开或资源被移除时，触发 `pw_resource_destroy`。
  2. 清理资源并通知客户端。

---

### 5. **使用场景**
以下是 `pw_resource` 的典型应用场景：

#### **绑定全局对象**
```c
static void on_global(void *data, uint32_t id, uint32_t permissions, const char *type, uint32_t version, const struct spa_dict *props) {
    struct pw_registry *registry = data;
    if (strcmp(type, PW_TYPE_INTERFACE_Node) == 0) {
        struct pw_resource *resource = pw_registry_bind(registry, id, type, version, 0);
        // 使用 resource 操作节点
    }
}
```
- 客户端通过注册表绑定到一个节点资源。

#### **创建客户端对象**
```c
struct pw_resource *resource = pw_resource_new(client, id, PW_PERM_ALL, PW_TYPE_INTERFACE_Client, PW_VERSION_CLIENT, sizeof(user_data));
```
- 创建一个客户端拥有的对象（如客户端自身的资源）。

#### **错误处理**
```c
pw_resource_error(resource, -EINVAL, "Invalid argument");
```
- 服务端向客户端报告错误。

---

### 6. **设计亮点**
- **灵活性**：
  - 通过 `type` 和 `version` 支持多种资源类型和版本。
- **模块化**：
  - 使用 `pw_protocol_marshal` 解耦协议实现，支持不同通信协议。
- **事件驱动**：
  - 通过 `spa_hook_list` 实现异步事件通知。
- **资源管理**：
  - 引用计数和自动清理机制确保资源生命周期可控。

---

### 7. **与其他组件的关系**
- **`pw_impl_client`**：
  - `pw_resource` 归属于某个客户端，客户端负责管理其资源集合。
- **`pw_proxy`**：
  - 客户端通过 `pw_proxy` 与 `pw_resource` 交互，形成客户端-服务端对称结构。
- **`pw_protocol`**：
  - 提供底层通信支持，`pw_resource` 依赖协议序列化消息。
- **`pw_global`**：
  - 服务端的全局对象通过 `bound_id` 与 `pw_resource` 关联。

---

### 8. **总结**
- **用途**：
  - `pw_resource` 是 PipeWire 中客户端拥有的资源抽象，用于表示和管理服务端对象或客户端创建的对象。
  - 它是客户端与服务端通信的核心桥梁，支持事件通知、方法调用和资源管理。
- **适用场景**：
  - 绑定全局对象（如节点、设备）。
  - 创建客户端本地资源。
  - 处理服务端事件和错误。
- **重要性**：
  - 作为 PipeWire 的基础组件，`pw_resource` 确保了客户端与服务端的高效交互，是构建音频/视频管道的关键。

如果你对 `pw_resource` 的某个功能（如事件机制或协议绑定）有具体疑问，或想分析其在某个场景下的应用，我可以进一步深入讲解！

