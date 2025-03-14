---
title: pipewire之examples分析
date: 2025-03-13 17:01:37
tags:
	- 音频
---

--

# export-spa.c和export-spa-device.c区别

我将基于你提供的两个文件

（一个用于导出 SPA Device，另一个用于导出 SPA Node），

分析它们之间的区别。

两个文件都展示了如何使用 PipeWire 的核心 API（`api_pw_core`）加载和导出 SPA（Simple Plugin API）组件，

但它们的用途、实现细节和目标对象有所不同。

以下是详细对比：

---

### 1. **总体目标**
- **SPA Device 示例**（第一个文件）：
  - 目标：加载并导出 SPA **设备（Device）**。
  - 用途：创建一个设备对象（如 V4L2 设备、ALSA 设备），并将其注册到 PipeWire 服务端，使其可被其他客户端发现和使用。
  - 示例命令：`./program v4l2/libspa-v4l2 api.v4l2.device`

- **SPA Node 示例**（第二个文件）：
  - 目标：加载并导出 SPA **节点（Node）**。
  - 用途：创建一个节点对象（如音频源、视频源），并将其注册到 PipeWire 服务端，通常用于数据流的输入或输出。
  - 示例命令：`./program v4l2/libspa-v4l2 api.v4l2.source [path]`

---

### 2. **代码结构对比**

#### **数据结构（`struct data`）**
| 属性            | SPA Device 示例           | SPA Node 示例                                               |
| --------------- | ------------------------- | ----------------------------------------------------------- |
| `loop`          | `pw_main_loop *`          | `pw_main_loop *`                                            |
| `context`       | `pw_context *`            | `pw_context *`                                              |
| `core`          | `pw_core *`               | `pw_core *`                                                 |
| `core_listener` | `spa_hook`                | `spa_hook`                                                  |
| **核心对象**    | `pw_impl_device *device`  | `spa_node *node`                                            |
| `library`       | `const char *` (SPA 库名) | `const char *` (SPA 库名)                                   |
| `factory`       | `const char *` (工厂名)   | `const char *` (工厂名)                                     |
| `path`          | 无                        | `const char *` (可选的目标路径)                             |
| **额外字段**    | 无                        | `pw_proxy *proxy`, `spa_hook proxy_listener`, `uint32_t id` |

- **区别**：
  - Device 示例使用 `pw_impl_device` 表示设备对象。
  - Node 示例使用 `spa_node` 表示节点对象，并增加了代理（`pw_proxy`）相关字段，用于追踪导出的全局 ID。

#### **主函数（`main`）**
| 部分             | SPA Device 示例                         | SPA Node 示例                                        |
| ---------------- | --------------------------------------- | ---------------------------------------------------- |
| **参数检查**     | 需要 2 个参数（library, factory）       | 需要 2 个参数 + 可选路径（library, factory, [path]） |
| **模块加载**     | `libpipewire-module-spa-device-factory` | `libpipewire-module-spa-node-factory`                |
| **核心对象创建** | `make_device`                           | `make_node`                                          |
| **清理**         | 销毁 `context` 和 `loop`                | 额外销毁 `proxy` 和 `core`                           |

- **区别**：
  - Device 示例加载设备工厂模块，Node 示例加载节点工厂模块。
  - Node 示例支持可选的 `path` 参数，用于指定目标对象（如设备路径）。

---

### 3. **核心对象创建函数对比**

#### **SPA Device 示例：`make_device`**
```c
static int make_device(struct data *data)
{
    struct pw_impl_factory *factory = pw_context_find_factory(data->context, "spa-device-factory");
    struct pw_properties *props = pw_properties_new(SPA_KEY_LIBRARY_NAME, data->library,
                                                    SPA_KEY_FACTORY_NAME, data->factory, NULL);
    data->device = pw_impl_factory_create_object(factory, NULL, PW_TYPE_INTERFACE_Device,
                                                 PW_VERSION_DEVICE, props, SPA_ID_INVALID);
    pw_core_export(data->core, SPA_TYPE_INTERFACE_Device, NULL,
                   pw_impl_device_get_implementation(data->device), 0);
    return 0;
}
```
- **流程**：
  1. 查找 `spa-device-factory` 工厂。
  2. 创建属性，指定库名和工厂名。
  3. 使用工厂创建 `pw_impl_device` 对象。
  4. 通过 `pw_core_export` 导出设备接口。

#### **SPA Node 示例：`make_node`**
```c
static int make_node(struct data *data)
{
    struct pw_properties *props = pw_properties_new(SPA_KEY_LIBRARY_NAME, data->library,
                                                    SPA_KEY_FACTORY_NAME, data->factory, NULL);
    struct spa_handle *hndl = pw_context_load_spa_handle(data->context, data->factory, &props->dict);
    void *iface;
    spa_handle_get_interface(hndl, SPA_TYPE_INTERFACE_Node, &iface);
    data->node = iface;
    if (data->path) {
        pw_properties_set(props, PW_KEY_NODE_AUTOCONNECT, "true");
        pw_properties_set(props, PW_KEY_TARGET_OBJECT, data->path);
    }
    data->proxy = pw_core_export(data->core, SPA_TYPE_INTERFACE_Node, &props->dict, data->node, 0);
    pw_proxy_add_listener(data->proxy, &data->proxy_listener, &proxy_events, data);
    return 0;
}
```
- **流程**：
  1. 创建属性，指定库名和工厂名。
  2. 使用 `pw_context_load_spa_handle` 加载 SPA 句柄。
  3. 从句柄中获取 `SPA_TYPE_INTERFACE_Node` 接口。
  4. 如果有 `path`，设置自动连接和目标对象属性。
  5. 通过 `pw_core_export` 导出节点接口，并添加代理监听器。

- **区别**：
  - **创建方式**：
    - Device 使用工厂（`pw_impl_factory_create_object`）直接创建设备。
    - Node 使用 `pw_context_load_spa_handle` 加载 SPA 句柄，再提取节点接口。
  - **属性支持**：
    - Node 支持额外的 `path` 参数，允许指定目标对象并启用自动连接。
  - **监听器**：
    - Node 添加了 `pw_proxy` 监听器，用于捕获绑定属性事件（例如全局 ID）。

---

### 4. **功能与用途对比**

| 特性         | SPA Device 示例                | SPA Node 示例                     |
| ------------ | ------------------------------ | --------------------------------- |
| **目标对象** | `pw_impl_device` (设备)        | `spa_node` (节点)                 |
| **接口类型** | `SPA_TYPE_INTERFACE_Device`    | `SPA_TYPE_INTERFACE_Node`         |
| **工厂模块** | `spa-device-factory`           | 不直接使用工厂，而是加载 SPA 句柄 |
| **用途**     | 管理硬件设备（如 V4L2 摄像头） | 处理数据流（如音频源、视频源）    |
| **额外功能** | 无                             | 支持 `path` 和代理事件监听        |
| **输出信息** | 无额外输出                     | 输出节点全局 ID                   |

- **SPA Device**：
  - 专注于设备管理，通常表示硬件资源。
  - 不直接与数据流交互，而是提供设备的控制接口。
- **SPA Node**：
  - 专注于数据处理，通常是数据流的起点或终点。
  - 支持自动连接到指定路径（如某个设备节点）。

---

### 5. **事件处理对比**
- **共同点**：
  - 两个示例都监听核心错误事件（`on_core_error`），并在核心错误时退出主循环。
- **不同点**：
  - Node 示例额外监听 `pw_proxy` 事件（`proxy_event_bound_props`），用于捕获节点绑定时的全局 ID 并打印。

---

### 6. **使用场景示例**
- **SPA Device**：
  ```bash
  ./device-example v4l2/libspa-v4l2 api.v4l2.device
  ```
  - 加载 V4L2 设备驱动，注册到 PipeWire，供其他客户端（如 `pw-cli`）访问。
- **SPA Node**：
  
  ```bash
  ./node-example v4l2/libspa-v4l2 api.v4l2.source /dev/video0
  ```
  - 加载 V4L2 视频源节点，连接到 `/dev/video0`，并输出其全局 ID。

---

### 总结
- **SPA Device 示例**：
  - 专注于设备对象的创建和导出。
  - 使用工厂模式，更贴近硬件设备管理。
  - 实现更简单，无需额外事件监听。
- **SPA Node 示例**：
  - 专注于节点对象的创建和导出。
  - 使用 SPA 句柄加载，支持目标路径和自动连接。
  - 增加了代理事件监听，提供更多交互性。

这两个文件展示了 PipeWire 如何通过类似的核心 API（`pw_core_export`）支持不同类型的 SPA 对象（Device 和 Node），反映了它们在功能和应用场景上的差异。如果你有具体问题或需要更深入分析某个部分，请告诉我！
