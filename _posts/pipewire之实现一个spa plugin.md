---
title: pipewire之实现一个spa plugin
date: 2025-03-11 13:25:37
tags:
	- 音频
---

--

在 PipeWire 中实现一个 SPA（Simple Plugin API）插件需要遵循 SPA 的插件框架，创建一个动态库（`.so` 文件），并定义特定的接口和功能。SPA 插件通常用于扩展 PipeWire 的功能，例如实现音频处理节点、设备支持或其他自定义功能。以下是实现一个简单 SPA 插件的详细步骤和示例代码，基于 PipeWire 的插件机制（如 `context.c` 中使用的 `spa_plugin_loader`）。

---

### 1. SPA 插件的基本概念
- **SPA 插件**: 一个动态加载的共享库，提供特定的功能（如节点、设备、格式转换）。
- **接口**: 通过 `struct spa_handle` 和 `struct spa_interface` 定义插件的功能。
- **加载**: PipeWire 使用 `pw_context_load_spa_handle` 加载插件（见 `context.c`）。
- **导出**: 插件必须导出一个符号（如 `spa_handle_factory_init`），供加载器调用。

---

### 2. 实现步骤

#### (1) 定义插件目标
假设我们要实现一个简单的音频处理插件（例如，一个增益节点），它接收音频输入，应用增益（放大或缩小音量），然后输出处理后的音频。

#### (2) 创建文件结构
- `my_gain_plugin.c`: 插件实现代码。
- `CMakeLists.txt`: 构建脚本（可选，推荐使用 CMake）。

#### (3) 编写插件代码
以下是一个完整的示例代码：

```c
/* my_gain_plugin.c */
/* SPDX-FileCopyrightText: Copyright © 2025 Your Name */
/* SPDX-License-Identifier: MIT */

#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <math.h>

#include <spa/param/audio/format-utils.h>
#include <spa/param/audio/raw.h>
#include <spa/node/node.h>
#include <spa/node/utils.h>
#include <spa/utils/hook.h>
#include <spa/utils/names.h>
#include <spa/utils/string.h>
#include <spa/pod/builder.h>
#include <spa/control/control.h>

/* 日志宏，简化示例 */
#define pw_log_debug(format, ...) printf("DEBUG: " format "\n", ##__VA_ARGS__)
#define pw_log_error(format, ...) fprintf(stderr, "ERROR: " format "\n", ##__VA_ARGS__)

/* 插件的私有数据结构 */
struct my_gain_data {
    struct spa_node node;       /* SPA 节点基类 */
    struct spa_hook_list hooks; /* 事件监听器 */
    float gain;                 /* 增益值，默认 1.0 */
    struct spa_io_buffers *in_io;  /* 输入缓冲区 IO */
    struct spa_io_buffers *out_io; /* 输出缓冲区 IO */
};

/* 处理输入输出端口的事件 */
static int impl_node_port_set_io(void *object, enum spa_direction direction, uint32_t port_id,
                                 uint32_t id, void *data, size_t size)
{
    struct my_gain_data *data = object;

    pw_log_debug("port_set_io: direction=%d, port_id=%u, id=%u", direction, port_id, id);

    if (id != SPA_IO_Buffers)
        return -EINVAL;

    if (direction == SPA_DIRECTION_INPUT && port_id == 0)
        data->in_io = data;
    else if (direction == SPA_DIRECTION_OUTPUT && port_id == 0)
        data->out_io = data;
    else
        return -EINVAL;

    return 0;
}

/* 处理音频数据 */
static int impl_node_process(void *object)
{
    struct my_gain_data *data = object;
    struct spa_io_buffers *in_io = data->in_io;
    struct spa_io_buffers *out_io = data->out_io;
    struct spa_buffer *in_buf, *out_buf;
    float *in_samples, *out_samples;
    uint32_t i, n_samples;

    if (in_io == NULL || out_io == NULL || in_io->status != SPA_STATUS_HAVE_DATA)
        return SPA_STATUS_NEED_DATA;

    in_buf = in_io->buffer;
    out_buf = out_io->buffer;

    if (in_buf->n_datas < 1 || out_buf->n_datas < 1)
        return -EINVAL;

    in_samples = in_buf->datas[0].data;
    out_samples = out_buf->datas[0].data;
    n_samples = in_buf->datas[0].chunk->size / sizeof(float);

    /* 应用增益 */
    for (i = 0; i < n_samples; i++)
        out_samples[i] = in_samples[i] * data->gain;

    out_io->status = SPA_STATUS_HAVE_DATA;
    in_io->status = SPA_STATUS_NEED_DATA;

    pw_log_debug("processed %u samples with gain %f", n_samples, data->gain);

    return SPA_STATUS_OK;
}

/* 枚举支持的格式 */
static int impl_node_enum_params(void *object, int seq, uint32_t id, uint32_t start,
                                 uint32_t num, const struct spa_pod *filter)
{
    struct my_gain_data *data = object;
    struct spa_pod_builder b = { 0 };
    uint8_t buffer[1024];
    struct spa_pod *param;

    spa_pod_builder_init(&b, buffer, sizeof(buffer));

    if (id != SPA_PARAM_EnumFormat)
        return 0;

    /* 支持浮点格式的立体声音频 */
    param = spa_format_audio_raw_build(&b, SPA_PARAM_EnumFormat,
                                       &SPA_AUDIO_INFO_INIT(
                                           .format = SPA_AUDIO_FORMAT_F32,
                                           .channels = 2,
                                           .rate = 48000));

    spa_node_emit_result(&data->hooks, seq, 0, SPA_RESULT_TYPE_NODE_PARAMS, param);

    return 1; /* 返回支持的格式数量 */
}

/* 设置格式 */
static int impl_node_set_param(void *object, uint32_t id, uint32_t flags, const struct spa_pod *param)
{
    struct my_gain_data *data = object;

    if (id != SPA_PARAM_Format || param == NULL)
        return -EINVAL;

    /* 检查格式（示例仅支持 F32 立体声 48kHz） */
    struct spa_audio_info info = { 0 };
    if (spa_format_parse(param, &info.media_type, &info.media_subtype) < 0 ||
        info.media_type != SPA_MEDIA_TYPE_audio ||
        info.media_subtype != SPA_MEDIA_SUBTYPE_raw ||
        info.info.raw.format != SPA_AUDIO_FORMAT_F32 ||
        info.info.raw.channels != 2 ||
        info.info.raw.rate != 48000) {
        pw_log_error("unsupported format");
        return -EINVAL;
    }

    pw_log_debug("format set: F32, 2 channels, 48kHz");
    return 0;
}

/* SPA 节点接口实现 */
static const struct spa_node_methods impl_node = {
    SPA_VERSION_NODE_METHODS,
    .port_set_io = impl_node_port_set_io,
    .process = impl_node_process,
    .enum_params = impl_node_enum_params,
    .set_param = impl_node_set_param,
};

/* 初始化插件实例 */
static int my_gain_init(struct spa_handle *handle)
{
    struct my_gain_data *data = (struct my_gain_data *)handle;

    data->gain = 1.0f; /* 默认增益 */
    spa_hook_list_init(&data->hooks);

    /* 设置节点接口 */
    data->node.iface = SPA_INTERFACE_INIT(
        SPA_TYPE_INTERFACE_Node,
        SPA_VERSION_NODE,
        &impl_node,
        data);

    pw_log_debug("my_gain plugin initialized");

    return 0;
}

/* 清理插件实例 */
static int my_gain_clear(struct spa_handle *handle)
{
    pw_log_debug("my_gain plugin cleared");
    return 0;
}

/* SPA 工厂函数 */
static const struct spa_handle_factory my_gain_factory = {
    SPA_VERSION_HANDLE_FACTORY,
    SPA_NAME_API_ALSA_PCM_SINK, /* 示例命名，可自定义 */
    NULL,                       /* info */
    sizeof(struct my_gain_data),
    my_gain_init,
    my_gain_clear,
};

/* 导出工厂函数 */
SPA_EXPORT
int spa_handle_factory_init(const struct spa_handle_factory **factory)
{
    *factory = &my_gain_factory;
    return 0;
}
```

---

### 3. 代码说明

#### (1) `struct my_gain_data`
- 插件的私有数据，包含节点接口（`spa_node`）和自定义字段（如 `gain`）。
- 嵌套 `spa_node` 模拟继承，扩展其功能。

#### (2) `impl_node` 接口
- 定义了节点的行为：
  - `port_set_io`: 设置输入输出缓冲区。
  - `process`: 处理音频数据，应用增益。
  - `enum_params`: 枚举支持的格式（这里是 F32 立体声 48kHz）。
  - `set_param`: 验证和设置格式。

#### (3) `my_gain_init` 和 `my_gain_clear`
- 初始化和清理插件实例，模拟构造函数和析构函数。

#### (4) `spa_handle_factory_init`
- 导出函数，PipeWire 通过此函数加载插件并获取工厂。

---

### 4. 构建插件

#### 使用 CMake
创建一个 `CMakeLists.txt`：
```cmake
cmake_minimum_required(VERSION 3.10)
project(my_gain_plugin C)

find_package(PipeWire REQUIRED)

add_library(my_gain_plugin SHARED my_gain_plugin.c)
target_include_directories(my_gain_plugin PRIVATE ${PIPEWIRE_INCLUDE_DIRS})
target_link_libraries(my_gain_plugin PRIVATE ${PIPEWIRE_LIBRARIES})

set_target_properties(my_gain_plugin PROPERTIES PREFIX "libspa-")
install(TARGETS my_gain_plugin LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/spa-0.2)
```

#### 编译
```bash
mkdir build && cd build
cmake ..
make
sudo make install
```

- 输出文件：`libspa-my_gain_plugin.so`，安装到 `/usr/lib/spa-0.2/`（默认路径）。

---

### 5. 在 PipeWire 中使用

#### 配置加载
编辑 PipeWire 配置文件（如 `/etc/pipewire/pipewire.conf` 或用户配置）：
```ini
context.modules = [
    { name = libspa-my_gain_plugin
      args = { gain = 2.0 } # 可选参数
    }
]
```

#### 通过代码加载
在客户端代码中：
```c
struct spa_handle *handle = pw_context_load_spa_handle(context, SPA_NAME_API_ALSA_PCM_SINK, NULL);
struct spa_node *node;
spa_handle_get_interface(handle, SPA_TYPE_INTERFACE_Node, (void **)&node);
```

---

### 6. 关键点与扩展

#### 关键点
1. **接口一致性**: 必须实现 `spa_node_methods` 的必要函数。
2. **内存管理**: 使用 `spa_buffer` 处理数据，避免直接分配。
3. **日志**: 通过 `pw_log_debug` 调试，便于排查问题。

#### 扩展建议
- **参数支持**: 添加 `SPA_PARAM_Prop` 支持动态调整 `gain`。
- **多格式**: 在 `enum_params` 中支持更多音频格式。
- **线程安全**: 使用锁保护 `gain` 的访问。

---

### 7. 与 PipeWire 的集成
- **加载**: `context.c` 中的 `pw_context_load_spa_handle` 调用 `spa_handle_factory_init`。
- **内存**: 数据缓冲区通过 `pw_mempool` 分配（见 `context.c`）。
- **事件**: 通过 `spa_hook_list` 触发节点事件（见 `control.c`）。

---

### 总结
实现一个 SPA 插件需要定义工厂函数、节点接口和处理逻辑，通过 `spa_handle_factory_init` 导出。上述示例展示了一个简单的增益插件，你可以根据需求扩展功能（如添加控制参数、支持视频等）。如果需要更复杂的示例或调试帮助，请告诉我！
