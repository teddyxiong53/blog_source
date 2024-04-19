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

在 Pipewire 中，SPA（Simple Plugin API）是一个插件架构，

它允许开发者编写可以在运行时动态加载的模块。

SPA 提供了一种方式来扩展 Pipewire 的功能，使其能够支持不同的协议、设备、编解码器等。

SPA 插件可以分为几个主要类别：

1. **Devices**: 这些插件用于处理音频和视频设备的接入，例如 ALSA、JACK、V4L2 等。
2. **Protocol**: 这些插件允许 Pipewire 使用不同的协议进行通信，例如 RTP、RTSP、HTTP 等。
3. **Formats**: 这些插件处理不同的音频和视频格式，包括编解码器。
4. **Extensions**: 这些插件为 Pipewire 添加额外的功能，例如对特定应用程序或硬件的支持。



SPA 插件架构使得 Pipewire 能够轻松地扩展和适应不同的使用场景，而无需重新编译或重启服务。

开发者可以通过实现特定的接口来创建新的插件，从而为 Pipewire 生态系统贡献新的功能。

  在配置和使用 Pipewire 时，您可能需要确保相关的 SPA 插件已安装并正确配置，以便 Pipewire 能够利用这些插件提供的功能。

例如，如果您想要使用 Pipewire 来处理 JACK 应用程序的音频，您需要确保 JACK 相关的 SPA 插件已安装。

## 如何创建SPA插件

创建 SPA（Simple Plugin API）插件需要对 Pipewire 的内部结构和 API 有深入的了解。下面我将提供一个简化的例子，展示如何创建一个基本的 SPA 插件。
首先，你需要确保你安装了 Pipewire 的开发包，这样你就可以包含必要的头文件和链接到 Pipewire 库。在基于 Debian 的系统上，你可以使用以下命令安装：
```bash
sudo apt install libpipewire-dev
```
接下来，我们将创建一个简单的 SPA 插件。这个插件不会做任何复杂的事情，只是展示了如何设置插件的基本结构和加载机制。
1. **创建插件源文件** (`example_plugin.c`):
```c
#include <pipewire/pipewire.h>
static const struct spa_handle_factory *factory;
static int
plugin_init(const struct spa_handle_factory *factory, const char *args)
{
    spa_handle_factory_log(&factory, "example plugin init with args '%s'\n", args);
    return 0;
}
static void
plugin_deinit(void)
{
    spa_handle_factory_log(&factory, "example plugin deinit\n");
}
static const struct spa_handle_info info = {
    .type = SPA_HANDLE_TYPE_PLUGIN,
    .version = SPA_VERSION_HANDLE_INFO,
    .init = plugin_init,
    .deinit = plugin_deinit,
};
const struct spa_handle_factory spa_handle_factory = {
    .info = &info,
    .size = sizeof(info),
};
```
2. **编译插件**:
   编译插件需要使用 `spa` 工具，这个工具通常随 Pipewire 一起安装。你可以使用以下命令来编译插件：
```bash
spa-build example_plugin.c -o example_plugin.so
```
3. **安装插件**:
   编译完成后，你需要将生成的共享对象文件（`example_plugin.so`）复制到系统的插件目录中。在 Linux 系统上，这个目录通常是 `/usr/lib/spa/plugins`。
4. **使用插件**:
   一旦插件被安装到正确的目录，Pipewire 在启动时会自动加载它。你可以通过查看 Pipewire 的日志来确认插件是否被成功加载。
请注意，这个例子非常基础，只是展示了如何创建一个可以被 Pipewire 加载的插件。实际的插件可能会更加复杂，需要实现特定的接口和功能。Pipewire 的官方文档和源代码中包含了更详细的示例和指南，可以帮助你深入了解如何为 Pipewire 开发更完整的插件。

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

# 参考资料

1、

https://wiki.archlinuxcn.org/wiki/PipeWire

2、用了200天的PipeWire到底好在哪？

https://zhuanlan.zhihu.com/p/499803807

3、什么是 PipeWire？PipeWire 的现状与未来

https://www.nxrte.com/jishu/13839.html