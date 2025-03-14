---
title: pipewire之client编写用到的结构体
date: 2025-03-13 15:50:37
tags:
	- 音频
---

--

在 PipeWire 中编写一个客户端（client）时，

你需要与 PipeWire 的核心 API 交互，

主要通过 `libpipewire` 提供的公开接口来实现。

PipeWire 的设计将内部实现（如以 `pw_impl_` 为前缀的结构体）与外部 API 分开，

因此客户端代码通常不会直接使用 `pw_impl_` 前缀的结构体，

而是通过公开的 `pw_` 前缀的结构体和函数来操作。

以下是编写 PipeWire 客户端时需要使用的主要结构体和相关流程的详细分析。

---

### 1. 编写 PipeWire 客户端的主要结构体

PipeWire 客户端通过 `libpipewire` 提供的 API 与 PipeWire 服务器通信，管理节点、链接、端口等资源。以下是主要使用的结构体：

#### 1.1. `struct pw_context`
- **作用**：
  - 客户端的核心上下文，用于初始化 PipeWire 环境。
  - 它是客户端与 PipeWire 服务器交互的入口。
- **来源**：
  - 通过 `pw_context_new()` 创建。
- **使用方式**：
  - 初始化客户端时使用，管理全局资源。
- **示例**：
  ```c
  struct pw_context *context = pw_context_new(pw_main_loop_new(NULL, NULL), NULL, 0);
  ```

#### 1.2. `struct pw_core`
- **作用**：
  - 表示客户端与 PipeWire 服务器的核心连接。
  - 用于执行远程操作（如同步、注册监听器）。
- **来源**：
  - 通过 `pw_context_connect()` 从 `pw_context` 创建。
- **使用方式**：
  - 管理核心操作，如获取注册表（registry）。
- **示例**：
  ```c
  struct pw_core *core = pw_context_connect(context, NULL, 0);
  ```

#### 1.3. `struct pw_registry`
- **作用**：
  - 表示 PipeWire 的注册表，用于发现全局对象（如节点、端口、链接）。
- **来源**：
  - 通过 `pw_core_get_registry()` 获取。
- **使用方式**：
  - 监听全局对象的变化，获取节点和端口信息。
- **示例**：
  ```c
  struct pw_registry *registry = pw_core_get_registry(core, PW_VERSION_REGISTRY, 0);
  ```

#### 1.4. `struct pw_client`
- **作用**：
  - 表示客户端对象，管理客户端的属性和状态。
- **来源**：
  - 自动创建，通常通过 `pw_registry` 的事件监听获取。
- **使用方式**：
  - 设置客户端属性，处理权限和元数据。
- **示例**：
  ```c
  struct pw_client *client = pw_registry_bind(registry, id, PW_TYPE_INTERFACE_Client, PW_VERSION_CLIENT, 0);
  ```

#### 1.5. `struct pw_node`
- **作用**：
  - 表示一个节点（如 `bluez_input` 或 ALSA sink）。
- **来源**：
  - 通过 `pw_registry` 的事件监听获取。
- **使用方式**：
  - 获取节点信息，管理端口和链接。
- **示例**：
  ```c
  struct pw_node *node = pw_registry_bind(registry, id, PW_TYPE_INTERFACE_Node, PW_VERSION_NODE, 0);
  ```

#### 1.6. `struct pw_port`
- **作用**：
  - 表示节点的端口（如输入或输出端口）。
- **来源**：
  - 通过 `pw_node_enum_ports()` 或注册表事件获取。
- **使用方式**：
  - 管理端口的链接和数据流。
- **示例**：
  ```c
  struct pw_port *port = pw_registry_bind(registry, id, PW_TYPE_INTERFACE_Port, PW_VERSION_PORT, 0);
  ```

#### 1.7. `struct pw_link`
- **作用**：
  - 表示两个端口之间的链接。
- **来源**：
  - 通过 `pw_core_create_object()` 或 `pw_link_new()` 创建。
- **使用方式**：
  - 连接源节点的输出端口到目标节点的输入端口。
- **示例**：
  ```c
  struct pw_link *link = pw_link_new(core, output_port, input_port, NULL, NULL, 0);
  ```

#### 1.8. `struct pw_main_loop`
- **作用**：
  - 主事件循环，用于处理 PipeWire 的事件和回调。
- **来源**：
  - 通过 `pw_main_loop_new()` 创建。
- **使用方式**：
  - 运行客户端的事件循环。
- **示例**：
  ```c
  struct pw_main_loop *loop = pw_main_loop_new(NULL, NULL);
  pw_main_loop_run(loop);
  ```

#### 1.9. `struct spa_hook`
- **作用**：
  - 监听器，用于注册回调函数。
- **来源**：
  - 通过 `spa_hook_list_init()` 初始化。
- **使用方式**：
  - 监听 `pw_registry` 或 `pw_node` 的事件。
- **示例**：
  ```c
  struct spa_hook registry_listener;
  pw_registry_add_listener(registry, &registry_listener, &registry_events, user_data);
  ```

#### 1.10. `struct pw_properties`
- **作用**：
  - 属性集合，用于设置对象属性（如节点延迟）。
- **来源**：
  - 通过 `pw_properties_new()` 创建。
- **使用方式**：
  - 配置客户端、节点或链接。
- **示例**：
  ```c
  struct pw_properties *props = pw_properties_new("node.latency", "256/48000", NULL);
  ```

---

### 2. 是否会使用 `pw_impl_` 前缀的结构体？

#### 2.1. 不会直接使用
- **原因**：
  - `pw_impl_` 前缀的结构体（如 `pw_impl_node`、`pw_impl_port`、`pw_impl_port_mix` 等）是 PipeWire 内部实现的私有数据结构，定义在 `src/pipewire/` 目录下。
  - 这些结构体不暴露给客户端 API（`libpipewire`），客户端代码无法直接访问。
- **替代**：
  - 客户端使用公开的 `pw_` 前缀结构体（如 `pw_node`、`pw_port`），它们是对 `pw_impl_` 结构的封装。
  - 例如：
    - `pw_node` 是对 `pw_impl_node` 的外部接口。
    - `pw_port` 是对 `pw_impl_port` 的外部接口。

#### 2.2. 间接交互
- **内部机制**：
  - 客户端通过 `pw_core` 和 `pw_registry` 间接操作 `pw_impl_node` 和 `pw_impl_port`。
  - 例如，`pw_link_new()` 内部会创建 `pw_impl_link`，并更新 `pw_impl_port` 的 `links` 字段。
- **你的场景**：
  - `bluez_input` 和 ALSA sink 的 `pw_impl_node` 和 `pw_impl_port` 由 PipeWire 服务器管理。
  - 客户端只需通过 `pw_node` 和 `pw_port` 获取信息，无需直接操作 `pw_impl_`。

#### 2.3. 调试时可能接触
- 如果你需要调试 PipeWire 内部行为（例如修改 `process_buffering`），可能需要查看 `pw_impl_` 结构体的实现。
- 但在正常客户端开发中，不涉及这些结构体。

---

### 3. 编写 PipeWire 客户端的典型流程

以下是一个简单的 PipeWire 客户端示例，展示主要结构体的使用：

#### 3.1. 初始化和连接
```c
#include <pipewire/pipewire.h>

struct data {
    struct pw_main_loop *loop;
    struct pw_context *context;
    struct pw_core *core;
    struct pw_registry *registry;
    struct spa_hook registry_listener;
};

static void registry_event_global(void *data, uint32_t id, uint32_t permissions,
                                 const char *type, uint32_t version,
                                 const struct spa_dict *props)
{
    struct data *d = data;
    printf("Object: id:%u type:%s\n", id, type);

    // 查找节点（如 bluez_input 和 ALSA sink）
    if (strcmp(type, PW_TYPE_INTERFACE_Node) == 0) {
        struct pw_node *node = pw_registry_bind(d->registry, id, type, version, 0);
        // 存储节点以供后续链接
    }
}

static const struct pw_registry_events registry_events = {
    PW_VERSION_REGISTRY_EVENTS,
    .global = registry_event_global,
};

int main(int argc, char *argv[]) {
    pw_init(&argc, &argv);

    struct data data = {0};

    // 初始化主循环和上下文
    data.loop = pw_main_loop_new(NULL, NULL);
    data.context = pw_context_new(pw_main_loop_get_loop(data.loop), NULL, 0);

    // 连接到 PipeWire 服务器
    data.core = pw_context_connect(data.context, NULL, 0);
    if (!data.core) {
        fprintf(stderr, "Failed to connect to PipeWire\n");
        return -1;
    }

    // 获取注册表并监听事件
    data.registry = pw_core_get_registry(data.core, PW_VERSION_REGISTRY, 0);
    pw_registry_add_listener(data.registry, &data.registry_listener,
                             &registry_events, &data);

    // 运行主循环
    pw_main_loop_run(data.loop);

    // 清理
    pw_context_destroy(data.context);
    pw_main_loop_destroy(data.loop);
    pw_deinit();

    return 0;
}
```

#### 3.2. 连接节点
假设你想将 `bluez_input` 的输出端口连接到 ALSA sink 的输入端口：
1. 在 `registry_event_global` 中记录 `bluez_input` 和 ALSA sink 的节点和端口。
2. 使用 `pw_link_new()` 创建链接：
   ```c
   struct pw_port *output_port = ...; // 从 bluez_input 获取
   struct pw_port *input_port = ...;  // 从 ALSA sink 获取
   struct pw_link *link = pw_link_new(data.core, output_port, input_port, NULL, NULL, 0);
   ```

---

### 4. 与你的场景的关联
- **客户端目标**：
  - 你可能想编写一个客户端来监控 `bluez_input` 和 ALSA sink 的状态，或者调整它们的链接。
- **丢帧问题**：
  
  - 客户端可以通过 `pw_properties` 调整 `node.latency`：
    ```c
    struct pw_properties *props = pw_properties_new("node.latency", "256/48000", NULL);
    pw_node_set_properties(node, props);
    ```
  - 这会影响 `pw_impl_node` 的 `latency` 字段，减少 underrun。
- **波形变形**：
  
  - 客户端无法直接修改 `process_buffering` 的填 0 逻辑，但可以通过增大缓冲区缓解问题。

---

### 5. 总结
- **主要结构体**：
  - `pw_context`、`pw_core`、`pw_registry`、`pw_node`、`pw_port`、`pw_link`、`pw_main_loop`。
- **是否使用 `pw_impl_`**：
  - 客户端代码不直接使用 `pw_impl_` 前缀的结构体。
  - 这些结构体由 PipeWire 服务器内部管理，客户端通过 `pw_` API 间接操作。
- **你的场景**：
  - 客户端可以通过调整 `node.latency` 减少 `bluez_input` 的丢帧，缓解波形变形。

如果需要更详细的客户端代码示例或调试建议，我可以进一步协助！有什么想补充的吗？
