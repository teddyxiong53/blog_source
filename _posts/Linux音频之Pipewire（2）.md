---
title: Linux音频之Pipewire（2）
date: 2024-12-20 14:12:51
tags:
	- 音频

---

--

# spa_node_call_ready 

`spa_node_call_ready` 是一个函数，它用于通知节点（node）已经准备好处理数据。

具体来说，当一个节点完成了数据处理或准备好接受新的数据时，它会调用 `spa_node_call_ready` 函数来通知其他节点或客户端。

这个函数的作用是：

1. 通知其他节点或客户端：节点已经准备好处理数据，可以接受新的数据或继续处理当前数据。
2. 触发事件：当节点调用 `spa_node_call_ready` 函数时，会触发一个事件，通知其他节点或客户端进行相应的处理。

在 PipeWire 项目中，`spa_node_call_ready` 函数通常用于以下场景：

1. 节点完成数据处理：当一个节点完成了数据处理时，它会调用 `spa_node_call_ready` 函数来通知其他节点或客户端。
2. 节点准备好接受新数据：当一个节点准备好接受新数据时，它会调用 `spa_node_call_ready` 函数来通知其他节点或客户端。

通过 `spa_node_call_ready` 函数，节点可以与其他节点或客户端进行通信，实现数据处理和传输的协调。

# spa_system

这个更加适合作为理解spa_interface接口与实现分离的设计理念。

这个对接了2种系统：linux和evl。

就看linux的就好了。

对上层提供了一样的接口。

spa_system_pollfd_create 这种风格的接口。

对应的methods结构体定义：

```
struct spa_system_methods {
	int (*pollfd_create) (void *object, int flags);
}
```

spa_system

```
struct spa_system { struct spa_interface iface; };
```

对应一个spa_handle_factory。

```
const struct spa_handle_factory spa_support_system_factory = {
	SPA_VERSION_HANDLE_FACTORY,
	SPA_NAME_SUPPORT_SYSTEM,
	NULL,
	impl_get_size,
	impl_init,
	impl_enum_interface_info
};
```

```
static const struct spa_system_methods impl_system = {
.pollfd_create = impl_pollfd_create,
```

```
static int impl_pollfd_create(void *object, int flags)
{
	struct impl *impl = object;
	int fl = 0, res;
	if (flags & SPA_FD_CLOEXEC)
		fl |= EPOLL_CLOEXEC;
	res = epoll_create1(fl);
	spa_log_debug(impl->log, "%p: new fd:%d", impl, res);
	return res < 0 ? -errno : res;
}
```

有4种fd：

* pollfd
* timerfd
* eventfd
* signalfd

然后加上：read/write/ioctl/close。

还有2个clock函数。

# volume插件使用

PipeWire 的 `volume` 插件用于调整音频流的音量，通常可以作为音频链的一部分动态插入使用。以下是使用 `volume` 插件的方式及其相关配置说明：

------

### **1. `volume` 插件的功能**

- **动态音量调整**：通过设置音量参数调整输入音频流的增益（gain）。
- **支持链路插入**：可插入在任何支持 SPA 节点的音频处理链中。
- **简单高效**：适合对音量进行实时调节的场景。

------

### **2. 插件加载方式**

在 PipeWire 的配置中，`volume` 插件通常以 `filter-chain` 的形式加载，并注册为一个处理节点。

------

### **3. 使用方法**

#### **方法一：通过 `filter-chain` 配置加载**

编辑或创建 `~/.config/pipewire/filter-chain.conf` 文件，添加 `volume` 节点配置。

```ini
context.objects = [
    {
        factory = spa-node-factory
        args = {
            node.name = "volume"
            factory.name = "support.volume"
            node.description = "Volume Control"
            node.properties = {
                volume = 0.8  # 设置默认音量（范围 0.0 到 1.0）
            }
        }
    }
]
```

在此配置中：

- **`volume`**：设置音量，默认范围为 `0.0`（静音）到 `1.0`（原始音量），也可以超过 1.0（增益）。

保存配置后，重启 PipeWire：

```bash
systemctl --user restart pipewire
```

------

#### **方法二：通过 CLI 动态创建**

可以使用 `pw-cli` 动态加载 `volume` 插件并连接到现有节点。

1. **创建 `volume` 节点**：

   ```bash
   pw-cli create-node support.volume volume=0.5
   ```

2. **连接节点**： 使用 `pw-link` 将 `volume` 节点连接到输入或输出设备：

   ```bash
   pw-link <input-node> <volume-node>
   pw-link <volume-node> <output-node>
   ```

------

#### **方法三：通过 API 动态管理**

在开发中，可以通过 PipeWire 的 API 动态加载 `volume` 插件并设置参数。

```c
#include <pipewire/pipewire.h>

void setup_volume_node(struct pw_context *context) {
    struct pw_properties *props = pw_properties_new(
        "factory.name", "support.volume",
        "node.name", "volume",
        "volume", "0.5", // 初始音量
        NULL
    );
    struct pw_node *volume_node = pw_context_create_node(context, "volume", props, NULL);

    if (volume_node) {
        pw_node_add_listener(volume_node, ...);  // 添加监听器处理事件
    }
}
```

------

### **4. 动态调节音量**

可以通过 `pw-cli` 或其他工具动态更改音量参数。

#### **使用 `pw-cli` 修改音量**

```bash
pw-cli set-param <volume-node-id> Props volume=0.7
```

#### **使用 API 修改音量**

```c
struct pw_proxy *proxy = pw_node_get_proxy(volume_node);
pw_proxy_set_param(proxy, SPA_TYPE_PARAM_Props, "volume", SPA_POD_Float(0.7));
```

------

### **5. 配置文件示例**

完整的 `filter-chain` 配置文件示例：

```ini
context.objects = [
    {
        factory = spa-node-factory
        args = {
            node.name = "volume"
            factory.name = "support.volume"
            node.description = "Volume Control"
            node.properties = {
                volume = 0.8
            }
        }
    }
]
```

------

### **6. 检查节点状态**

加载完成后，可以使用 `pw-cli` 或 `pw-dump` 检查 `volume` 节点是否生效。

```bash
pw-cli ls Node
```

输出示例：

```
id 42: Node "volume"
    Props:
        volume = 0.8
```

------

### **7. 实现动态效果**

- **场景 1**：对流媒体播放进行音量动态调节。
- **场景 2**：与其他过滤器（如 `echo`、`equalizer`）组合使用，实现更复杂的音频效果链。

------

### **总结**

| 步骤             | 操作                                         |
| ---------------- | -------------------------------------------- |
| **加载插件**     | 使用配置文件或 `pw-cli` 加载 `volume` 节点。 |
| **连接节点**     | 使用 `pw-link` 连接输入输出设备。            |
| **动态调整音量** | 使用 CLI 或 API 修改 `volume` 参数。         |

`volume` 插件是 PipeWire 中重要的基础工具，灵活使用可以满足各种实时音量调节需求。

# pw_context_create_link

```
pw_core_create_object
	create_object
```

# pw_filter

`pw_filter` 是 PipeWire 提供的一个高级 API，用于在客户端应用中实现音频或视频数据的流式处理和动态过滤。它是 **PipeWire 简化客户端开发** 的工具之一，专注于处理数据流（输入或输出）。

------

### **`pw_filter` 的主要用途**

| 用途                   | 描述                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **数据流处理**         | 用于处理从 PipeWire 节点发送或接收的音频/视频数据。          |
| **实时过滤**           | 可应用自定义的滤波器、音量调节、效果处理等功能。             |
| **轻量级节点创建**     | 客户端应用可使用 `pw_filter` 轻松创建动态处理节点。          |
| **高效数据交互**       | 支持低延迟和高效率的数据流交互，适合实时性要求高的场景。     |
| **易用的事件驱动模型** | 提供回调机制处理数据和事件，无需直接操作低级别的 PipeWire 接口。 |

------

### **常见使用场景**

#### **1. 音频数据的实时处理**

- 创建一个 `pw_filter` 作为数据处理节点，接收音频流进行动态滤波或效果处理。
- 示例：自定义均衡器、音量控制、混音。

#### **2. 视频数据的实时处理**

- 用于处理视频流，比如应用滤镜、调整分辨率等。
- 示例：实时流媒体传输或视频处理。

#### **3. 音频/视频录制或播放**

- 使用 `pw_filter` 直接从设备采集音频/视频数据，或者将数据输出到指定设备。

------

### **`pw_filter` 的核心接口**

以下是 `pw_filter` 的核心 API 和用途：

| 函数                       | 用途                                                    |
| -------------------------- | ------------------------------------------------------- |
| `pw_filter_new()`          | 创建一个新的 `pw_filter` 对象。                         |
| `pw_filter_add_listener()` | 为 `pw_filter` 添加事件监听器（如状态改变、数据接收）。 |
| `pw_filter_connect()`      | 将 `pw_filter` 连接到 PipeWire 中的设备或流。           |
| `pw_filter_destroy()`      | 销毁 `pw_filter` 对象，释放资源。                       |
| `pw_filter_set_param()`    | 设置参数，如采样率、格式等。                            |
| `pw_filter_emit_process()` | 回调处理函数，用于处理音频或视频数据。                  |

------

### **典型用法**

以下是一个使用 `pw_filter` 实现简单音频处理的例子：

#### **1. 初始化 PipeWire 和上下文**

```c
struct pw_main_loop *loop = pw_main_loop_new(NULL);
struct pw_context *context = pw_context_new(pw_main_loop_get_loop(loop), NULL, 0);
```

#### **2. 创建 `pw_filter`**

```c
struct pw_filter *filter = pw_filter_new(context, "My Filter", NULL);
```

#### **3. 添加事件回调**

```c
static void on_process(void *data) {
    struct pw_buffer *buffer;
    struct spa_buffer *spa_buf;

    if ((buffer = pw_filter_dequeue_buffer(filter)) == NULL) {
        return;
    }

    spa_buf = buffer->buffer;
    if (spa_buf->datas[0].data != NULL) {
        // 处理音频数据
        memset(spa_buf->datas[0].data, 0, spa_buf->datas[0].chunk->size); // 简单静音处理
    }

    pw_filter_queue_buffer(filter, buffer);
}

struct pw_filter_events filter_events = {
    PW_VERSION_FILTER_EVENTS,
    .process = on_process, // 注册数据处理回调
};

pw_filter_add_listener(filter, &listener, &filter_events, NULL);
```

#### **4. 连接到目标节点**

```c
pw_filter_connect(filter,
    PW_DIRECTION_INPUT,  // 数据流方向
    PW_FILTER_FLAG_DRIVER,  // 标志位
    NULL, 0);
```

#### **5. 启动主循环**

```c
pw_main_loop_run(loop);
```

#### **6. 清理资源**

```c
pw_filter_destroy(filter);
pw_context_destroy(context);
pw_main_loop_destroy(loop);
```

------

### **回调机制**

- `pw_filter` 的核心是事件驱动模型，用户需要提供回调处理音频或视频数据。
- 典型回调包括：
  - **`process`**：每当有新数据到达时触发，用户在这里实现自定义数据处理逻辑。
  - **`state_changed`**：过滤器状态改变时触发，通常用于监控连接状态。

------

### **优点**

| 优点       | 描述                                                      |
| ---------- | --------------------------------------------------------- |
| **易用性** | 提供封装好的接口，开发者无需直接操作低级别 PipeWire API。 |
| **实时性** | 支持高效的实时数据处理，满足音频/视频应用的需求。         |
| **灵活性** | 可用于音频和视频流的多种场景，支持自定义参数和逻辑。      |
| **模块化** | 可以作为独立的过滤模块，方便与 PipeWire 的其他组件集成。  |

------

### **总结**

`pw_filter` 是 PipeWire 为简化客户端开发提供的重要工具，适用于音频或视频流的实时处理。它通过事件驱动模型和灵活的配置接口，使开发者可以高效构建各种数据处理应用，如音频特效、流媒体处理和实时采集等。

# adapter-control

```
audiotestsrc -> adapter -> alsa-pcm-sink 
```



# pipewire的spa plugin ffmpeg怎么使用

PipeWire 的 `SPA plugin ffmpeg` 是一种插件，用于通过 SPA (Simple Plugin API) 框架集成 FFmpeg 功能，提供对多种媒体格式的支持。这种插件主要用于处理音视频的编码、解码和格式转换。

------

### **主要用途**

| 用途           | 描述                                                         |
| -------------- | ------------------------------------------------------------ |
| **音视频解码** | 使用 FFmpeg 解码音频或视频流，例如 MP3、AAC、H264 等常见格式。 |
| **音视频编码** | 将原始音频或视频数据编码为特定格式，比如 MP3 或 H264。       |
| **格式转换**   | 在不同的音频/视频格式之间进行转码或重采样。                  |
| **管道集成**   | 将 FFmpeg 的强大功能直接集成到 PipeWire 流处理中，支持更多的格式。 |

------

### **启用插件**

1. **插件安装**
    确保系统已经安装了 PipeWire 并且其构建时启用了 FFmpeg 插件支持。通常需要以下依赖：

   - FFmpeg 库（例如 `libavcodec`、`libavformat`、`libswresample` 等）

   - 包管理器安装 FFmpeg 开发头文件：

     ```bash
     sudo apt install libavcodec-dev libavformat-dev libswresample-dev
     ```

2. **检查插件是否可用**
    确认插件是否被 PipeWire 加载：

   ```bash
   pw-cli dump spa-plugin | grep ffmpeg
   ```

   输出中应包含 `ffmpeg` 相关信息。

3. **插件配置文件**

   - 通常，FFmpeg 插件在 PipeWire 的配置文件中自动加载。

   - 检查 `/usr/share/pipewire` 或 `/etc/pipewire` 目录下是否存在加载配置。

   - 如果插件未加载，可以在 

     ```
     pipewire.conf
     ```

      或自定义配置文件中添加：

     ```ini
     context.spa-libs = {
         "support/libspa-ffmpeg" = "/usr/lib/spa-0.2/ffmpeg/libspa-ffmpeg.so"
     }
     ```

------

### **典型用法**

#### **1. 使用 FFmpeg 插件进行解码**

- 假设需要通过 PipeWire 处理 MP3 文件。
- 使用 `pw-cli` 或编写程序将数据通过 PipeWire 的 FFmpeg 节点解码为原始 PCM 数据。

示例步骤：

1. 创建 FFmpeg 节点

   ```bash
   pw-cli create-node support.libspa-ffmpeg
   ```

2. 连接数据源和目标

   - 数据源：MP3 文件或流媒体。
   - 目标：音频输出节点（如 ALSA 或蓝牙设备）。

#### **2. 在客户端程序中使用**

PipeWire 的客户端 API 可直接与 FFmpeg 插件交互。例如：

```c
#include <pipewire/pipewire.h>
#include <spa/param/audio/format-utils.h>

void setup_ffmpeg_node(struct pw_context *context) {
    struct pw_properties *props = pw_properties_new(
        PW_KEY_MEDIA_TYPE, "Audio",
        PW_KEY_MEDIA_CATEGORY, "Playback",
        PW_KEY_MEDIA_ROLE, "Music",
        NULL);

    struct pw_core *core = pw_context_connect_self(context, NULL, 0);

    struct pw_node *node = pw_node_new(context, "ffmpeg-decoder", props);
    pw_node_register(node, NULL);
    pw_core_add_object(core, (struct pw_global *)node);
}
```

------

### **3. 配置格式转换**

可以通过 `pw-cli` 设置目标格式，例如将音频从 MP3 转为 PCM：

```bash
pw-cli set-param <node-id> spa:audio/format '{ "format": "S16LE", "rate": 44100, "channels": 2 }'
```

------

### **优点**

| 特性             | 描述                                                 |
| ---------------- | ---------------------------------------------------- |
| **多格式支持**   | 凭借 FFmpeg，支持广泛的音视频格式。                  |
| **高效流式处理** | 与 PipeWire 的流处理机制结合，实现低延迟和高效解码。 |
| **模块化设计**   | 可单独加载或卸载，不影响其他 PipeWire 模块。         |

------

### **常见问题**

1. 插件未加载
   - 确保插件库路径正确，并检查 `pipewire.conf` 是否配置了 `ffmpeg`。
2. 缺少依赖
   - 安装 FFmpeg 所需的库和开发头文件。
3. 性能问题
   - 检查系统是否启用了适当的硬件加速（如 VAAPI 或 CUDA）。

------

### **总结**

`SPA plugin ffmpeg` 为 PipeWire 提供了强大的音视频处理能力，支持多种格式的解码、编码和格式转换。通过加载和配置此插件，可以轻松扩展 PipeWire 的多媒体功能，满足复杂的音视频处理需求。

# 依次加载的pw module

```
rt
protocol-native

libpipewire-module-spa-device-factory
	这个是用于创建在server context里运行的device。
libpipewire-module-spa-node-factory
	这个是用于创建在server context里运行的node。
libpipewire-module-client-node
	创建在client context运行的node。
libpipewire-module-client-device 
	创建在client context运行的device。
```

# pipewire的metadata到底是指什么

在 PipeWire 中，**Metadata** 是一种机制，

用于存储和共享系统中与节点或链接相关的附加信息。

这些信息并不直接影响音频或视频流的处理，

但对管理、显示和控制非常重要。

------

### **Metadata 的作用**

1. **附加信息存储**
    为节点、链接或其他对象存储==额外的键值对信息。==
2. **集中共享**
    使多个应用或插件可以访问和使用这些信息。
3. **动态更新**
    Metadata 可在运行时动态更改，并通知相关组件。
4. **控制和调试**
    提供关于系统状态的描述性信息，例如优先级、位置、用途等。

------

### **Metadata 的典型使用场景**

| 场景           | 示例                                          |
| -------------- | --------------------------------------------- |
| **设备描述**   | 存储节点的描述性信息，如设备名称或型号。      |
| **优先级设置** | 指定某个节点为首选设备，例如 "默认音频输出"。 |
| **位置标识**   | 标记设备的物理位置，例如 "左前置扬声器"。     |
| **应用间协作** | 在应用间共享配置数据，例如 EQ 设置。          |

------

### **Metadata 的结构**

Metadata 是以键值对形式存储，通常基于以下结构：

- **对象**：特定的 PipeWire 对象（如节点、设备或链接）。
- **键值对**：附加信息的键和值。

------

### **如何使用 Metadata**

#### **1. 启用 Metadata 模块**

确保配置文件中加载了 `libpipewire-module-metadata` 模块（默认已启用）。

在 `pipewire.conf` 中：

```ini
{ name = libpipewire-module-metadata }
```

#### **2. 查看现有 Metadata**

使用 `pw-cli` 查看 Metadata 信息：

```bash
pw-metadata
```

输出示例：

```plaintext
object 0 type PipeWire:Interface:Metadata/3
update: id: 32, key: "default.audio.sink", value: "alsa_output.pci-0000_00_1b.0.analog-stereo"
update: id: 45, key: "default.audio.source", value: "alsa_input.pci-0000_00_1b.0.analog-stereo"
```

解释：

- `default.audio.sink`: 默认音频输出设备。
- `default.audio.source`: 默认音频输入设备。

#### **3. 设置 Metadata**

使用 `pw-cli` 添加或更新 Metadata：

```bash
pw-metadata set default.audio.sink "my-audio-device"
```

------

### **代码示例**

通过 C API 操作 Metadata：

```c
#include <pipewire/pipewire.h>

void set_metadata(struct pw_core *core) {
    struct pw_metadata *metadata = pw_context_create_metadata(core, NULL, 0);
    if (metadata) {
        pw_metadata_set(metadata, 0, "default.audio.sink", "alsa_output.my_device", NULL);
        pw_metadata_set(metadata, 0, "device.description", "My Custom Audio Output", NULL);
    }
}
```

------

### **动态切换设备**

通过设置 Metadata，可以动态更改系统的默认音频设备：

1. 查看设备列表：

   ```bash
   pw-cli dump Node
   ```

2. 更新默认输出：

   ```bash
   pw-metadata set default.audio.sink "alsa_output.new_device"
   ```

------

### **总结**

Metadata 是 PipeWire 中强大的辅助机制，用于存储和共享系统中附加信息。通过 Metadata，用户和应用可以更好地协作、控制和定制系统的行为，而不会直接影响音视频流的处理逻辑。

# pw_thread_loop 使用

`pw_thread_loop` 是 PipeWire 提供的一个线程化事件循环，用于在专用线程中运行任务，例如音频处理或设备管理。通过这种机制，可以避免与主线程的竞争，并保证实时性任务的执行效率。

------

### **主要功能**

| 功能           | 描述                                       |
| -------------- | ------------------------------------------ |
| **线程化循环** | 独立线程运行事件循环。                     |
| **线程安全**   | 提供锁机制以安全地在主线程和子线程间通信。 |
| **实时处理**   | 支持实时优先级的任务调度。                 |

------

### **核心 API**

| 函数                      | 描述                                         |
| ------------------------- | -------------------------------------------- |
| `pw_thread_loop_new`      | 创建一个新的线程事件循环。                   |
| `pw_thread_loop_start`    | 启动事件循环线程。                           |
| `pw_thread_loop_stop`     | 停止事件循环线程。                           |
| `pw_thread_loop_lock`     | 加锁，阻止其他线程修改共享资源。             |
| `pw_thread_loop_unlock`   | 解锁，允许其他线程继续操作。                 |
| `pw_thread_loop_signal`   | 唤醒事件循环线程。                           |
| `pw_thread_loop_wait`     | 等待信号，通常用于线程间同步。               |
| `pw_thread_loop_destroy`  | 销毁事件循环并释放资源。                     |
| `pw_thread_loop_get_loop` | 获取底层的 `pw_loop`，用于附加事件源等操作。 |

------

### **基本使用流程**

#### **1. 创建事件循环**

使用 `pw_thread_loop_new` 创建一个新的线程事件循环：

```c
struct pw_thread_loop *loop = pw_thread_loop_new("my-loop", NULL);
if (!loop) {
    fprintf(stderr, "Failed to create thread loop\n");
    return -1;
}
```

#### **2. 启动事件循环**

调用 `pw_thread_loop_start` 启动线程和事件循环：

```c
if (pw_thread_loop_start(loop) != 0) {
    fprintf(stderr, "Failed to start thread loop\n");
    pw_thread_loop_destroy(loop);
    return -1;
}
```

#### **3. 在事件循环中执行任务**

使用 `pw_thread_loop_lock` 和 `pw_thread_loop_unlock` 保护共享资源操作：

```c
pw_thread_loop_lock(loop);

// 在锁定的上下文中执行任务，例如修改共享数据或注册事件。
do_some_shared_operation();

// 解锁以允许其他线程访问资源。
pw_thread_loop_unlock(loop);
```

#### **4. 信号与等待**

在线程间进行通信，例如通知任务完成：

```c
// 在主线程中唤醒事件循环线程。
pw_thread_loop_signal(loop, false);

// 在事件循环线程中等待信号。
pw_thread_loop_wait(loop);
```

#### **5. 停止与销毁**

完成工作后，停止事件循环并释放资源：

```c
pw_thread_loop_stop(loop);
pw_thread_loop_destroy(loop);
```

------

### **完整示例**

以下代码展示了如何使用 `pw_thread_loop` 在专用线程中执行任务：

```c
#include <pipewire/pipewire.h>
#include <stdio.h>

void *worker_task(void *data) {
    struct pw_thread_loop *loop = data;

    pw_thread_loop_lock(loop);
    printf("Task running in thread loop\n");
    // 模拟工作
    pw_thread_loop_signal(loop, false);
    pw_thread_loop_unlock(loop);

    return NULL;
}

int main() {
    struct pw_thread_loop *loop;

    // 初始化 PipeWire
    pw_init(NULL, NULL);

    // 创建线程循环
    loop = pw_thread_loop_new("example-loop", NULL);
    if (!loop) {
        fprintf(stderr, "Failed to create thread loop\n");
        return -1;
    }

    // 启动线程循环
    if (pw_thread_loop_start(loop) != 0) {
        fprintf(stderr, "Failed to start thread loop\n");
        pw_thread_loop_destroy(loop);
        return -1;
    }

    // 执行任务
    pw_thread_loop_lock(loop);
    printf("Main thread: scheduling task\n");
    pw_thread_loop_signal(loop, false);
    pw_thread_loop_unlock(loop);

    // 等待任务完成
    pw_thread_loop_wait(loop);

    // 停止并销毁循环
    pw_thread_loop_stop(loop);
    pw_thread_loop_destroy(loop);

    return 0;
}
```

------

### **注意事项**

1. **实时优先级**
    如果需要实时性能，可以在启动线程时配置优先级。

   ```c
   pw_thread_loop_set_priority(loop, 10);
   ```

2. **线程同步**
    避免在没有锁保护的情况下访问共享数据。

3. **事件源**
    可以将事件源（如定时器、文件描述符等）附加到 `pw_loop`，实现更复杂的功能。

------

### **总结**

`pw_thread_loop` 提供了一个安全、高效的线程化事件循环工具，适用于实时任务和多线程 PipeWire 应用。通过其锁机制和信号通信，开发者可以在复杂任务中保证线程安全和数据完整性。

# pw_stream

pw_stream是用来跟pipewire server交换数据用的。

它是一个wrapper，包装了pw_client_node的proxy，带有一个converter。

这个意味着stream可以自动转换server需要的格式。

pw_stream可以：

* 消费pipewire过来的stream。
* 生产pipewire需要的stream。

你可以连接到server的指定port上。也可以让pipewire自动帮你选择一个port。



对于复杂的node，例如filter或者有多个input和output的node，

你需要使用pw_filter，或者你自己写一个pw_node并且用pw_core_export暴露给pipewire。

## 关于stream的delay

```
pw_stream_get_time_n
	这个函数拿到时间戳。
pw_time.ticks 
	这个是一个递增的counter。
pw_time.delay
```

```
*           stream time domain           graph time domain
 *         /-----------------------\/-----------------------------\
 *
 * queue     +-+ +-+  +-----------+                 +--------+
 * ---->     | | | |->| converter | ->   graph  ->  | kernel | -> speaker
 * <----     +-+ +-+  +-----------+                 +--------+
 * dequeue   buffers                \-------------------/\--------/
 *                                     graph              internal
 *                                    latency             latency
 *         \--------/\-------------/\-----------------------------/
 *           queued      buffered            delay
```

# pw_resource用途

在 PipeWire 中，`pw_resource` 是一种用于管理客户端与服务端之间通信的对象。它代表了服务端中的一个资源（Resource），通常绑定到某个客户端，并为客户端提供访问服务端对象的接口。

------

### **主要用途**

| 用途               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **客户端资源管理** | 每个客户端可以通过 `pw_resource` 与服务端的某些对象进行交互。 |
| **方法调用的代理** | 通过 `pw_resource` 将客户端请求映射到服务端的实际实现上。    |
| **权限控制**       | 资源可以检查客户端的权限，确保只有授权的客户端可以执行某些操作。 |
| **事件分发**       | 服务端可以通过资源向客户端发送事件通知，例如状态更新或错误。 |
| **接口绑定**       | `pw_resource` 绑定特定的接口类型，用于描述客户端可以调用的方法和接收的事件。 |

------

### **资源生命周期**

1. **创建**
    资源由 `pw_client` 创建，通常是某个服务端对象（如 `pw_node`、`pw_link`）的代理。

   ```c
   struct pw_resource *resource = pw_resource_new(client, id, permissions, type, version, user_data);
   ```

2. **方法调用**
    客户端调用资源上的方法，资源会将调用映射到服务端对应的实现。

3. **事件分发**
    服务端通过资源向客户端发送事件，例如通过接口中定义的回调方法。

4. **销毁**
    当资源或客户端断开连接时，资源被销毁。

------

### **主要 API**

| 函数                              | 描述                                         |
| --------------------------------- | -------------------------------------------- |
| `pw_resource_new`                 | 创建新的资源对象。                           |
| `pw_resource_add_listener`        | 添加资源监听器，用于接收客户端调用的事件。   |
| `pw_resource_add_object_listener` | 添加资源对象监听器，绑定特定接口类型的回调。 |
| `pw_resource_set_bound_id`        | 设置资源绑定的服务端对象的全局 ID。          |
| `pw_resource_get_client`          | 获取该资源绑定的客户端对象。                 |
| `pw_resource_error`               | 向客户端报告资源错误。                       |
| `pw_resource_remove`              | 手动移除资源。                               |
| `pw_resource_get_bound_id`        | 获取资源绑定的服务端对象的全局 ID。          |

------

### **代码示例**

#### **1. 创建资源**

以下代码展示了如何在服务端为客户端创建一个资源：

```c
struct pw_resource *resource;
uint32_t id = 42; // 客户端请求的对象 ID

resource = pw_resource_new(client, id, PW_PERM_ALL, PW_TYPE_INTERFACE_Node, PW_VERSION_NODE, NULL);
if (!resource) {
    fprintf(stderr, "Failed to create resource\n");
    return -1;
}
```

#### **2. 添加接口回调**

为资源绑定接口方法的实现：

```c
static const struct pw_node_methods node_methods = {
    .add_listener = my_node_add_listener,
    .set_param = my_node_set_param,
    // 其他方法实现...
};

pw_resource_add_object_listener(resource, &node_methods, user_data);
```

#### **3. 分发事件**

服务端通过资源向客户端发送事件：

```c
static void send_event(struct pw_resource *resource) {
    struct pw_node_events *events = pw_resource_get_user_data(resource);
    if (events && events->info) {
        events->info(resource, &node_info);
    }
}
```

#### **4. 销毁资源**

当资源不再需要时，手动销毁：

```c
pw_resource_remove(resource);
```

------

### **常见使用场景**

1. **客户端请求服务端对象**
    客户端通过 `pw_core` 请求一个对象（如 Node 或 Link），服务端会为其创建一个对应的 `pw_resource`。
2. **服务端通知客户端**
    服务端通过资源向客户端发送事件，例如节点状态变化或参数更新。
3. **动态权限管理**
    `pw_resource` 可以根据客户端的权限检查是否允许其执行某些操作。

------

### **示例：Node 资源绑定**

以下展示了一个为 `Node` 创建资源并绑定方法的完整流程：

```c
// 创建 Node 资源
struct pw_resource *node_resource = pw_resource_new(client, id, PW_PERM_ALL, PW_TYPE_INTERFACE_Node, PW_VERSION_NODE, NULL);

// 设置绑定的 Node 对象
pw_resource_set_bound_id(node_resource, node->global->id);

// 添加回调
pw_resource_add_object_listener(node_resource, &node_methods, node);
```

客户端可以通过该资源调用与 `Node` 相关的方法，服务端通过绑定的接口实现提供响应。

------

### **总结**

`pw_resource` 是 PipeWire 服务端与客户端通信的重要桥梁，主要用于管理资源、分发事件和处理客户端请求。通过其灵活的设计，开发者可以为不同的服务端对象创建统一的接口代理，实现高效、可扩展的系统架构。

# pw_proxy

```
 * The proxy object is a client side representation of a resource
 * that lives on a remote PipeWire instance.
```

pw_proxy就是在client这一边用来访问存放在server上的资源的代理。

用来跟远程object通信的。

# core_hello

这个函数`core_hello`是PipeWire的一个核心函数，用于处理客户端的hello消息。它的主要功能是：

1. 记录调试日志，显示客户端的hello消息。
2. 遍历客户端的对象列表，销毁所有资源。
3. 更新资源的版本号。
4. 清空客户端的内存池。
5. 获取核心信息，并更新客户端的信息。
6. 如果客户端版本号大于或等于3，则绑定全局对象。

函数返回0表示成功，否则返回错误码。

# PIPEWIRE_INTERNAL环境变量的用途

`PIPEWIRE_INTERNAL` 是 PipeWire 中一个特殊的环境变量，主要用于标识内部或特殊运行模式，而非用户或外部应用常规使用的模式。

------

### **用途和作用**

| **用途**         | **描述**                                                     |
| ---------------- | ------------------------------------------------------------ |
| **调试和开发**   | 在开发或调试 PipeWire 内部组件时，标识某些特定的运行路径或行为。 |
| **内部实例隔离** | 在某些情况下，需要运行一个与正常用户会话隔离的 PipeWire 实例，这时可以通过设置该变量实现。 |
| **模块加载控制** | 限制或调整 PipeWire 加载模块的方式，避免加载某些非必要模块，从而简化调试环境。 |
| **减少干扰**     | 防止内部 PipeWire 实例与系统范围的服务（如主 PipeWire 实例或客户端）发生冲突。 |

------

### **具体实现逻辑**

在 PipeWire 的代码中，`PIPEWIRE_INTERNAL` 可能会通过以下方式发挥作用：

1. **检查是否设置该变量**
    某些模块或代码路径会判断 `PIPEWIRE_INTERNAL` 是否存在，从而决定是否启用某些功能或模块。

   ```c
   const char *env = getenv("PIPEWIRE_INTERNAL");
   if (env) {
       // 内部模式逻辑
   }
   ```

2. **限制全局资源访问**
    内部模式下，PipeWire 可能会避免注册全局资源，如系统范围的音频设备或外部客户端。

3. **定制化行为**
    可以通过该环境变量，触发特定的调试行为，例如更详细的日志输出或跳过某些复杂的初始化步骤。

------

### **使用场景**

以下是 `PIPEWIRE_INTERNAL` 的常见使用场景：

1. **开发人员测试内部功能**
    用于 PipeWire 核心开发者在调试模块或协议实现时，启动内部实例。

   ```bash
   PIPEWIRE_INTERNAL=1 pipewire
   ```

2. **隔离实例运行**
    在运行 PipeWire 的多个实例时，确保它们互不干扰，例如在容器化环境或沙盒环境中使用。

3. **实验性功能**
    某些实验性功能可能仅在内部模式下启用，而不会对普通用户可见。

------

### **注意事项**

- **普通用户不需要设置**：`PIPEWIRE_INTERNAL` 主要是为了内部使用或开发者测试，普通用户使用 PipeWire 时无需设置。
- **影响行为**：设置该变量可能导致 PipeWire 不按预期加载某些模块，或与正常用户会话不兼容，因此建议仅用于特定场景。
- **文档较少**：由于其是内部使用的功能，官方文档中对其描述可能较少，需要参考源码了解具体实现。

------

### **总结**

`PIPEWIRE_INTERNAL` 是一个用于控制 PipeWire 内部运行模式的环境变量，主要用于开发、调试或隔离实例运行。它的设置会影响 PipeWire 的行为，普通用户无需关心，开发者可以用它来简化内部测试或实现定制化功能。

# pipewire和pipewire-pulse的关系

他们是一个程序，pipewire-pulse是指向pipewire的软链接。

程序名字会影响所使用的配置文件。是代码这里决定的：

```
	snprintf(path, sizeof(path), "%s.conf", argv[0]);
	config_name = basename(path);
```

配置文件名字是根据可执行程序的名字来决定的。



# 同时运行多个pipewire进程，他们之间是如何配合工作的？



在常规情况下，系统中通常只会运行一个 PipeWire 服务进程（`pipewire`），

它作为一个全局服务管理所有客户端的音频和视频资源。

然而，在某些场景下，可能需要同时运行多个 PipeWire 实例，

比如用于隔离、沙盒测试或多用户环境。

这些实例之间并不会直接配合工作，而是通过特定的机制实现互相隔离或独立运行。

------

### **多个 PipeWire 实例的典型运行场景**

| 场景               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **用户隔离**       | 每个用户会话运行独立的 PipeWire 实例，例如在多用户服务器环境中，每个用户的实例互相隔离。 |
| **容器或沙盒环境** | 在容器中运行单独的 PipeWire 实例，避免与宿主机上的 PipeWire 产生冲突。 |
| **开发和调试**     | 开发者在不同的调试会话中运行多个实例，用于测试不同配置或模块功能。 |

------

### **实例之间的隔离与独立性**

1. **配置文件隔离**

   - 每个 PipeWire 实例加载独立的配置文件（默认是 `/etc/pipewire` 和 `~/.config/pipewire` 中的配置）。

   - 通过指定 

     ```
     PIPEWIRE_CONFIG_FILE
     ```

      环境变量可以显式指定每个实例的配置路径：

     ```bash
     PIPEWIRE_CONFIG_FILE=/path/to/config pipewire
     ```

2. **通信端点隔离**

   - PipeWire 使用 Unix 域套接字或共享内存进行通信，默认情况下，套接字会在 `/run/user/<UID>/pipewire-0` 中创建。

   - 每个实例可以通过 

     ```
     PIPEWIRE_RUNTIME_DIR
     ```

      环境变量指定不同的套接字目录，以避免冲突：

     ```bash
     PIPEWIRE_RUNTIME_DIR=/tmp/pipewire-instance-1 pipewire
     PIPEWIRE_RUNTIME_DIR=/tmp/pipewire-instance-2 pipewire
     ```

3. **资源命名隔离**

   - 每个实例注册的全局资源（如节点、链路）在其命名空间内是唯一的，不会与其他实例冲突。

4. **模块加载独立**

   - 每个实例可以加载不同的模块，模块配置由各自的配置文件控制。

------

### **实例之间的交互**

在正常情况下，多个 PipeWire 实例是相互隔离的，不会直接配合工作。然而，某些场景下可能需要它们之间进行通信或资源共享，可以通过以下方式实现：

1. **共享虚拟设备**
   - 一个实例可以通过虚拟设备（如 `pw-loopback`）将其资源输出到另一个实例中。
   - 配置示例：
     - 实例 A 运行一个虚拟 sink。
     - 实例 B 将其音频通过 `pw-link` 链接到实例 A 的虚拟 sink。
2. **通过 PulseAudio 插件间接共享**
   - 如果多个实例都支持 PulseAudio API，则可以通过 PulseAudio 插件间接实现交互。
   - 示例：实例 A 提供 PulseAudio 兼容的 sink，实例 B 使用 PulseAudio 客户端连接到该 sink。
3. **通过网络协议共享**
   - 使用 PipeWire 的 `libpipewire-module-protocol-native` 模块，允许一个实例通过网络向另一个实例共享资源。

------

### **实践示例**

#### **同时运行两个实例**

1. 启动第一个实例：

   ```bash
   PIPEWIRE_RUNTIME_DIR=/tmp/pipewire-instance-1 PIPEWIRE_CONFIG_FILE=/path/to/config1 pipewire
   ```

2. 启动第二个实例：

   ```bash
   PIPEWIRE_RUNTIME_DIR=/tmp/pipewire-instance-2 PIPEWIRE_CONFIG_FILE=/path/to/config2 pipewire
   ```

3. 使用 `pw-cli` 查看实例状态：

   ```bash
   PIPEWIRE_RUNTIME_DIR=/tmp/pipewire-instance-1 pw-cli info
   PIPEWIRE_RUNTIME_DIR=/tmp/pipewire-instance-2 pw-cli info
   ```

------

### **注意事项**

1. **性能开销**
   - 同时运行多个实例会消耗更多的系统资源，尤其是在处理高负载的音频或视频流时。
2. **数据一致性**
   - 如果需要实例间共享数据，需谨慎设计资源同步机制，以避免数据竞争或冲突。
3. **调试复杂度**
   - 多实例运行可能导致调试难度增加，建议在开发和调试时使用清晰的日志配置。

------

### **总结**

多个 PipeWire 实例通常是互相独立运行的，使用不同的配置文件、通信端点和资源命名空间。如果需要交互，可以通过虚拟设备、网络协议或其他间接方式实现。在实际应用中，这种多实例架构适用于隔离需求较高的场景，例如多用户环境、容器化部署或开发调试。

# 同时运行pipewire和pipewire-pluse呢？

同时运行 `pipewire` 和 `pipewire-pulse` 是一种常见的场景，特别是为了兼容 PulseAudio 客户端。`pipewire-pulse` 是 PipeWire 的一个模块，旨在为基于 PulseAudio 的应用程序提供兼容层。通过这种方式，使用 PulseAudio 的应用程序可以无缝地与 PipeWire 协同工作，从而利用 PipeWire 提供的更强大和灵活的音频处理功能。

### **如何同时运行 `pipewire` 和 `pipewire-pulse`**

1. `pipewire` 进程

   ：

   - `pipewire` 是 PipeWire 的核心进程，负责处理音频和视频流。它充当整个系统中音频和视频的中央管理器。

2. `pipewire-pulse` 模块

   ：

   - `pipewire-pulse` 是一个兼容 PulseAudio 的模块，允许 PulseAudio 客户端（如传统的桌面应用程序）通过 PipeWire 管理音频流。
   - 它实现了 PulseAudio API，因此大多数使用 PulseAudio 的应用程序可以透明地切换到 PipeWire 上。

### **启动顺序**

通常，PipeWire 和 `pipewire-pulse` 模块会作为一个整体启动，但你也可以手动启动它们。

1. **启动 PipeWire**： `pipewire` 进程需要首先启动，它会初始化音频和视频流的处理。

   ```bash
   pipewire
   ```

2. **启动 `pipewire-pulse`**： `pipewire-pulse` 作为一个独立的进程或模块运行，通常它会在启动 `pipewire` 后自动启动，但如果没有，可以手动启动：

   ```bash
   pipewire-pulse
   ```

3. **同时运行（手动方式）**： 如果你希望分别控制这两个进程，你可以在终端中分别启动它们，确保它们运行在不同的进程中：

   ```bash
   pipewire  # 启动 PipeWire 核心进程
   pipewire-pulse  # 启动 PulseAudio 兼容层
   ```

### **配置文件**

在某些情况下，你可能希望自定义这两个进程的行为。你可以编辑它们的配置文件，特别是 `pipewire-pulse` 的配置文件，通常位于：

- `/etc/pipewire/pipewire-pulse.conf`（系统级配置）
- `~/.config/pipewire/pipewire-pulse.conf`（用户级配置）

这些文件允许你配置 PipeWire 和 PulseAudio 兼容层的详细行为，例如，PulseAudio 客户端的行为或共享音频设备的配置。

### **如何协同工作**

- **音频流共享**：`pipewire-pulse` 提供 PulseAudio 客户端与 PipeWire 系统之间的桥梁，使得 PulseAudio 客户端可以透明地使用 PipeWire 管理的音频设备。音频流从 PulseAudio 客户端经过 `pipewire-pulse` 转发到 PipeWire 核心。
- **虚拟设备**：`pipewire-pulse` 会提供一个名为 PulseAudio 的虚拟设备，它与传统的 PulseAudio 的 `alsa-sink` 等设备类似，允许应用程序与之交互。

### **调试和验证**

- **验证 `pipewire-pulse` 是否正在运行**： 你可以通过检查 `pipewire-pulse` 进程是否启动来确认它是否在运行。

  ```bash
  ps aux | grep pipewire-pulse
  ```

- **检查 PulseAudio 的状态**： 你可以使用 `pactl` 命令检查 PipeWire 是否作为 PulseAudio 后端正常工作：

  ```bash
  pactl info
  ```

- **查看 PipeWire 状态**： 如果 `pipewire-pulse` 正常运行，你可以使用 `pw-cli` 或 `pw-top` 查看 PipeWire 的运行状态：

  ```bash
  pw-cli info
  pw-top
  ```

### **为什么要同时运行 PipeWire 和 `pipewire-pulse`？**

1. **兼容性**：
   - 许多现有的桌面应用程序和软件（例如浏览器、媒体播放器）依赖于 PulseAudio 作为音频后端。使用 `pipewire-pulse` 可以确保这些应用程序在 PipeWire 环境中正常工作，而不需要重构或更改现有代码。
2. **迁移**：
   - 对于已经依赖 PulseAudio 的系统和应用程序，`pipewire-pulse` 提供了平滑的过渡到 PipeWire 的路径。用户可以在不改变应用程序的情况下享受 PipeWire 的优势，如更低延迟、更高效的多媒体处理和更强大的音频流管理。
3. **性能优化**：
   - PipeWire 提供的 API 比 PulseAudio 更加灵活和强大，可以更好地处理复杂的音频路由、音效处理等，用户可以利用这些功能，同时保持对传统应用程序的支持。

### **总结**

- **`pipewire`** 是 PipeWire 的核心进程，负责处理所有音频和视频流。
- **`pipewire-pulse`** 是一个兼容 PulseAudio 的模块，使基于 PulseAudio 的应用程序能够使用 PipeWire 作为音频管理后端。
- 你可以分别启动这两个进程，确保它们正常工作并互不干扰。
- 使用 `pipewire-pulse` 可以确保传统的 PulseAudio 应用程序能在 PipeWire 环境中运行，同时享受 PipeWire 的先进特性。

这种配置非常适用于迁移到 PipeWire 系统，特别是在需要兼容大量基于 PulseAudio 的应用程序的情况下。



# 概念辨析

一个模块是一个共享对象，

用于向 PipeWire 客户端添加功能。

它有一个初始化函数，在模块加载时会被调用。

模块可以在核心进程中加载，

也可以在任何客户端进程中加载。

==客户端不会将加载的模块导出到注册表中。==

稍后我们将看到模块的示例以及如何加载它们。



设备是一个表示底层 API 的句柄，

然后用于创建节点或其他设备。

设备的例子是 ALSA PCM 卡或 V4L2 设备。

设备有一个配置文件。



权限目前还没有用起来。

因为所有客户端都默认具有 `rwxm` 权限：读取、写入、执行、元数据。



每个对象至少实现 `add_listener` 方法，允许任何客户端注册事件监听器。事件通过 PipeWire API 来暴露可能随时间变化的对象信息（例如节点的状态）。



一旦在一个process中创建了一个对象，

就可以将其导出到核心的注册表中，

使其成为图的一部分。

导出后，对象将被暴露并可以被其他客户端访问；

这将我们带入了新的部分：客户端如何获取访问权限并与图进行交互。



与 PipeWire 实例交互的最简单方式是依赖 `libpipewire` 共享对象库。

这是一个 C 库，允许连接到核心。

连接步骤如下：

* 初始化库使用 `pw_init` ，其主要目标是设置日志。
* 创建一个事件循环实例
* 使用 `pw_context_new` 创建一个 PipeWire 上下文实例。该上下文将处理与 PipeWire 的通信过程，在事件循环中添加所需的内容。它还将从文件系统中查找并解析配置文件。
* 将上下文连接到核心守护进程使用 `pw_context_connect` 。这做了两件事：初始化通信方式并返回核心对象的代理。



事件监听器因此是客户端可以使用 `pw_*_add_listener` 注册在代理对象上的回调， `pw_*_add_listener` 接受一个定义函数指针列表的 `struct pw_*_events` ；星号应被对象类型替换。 `libpipewire` 库会将这个新监听器告知远程对象，以便在发生新事件时通知客户端。



client.conf 和 client-rt.conf 之间的区别在于 client-rt.conf 加载了 libpipewire-module-rt，这使得进程及其线程启用了实时优先级。



`context.objects` 允许通过提供与参数关联的工厂名称来静态创建对象。

这正是 daemon 的 pipewire.conf 用于创建虚拟节点，

或 minimal.conf 用于静态创建 ALSA 设备和节点以及静态节点的方式。



# minimal.conf

minimal.conf，作为那些希望在没有会话管理器的情况下运行 PipeWire 的示例（静态配置的 ALSA 设备、节点和链接）。



# portal

Flatpaks 是桌面沙盒应用程序，

依赖于 portal（一个暴露 D-Bus 接口的过程）来访问系统级功能，如打印和音频。

在我们的情况下， `libpipewire-module-portal` 允许 portal 进程处理 Flatpak 应用程序相关的音频权限管理。

更多信息请参见 module-portal.c 和 xdg-desktop-portal。

# quantum

一个周期处理的样本数量称为量子quantum。



# node分类

一个节点可以有两种类型：它可以是驱动节点（driver node）或跟随节点（follower node）。

对于每个子图，有一个单一的驱动节点，

除了处理样本之外，

还负责提供时间信息：

图执行周期应该在何时开始。

其他节点是跟随节点；它们在每个周期中执行。



大多数跟随节点支持不连接到驱动节点。

它们处于挂起状态，其处理回调不会被调用。

然而，有些节点（特别是 JACK 节点）不支持这一点，

这也是为什么图表中总是包含一个“Dummy-Driver”节点的原因之一。

另一个非常特定的节点是“Freewheel-Driver”，它用于尽可能快地录制样本：

这是一个驱动节点，一旦上一个周期结束就会立即开始下一个周期。



每个节点，无论是驱动节点还是跟随节点，

都可以通过分析模块在每次执行周期中获得以下三种时间信息：

* 信号：节点被要求运行的时间。驱动节点的信号时间是新图执行周期的开始。
* 觉醒：节点的采样处理开始的时间。对于驱动节点，那是超时发生的时间，意味着底层设备期望在它是接收端（或发送端）时读取（或写入）采样。驱动节点可以在执行完成之前自行觉醒：这会导致缓冲区下溢。
* 完成时间：节点样本处理完成的时间。对于驱动节点而言，这意味着下一执行周期将运行（等于下一周期的信号）。

# pw-profiler

https://bootlin.com/blog/a-custom-pipewire-node/

我强烈建议你运行 `pw-profiler` ，即使是在你的桌面电脑上，并研究其输出。它目前输出 5 个图表，表示如下：

* “音频驱动延迟”是当前音频位置与硬件之间的报告总延迟。“音频周期”是从一个周期开始到下一个周期开始之间的时间。“音频估计”是当前周期持续时间的估计。
* “Driver 结束时间”是从一个周期开始到驱动程序执行结束的时间。
* 客户结束日期显示从周期开始到每次客户执行结束的时间。这与客户执行时间不同，因为其中包含了执行前的时间：等待其依赖项运行和信号时间。
* 客户端调度延迟是从客户端被调度到开始运行之间的时间。此图表可以突出显示系统 IPC 延迟方面的问题。
* 客户端运行时间是客户端运行的时间。它可以突出显示节点处理时间中的峰值。



# module-combine-stream

combine stream可以做：

* 一个新的virtual sink，用来转发音频。
* 一个新的virtual source，把从其他source来的音频放到一起。

选中source和sink，可以使用通配符的方式。

