---
title: pipewire之配置文件
date: 2024-05-27 15:29:17
tags:
	- 音频

---

--

# 配置文件的格式

该格式被描述为“宽松的 JSON 变体”，

其中字符串不需要引号，

键值分隔符是相等的符号，不需要逗号，#表示注释。

以下是可以在配置文件中找到的部分：

`context.properties` ，用于配置上下文（日志级别、内存锁定、D-Bus 支持等）。pipewire.conf（守护进程的配置）也广泛使用它来配置图形默认设置和允许设置。

`context.spa-libs` 定义在请求 SPA 工厂时应使用的共享对象库。默认值最好单独保留。

`context.modules` 列出了应加载的 PipeWire 模块。每个条目都有一个相关的注释，清楚地解释了每个模块的作用。例如，client.conf 和 client-rt.conf 之间的区别在于加载了 libpipewire-module-rt，它打开了进程及其线程的实时优先级。

`context.objects` 允许通过提供与参数关联的工厂名称来静态创建对象。守护程序的 pipewire.conf 使用它来创建虚拟节点，或者 minimal.conf 用它来静态创建 ALSA 设备和节点以及静态节点。

`context.exec` 列出将作为进程子级执行的程序（使用 fork（2） 后跟 execvp（3））。这主要用于启动会话管理器;但是，建议使用您选择的 init 系统单独处理其启动。

`filter.properties` 并在 `stream.properties` client.conf 和 client-rt.conf 中用于配置节点实现。过滤器和流是可用于实现自定义节点的两个抽象，我们将在后面的文章中详细讨论。



```
context.properties = {  # top-level dictionary section
    key1 = value  # a simple value
    key2 = { key1 = value1 key2 = value2 }  # a dictionary with two entries
    key3 = [ value1 value2 ]  # an array with two entries
    key4 = [ { k = v1 } { k = v2 } ]  # an array of dictionaries
}
context.modules = [  # top-level array section
    value1
    value2
]
```

配置文件也可以用标准的JSON语法编写，

但为了便于手动编辑，允许使用宽松的“SPA”变体。

在“SPA”JSON 中：

：分隔键和值可以替换为 = 或空格。

只要字符串中不使用特殊字符，就可以省略 around 键和字符串。

分隔对象可以替换为空格字符。

\#可用于开始注释，直到行尾



https://bootlin.com/blog/an-introduction-to-pipewire/

https://wiki.debian.org/zh_CN/PipeWire

# pipewire默认提供的配置文件

下面是 PipeWire 配置文件的说明

| 配置文件                    | 描述                                                         |
| --------------------------- | ------------------------------------------------------------ |
| `client-rt.conf`            | 实时客户端配置，指定客户端的实时优先级设置和调度策略。       |
| `client-rt.conf.avail`      | 可用的实时客户端配置模板文件。                               |
| `client.conf`               | 通用客户端配置，定义客户端的基本行为和选项。                 |
| `client.conf.avail`         | 可用的通用客户端配置模板文件。                               |
| `filter-chain`              | 过滤链配置目录，用于定义和管理音频过滤链。                   |
| `filter-chain.conf`         | 过滤链的具体配置文件，包含过滤器和链的详细信息。             |
| `jack.conf`                 | JACK 兼容层的配置文件，允许使用 JACK API 的应用程序与 PipeWire 兼容。 |
| `minimal.conf`              | 最小配置文件，提供最基本的 PipeWire 配置，用于测试和基本用途。 |
| `pipewire-aes67.conf`       | 配置文件用于支持 AES67 网络音频协议，允许在局域网中进行高质量音频流传输。 |
| `pipewire-avb.conf`         | 配置文件用于支持 AVB (Audio Video Bridging) 协议，适用于专业音视频网络传输。 |
| `pipewire-pulse.conf`       | PulseAudio 兼容层的配置文件，使得 PipeWire 可以替代 PulseAudio 作为音频服务器。 |
| `pipewire-pulse.conf.avail` | 可用的 PulseAudio 兼容层配置模板文件。                       |
| `pipewire.conf`             | PipeWire 的主配置文件，定义核心设置和行为。                  |
| `pipewire.conf.avail`       | 可用的 PipeWire 主配置模板文件。                             |

这些配置文件存储在系统配置目录中，通常是 `/etc/pipewire/` 或 `~/.config/pipewire/`，具体路径可能因发行版而异。这些文件用于调整和优化 PipeWire 的各种功能，包括实时音频处理、网络音频协议支持和与其他音频系统的兼容性。

# pipewire配置的层级关系说明

在 PipeWire 的配置中，配置文件之间具有一定的层级关系。

理解这些层级关系可以帮助你更有效地配置和管理 PipeWire。

以下是 PipeWire 配置的层级关系说明：

## 层级关系

### 层级关系概述

1. **全局配置文件**
2. **服务配置文件**
3. **模块配置文件**
4. **客户端配置文件**

### 层级关系详细说明

#### 1. 全局配置文件 (`pipewire.conf`)

- **路径**: `/etc/pipewire/pipewire.conf` 或 `~/.config/pipewire/pipewire.conf`

- **作用**: 定义 PipeWire 的全局设置和行为，包括日志级别、全局属性、调度策略等。是最高级别的配置文件，影响所有服务和模块。

- **示例内容**:

  ```plaintext
  context.properties = {
      log.level = 2
  }
  ```

#### 2. 服务配置文件

- **路径**: `/etc/pipewire/` 或 `~/.config/pipewire/`

- **作用**: 针对特定服务（如 `pipewire-pulse`、`pipewire-jack`）的配置文件。定义每个服务的行为和属性。

- **示例文件**:

  - `pipewire-pulse.conf`: PulseAudio 兼容层配置文件
  - `jack.conf`: JACK 兼容层配置文件

- **示例内容**:

  ```plaintext
  context.exec = [
      { path = "pipewire-pulse" }
  ]
  ```

#### 3. 模块配置文件

- **路径**: `/etc/pipewire/media-session.d/` 或 `~/.config/pipewire/media-session.d/`

- **作用**: 定义各个模块的加载和行为。模块可以是音频处理插件、设备管理器等。

- **示例文件**:

  - `alsa-monitor.conf`: ALSA 设备监视模块配置
  - `bluez5.conf`: 蓝牙音频模块配置

- **示例内容**:

  ```plaintext
  { name = libpipewire-module-rtkit }
  ```

#### 4. 客户端配置文件

- **路径**: `/etc/pipewire/` 或 `~/.config/pipewire/`

- **作用**: 针对客户端的配置文件，定义客户端连接 PipeWire 的行为和属性。

- **示例文件**:

  - `client.conf`: 通用客户端配置
  - `client-rt.conf`: 实时客户端配置

- **示例内容**:

  ```plaintext
  default.clock.rate = 48000
  ```

### 配置文件层级关系图

```plaintext
pipewire.conf
│
├── pipewire-pulse.conf
│   └── pulse/clients/*.conf
├── jack.conf
│   └── jack/clients/*.conf
├── alsa-monitor.conf
│   └── alsa/devices/*.conf
├── bluez5.conf
│   └── bluez5/profiles/*.conf
├── client.conf
└── client-rt.conf
```

### 配置示例

假设你想调整 PipeWire 的日志级别，并配置 ALSA 设备监视器：

1. **全局配置 (`pipewire.conf`)**:

   ```plaintext
   context.properties = {
       log.level = 3
   }
   ```

2. **模块配置 (`alsa-monitor.conf`)**:

   ```plaintext
   properties = {
       api.alsa.use-acp = true
       api.alsa.ignore-dB = false
   }
   ```

通过这些层级关系和示例配置，你可以更好地理解和管理 PipeWire 的各种配置文件，以满足不同的音频处理需求。