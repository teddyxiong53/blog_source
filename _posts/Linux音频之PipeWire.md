---
title: Linux音频之PipeWire
date: 2024-04-10 15:32:17
tags:
	- 音频

---

--

# 资源收集

bootlin的文章，非常好。高屋建瓴。

https://bootlin.com/blog/an-introduction-to-pipewire/

https://bootlin.com/doc/training/audio/audio-slides.pdf

https://bootlin.com/blog/hands-on-installation-of-pipewire/

arch wiki

https://wiki.archlinuxcn.org/wiki/PipeWire

官方仓库的wiki，这里算是最权威的最及时的信息了。

https://gitlab.freedesktop.org/pipewire/pipewire/-/wikis/home

尤其是这个QA，回答了很多我关心的问题。

https://gitlab.freedesktop.org/pipewire/pipewire/-/wikis/FAQ

这里说明了配置的详细含义。

https://gitlab.freedesktop.org/pipewire/pipewire/-/wikis/Config-PipeWire

# 简介1

PipeWire 是一个服务器和 API，

用于在 Linux 上处理多媒体。

==它最常见的用途是为 Wayland 和 Flatpak 应用程序实现屏幕共享、远程桌面以及不同软件之间其他形式的音频和视频路由。==

根据它的官方FAQ，“你可以把它看作是应用程序和库可以使用的驱动之上的多媒体路由层”。

相较于 PulseAudio 专注于消费级音频和 JACK 专注于专业级音频，PipeWire 的目标是为所有级别的用户工作。

在其他技术中，==PipeWire 通过提供在不同的缓冲区大小之间动态切换的能力来实现这一目标==，以适应不同音频应用的不同延迟要求。

在 Debian 10 中，PipeWire 0.2.5 是可用的，它应该不需要手动安装，因为它通常被使用它的应用程序作为一个依赖项带入。

在 Debian 11中，PipeWire 0.3.19 是可用的，并且可以试验性地用来替代 [ALSA](https://wiki.debian.org/ALSA) 用户空间库、[PulseAudio](https://wiki.debian.org/PulseAudio) 和 [JACK](https://wiki.debian.org/JACK)。这是一个存在文档但不支持的用例。

在 Debian Testing 和 Debian Unstable 中有更新的 PipeWire 版本。对于这些分发的用户来说，PipeWire 应该更加可靠，在许多用例下可以很好地替代。



# 简介2

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

# buildroot下使用pipewire

这篇文章非常不错。

https://bootlin.com/blog/hands-on-installation-of-pipewire/

在启动过程中，守护程序会尝试创建客户端将用来与其通信的 UNIX 套接字;

其默认名称为 `pipewire-0` 。

但是，如果没有特定的环境变量，PipeWire 不知道该把它放在哪里。

因此，解决方法是 `pipewire` 使用 `XDG_RUNTIME_DIR` 变量集进行调用：

```
$ XDG_RUNTIME_DIR=/run pipewire
[W][03032.468669] pw.context   | [       context.c:  353 pw_context_new()] 0x507978: can't load dbus library: support/libspa-dbus
[E][03032.504804] pw.module    | [   impl-module.c:  276 pw_context_load_module()] No module "libpipewire-module-rt" was found
[E][03032.530877] pw.module    | [   impl-module.c:  276 pw_context_load_module()] No module "libpipewire-module-portal" was found
```

仍然会出现一些警告，但它们不会阻止 PipeWire 的进程：

第一行是意料之中的，因为我们编译了不支持 D-Bus 的 PipeWire。

第二个原因是默认配置调用了一个 PipeWire 模块，该模块使用 setpriority（2） 使守护进程实时，并使用带有 SCHED_FIFO的 pthread_setschedparam（3） 使线程实时。直到最近，如果 D-Bus 支持不可用，该模块才被编译，因为它对 RTKit 有一个回退（D-Bus RPC 要求增强的进程优先级，用于避免为每个进程授予权限）。这在较新的版本中得到了修复，因为如果 D-Bus 不可用，该模块现在正在编译时没有 RTKit 回退，但我们使用的稳定 Buildroot 版本正在打包旧版本的 PipeWire。

第三个指的是 xdg-desktop-portal 中的门户，这是一个基于 D-Bus 的接口，用于向 Flatpak 应用程序公开各种 API。对于嵌入式用途，这对我们来说无关紧要。

可以覆盖默认的 PipeWire 守护程序配置以删除这些警告：

 `support.dbus` in `context.properties` 控制 D-Bus 库的加载，要加载的模块在 中 `context.modules` 声明。

默认配置位于 ， `/usr/share/pipewire/pipewire.conf` 

覆盖的一个好方法是新建的 `/etc/pipewire` 同名文件。

提示：PipeWire 的日志记录使用 `PIPEWIRE_DEBUG` 环境变量进行控制，如文档中所述。



我们没有看到ALSA PCM设备的原因是

PipeWire不负责监控 `/dev` 和向图形添加新节点;

这是我们session manager的责任。

WirePlumber 的配置需要从默认值更新，以避免由于缺少一些可选依赖项而崩溃。

要更新它，推荐的方法与 PipeWire 相同：

使用位于 中的 `/etc/wireplumber` 配置文件重载配置文件。

以下是默认配置的问题：

最后两个问题可以通过使用以下 Lua 配置脚本来解决 `/etc/wireplumber/main.lua.d/90-disable-dbus.lua` ：

```
alsa_monitor.properties["alsa.reserve"] = false
default_access.properties["enable-flatpak-portal"] = false
```

完成所有操作后，WirePlumber 的守护程序将继续运行并成功连接到 PipeWire：



就是这样

WirePlumber 现在已经检测到我们的 ALSA 接收器和源，并将它们作为节点添加到 PipeWire 图中。

它将检测我们添加到图形中的源节点，并将它们链接到 ALSA 接收器节点，输出音频供我们的耳朵欣赏。



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





# pipewire支持leaudio

自版本 0.3.59 起，PipeWire 支持 LE Audio 的基本音频配置文件 (BAP)，用于(LC3) 的连接同步流 (CIS)

得益于 PipeWire 的模块化架构，它已为未来的编解码器做好了准备

它支持双向音频，可以充当中央或外围设备。

在前一种情况下，它允许最终用户选择新的音频配置文件，

而在后一种情况下，它会自动将蓝牙音频流连接到本地音频输入和输出。

这为 BlueZ 和 PipeWire 中的 Auracast 支持铺平了道路。

如果您有兴趣尝试此操作，则必须安装 https://github.com/google/liblc3.git 中的 LC3 编解码器。 

PipeWire 构建必须使用选项“-Dbluez5-codec-lc3=enabled”进行配置。



LE Audio 是蓝牙音频堆栈的全新实现，

它取代了“经典音频”A2DP 和 HFP 配置文件。

它的默认编解码器是 LC3，

==但由于它是对所有内容的重写，因此编解码器只是更改的一小部分。==

主要的Linux LE Audio实现由三个项目组成：（i）Linux内核，（ii）BlueZ，（iii）声音服务器部分，即Pipewire。

LE Audio 实现的主体在 （i） 和 （ii） 中。Pipewire 部分 （iii） 相对较小且简单，主要负责编解码器支持以及与音响系统其余部分的集成。





https://www.bluez.org/le-audio-support-in-pipewire/

https://gitlab.freedesktop.org/pipewire/pipewire/-/wikis/LE-Audio-+-LC3-support

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

## 跟alsa的具体对接

/usr/share/alsa/alsa.conf.d

这个下面放了2个配置文件。

```
50-pipewire.conf          
99-pipewire-default.conf
```

我在我的/etc/asound.conf的最前面加上这2行：

```
<confdir:alsa.conf.d/50-pipewire.conf>
<confdir:alsa.conf.d/99-pipewire-default.conf>
```

现在aplay -L就能识别到了。



# dbus

PipeWire 需要活动的 D-Bus 用户会话总线。

如果您的桌面环境、窗口管理器或 Wayland 合成器配置为提供此功能，则不需要进一步配置。

否则，可能需要使用 `dbus-run-session(1)` .

PipeWire 还要求在环境中定义 `XDG_RUNTIME_DIR` 环境变量才能正常工作。

在 PipeWire 中，会话管理器负责互连媒体源和接收器以及强制执行路由策略。如果没有会话管理器，PipeWire 将无法运行。



# 写一个pw node

https://bootlin.com/blog/a-custom-pipewire-node/

# 简单指导



## 采样率

默认情况下，PipeWire 启用 1 个采样率 （48000 Hz）。

所有东西都将使用高质量的重采样器重新采样到这个速率。这足以提供良好的默认体验。

你也可以启动多个采样率的支持。

方法是在 `~/.config/pipewire/pipewire.conf.d/10-rates.conf` 创建一个包含以下内容的新文件：

```
# Adds more common rates
context.properties = {
    default.clock.allowed-rates = [ 44100 48000 88200 96000 ]
}
```

您还可以强制采样率为 96000Hz，用于数据处理：

```plaintext
pw-metadata -n settings 0 clock.force-rate 96000
```

您可以切换回到动态采样率选择：

```plaintext
pw-metadata -n settings 0 clock.force-rate 0
```



如果您有一个 （Pro） 声卡，其中每个捕获通道都是不同的麦克风或乐器，则可以从每个通道中制作新的源。

## 切分设备

如果您有一个 （Pro） 声卡，其中每个捕获通道都是不同的麦克风或乐器，则可以从每个通道中制作新的源。

以下示例创建 2 个新源，一个来自通道 1 （AUX0） 的麦克风，一个来自通道 2 （AUX1） 的吉他。请确保将 target.object 更改为卡的名称。

`~/.config/pipewire/pipewire.conf.d/20-mic-split.conf` 创建一个包含以下内容的新文件：

```
context.modules = [
    {   name = libpipewire-module-loopback
        args = {
            node.description = "Microphone"
            capture.props = {
                node.name = "capture.Mic"
                audio.position = [ AUX0 ]
                stream.dont-remix = true
                target.object = "alsa_input.usb-BEHRINGER_UMC404HD_192k-00.pro-input-0"
                node.passive = true
            }
            playback.props = {
                node.name = "Mic"
                media.class = "Audio/Source"
                audio.position = [ MONO ]
            }
        }
    }
    {   name = libpipewire-module-loopback
        args = {
            node.description = "Guitar"
            capture.props = {
                node.name = "capture.Guitar"
                audio.position = [ AUX1 ]
                stream.dont-remix = true
                target.object = "alsa_input.usb-BEHRINGER_UMC404HD_192k-00.pro-input-0"
                node.passive = true
            }
            playback.props = {
                node.name = "Guitar"
                media.class = "Audio/Source"
                audio.position = [ MONO ]
            }
        }
    }
]
```



以下示例创建了 2 个新的立体声接收器，一个来自通道 1-2 （AUX0-AUX1） 的扬声器，一个来自通道 3-4 （AUX2-AUX3） 的耳机。请确保将 target.object 更改为卡的名称。

`~/.config/pipewire/pipewire.conf.d/20-playback-split.conf` 创建一个包含以下内容的新文件：

```
context.modules = [
    {   name = libpipewire-module-loopback
        args = {
            node.description = "Speakers"
            capture.props = {
                node.name = "Speakers"
                media.class = "Audio/Sink"
                audio.position = [ FL FR ]
            }
            playback.props = {
                node.name = "playback.Speakers"
                audio.position = [ AUX0 AUX1 ]
                target.object = "alsa_output.usb-BEHRINGER_UMC404HD_192k-00.pro-output-0"
                stream.dont-remix = true
                node.passive = true
            }
        }
    }
    {   name = libpipewire-module-loopback
        args = {
            node.description = "Headphones"
            capture.props = {
                node.name = "Headphones"
                media.class = "Audio/Sink"
                audio.position = [ FL FR ]
            }
            playback.props = {
                node.name = "playback.Headphones"
                audio.position = [ AUX2 AUX3 ]
                target.object = "alsa_output.usb-BEHRINGER_UMC404HD_192k-00.pro-output-0"
                stream.dont-remix = true
                node.passive = true
            }
        }
    }
]
```

## upmix

默认情况下，PipeWire 不会将立体声音频上混为多声道 5.1 或 7.1 音频，因为默认行为应该是按原样路由音频，而不是对音频应用滤波器。


您需要在 PulseAudio 客户端、Native PipeWire 客户端和蓝牙设备中手动启用 umixing。

当pipewire用作蓝牙接收器（扬声器）时，传入的立体声信号可以上混为多声道。

要启用蓝牙输入的上混，请创建包含以下内容的文件 '~/.config/wireplumber/wireplumber.conf.d/40-upmix.conf：

```
# Enables upmixing
stream.properties = {
    channelmix.upmix      = true
    channelmix.upmix-method = psd
    channelmix.lfe-cutoff = 150
    channelmix.fc-cutoff  = 12000
    channelmix.rear-delay = 12.0
}
```

## 音量

客户端和其他应用程序能够更改流的音量。

音量通常表示为 0.0（静音）、1.0（无消音）和 10.0（非常响亮）之间的值。

您可以通过修改各个图层的 `channelmix.min-volume` 和 `channelmix.max-volume` stream 属性来禁用或限制此行为。

将 channelmix.max-volume` 设置为 `channelmix.min-volume` 相同的值实质上是将音量锁定到特定值。

其他最小值/最大值可用于限制音量。

要限制本机客户端或 ALSA 客户端的volume，

请创建一个文件 `~/.config/pipewire/client-rt.conf.d/50-volume-limit.conf` 

```
# Limits volume between 0.0 and 1.0
stream.properties = {
    channelmix.min-volume   = 0.0
    channelmix.max-volume   = 1.0
}
```

要启用蓝牙的音量限制，请创建一个包含以下内容的文件 `~/.config/wireplumber/wireplumber.conf.d/50-volume-limit.conf` ：

```
# Limits volume between 0.0 and 1.0
stream.properties = {
    channelmix.min-volume   = 0.0
    channelmix.max-volume   = 1.0
}
```

要为 wirelumber 制作的 ALSA 节点启用volume限制，请创建一个包含以下内容的文件 `~/.config/wireplumber/wireplumber.conf.d/60-volume-limit.conf` ：

```
monitor.alsa.rules = [
  {
    matches = [
      # This matches the value of the 'node.name' property of the node.
      {
        node.name = "~alsa_.*"
      }
    ]
    actions = {
      update-props = {
        channelmix.min-volume   = 0.0
        channelmix.max-volume   = 1.0
      }
    }
  }
]
```

## 延迟控制

PipeWire 处理图的延迟主要由缓冲区大小和处理图的采样率（称为量子）的组合决定。

量子是每个图形处理周期处理的数据量（以时间为单位）。

默认情况下，PipeWire将根据可用客户端和配置的限制和默认值选择最佳量程。

您可以使用以下命令强制量子，例如 256：

```plaintext
pw-metadata -n settings 0 clock.force-quantum 256
```

您可以通过以下方式再次恢复动态行为：

```plaintext
pw-metadata -n settings 0 clock.force-quantum 0
```

ALSA 客户端使用额外的环形缓冲区，这可能会增加延迟。

==使用 `PIPEWIRE_ALSA` 环境变量来控制 ALSA 客户端的缓冲区大小和周期大小：==

```plaintext
PIPEWIRE_ALSA='{ alsa.buffer-bytes=16384 alsa.period-bytes=128 }' aplay ...
```

# 环境变量

https://docs.pipewire.org/page_man_pipewire_1.html

这里列举了很多环境变量。

`PIPEWIRE_LATENCY` 环境变量可用于配置应用程序的延迟：

`PIPEWIRE_RUNTIME_DIR` `USERPROFILE` ， `XDG_RUNTIME_DIR` 用于查找服务器（和本机客户端）上的 PipeWire 套接字。


 `PIPEWIRE_CORE` 是要创建的套接字的名称。


 `PIPEWIRE_REMOTE` 是要连接到的套接字的名称。


 `PIPEWIRE_DAEMON` 设置为 true，则进程将成为新的 PipeWire 服务器。

`PIPEWIRE_CONFIG_DIR` `HOME` ， `XDG_CONFIG_HOME` 用于查找配置文件目录。


 `PIPEWIRE_CONFIG_PREFIX` 并 `PIPEWIRE_CONFIG_NAME` 用于覆盖应用程序提供的配置前缀和配置名称。


 `PIPEWIRE_NO_CONFIG` 启用 （false） 或禁用 （true） 覆盖默认配置。



最小/最大/默认量子分别为 0.6ms （32/48000）、170.6ms （8192/48000） 和 21.3ms （1024/48000）。

正如配置文件所解释的那样，配置选项可以拆分为单独的文件。数字表示它们的加载顺序，以下是示例：

# client的配置

客户端配置文件遵循通用 PipeWire 配置文件。

对于客户端， `core.daemon` 该属性通常设置为 false。

客户端通常只有一组有限的 `context.spa-libs` ，通常用于创建音频节点和轮询循环。

# alsa插件

ALSA 插件使用 client-rt.conf 文件。

所有 ALSA 客户端都将创建一个流，因此流属性和规则将照常工作。

指示 ALSA 客户端链接到特定的接收器或源 `object.serial` 或 `node.name` .

例如：

```plaintext
PIPEWIRE_NODE=alsa_output.pci-0000_00_1b.0.analog-stereo aplay ...
```


在给定的音频接收器上播放播放。

# so文件

/usr/lib/pipewire-0.3目录下：

```
libpipewire-module-access.so
libpipewire-module-adapter.so
libpipewire-module-client-device.so
libpipewire-module-client-node.so
libpipewire-module-combine-stream.so
libpipewire-module-echo-cancel.so
libpipewire-module-fallback-sink.so
libpipewire-module-filter-chain.so
libpipewire-module-link-factory.so
libpipewire-module-loopback.so
libpipewire-module-metadata.so
libpipewire-module-netjack2-driver.so
libpipewire-module-netjack2-manager.so
libpipewire-module-parametric-equalizer.so
libpipewire-module-pipe-tunnel.so
libpipewire-module-portal.so
libpipewire-module-profiler.so
libpipewire-module-protocol-native.so
libpipewire-module-protocol-pulse.so
libpipewire-module-protocol-simple.so
libpipewire-module-raop-sink.so
libpipewire-module-rt.so
libpipewire-module-rtp-sap.so
libpipewire-module-rtp-sink.so
libpipewire-module-rtp-source.so
libpipewire-module-session-manager.so
libpipewire-module-spa-device-factory.so
libpipewire-module-spa-device.so
libpipewire-module-spa-node-factory.so
libpipewire-module-spa-node.so
libpipewire-module-vban-recv.so
libpipewire-module-vban-send.so
```



# 为什么配置都是用libpipewire-module-loopback 这个

`libpipewire-module-loopback` 是 PipeWire 中一个常用的模块，用于创建音频环回设备。

它允许音频数据从一个源流到另一个目标，实现音频的重路由和环回。

这在音频处理和配置中非常有用，特别是在需要将音频从一个输入设备传输到一个输出设备时。

### 为什么使用 `libpipewire-module-loopback`

1. **音频重路由**：可以将音频从一个源重路由到另一个目标，例如将麦克风输入重路由到扬声器输出，或将应用程序的音频输出重路由到另一个应用程序的音频输入。

2. **实时音频处理**：在实时音频处理中，可以使用环回设备将音频流传输到处理模块进行处理，然后再输出到目的设备。

3. **音频测试和调试**：在音频系统测试和调试过程中，环回设备可以帮助捕捉和分析音频流，确保音频数据传输的正确性。

4. **灵活性**：通过配置 `libpipewire-module-loopback`，==可以实现复杂的音频路由方案，以满足不同的音频处理需求。==

### 使用 `libpipewire-module-loopback` 的配置示例

下面是一个如何配置 `libpipewire-module-loopback` 模块的示例配置文件：

```ini
context.modules = [
    { name = libpipewire-module-loopback
        args = {
            node.name = "loopback-device"
            capture.props = {
                media.class = Audio/Source
                node.description = "Loopback Source"
            }
            playback.props = {
                media.class = Audio/Sink
                node.description = "Loopback Sink"
            }
        }
    }
]
```

### 配置文件说明

- `context.modules`：这是一个模块加载列表，PipeWire 在启动时会加载这些模块。
- `name = libpipewire-module-loopback`：指定加载 `libpipewire-module-loopback` 模块。
- `args`：提供模块的参数。
  - `node.name`：设置环回设备的节点名称。
  - `capture.props`：设置捕获端口的属性，例如媒体类和节点描述。
  - `playback.props`：设置回放端口的属性，例如媒体类和节点描述。

### 示例解释

1. **加载模块**：加载 `libpipewire-module-loopback` 模块来创建一个环回设备。
2. **设置节点名称**：将环回设备命名为 `loopback-device`。
3. **捕获属性**：设置捕获端口的属性，使其显示为 `Audio/Source`，并描述为 `Loopback Source`。
4. **回放属性**：设置回放端口的属性，使其显示为 `Audio/Sink`，并描述为 `Loopback Sink`。

### 使用场景

- **将麦克风输入重定向到虚拟设备**，从而使多个应用程序可以同时访问麦克风输入。
- **创建虚拟音频设备**，将来自不同应用程序的音频流合并到一个虚拟输出设备中。
- **实时音频效果处理**，将输入音频流传递到处理模块，再输出处理后的音频。

通过配置 `libpipewire-module-loopback`，你可以灵活地管理和路由音频流，满足各种复杂的音频处理需求。这使得 PipeWire 在专业音频处理和一般桌面音频管理中都非常强大和灵活。

# 1

XDG_CONFIG_DIR的内容生成了这些：

```
# ls -lh
total 0      
drwx------    3 root     root          60 Jan  1 03:56 dbus-1
srwxr-xr-x    1 root     root           0 Jan  1 03:56 pipewire-0
srwxr-xr-x    1 root     root           0 Jan  1 03:56 pipewire-0-manager
-rw-r-----    1 root     root           0 Jan  1 03:56 pipewire-0-manager.lock
-rw-r-----    1 root     root           0 Jan  1 03:56 pipewire-0.lock
```



# 参考资料

1、

https://wiki.archlinuxcn.org/wiki/PipeWire

2、用了200天的PipeWire到底好在哪？

https://zhuanlan.zhihu.com/p/499803807

3、什么是 PipeWire？PipeWire 的现状与未来

https://www.nxrte.com/jishu/13839.html

4、PipeWire，改变 Linux 多媒体格局的媒体服务

https://www.collabora.com/news-and-blog/blog/2020/03/05/pipewire-the-media-service-transforming-the-linux-multimedia-landscape/