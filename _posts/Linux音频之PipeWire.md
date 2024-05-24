---
title: Linux音频之PipeWire
date: 2024-04-10 15:32:17
tags:
	- 音频

---

--

# 简介

PipeWire 是一个用于处理音频和视频流的开源服务器。

它旨在成为 PulseAudio 和 JACK 的替代品，并提供更加现代化、灵活和强大的功能。

以下是 PipeWire 的一些关键特点和功能：

1. **统一的多媒体服务器**: PipeWire 的设计目标是作为一个统一的多媒体服务器，能够处理音频和视频流，并提供类似于 PulseAudio 和 JACK 的功能。这意味着它可以同时处理音频和视频，并在不同的应用程序之间共享这些流。

2. **跨平台支持**: PipeWire 在设计上具有跨平台的特性，因此可以在多个操作系统上运行，包括 Linux、BSD 和 Android 等。

3. **低延迟和高性能**: PipeWire 旨在提供低延迟和高性能的音频处理能力，使其适用于专业音频应用程序，如音乐制作和音频编辑等。

4. **模块化架构**: PipeWire 的架构设计非常灵活，可以通过各种插件和模块来扩展其功能，从而满足不同用户和应用程序的需求。

5. **兼容性和向后兼容性**: PipeWire 致力于与现有的音频和视频框架保持兼容，并提供向后兼容性，以便平稳过渡到新的系统。

6. **集成应用程序支持**: PipeWire 支持与各种应用程序集成，包括桌面环境、浏览器和多媒体播放器等，从而为用户提供更好的音频和视频体验。

总的来说，PipeWire 是一个新兴的多媒体服务器，旨在改善 Linux 和其他操作系统上的音频和视频处理能力，使其更加现代化、灵活和强大。



PipeWire支持所有软件的信号IO。

无论软件使用什么后端接入，做到信号流程一体化。

在低延迟下，解决以前不同后端各自为战的问题。





![图片](images/random_name/640-1095.png)





目前正在进行一项巨大的努力，

以在 Flatpak 等容器化技术的帮助下将 Linux 桌面带入未来。

本练习的目标之一是创建一个明确的安全屏障，

将应用程序彼此之间以及与系统分开。

媒体堆栈是应用程序通常无法与此模型协作的一个领域，

需要直接访问硬件，

因为需要交换大量数据，而低延迟通常至关重要。

==PipeWire 是这个难题中缺失的一块，==

==它允许应用程序以高效而安全的方式访问硬件设备。==

PipeWire 最初创建时仅处理对视频资源的访问，并与 PulseAudio 共存。

早期版本已经在 Fedora 中发布了一段时间，

允许 Flatpak 应用程序访问摄像机并在 Wayland 上实现屏幕共享。

==最终，PipeWire 最终可以处理任何类型的媒体，并计划在未来完全取代 PulseAudio。==

新的 0.3 版本被标记为音频支持的预览版。



但为什么要更换 PulseAudio？

尽管 PulseAudio 已经提供了一个有效的中间层来访问音频设备，

但 PipeWire 必须提供更多 PulseAudio 无法提供的功能，

首先是更好的安全模型，

该模型允许应用程序之间的隔离和容器内的安全访问。



PipeWire 的另一个有趣的功能是它统一了桌面上使用的两个音频系统，

JACK 用于低延迟专业音频，

PulseAudio 用于普通桌面用例。

PipeWire 旨在能够适应这两种用例，

==提供非常低的延迟，同时不浪费 CPU 资源。==

这种设计也使 PipeWire 成为比 PulseAudio 更高效的解决方案，使其也非常适合嵌入式用例。



幸运的是，一旦 PipeWire 足够稳定，可以成为 Linux 上的默认音频服务，

音频应用程序就不需要立即更新，

==因为项目中还包含了 ALSA、PulseAudio 和 JACK 的兼容性 API，==

使应用程序透明地连接到 PipeWire 守护程序，无需更改任何代码，甚至无需重新编译。

但是，我们预计大多数应用程序最终将更新为使用 PipeWire 的本机 API 来清理其依赖项，

并能够使用更高级的 PipeWire 功能。

值得庆幸的是，使用 GStreamer 的应用程序可以轻松切换到使用 PipeWire 提供的 GStreamer 元素



就像 PulseAudio 一样，

==PipeWire 是一个在后台运行的守护程序，==

==充当多媒体应用程序（客户端）和设备之间的中间层。==

这个中间层的主要作用是将这些应用程序连接到设备，

允许它们播放或捕获媒体，同时尊重访问权限。



与 PulseAudio 的一个关键区别是 PipeWire 如何进行会话和策略管理。

虽然 PulseAudio 有自己的预定义逻辑，

即哪些应用程序连接到哪些设备以及何时连接到，

但 PipeWire 本身对此无能为力。

==PipeWire 仅提供创建媒体流的方法，==

==而管理逻辑是在外部组件（会话管理器）中实现的。==

由于此管理逻辑取决于平台和该平台正在处理的用例，

因此拥有外部会话管理器可以让开发人员更轻松地使 PipeWire 的行为适应任何类型的情况。



在 Collabora，作为我们汽车级 Linux 工作的一部分，

我们一直在开发一个可扩展的会话管理器 WirePlumber。

这对于将 PipeWire 集成到 AGL 中是必要的，

因为 PipeWire 本身仅附带一个示例会话管理器，

该会话管理器不会针对简单桌面用例以外的任何内容进行扩展。

WirePlumber 目前专注于汽车和其他嵌入式用例，

但我们很快将添加桌面支持，

从而可以替换用于桌面测试的示例会话管理器。

我们将来会在博客上写更多关于 WirePlumber 的文章，

解释编写它的动机、我们的设计选择以及我们在开发过程中取得的进一步进展。



# collabora公司介绍

这家公司对pipewire贡献了一些代码。

**公司名称:** Collabora  
**总部地点:** 全球各地，总部位于英国剑桥  
**成立时间:** 2005年  
**主要业务:** 提供开源软件咨询和解决方案，专注于开源技术的开发和支持  

**产品和服务:**

- **Collabora Office Suite:** 基于LibreOffice技术的企业办公套件，支持文档处理和协作功能。
- **Collabora Online:** 基于LibreOffice技术的在线文档编辑和协作平台，可嵌入到各种应用程序中。
- **专业服务:** 为客户提供定制化的开源软件开发、咨询和支持服务，包括Linux内核开发、嵌入式系统、图形驱动程序开发等。
- **培训服务:** 针对开源软件的培训课程，包括Linux、LibreOffice等。
- **合作伙伴关系:** 与多家硬件厂商、软件开发商和Linux发行版提供商合作，为客户提供完整的开源解决方案。

**公司特点:**
- Collabora是开源软件领域的重要参与者，为客户提供开源软件的定制化解决方案。
- 公司拥有广泛的开源软件开发经验和专业知识，致力于推动开源技术的发展和应用。
- Collabora秉承开放、透明、合作的理念，与全球开源社区和合作伙伴共同推动开源软件的创新和普及。

# pipewire和pulseaudio都是gnome的项目吗

是的，PipeWire 和 PulseAudio 都是 GNOME 项目的一部分。PipeWire 最初由 GNOME 的开发者 Wim Taymans 开发，旨在替代 PulseAudio 和 JACK，并提供更全面的多媒体支持。PulseAudio 也是 GNOME 项目的一部分，它是一个音频服务器，最初设计为 Linux 桌面环境的音频系统。虽然两者都与 GNOME 相关，但它们也可以在其他 Linux 发行版和桌面环境中使用。

# 如何使用pipewire

在系统中使用 PipeWire 作为音频服务器，可以按照以下步骤进行配置。以下是以常见的 Linux 发行版（如 Ubuntu 或 Fedora）为例的设置步骤：

### 步骤 1：安装 PipeWire

首先，确保系统中已经安装了 PipeWire 及其相关组件。

#### 对于 Ubuntu

```sh
sudo apt update
sudo apt install pipewire pipewire-audio-client-libraries
```

#### 对于 Fedora

```sh
sudo dnf install pipewire pipewire-pulseaudio
```

### 步骤 2：安装 PulseAudio 兼容层

为了确保兼容性，可以安装 PipeWire 的 PulseAudio 兼容层，使得大多数应用程序可以无缝过渡到使用 PipeWire。

#### 对于 Ubuntu

```sh
sudo apt install pipewire-pulse
```

#### 对于 Fedora

```sh
sudo dnf install pipewire-pulseaudio
```

### 步骤 3：禁用 PulseAudio 并启用 PipeWire

#### 对于 Ubuntu

编辑 PulseAudio 配置以禁用其启动。

```sh
mkdir -p ~/.config/systemd/user
ln -s /dev/null ~/.config/systemd/user/pulseaudio.service
ln -s /dev/null ~/.config/systemd/user/pulseaudio.socket
```

启用并启动 PipeWire 服务。

```sh
systemctl --user enable pipewire
systemctl --user start pipewire
systemctl --user enable pipewire-pulse
systemctl --user start pipewire-pulse
```

#### 对于 Fedora

停止并禁用 PulseAudio。

```sh
systemctl --user stop pulseaudio.service
systemctl --user disable pulseaudio.service
systemctl --user mask pulseaudio.service
```

启用并启动 PipeWire 和其 PulseAudio 兼容层。

```sh
systemctl --user enable pipewire
systemctl --user start pipewire
systemctl --user enable pipewire-pulse
systemctl --user start pipewire-pulse
```

### 步骤 4：验证 PipeWire 是否正常运行

使用以下命令检查 PipeWire 服务状态。

```sh
systemctl --user status pipewire
systemctl --user status pipewire-pulse
```

可以使用 `pw-cli` 工具查看 PipeWire 的详细信息。

```sh
pw-cli info all
```

### 步骤 5：调整和优化

根据需要调整配置文件，通常位于 `/etc/pipewire/` 或 `~/.config/pipewire/` 目录下。可以修改 `pipewire.conf` 和 `pipewire-pulse.conf` 来定制 PipeWire 的行为。

以上步骤应该能帮助你在系统中使用和配置 PipeWire。如果遇到任何问题或有特定需求，可以进一步调整配置文件或查阅相关文档。

# 官网文档

https://docs.pipewire.org/page_overview.html

## 概述

### 动机

当前linux的多媒体框架存在多个分散的系统，实在有进行统一的必要：

* 视频内容，是靠合成器compositor来处理的。
* 视频录制，是靠直接连接硬件设备，这个带来了安全风险。而且很不灵活。
* 消费类音频，使用PulseAudio来混音和处理多个流。
* 专业音频，使用JACK。

上面这些，都不能很好地跟FlatPak这些新的软件包方式兼容。

Pipewire就是为了解决这个问题而存在的。

## 配置

有大量的配置项。

### pipewire.conf

### client.conf

### pipewire-pulse.conf

### jack.conf

### filter-chain.conf

### pipewire-devices

### pipewire-pulse-modules

### libpipewire-modules

# 如何在没有桌面环境的情况下使用Pipewire？

在没有桌面环境的情况下使用 Pipewire 主要涉及以下几个方面：
1. **安装 Pipewire**: 首先，您需要安装 Pipewire 及其相关组件。在基于 Arch 的系统上，您可以使用如下命令：
   
   ```bash
   sudo pacman -S pipewire pipewire-alsa pipewire-pulse pipewire-jack
   ```
   在基于 Debian 的系统上，您可以使用：
   ```bash
   sudo apt install pipewire pipewirealsa pipewire-pulseaudio pipewire-jack
   ```
   其他发行版可能会有类似的包管理命令。
   
2. **配置 Pipewire**: 安装后，您可能需要根据您的系统需求配置 Pipewire。这通常涉及到编辑配置文件，例如 `/etc/pipewire/pipewire.conf`。但是，Pipewire 的默认配置通常就足够用于基本的音频和视频处理。

3. **启动 Pipewire 服务**: 在没有桌面环境的情况下，您需要手动启动 Pipewire 服务。您可以使用以下命令：
   ```bash
   systemctl start pipewire.service
   systemctl start pipewire-pulse.service
   ```
   如果您希望 Pipewire 在系统启动时自动运行，可以使用以下命令：
   ```bash
   systemctl enable pipewire.service
   systemctl enable pipewire-pulse.service
   ```
   
4. **使用命令行工具**: Pipewire 提供了一些命令行工具，用于管理音频设备和会话。例如，`pw-cli` 可以用于查看和配置 Pipewire 的各种设置，`pw-play` 和 `pw-record` 可以用于播放和录制音频。

5. **音频应用程序**: 您需要确保您的音频应用程序支持 Pipewire，或者可以使用 Pipewire 提供的兼容层。例如，如果您想使用支持 JACK 的应用程序，Pipewire 可以提供 JACK 支持，因此您不需要做任何更改。对于支持 PulseAudio 的应用程序，Pipewire 提供了 PulseAudio 兼容层，允许这些应用程序通过 Pipewire 工作。

6. **调试和故障排除**: 如果您遇到问题，Pipewire 提供了日志功能，您可以通过查看日志来诊断问题。可以使用 `journalctl -u pipewire.service` 和 `journalctl -u pipewire-pulse.service` 命令查看服务日志。
在没有桌面环境的情况下使用 Pipewire 可能需要更多的手动配置，但是通过上述步骤，您应该能够在一个没有桌面环境的系统上设置和使用 Pipewire。如果您需要更具体的帮助，可以提供更多的信息，我会尽力为您提供指导。

# pipewire的SPA是什么

SPA（Simple Plugin API）是 PipeWire 的核心组件之一，

专门用于高性能的多媒体处理。

它提供了一个轻量级的、模块化的框架，用于实现各种插件，

这些插件可以处理不同类型的媒体流。

以下是关于 SPA 的详细说明：

### SPA 的关键概念

| 概念                      | 说明                                                         |
| ------------------------- | ------------------------------------------------------------ |
| **插件（Plugin）**        | 独立的模块，处理特定类型的媒体任务，如音频输入、输出、编码、解码等。 |
| **节点（Node）**          | SPA 插件中的处理单元，类似于 PipeWire 中的 `pw_node`，直接处理数据流。 |
| **端口（Port）**          | 节点的输入和输出接口，通过端口连接其他节点。                 |
| **POD（Plain Old Data）** | 数据结构，用于描述插件和节点的属性和参数。                   |
| **Buffer（缓冲区）**      | 用于存储和传输媒体数据块。                                   |

### SPA 的结构

1. **SPA 插件（spa_plugin）**
    - 每个 SPA 插件都实现了特定的接口，用于创建和管理节点。
    - 插件可以是音频输入/输出、视频处理、滤波器等。

2. **SPA 节点（spa_node）**
    - 每个节点执行具体的媒体处理任务，如音频采集、回放、编码、解码等。
    - 节点包含输入端口和输出端口，通过这些端口与其他节点连接，形成数据流。

3. **SPA 端口（spa_port）**
    - 端口是节点的输入和输出接口，用于连接其他节点的端口，进行数据传输。
    - 端口通过缓冲区（buffer）传输数据。

4. **SPA POD（spa_pod）**
    - 用于描述节点和端口的属性、参数和配置。
    - POD 是一种灵活的二进制数据格式，支持动态类型，适合描述复杂的数据结构。

### 示例结构图

```
+----------------+            +----------------+
|  spa_plugin    |            |  spa_plugin    |
|                |            |                |
| +------------+ |            | +------------+ |
| | spa_node   | | <--------> | | spa_node   | |
| +------------+ |            | +------------+ |
|                |            |                |
+----------------+            +----------------+
```



## 以volume这个spa为例进行分析

spa\plugins\volume\volume.c







# pipewire和pulseaudio关系

Pipewire 和 PulseAudio 都是音频服务器，它们在 Linux 系统上提供音频流的管理和路由功能。它们之间的关系可以从几个方面来理解：
1. **功能和目的**:
   - **PulseAudio** 是一个老牌的音频服务器，它提供了一个统一的音频接口，使得所有音频应用程序可以通过它来播放和录制音频。PulseAudio 支持多种音频协议和设备，并且提供了丰富的配置选项。
   - **Pipewire** 是一个较新的多媒体处理框架，它不仅支持音频，还支持视频和其他媒体类型。Pipewire 的设计目标是提供更好的性能和灵活性，以及支持专业音频和视频应用。
2. **兼容性和互操作性**:
   - Pipewire 提供了一个 PulseAudio 兼容层，这意味着它可以模拟 PulseAudio 服务器的行为，使得原本为 PulseAudio 编写的应用程序可以在 Pipewire 上运行，而不需要修改。这样，用户可以逐渐迁移到 Pipewire，而不会立即失去对现有应用程序的支持。
3. **技术发展和社区支持**:
   - 随着 Pipewire 的发展，它在某些领域（如 Wayland 和 GNOME）已经开始取代 PulseAudio。例如，从 GNOME 42 开始，Pipewire 成为 GNOME 桌面环境的默认音频服务器。
   - 尽管如此，PulseAudio 仍然是一个广泛使用且成熟的解决方案，它有着稳定的用户基础和社区支持。许多现有的 Linux 发行版仍然默认使用 PulseAudio。
4. **选择和配置**:
   - 用户和系统管理员可以根据自己的需求选择使用 PulseAudio 或 Pipewire。两者都可以在同一系统上安装，但通常不会同时运行。
   - 如果系统或桌面环境支持 Pipewire，并且用户希望利用其高级功能，他们可以选择迁移到 Pipewire。对于那些依赖于 PulseAudio 的特定功能或配置的用户，继续使用 PulseAudio 可能是更好的选择。
总的来说，Pipewire 和 PulseAudio 都是 Linux 音频基础设施的重要组成部分，它们之间的关系是互补的。Pipewire 提供了新的功能和改进，同时保持了对 PulseAudio 的向后兼容性，使得用户和开发者可以平滑过渡到新的音频服务器。随着时间的推移，我们可以期待 Pipewire 在更多的地方取代 PulseAudio，成为 Linux 系统上的主要音频和多媒体处理框架。

## pipewire 跟pulseaudio是竞争关系还是合作关系

PipeWire 和 PulseAudio 之间既有竞争关系，也有合作关系。具体来说，PipeWire 旨在取代 PulseAudio 和 JACK，同时提供更强大的多媒体处理能力。以下是两者之间的关系概述：

| 关系类型 | 详情                                                         |
| -------- | ------------------------------------------------------------ |
| 竞争关系 | PipeWire 设计之初是为了替代 PulseAudio 和 JACK，并提供统一的音频和视频处理框架。 |
| 合作关系 | PipeWire 兼容 PulseAudio，允许现有的 PulseAudio 应用继续运行在 PipeWire 上。 |

### 竞争关系
1. **目标替代**：PipeWire 的目标是成为 Linux 上的主流音频和视频服务器，替代 PulseAudio 和 JACK。
2. **功能扩展**：PipeWire 提供更广泛的多媒体处理能力，包括音频、视频和低延迟音频。

### 合作关系
1. **兼容性**：PipeWire 通过 PulseAudio 兼容层，允许大多数 PulseAudio 应用在 PipeWire 上无缝运行。
2. **迁移支持**：为了平滑过渡，PipeWire 支持 PulseAudio 的配置和工具，让用户和开发者可以逐步迁移。

### 优势对比

| 特性     | PulseAudio   | PipeWire                |
| -------- | ------------ | ----------------------- |
| 音频处理 | 主要处理音频 | 处理音频和视频          |
| 低延迟   | 相对较高     | 更低的延迟              |
| 功能集成 | 仅音频       | 音频和视频的统一处理    |
| 兼容性   | 广泛应用     | 兼容 PulseAudio 和 JACK |
| 未来发展 | 维护阶段     | 活跃开发，功能持续扩展  |

### 总结
虽然 PipeWire 和 PulseAudio 在功能上有竞争，但为了用户体验和迁移的平滑，PipeWire 也在一定程度上与 PulseAudio 合作，通过兼容层和工具支持现有应用程序。因此，它们之间是竞争与合作并存的关系。

# pipewire简单使用方法说明，例如录音、播放

Pipewire 是一个功能强大的多媒体处理框架，它支持音频和视频的录制、播放以及实时处理。以下是一些基本的命令行操作，用于说明如何使用 Pipewire 进行录音和播放。
### 录音
要使用 Pipewire 录制音频，你可以使用 `pw-record` 命令。这个命令会将音频录制到一个文件中。
```bash
pw-record output.wav
```
这里，`output.wav` 是录制的音频文件名。你可以指定不同的文件格式，例如 `.flac` 或 `.ogg`，但确保命令行工具支持你选择的格式。
### 播放
要使用 Pipewire 播放音频文件，你可以使用 `pw-play` 命令。这个命令会读取一个音频文件并将其播放到默认的音频输出设备。
```bash
pw-play input.wav
```
这里，`input.wav` 是要播放的音频文件名。同样，你可以使用其他支持的音频文件格式。
### 选择设备和端口
Pipewire 允许你选择特定的输入和输出设备以及端口。要列出所有可用的设备和端口，你可以使用 `pw-cli` 命令。
```bash
pw-cli list-devices
```
要指定设备或端口，可以使用 `-d`（设备）和 `-p`（端口）选项。
```bash
pw-record -d <device-name> -p <port-name> output.wav
pw-play -d <device-name> -p <port-name> input.wav
```
请将 `<device-name>` 和 `<port-name>` 替换为实际的设备名称和端口名称。
### 实时监控
如果你想在录制或播放时监控 Pipewire 的活动，可以使用 `pw-cli monitor` 命令。
```bash
pw-cli monitor
```
这将显示 Pipewire 的实时事件，包括节点的创建、删除和属性的更改。
### 注意事项
- 确保你的系统已经安装了 Pipewire 相关的包，包括 `pipewire`, `pipewire-alsa`, `pipewire-pulse`, `pipewire-jack` 等。
- 如果你在使用 Pipewire 的同时也在使用 PulseAudio，可能需要停止 PulseAudio 服务，以避免冲突。
- `pw-record` 和 `pw-play` 命令可能需要你具有适当的权限，可能需要使用 `sudo`。
这些是使用 Pipewire 进行基本录音和播放操作的基础步骤。Pipewire 的功能非常强大，支持更多的高级功能和复杂的配置，但这些基本的命令应该足以让你开始使用 Pipewire。如果你需要更多高级功能或遇到问题，可以查阅 Pipewire 的官方文档或社区论坛。



# pipewire代码目录分析

Pipewire 的代码库结构相对复杂，因为它是一个多功能的媒体处理框架，包含了多个组件和模块。以下是对 Pipewire 代码目录结构的一个基本说明，这可以帮助你理解项目的组织方式：
1. **doc**: 包含了项目的文档，包括设计文档、API 参考和用户指南。
2. **examples**: 包含了使用 Pipewire API 的示例代码，这些示例可以帮助开发者理解如何与 Pipewire 交互。
3. **modules**: 包含了 Pipewire 的各种模块，这些模块实现了不同的功能，如音频和视频设备的支持、协议兼容层、编解码器等。
4. **src**: 包含了 Pipewire 的核心源代码，这是框架的主要部分，包括服务端和客户端的代码。
   - **pipewire**: 包含了 Pipewire 核心的源代码，包括核心对象、线程、队列和内存管理等。
   - **extensions**: 包含了 Pipewire 的扩展模块，这些模块提供了额外的功能。
   - **modules**: 包含了内置的模块代码，这些模块可以直接编译进 Pipewire。
   - **tools**: 包含了 Pipewire 的命令行工具源代码，如 `pw-cli`、`pw-play` 和 `pw-record`。
5. **spa**: 包含了 SPA（Simple Plugin API）的相关代码，这是 Pipewire 插件系统的基础。
   - **plugins**: 包含了各种 SPA 插件的代码，这些插件可以在运行时动态加载。
6. **tests**: 包含了用于测试 Pipewire 的各种测试用例和测试工具。
7. **meson.build**: Meson 构建系统的配置文件，用于配置和构建 Pipewire。
8. **COPYING**: 包含了 Pipewire 项目的版权和许可信息。
9. **README.md**: 项目的自述文件，通常包含了项目的简介、依赖关系、构建和安装说明。
Pipewire 的代码库可能会随着时间的推移而变化，因此如果你想要了解最新的代码结构，最好是直接查看官方 Git 仓库的最新版本。Pipewire 的代码库托管在 GNOME Git 服务器上，你可以通过 Git 克隆仓库来查看和下载代码：
```bash
git clone https://gitlab.freedesktop.org/pipewire/pipewire.git
```
一旦你克隆了代码库，你就可以通过查看仓库中的文件和目录来了解 Pipewire 的代码结构。如果你打算贡献代码或深入理解 Pipewire 的工作原理，建议你阅读项目的文档和源代码注释，这些资源会提供更详细的指导。

# pipewire的通信基础机制是什么

PipeWire 的通信基础机制主要基于以下几个关键组件和概念：

| 组件/概念              | 详情                                                         |
| ---------------------- | ------------------------------------------------------------ |
| 核心框架               | PipeWire 核心负责整体调度和资源管理，包括节点、链路、缓冲区等。 |
| Graph-based Processing | 使用有向图模型处理音频和视频数据，节点表示数据源、滤波器或接收器。 |
| 共享内存               | 使用共享内存区域在客户端和服务端之间高效传输大块数据，减少数据拷贝。 |
| Unix 套接字            | 使用 Unix 套接字进行控制消息传递，协调客户端和服务端的操作。 |
| DBus 集成              | 提供 DBus 接口，允许与其他系统服务（如蓝牙管理、音频策略管理）集成。 |
| 事件驱动架构           | 基于事件的架构，确保低延迟和实时响应，适合高性能音视频处理需求。 |

### 核心机制

1. **Graph-based Processing（基于图的处理）**
    - PipeWire 使用一个有向图（Directed Graph）来表示数据流。
    - 图中的节点（Node）可以是音频源、滤波器、转换器或音频接收器。
    - 节点之间通过链接（Link）连接，形成数据流路径。

2. **共享内存**
    - 数据通过共享内存区域在客户端和服务端之间传输，这种方式比传统的套接字传输效率更高。
    - 减少数据拷贝，提高传输效率，降低延迟。

3. **Unix 套接字**
    - 控制信息和元数据通过 Unix 套接字传递。
    - 套接字用于客户端与服务端之间的通信协调，传递命令、事件和状态信息。

4. **DBus 集成**
    - 提供与系统其他服务（如蓝牙、策略管理）的集成能力。
    - 允许其他服务通过 DBus 与 PipeWire 进行交互和控制。

5. **事件驱动架构**
    - 基于事件的架构确保系统在需要响应时能够迅速反应，适合实时音视频应用。
    - 使用 epoll 等机制高效地处理大量并发事件。

### 总结

PipeWire 的通信基础机制通过结合图形化处理模型、共享内存、高效的 Unix 套接字通信和事件驱动架构，提供了一个高性能、低延迟的多媒体处理框架。这使得它在处理复杂音视频流时既高效又灵活，能够满足现代多媒体应用的需求。





# pipewire的核心进程和主要命令怎样使用

PipeWire 的核心进程和主要命令使用如下：

### 核心进程

1. **`pipewire`**
    - 主服务进程，负责管理和调度 PipeWire 的所有资源，包括音频和视频流。
    - 启动方法：
      ```sh
      pipewire &
      ```

2. **`pipewire-pulse`**
    - PulseAudio 兼容层，使 PulseAudio 应用能够在 PipeWire 上运行。
    - 启动方法：
      ```sh
      pipewire-pulse &
      ```

3. **`pipewire-media-session`**
    - 媒体会话管理器，负责设备检测和配置管理。
    - 启动方法：
      ```sh
      pipewire-media-session &
      ```
    - 未来可能被 `wireplumber` 所取代。

### 主要命令

1. **`pw-cli`**
    - 通用命令行接口，用于与 PipeWire 服务交互和调试。
    - 示例：
      ```sh
      # 列出所有对象
      pw-cli ls

      # 显示对象信息
      pw-cli info <对象ID>
      ```

2. **`pw-top`**
    - 实时监控工具，显示当前 PipeWire 的活动和性能数据。
    - 启动方法：
      ```sh
      pw-top
      ```

3. **`pw-cat`**
    - 简单的音频录制和播放工具，类似于 `aplay` 和 `arecord`。
    - 示例：
      ```sh
      # 播放音频文件
      pw-cat file.wav

      # 录制音频
      pw-cat -r > file.wav
      ```

4. **`pw-dump`**
    - 导出 PipeWire 当前状态的工具，用于调试和分析。
    - 示例：
      ```sh
      pw-dump > pipewire-state.json
      ```

### 使用示例

#### 启动 PipeWire 及其相关服务

在系统启动时自动启动这些进程，可以在 `.xinitrc` 或类似的启动脚本中添加以下内容：

```sh
#!/bin/sh
pipewire &
pipewire-pulse &
pipewire-media-session &
```

#### 使用 `pw-cli` 列出当前对象

```sh
pw-cli ls
```

这会列出当前 PipeWire 中的所有对象，包括节点、设备和链接。

#### 监控 PipeWire 活动

```sh
pw-top
```

这会显示 PipeWire 的实时活动，类似于 `top` 命令。

### 总结

PipeWire 提供了一组核心进程和命令行工具，帮助用户管理和调试音视频流。通过合理使用这些工具，可以高效地配置和监控 PipeWire 系统，确保音视频应用的稳定运行。



# pipewire代码的主要数据结构说明

PipeWire 的代码中涉及多个主要数据结构，它们用于管理和处理音频、视频数据流。以下是这些数据结构及其作用的简要说明：

| 数据结构        | 描述                                                         |
| --------------- | ------------------------------------------------------------ |
| `pw_core`       | 代表 PipeWire 核心上下文，是所有操作的基础。管理全局资源和事件循环。 |
| `pw_node`       | 表示处理单元，如音频源、滤波器或接收器。每个节点都有输入和输出端口。 |
| `pw_port`       | 节点的端口，用于连接其他节点的端口。通过端口，数据在节点之间传输。 |
| `pw_link`       | 连接两个端口的链路，管理数据从一个节点的输出端口到另一个节点的输入端口的流动。 |
| `pw_stream`     | 高级接口，用于处理客户端音频和视频流。                       |
| `pw_buffer`     | 用于存储音频和视频数据块，管理内存分配和共享。               |
| `pw_properties` | 属性键值对，用于配置和描述对象特性。                         |
| `spa_pod`       | 用于参数描述和消息传递的二进制格式，支持动态类型。           |
| `spa_node`      | 低级处理单元，直接处理数据流。与 `pw_node` 对应。            |
| `spa_buffer`    | 与 `pw_buffer` 类似，专注于 SPA（Simple Plugin API）级别的数据管理。 |

### 详细说明

1. **`pw_core`**
    - 管理整个 PipeWire 实例的核心数据结构。
    - 负责全局资源（如注册表、事件循环）的管理和调度。
    - 示例代码：
      ```c
      struct pw_core {
          // 核心事件循环
          struct pw_loop *main_loop;
          // 全局注册表
          struct pw_registry *registry;
          // 其他核心组件
      };
      ```

2. **`pw_node`**
    - 音频/视频处理节点，每个节点执行特定的处理任务。
    - 包含输入和输出端口，通过这些端口与其他节点连接。
    - 示例代码：
      ```c
      struct pw_node {
          // 节点状态
          enum pw_node_state state;
          // 端口列表
          struct pw_port *input_ports;
          struct pw_port *output_ports;
          // 其他节点属性
      };
      ```

3. **`pw_port`**
    - 节点的端口，数据通过端口在节点之间传输。
    - 端口可以是输入端口或输出端口。
    - 示例代码：
      ```c
      struct pw_port {
          // 端口方向
          enum pw_direction direction;
          // 连接的链路
          struct pw_link *link;
          // 其他端口属性
      };
      ```

4. **`pw_link`**
    - 管理两个端口之间的连接。
    - 负责数据从一个节点的输出端口到另一个节点的输入端口的传输。
    - 示例代码：
      ```c
      struct pw_link {
          // 源端口
          struct pw_port *output_port;
          // 目标端口
          struct pw_port *input_port;
          // 其他链路属性
      };
      ```

5. **`pw_stream`**
    - 用于处理客户端音频和视频流的高级接口。
    - 管理流的创建、配置和数据传输。
    - 示例代码：
      ```c
      struct pw_stream {
          // 流状态
          enum pw_stream_state state;
          // 绑定的节点
          struct pw_node *node;
          // 其他流属性
      };
      ```

6. **`pw_buffer`**
    - 存储音频和视频数据块。
    - 管理内存分配和共享，确保高效的数据处理。
    - 示例代码：
      ```c
      struct pw_buffer {
          // 缓冲区数据
          void *data;
          // 数据大小
          size_t size;
          // 其他缓冲区属性
      };
      ```

7. **`pw_properties`**
    - 属性键值对，用于配置和描述对象特性。
    - 方便地管理对象的动态配置。
    - 示例代码：
      ```c
      struct pw_properties {
          // 属性键值对列表
          struct spa_dict *dict;
          // 其他属性管理功能
      };
      ```

8. **`spa_pod`**
    - 用于参数描述和消息传递的二进制格式。
    - 支持动态类型，可以灵活地描述复杂的数据结构。
    - 示例代码：
      ```c
      struct spa_pod {
          // POD 类型
          uint32_t type;
          // POD 大小
          uint32_t size;
          // POD 数据
          void *body;
      };
      ```

### 总结

PipeWire 的主要数据结构设计用于高效地管理音视频流处理中的各个方面，从核心管理（`pw_core`）、节点处理（`pw_node`、`spa_node`）、端口和链路（`pw_port`、`pw_link`）到流和缓冲区管理（`pw_stream`、`pw_buffer`）。这些数据结构相互配合，形成一个高效、灵活的多媒体处理框架。

# pipewire使用了跟gstreamer类似的pipeline设计模式吗

是的，PipeWire 使用了类似于 GStreamer 的 pipeline 设计模式。以下是两者在设计模式上的一些比较和说明：

| 特性           | GStreamer                             | PipeWire                                     |
| -------------- | ------------------------------------- | -------------------------------------------- |
| 基本概念       | 使用 `element` 和 `pad` 组成 pipeline | 使用 `node` 和 `port` 组成 pipeline          |
| 数据流模型     | 基于 pull 和 push 模型的数据流处理    | 基于 pull 和 push 模型的数据流处理           |
| 连接方式       | `pad` 用于连接 `element`              | `port` 用于连接 `node`                       |
| 处理单元       | `element` 表示一个处理单元            | `node` 表示一个处理单元                      |
| 支持的数据类型 | 主要用于音频和视频                    | 支持音频、视频和其他类型的数据               |
| 共享内存       | 通常使用内存缓冲区进行数据传输        | 通过共享内存区域在客户端和服务端之间传输数据 |

### 主要相似点

1. **Pipeline 架构**
   - 两者都使用了 pipeline 设计模式，其中数据通过一系列处理单元（节点/元素）传输，每个单元执行特定的任务。
   - 这种模式允许灵活地组合和重用不同的处理单元，形成复杂的多媒体处理流程。

2. **节点和端口**
   - GStreamer 中的 `element`（元素）相当于 PipeWire 中的 `node`（节点）。
   - GStreamer 中的 `pad`（插口）相当于 PipeWire 中的 `port`（端口）。
   - 元素和节点都有输入和输出端口，通过这些端口进行连接和数据传输。

3. **数据流处理**
   - 两者都支持基于 pull 和 push 模型的数据流处理，确保数据在 pipeline 中的高效传输。
   - 支持低延迟和高性能的数据处理，适合实时音视频应用。

### 主要区别

1. **数据类型的支持**
   - GStreamer 主要用于音频和视频流处理。
   - PipeWire 除了音频和视频，还支持其他类型的数据流处理，例如 VR/AR 数据。

2. **共享内存机制**
   - GStreamer 通常使用内存缓冲区进行数据传输。
   - PipeWire 通过共享内存区域在客户端和服务端之间传输大块数据，减少数据拷贝，提高传输效率，降低延迟。

3. **整体架构**
   - GStreamer 是一个用户空间的多媒体框架，独立于系统的音频和视频服务。
   - PipeWire 作为系统级的多媒体框架，试图统一音频和视频处理，取代 PulseAudio 和 JACK，提供更广泛的多媒体支持。

### 示例比较

#### GStreamer 示例

创建一个简单的音频播放 pipeline：

```sh
gst-launch-1.0 filesrc location=music.mp3 ! decodebin ! audioconvert ! audioresample ! autoaudiosink
```

#### PipeWire 示例

在 PipeWire 中，虽然没有直接的命令行工具来创建 pipeline，但可以使用类似 `pw-cli` 等工具进行配置和调试：

```sh
# 列出所有节点
pw-cli ls Node

# 创建一个新的节点（假设有一个简单的音频播放节点）
pw-cli create-node simple-audio-player

# 连接节点的端口
pw-cli connect simple-audio-player:output simple-audio-output:input
```

### 总结

PipeWire 使用了与 GStreamer 类似的 pipeline 设计模式，但在架构、数据类型支持和系统集成方面有所不同。PipeWire 的设计目标是提供一个统一的多媒体处理框架，涵盖音频、视频和其他数据类型，具有更高的性能和更低的延迟。

# pipewire的代码架构设计分析，例如impl的机制

PipeWire 的代码架构设计非常模块化和灵活，其中的一些关键设计特点包括：

### 1. 模块化设计
- PipeWire 的核心设计思想之一是模块化。它将功能划分为不同的模块，每个模块都有清晰的责任和接口。
- 模块化设计使得 PipeWire 更易于扩展和定制，可以根据特定需求添加或删除模块，而不影响整体系统的稳定性。

### 2. 实现（Impl）的机制
- PipeWire 使用了一种常见的设计模式，即接口与实现（Interface and Implementation）分离。
- 在 PipeWire 中，接口是公开的，而实现则是私有的，只对内部可见。这种设计使得接口与实现之间的耦合度降低，提高了代码的可维护性和可扩展性。
- 典型的示例是通过隐藏结构体的成员来实现这种接口和实现的分离。

### 3. 核心组件
- PipeWire 的核心组件包括核心框架（Core Framework）、Session Management、Graph Management、Device Management 等。
- 核心框架负责整体的调度和资源管理，Session Management 管理客户端会话，Graph Management 负责音视频图的管理，Device Management 则处理设备的发现和管理。

### 4. 插件架构
- PipeWire 支持插件架构，允许用户通过加载插件来扩展其功能。
- 插件可以是节点（Nodes）、端口（Ports）、模块、设备驱动程序等。这种灵活的插件架构使得 PipeWire 可以适应不同的应用场景和需求。

### 5. 跨平台支持
- PipeWire 的设计充分考虑了跨平台支持。它可以在不同的操作系统上运行，并提供统一的接口和行为。
- 这种跨平台支持使得 PipeWire 在各种嵌入式和桌面环境中都能够发挥作用，并提供一致的用户体验和开发体验。

### 6. 架构演进
- PipeWire 的架构是不断演进的。它持续吸收新的技术和思想，不断改进和优化，以满足不断变化的多媒体处理需求。
- 这种架构演进保持了 PipeWire 在技术领域的领先地位，并确保它能够持续提供高性能、稳定可靠的多媒体处理服务。

### 总结
PipeWire 的代码架构设计充分体现了模块化、接口与实现分离、插件架构和跨平台支持等设计原则。这些设计特点使得 PipeWire 成为一个灵活、高性能的多媒体处理框架，适用于各种不同的应用场景和需求。

# spa_handle_factory 是用的什么设计模式

在 PipeWire 中，`spa_handle_factory` 并不是一个特定的设计模式，而是一种机制或概念，用于创建和管理 SPA（Simple Plugin API）插件的实例。让我解释一下：

### SPA（Simple Plugin API）

SPA 是 PipeWire 中的一个核心组件，它提供了一种轻量级的、模块化的框架，用于实现各种插件，这些插件可以处理不同类型的媒体流。SPA 提供了一组接口和约定，使得插件之间的交互和集成变得简单而灵活。

### spa_handle_factory

`spa_handle_factory` 是 SPA 中的一个概念，它代表了一个插件工厂，负责创建和管理特定类型插件的实例。具体来说，`spa_handle_factory` 提供了以下功能：

1. **创建插件实例**：通过 `spa_handle_factory`，可以请求创建一个特定类型的插件实例。
2. **销毁插件实例**：当不再需要插件实例时，可以通过 `spa_handle_factory` 销毁它。
3. **参数配置**：`spa_handle_factory` 可能允许对插件实例进行参数配置，以满足特定的需求。
4. **错误处理**：`spa_handle_factory` 可能会处理插件创建过程中的错误，提供适当的错误处理机制。

### 设计模式的相关性

虽然 `spa_handle_factory` 并不是一个传统意义上的设计模式，但是它的设计与工厂模式有一些相似之处。工厂模式是一种创建型设计模式，旨在提供一个统一的接口，用于创建对象的实例，而不需要暴露对象的创建逻辑。在 PipeWire 中，`spa_handle_factory` 提供了一种类似的机制，用于创建 SPA 插件的实例，封装了插件的创建细节，使得客户端可以通过统一的接口来请求插件的创建，而无需了解插件创建的具体实现细节。

### 总结

`spa_handle_factory` 是 PipeWire 中用于创建和管理 SPA 插件实例的机制，它提供了一种统一的接口，用于请求插件的创建和销毁，并可能提供参数配置和错误处理等功能。虽然它不是一个特定的设计模式，但与工厂模式有一些相似之处，都是为了封装对象的创建过程，提供统一的接口。

# wireplumber

## 简介

WirePlumber 是 PipeWire 生态系统中的一部分，它是一个灵活的会话管理器和策略引擎，旨在提供更高级的音频和视频设备管理以及媒体流路由功能。下面是关于 WirePlumber 的一些信息：

### 功能和特点：

1. **会话管理**：
   - WirePlumber 可以管理多个音频和视频会话，包括应用程序、设备和系统级别的会话。
   - 它可以跟踪会话的创建、销毁和状态变化，并提供相应的管理和控制功能。

2. **设备管理**：
   - WirePlumber 可以自动发现和管理系统中的音频和视频设备，包括声卡、摄像头、扬声器等。
   - 它可以为每个设备创建一个相应的会话，并提供统一的接口用于设备的配置和控制。

3. **流路由**：
   - WirePlumber 可以根据用户定义的规则和策略来动态路由音频和视频流。
   - 它可以根据应用程序、设备、会话等因素来自动选择合适的路由方案，以满足不同的需求和场景。

4. **策略引擎**：
   - WirePlumber 具有灵活的策略引擎，可以根据用户定义的规则和条件来动态调整路由和设备配置。
   - 它可以根据不同的场景和需求自动执行相应的策略，以实现最佳的音视频体验。

5. **与 PipeWire 的集成**：
   - WirePlumber 是 PipeWire 生态系统的一部分，与 PipeWire 紧密集成。
   - 它可以直接与 PipeWire 核心和其他组件进行通信和交互，利用 PipeWire 提供的功能和接口。

### 使用场景：

- **多媒体应用开发**：作为一个灵活的会话管理器，WirePlumber 可以帮助开发人员管理和控制多媒体应用程序的音视频会话，提供更好的用户体验。
- **音视频设备管理**：WirePlumber 可以帮助系统管理员自动发现和管理系统中的音视频设备，简化设备配置和管理流程。
- **音视频路由和策略控制**：WirePlumber 可以根据用户定义的规则和策略来动态路由音视频流，实现更灵活、智能的音视频路由和策略控制。

### 总结：

WirePlumber 是 PipeWire 生态系统中的一个重要组件，它为用户和开发人员提供了强大的会话管理、设备管理和流路由功能，使得多媒体应用开发和系统管理变得更加简单和灵活。

# pipewire使用lua做了什么

PipeWire 使用 Lua 作为配置和脚本语言，主要用于以下方面：

1. **配置管理**：
   - Lua 可以用来编写 PipeWire 的配置文件，配置文件中可以定义音视频设备、流路由、策略规则等。
   - 使用 Lua 编写配置文件可以更灵活地定义复杂的配置规则，满足不同用户和应用的需求。

2. **脚本扩展**：
   - Lua 可以用来编写 PipeWire 的扩展脚本，实现自定义的音视频处理逻辑和功能。
   - 用户可以编写 Lua 脚本来扩展 PipeWire 的功能，例如自定义的效果处理、自动化任务等。

3. **动态控制**：
   - Lua 脚本可以与 PipeWire 核心进行交互，动态控制音视频流的创建、连接、调度等操作。
   - 使用 Lua 脚本可以实现动态的音视频流管理和控制，根据不同的条件和场景自动执行相应的操作。

4. **策略引擎**：
   - Lua 可以用来编写 PipeWire 的策略规则，根据不同的策略来调整音视频路由和设备配置。
   - 用户可以编写 Lua 脚本来定义特定的策略规则，例如根据应用程序、设备类型、用户偏好等因素来动态调整音视频路由和配置。

5. **事件处理**：
   - Lua 脚本可以响应 PipeWire 发出的事件，实现特定的事件处理逻辑。
   - 使用 Lua 脚本可以监听 PipeWire 的各种事件，如设备连接、流状态变化等，根据事件触发相应的处理逻辑。

总的来说，PipeWire 使用 Lua 作为配置和脚本语言，主要用于实现灵活的配置管理、扩展功能、动态控制和事件处理等功能，使得 PipeWire 更加灵活和可定制。

## lua编写pipewire配置文件示例

以下是一个简单的 Lua 示例，用于编写 PipeWire 的配置文件。这个示例配置文件用于定义一些音频设备和流路由规则。

```lua
-- 导入 PipeWire Lua API
pw = require("pipewire")

-- 创建 PipeWire 上下文
context = pw.Context.new()

-- 创建音频设备
device1 = pw.Device.new(context, {
    name = "Microphone",
    description = "Built-in microphone",
    direction = "Input",
    priority = 100,
    -- 其他设备属性
})

device2 = pw.Device.new(context, {
    name = "Speakers",
    description = "Built-in speakers",
    direction = "Output",
    priority = 100,
    -- 其他设备属性
})

-- 创建流路由规则
route1 = pw.Route.new(context, {
    match_device = "Microphone",
    match_role = "Capture",
    target_device = "Speakers",
    target_role = "Playback",
    -- 其他路由规则
})

-- 添加设备和路由规则到 PipeWire 上下文
context:add_device(device1)
context:add_device(device2)
context:add_route(route1)

-- 启动 PipeWire 上下文
context:start()
```

在这个示例中，我们首先导入了 PipeWire Lua API，并创建了一个 PipeWire 上下文。然后，我们创建了两个音频设备（一个输入设备和一个输出设备），以及一个流路由规则。最后，我们将设备和路由规则添加到 PipeWire 上下文中，并启动了上下文。这样，PipeWire 就可以根据配置文件中定义的设备和路由规则来管理音频设备和流路由了。

## lua编写pipewire扩展

没问题！下面是一个简单的 Lua 示例，用于编写 PipeWire 的扩展脚本。这个示例展示了如何使用 Lua 来编写一个简单的 PipeWire 扩展，用于在音频流中添加混响效果。

```lua
-- 导入 PipeWire Lua API
pw = require("pipewire")

-- 注册 PipeWire 扩展
extension = pw.Extension("reverb-extension", {
    name = "Reverb Effect Extension",
    version = "1.0",
    author = "Your Name",
    description = "Add reverb effect to audio streams",
})

-- 定义混响效果函数
function add_reverb(buffer)
    -- 在这里添加混响效果的逻辑
    -- 例如，将音频数据进行处理，添加混响效果
end

-- 监听音频流事件
extension:on("stream-added", function(stream)
    -- 检查是否为音频流
    if stream.media_type == "Audio" then
        -- 如果是音频流，则为其添加混响效果
        add_reverb(stream.buffer)
    end
end)

-- 启动扩展
extension:start()
```

在这个示例中，我们首先导入了 PipeWire Lua API，并创建了一个 PipeWire 扩展。然后，我们定义了一个名为 `add_reverb` 的函数，用于在音频流中添加混响效果。接着，我们监听了 PipeWire 的 `stream-added` 事件，当有新的音频流加入时，我们会检查它是否为音频流，如果是的话，就调用 `add_reverb` 函数为其添加混响效果。最后，我们启动了扩展，使得它可以开始监听和处理音频流事件。

这只是一个简单的示例，实际的混响效果处理可能会更加复杂，需要根据具体的需求和场景来实现。

# pipewire支持leaudio

自版本 0.3.59 起，PipeWire 支持 LE Audio 的基本音频配置文件 (BAP)，用于(LC3) 的连接同步流 (CIS)

得益于 PipeWire 的模块化架构，它已为未来的编解码器做好了准备

它支持双向音频，可以充当中央或外围设备。

在前一种情况下，它允许最终用户选择新的音频配置文件，

而在后一种情况下，它会自动将蓝牙音频流连接到本地音频输入和输出。

这为 BlueZ 和 PipeWire 中的 Auracast 支持铺平了道路。

如果您有兴趣尝试此操作，则必须安装 https://github.com/google/liblc3.git 中的 LC3 编解码器。 

PipeWire 构建必须使用选项“-Dbluez5-codec-lc3=enabled”进行配置。





https://www.bluez.org/le-audio-support-in-pipewire/

# pipewire-alsa怎么使用

pipewire-alsa\conf\99-pipewire-default.conf

这个的内容：

```
pcm.!default {
    type pipewire
    playback_node "-1"
    capture_node  "-1"
    hint {
        show on
        description "Default ALSA Output (currently PipeWire Media Server)"
    }
}

ctl.!default {
    type pipewire
}

```

就是把alsa的default录音和播放设备都设置为了pipewire设备。

编写代码是这样：

pipewire-alsa\tests\test-pipewire-alsa-stress.c

对应的alsa插件的实现是：

pipewire-alsa\alsa-plugins\pcm_pipewire.c

# 跟bluez的对接

从这些代码来看，这个功能跟bluealsa的代码类似。

spa\plugins\bluez5\a2dp-codec-aac.c

那是不是bluealsa实现了对liblc3的对接，也可以实现类似的leaudio播放功能？



# 参考资料

1、

https://wiki.archlinuxcn.org/wiki/PipeWire

2、用了200天的PipeWire到底好在哪？

https://zhuanlan.zhihu.com/p/499803807

3、什么是 PipeWire？PipeWire 的现状与未来

https://www.nxrte.com/jishu/13839.html

4、PipeWire，改变 Linux 多媒体格局的媒体服务

https://www.collabora.com/news-and-blog/blog/2020/03/05/pipewire-the-media-service-transforming-the-linux-multimedia-landscape/