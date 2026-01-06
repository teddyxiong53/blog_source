---
title: pipewire之spa-plugins
date: 2025-05-30 10:52:37
tags:
	- 音频
---

--

# 官方文档分析

### SPA Plugins 文档翻译总结

本文件介绍了 **SPA plugins** 的基本概念，**SPA plugins** 是动态加载的对象，包含可在运行时检查和使用的接口。本文档分为使用 API 和实现新插件两部分，保留专有名词术语和图表。

#### 概述
使用 **SPA plugin** 的步骤包括：
1. **加载** 共享库。
2. **枚举** 可用 **factories**。
3. **枚举** 每个 **factory** 的接口。
4. **实例化** 所需接口。
5. **使用** 接口特定功能。

伪代码示例（加载 **logger** 接口）：

```python
handle = dlopen("$SPA_PLUGIN_DIR/support/libspa-support.so")
factory_enumeration_func = dlsym(handle, SPA_HANDLE_FACTORY_ENUM_FUNC_NAME)
spa_log *logger = NULL

while True:
    factory = get_next_factory(factory_enumeration_func):
    if factory != SPA_NAME_SUPPORT_LOG: # <spa/utils/name.h>
        continue

    interface_info = get_next_interface_info(factory)
    if info->type != SPA_TYPE_INTERFACE_Log: # </spa/support/log.h>
        continue

    interface = spa_load_interface(handle, interface_info->type)
    logger = (struct spa_log *)interface
    break

spa_log_error(log, "This is an error message\n")
```

**SPA plugins** 通常安装在 `/usr/lib64/spa-0.2/`，通过 `pkg-config --variable plugindir libspa-0.2` 获取路径。插件和 API 版本化，支持多版本共存。**spa-inspect** 工具提供命令行接口检查插件：

```
$ export SPA_PLUGIN_DIR=$(pkg-config --variable plugindir libspa-0.2)
$ spa-inspect ${SPA_PLUGIN_DIR}/support/libspa-support.so
...
factory version:		1
factory name:		'support.cpu'
factory info:
  none
factory interfaces:
 interface: 'Spa:Pointer:Interface:CPU'
factory instance:
 interface: 'Spa:Pointer:Interface:CPU'
skipping unknown interface
factory version:		1
factory name:		'support.loop'
factory info:
  none
factory interfaces:
 interface: 'Spa:Pointer:Interface:Loop'
 interface: 'Spa:Pointer:Interface:LoopControl'
 interface: 'Spa:Pointer:Interface:LoopUtils'
...
```

#### 打开插件
使用平台特定 API（如 Linux 的 `dlopen()`）加载插件。插件路径由厂商路径和 `.so` 文件组成，例如加载 `support/libspa-support.so`：

```c
#define SPA_PLUGIN_DIR	/usr/lib64/spa-0.2/"
void *hnd = dlopen(SPA_PLUGIN_DIR"/support/libspa-support.so", RTLD_NOW);
```

通常使用 `SPA_PLUGIN_DIR` 环境变量或 `pkg-config` 的 `plugindir` 确定路径。插件需包含唯一公共符号 `spa_handle_factory_enum`（由 `SPA_HANDLE_FACTORY_ENUM_FUNC_NAME` 定义）：

```c
spa_handle_factory_enum_func_t enum_func;
enum_func = dlsym(hnd, SPA_HANDLE_FACTORY_ENUM_FUNC_NAME));
```

若无此符号，库不是有效的 **SPA plugin**。

#### 枚举 Factories
通过 `enum_func` 枚举插件中的 **factories**：

```c
uint32_t i;
const struct spa_handle_factory *factory = NULL;
for (i = 0;;) {
	if (enum_func(&factory, &i) <= 0)
		break;
	// check name and version, introspect interfaces,
	// do something with the factory.
}
```

**Factory** 包含版本、名称、属性和功能函数，可通过 `spa_handle_factory_enum_interface_info()` 枚举接口类型（字符串标识）。常见 **factory** 名称定义在 `<spa/utils/names.h>`，如：

```c
#define SPA_NAME_SUPPORT_CPU            "support.cpu"                   // A CPU interface
#define SPA_NAME_SUPPORT_LOG            "support.log"                   // A Log interface
#define SPA_NAME_SUPPORT_DBUS           "support.dbus"                  // A DBUS interface
```

名称通常映射到特定插件，支持替代实现。

#### 创建 Handle
选择适合的 **factory** 后，分配对象内存（**SPA** 不自行分配内存）：

```c
struct spa_dict *extra_params = NULL;
size_t size = spa_handle_factory_get_size(factory, extra_params);
```

根据 `extra_params` 获取所需内存大小，然后分配并初始化：

```c
handle = calloc(1, size);
spa_handle_factory_init(factory, handle,
			NULL, // info
			NULL, // support
			0     // n_support
			);
```

**info** 参数与 `get_size()` 的额外属性一致，**support** 提供支持对象（如日志或主循环 API）。

#### 获取接口
从 **handle** 获取接口：

```c
void *iface;
spa_handle_get_interface(handle, SPA_NAME_SUPPORT_LOG, &iface);
struct spa_log *log = iface;
spa_log_warn(log, "Hello World!\n");
```

成功后，`iface` 可转换为对应接口（如 `struct spa_log *`）并调用其方法。

#### 清理对象
使用完毕后，通过 `spa_handle_clear()` 清理 **handle**，并用 `dlclose()` 卸载库。

#### SPA 接口
接口是包含类型（字符串）、版本和方法实现的结构，定义在头文件中（如 `<spa/support/log.h>`）。调用接口方法即调用实现中的对应函数。部分接口（如 **log**）提供额外字段（如日志级别）。

#### SPA 事件
接口支持注册回调（**hook** 或 **listener**）以接收事件通知。例如，**struct spa_node** 接口的事件注册：

```c
static void node_info(void *data, const struct spa_node_info *info)
{
	printf("got node info!\n");
}

static struct spa_node_events node_events = {
	SPA_VERSION_NODE_EVENTS,
        .info = node_info,
};

struct spa_hook listener;
spa_zero(listener);
spa_node_add_listener(node, &listener, &node_event, my_data);
```

通过 `spa_node_add_listener()` 注册监听器，事件触发时调用回调（如 `node_info`）。事件结构包含版本字段（如 `SPA_VERSION_NODE_EVENTS`），支持向后兼容。移除监听器使用：

```c
spa_hook_remove(&listener);
```

#### API 结果
**SPA** 使用事件推送结果，避免分配和所有权问题。结果通过回调传递，应用可选择性保留数据。

##### 同步结果
枚举 **node** 参数示例：

```c
static void node_result(void *data, int seq, int res,
		uint32_t type, const void *result)
{
        const struct spa_result_node_params *r =
                (const struct spa_result_node_params *) result;
	printf("got param:\n");
	spa_debug_pod(0, NULL, r->param);
}

struct spa_hook listener = { 0 };
static const struct spa_node_events node_events = {
	SPA_VERSION_NODE_EVENTS,
	.result = node_result,
};

spa_node_add_listener(node, &listener, &node_events, node);
int res = spa_node_enum_params(node, 0, SPA_PARAM_EnumFormat, 0, MAXINT, NULL);
spa_hook_remove(&listener);
```

##### 异步结果
异步结果通过相同回调推送，返回值通过 `SPA_RESULT_IS_ASYNC(res)` 判断，序列号通过 `SPA_RESULT_ASYNC_SEQ(res)` 获取。

#### 实现新插件
（内容待完善）

总结：**SPA plugins** 是动态加载的模块，提供运行时可检查的接口。使用流程包括加载库、枚举 **factories** 和接口、实例化并使用接口。事件机制支持异步通知，结果通过事件推送以避免分配问题。插件安装在标准路径，支持版本化管理。
