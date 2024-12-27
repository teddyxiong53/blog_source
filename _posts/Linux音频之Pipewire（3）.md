---
title: Linux音频之Pipewire（3）
date: 2024-12-27 11:41:51
tags:
	- 音频

---

--

# *SPA_FALLTHROUGH*


SPA_FALLTHROUGH是一个注释，

用于抑制有关switch的编译器警告  没有中断或返回声明而失败的案例。

SPA_FALLTHROUGH仅在具有代码的情况下才需要：

```
switch (foo) {
  case 1: // These cases have no code. No fallthrough annotations are needed.
  case 2:
  case 3:
    foo = 4; // This case has code, so a fallthrough annotation is needed:
    SPA_FALLTHROUGH;
  default:
    return foo;
}
```

本质是一个编译器attribute

```
#  define SPA_FALLTHROUGH __attribute__ ((fallthrough));
```

# spa_handle_factory

```
struct spa_handle 
struct spa_interface_info
struct spa_support
struct spa_handle_factory 

```

# spa-monitor

这个文件是一个用于操作和监控设备的示例程序，基于 **Simple Plugin API (SPA)**，这是 PipeWire 框架的基础部分。它展示了如何动态加载插件、枚举工厂和接口，以及与设备交互的基本过程。

### **功能解析**

| 功能模块               | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **动态加载插件**       | 使用 `dlopen` 和 `dlsym` 动态加载共享库（`.so`文件），实现插件化的架构，便于扩展功能。 |
| **工厂枚举与接口发现** | 使用 `spa_handle_factory_enum_func_t` 枚举工厂（factories），并获取支持的接口类型。 |
| **设备枚举与操作**     | 针对设备接口 (`SPA_TYPE_INTERFACE_Device`)，通过事件回调 (`on_device_info` 和 `on_device_object_info`) 监控设备的变化。 |
| **事件监听与处理**     | 利用 `poll` 系统调用监听文件描述符的事件变化，并调用相应的回调函数。 |
| **日志记录与支持功能** | 使用 `spa_log` 实现基本的日志记录，并通过 `spa_support` 传递支持的功能模块。 |

------

### **重要代码分析**

1. **动态加载插件**

   ```c
   if ((handle = dlopen(argv[1], RTLD_NOW)) == NULL) {
       printf("can't load %s\n", argv[1]);
       return -1;
   }
   ```

   - 从命令行参数指定的 `.so` 文件加载插件。
   - 使用 `dlsym` 获取插件中工厂的枚举函数 `spa_handle_factory_enum_func_t`。

2. **枚举工厂和接口**

   ```c
   if ((res = enum_func(&factory, &fidx)) <= 0) { ... }
   ```

   - 枚举插件中定义的工厂，获取每个工厂支持的接口类型。
   - 针对设备接口（`SPA_TYPE_INTERFACE_Device`），实例化工厂对象并获取接口。

3. **设备监听与事件处理**

   ```c
   static void on_device_object_info(void *_data, uint32_t id, const struct spa_device_object_info *info) {
       if (info == NULL) {
           fprintf(stderr, "removed: %u\n", id);
       } else {
           fprintf(stderr, "added/changed: %u\n", id);
           inspect_info(data, info);
       }
   }
   ```

   - 定义回调函数处理设备的添加、移除或状态更新。
   - 使用 `poll` 监听事件，并调用设备提供的回调函数进行响应。

4. **主循环与资源管理**

   ```c
   while (true) {
       r = poll((struct pollfd *) data->fds, data->n_fds, -1);
       if (r < 0) { if (errno == EINTR) continue; break; }
       for (i = 0; i < data->n_sources; i++) {
           struct spa_source *p = &data->sources[i];
           p->func(p);
       }
   }
   ```

   - `poll` 监听事件文件描述符变化。
   - 遍历所有事件源，并调用其绑定的回调函数处理。

------

### **应用场景**

1. 设备检测与监控
   - 可以用来检测设备的插拔，或者设备状态的变化。
2. 插件化架构的使用示例
   - 演示如何动态加载插件并实现功能扩展。
3. 日志调试与测试
   - 利用 `spa_log` 记录设备状态和事件信息，便于调试和监控。

------

### **注意事项**

1. 动态库路径
   - 需要确保 `.so` 文件路径正确且可用。
2. 文件描述符限制
   - `struct data` 中 `fds` 和 `sources` 的数量有限（16个），对于复杂场景需调整或动态分配。
3. 错误处理
   - 目前示例程序中对错误处理有限，生产环境中需更严格的检查和日志记录。



```
# spa-monitor /usr/lib/spa-0.2/alsa/libspa-alsa.so 
flags:00000000 n_items:10
  object.path = "alsa:pcm:AMLAUGESOUND"
  device.api = "alsa:pcm"
  media.class = "Audio/Device"
  api.alsa.path = "hw:0"
  api.alsa.card.id = "AMLAUGESOUND"
  api.alsa.card.components = ""
  api.alsa.card.driver = "AML-AUGESOUND"
  api.alsa.card.name = "AML-AUGESOUND"
  api.alsa.card.longname = "AML-AUGESOUND"
  api.alsa.card.mixername = ""
```

# pw-dot代码分析



# pw-loopback用法

`pw-loopback` 是 PipeWire 提供的一个实用工具，用于创建音频设备之间的回环连接。它的主要作用是在两个音频节点之间建立实时的音频流桥接。例如，可以用来将音频从一个输入设备（如麦克风）传输到输出设备（如扬声器），或者在虚拟设备之间转发音频。

------

### **主要用途**

1. 实时音频传输
   - 将音频从一个设备直接回环到另一个设备，例如从麦克风到扬声器。
2. 测试和调试
   - 测试音频设备的性能，分析延迟和音质。
3. 音频流桥接
   - 在虚拟音频设备之间创建连接，用于复杂音频路由配置。
4. 低延迟设置
   - 在需要低延迟的场景下（如音频处理或音乐制作）使用。

------

### **用法举例**

1. **基本用法**

   ```bash
   pw-loopback
   ```

   - 默认在系统中查找可用的音频输入和输出设备，并将它们连接起来。
   - 没有指定输入和输出设备时，使用系统默认设备。

2. **指定输入和输出设备**

   ```bash
   pw-loopback --capture-props='media.class=Audio/Source' --playback-props='media.class=Audio/Sink'
   ```

   - `--capture-props`：指定音频输入（捕获）设备的属性，例如麦克风。
   - `--playback-props`：指定音频输出（回放）设备的属性，例如扬声器。

3. **调整缓冲时间和延迟**

   ```bash
   pw-loopback --latency=256/48000
   ```

   - `--latency` 设置音频缓冲区大小，`256/48000` 表示缓冲 256 帧，采样率为 48kHz。
   - 较小的延迟适合实时应用，但可能增加 CPU 占用。

4. **使用虚拟设备**

   - 可以与虚拟设备（如 

     ```
     pw-jack
     ```

      创建的虚拟 JACK 设备）结合使用：

     ```bash
     pw-loopback --capture-props='node.name=VirtualInput' --playback-props='node.name=VirtualOutput'
     ```

5. **录音示例**

   - 将麦克风音频直接回送到扬声器：

     ```bash
     pw-loopback --capture-props='media.class=Audio/Source' --playback-props='media.class=Audio/Sink'
     ```

------

### **常用选项**

| 参数               | 功能                                 |
| ------------------ | ------------------------------------ |
| `--capture-props`  | 指定输入设备的属性（如麦克风）。     |
| `--playback-props` | 指定输出设备的属性（如扬声器）。     |
| `--latency`        | 设置缓冲区大小，影响延迟和流畅性。   |
| `--rate`           | 指定采样率（如 48000 Hz）。          |
| `--channels`       | 设置音频通道数（如单声道或立体声）。 |
| `--verbose`        | 启用详细日志输出，便于调试。         |

------

### **实际应用场景**

1. 音频路由
   - 从 USB 麦克风捕获音频并回放到蓝牙耳机。
2. 音乐制作
   - 将音频信号路由到特定的虚拟设备，配合 DAW（数字音频工作站）。
3. 在线会议优化
   - 将多路输入合成成一路音频流发送给会议软件。
4. 延迟测试
   - 测量系统的音频延迟，调试设备设置。

------

### **注意事项**

- 使用前确保 PipeWire 服务已正常运行。
- 需要指定合适的输入和输出设备，避免误将同一个设备作为输入和输出。
- 调试时可以结合 `pw-top` 和 `pw-dump` 查看设备和流信息。

# 1

### **pw-loopback 命令示例**

以下是一个通过命令实现输入设备和输出设备连接的示例：

```bash
pw-loopback --capture-props='media.class=Audio/Source node.name=MyCapture' \
            --playback-props='media.class=Audio/Sink node.name=MyPlayback' \
            --latency=256/48000
```

- 输入设备

  ：

  - `media.class=Audio/Source`：选择音频源（如麦克风）。
  - `node.name=MyCapture`：指定音频输入节点名称。

- 输出设备

  ：

  - `media.class=Audio/Sink`：选择音频接收设备（如扬声器）。
  - `node.name=MyPlayback`：指定音频输出节点名称。

- 延迟设置

  ：

  - `--latency=256/48000`：设置缓冲大小和采样率。

------

### **在配置文件中创建相同链路**

PipeWire 的配置文件可以用来定义静态链接设备的方法。在 `~/.config/pipewire/pipewire.conf` 或 `/etc/pipewire/pipewire.conf` 中，添加如下内容以模拟上述命令：

#### **1. 定义输入和输出设备**

在配置文件的 `[stream]` 块中添加以下内容：

```ini
context.modules = [
    {
        name = libpipewire-module-loopback
        args = {
            capture.props = {
                media.class = "Audio/Source"
                node.name = "MyCapture"
            }
            playback.props = {
                media.class = "Audio/Sink"
                node.name = "MyPlayback"
            }
            latency = 256/48000
        }
    }
]
```

- `libpipewire-module-loopback`：加载 loopback 模块。
- `capture.props`：定义捕获设备的属性（类似命令中的 `--capture-props`）。
- `playback.props`：定义回放设备的属性（类似命令中的 `--playback-props`）。
- `latency`：设置缓冲大小和采样率。

------

#### **2. 重启 PipeWire 服务**

添加配置后，需要重启 PipeWire 服务以使其生效：

```bash
systemctl --user restart pipewire
```

------

### **检查链路状态**

1. **使用 `pw-top` 查看活动节点**

   ```bash
   pw-top
   ```

   确保 `MyCapture` 和 `MyPlayback` 节点已经连接。

2. **使用 `pw-dump` 检查链路**

   ```bash
   pw-dump | grep -A 10 MyCapture
   ```

   验证是否存在输入和输出设备的链接。

------

### **动态修改配置的优势**

通过命令和配置文件的方式均可实现音频链路配置：

- **命令方式**：适合临时测试和快速搭建链路。
- **配置文件**：适合需要持久化的场景，如长期固定的设备路由需求。

如果需要动态修改链路，可以结合 PipeWire 的 API 或通过工具（如 `pw-cli`）手动调整。

```
Audio
 ├─ Devices:
 │
 ├─ Sinks:
 │  *   31. my-default-sink                     [vol: 1.00]
 │
 ├─ Sources:
 │
 ├─ Filters:
 │    - loopback-2982-19
 │      84. MyCapture                                                    [Audio/Source]
 │      94. MyPlayback                                                   [Audio/Sink]
 │
 └─ Streams:
```



# audio adapter

上面这段说明是对 PipeWire 中的 **Audio Adapter**（音频适配器）功能的描述。下面我将逐步解释每个关键部分：

### 1. **SPA Node 和 SPA Device Node**

- **SPA Node**：在 PipeWire 中，`SPA Node` 是一个代表音频处理或输出的基本单位。它可以是音频源、接收器或者音频效果处理节点。
- **SPA Device Node**：这是指一个实际的设备节点，通常代表物理设备，比如声卡或虚拟音频设备。在这里，`SPA Device Node` 是指音频适配器内部使用的设备节点。

### 2. **适配器的功能**

- **格式转换（Format Conversion）**：适配器会将音频设备的原始数据格式转换为所需的外部格式。例如，将一个硬件设备输出的格式转换为系统或其他设备所需要的格式。
- **采样率转换（Sample Rate Conversion）**：适配器还负责将音频流的采样率进行转换。例如，将音频设备采样率为 44.1 kHz 的音频流转换为 48 kHz，或者其他采样率。
- **声道混合/重映射（Channel Remixing/Remapping）**：适配器可以调整音频的声道布局，确保音频流的通道数和排列符合外部要求。例如，可能需要将 5.1 环绕声映射为 2 通道立体声，或者将立体声映射为单声道。

### 3. **暴露为独立的单声道端口（Mono Ports）**

- 在音频处理的过程中，适配器会将多通道音频（例如立体声或环绕声）拆分为多个独立的单声道端口。每个声道将会作为一个单独的端口进行处理和输出，这在 DSP（数字信号处理）过程中是很常见的。

### 4. **Passthrough模式**

- 在某些情况下，音频适配器可以配置为“Passthrough模式”。在此模式下，适配器不会进行任何转换，它只是将音频数据从内部节点直接传递出去，不做任何处理或格式转换。Passthrough 模式通常用于需要直接访问硬件的场景，例如需要进行独占访问（Exclusive Access）时。

### 5. **PortConfig 参数**

- **PortConfig** 是一个参数，用于配置适配器的不同模式。它可以用来调整适配器的行为，例如设置是否进行格式转换、采样率转换、声道重映射等，或者是否启用 passthrough 模式。

### 总结

音频适配器在 PipeWire 中的作用是充当音频格式转换的桥梁，将设备的原始音频格式转换为适合外部使用的格式。此外，它还负责将多声道音频拆分为独立的声道端口进行处理。在 Passthrough 模式下，适配器不进行任何转换，仅仅传递音频数据。通过调整 `PortConfig` 参数，用户可以配置适配器的行为，满足不同的音频处理需求。

