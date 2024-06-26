---
title: pulseaudio研究（1）
date: 2021-11-29 11:07:33
tags:
	- 音频

---

--

# 对pulseaudio的一篇全面论述文章

https://gavv.net/articles/pulseaudio-under-the-hood/

现有的文档没有提供鸟瞰图和对 PulseAudio 功能和设计的解释，也没有涵盖许多实现细节。

因此，总体情况仍然不明朗。高级配置看起来很神秘，因为首先需要了解引擎盖下发生的事情。模块编写器的学习曲线也很高。

本文档试图填补这一空白，并概述了 PulseAudio 的功能、架构和内部结构。更准确地说，它有三个目标：

- 描述可用功能
- 解释其底层设计和重要的实现细节
- 提供编写客户机和服务器模块的起点

它没有提供 PulseAudio 配置和 API 的详细参考或教程。

PulseAudio 是 POSIX 操作系统（主要针对 Linux）的声音服务器，

充当单个或多个主机上的硬件设备驱动程序和应用程序之间的代理和路由器。

## PulseAudio 旨在实现许多目标。

**桌面音频的抽象层**

PulseAudio 管理所有音频应用程序、本地和网络流、设备、滤波器和音频 I/O。它提供了一个抽象层，将所有这些东西组合在一个地方。

**可编程行为**

丰富的 API 提供了用于检查和控制所有可用对象及其持久性和运行时属性的方法。这样就可以用 GUI 工具替换配置文件。许多桌面环境都提供此类工具。

**自动设置**

PulseAudio 设计为开箱即用。它自动检测和配置本地网络中可用的本地设备和声音服务器。它还实现了许多用于自动音频管理和路由的策略。

**灵活性**

PulseAudio 为用户提供了高度的灵活性。可以将任何应用程序的任何流连接到任何本地或远程设备，配置每个流和每个设备的volume，构建声音处理链等。

**扩展**

PulseAudio 为服务器扩展提供了一个框架，许多内置功能都以模块的形式实现。非官方的第三方模块也存在，但是，上游并不能保证树外模块的稳定 API。



## 以下列表介绍了 PulseAudio 中实现的功能。

**协议和网络**

PulseAudio 支持多种网络协议，可与客户端、远程服务器和第三方软件进行通信。

**设备驱动程序**

PulseAudio 支持多个后端与硬件设备和控件进行交互。它支持热插拔并自动配置新设备。

**声音处理**

PulseAudio 实现了各种声音处理工具，如混音、采样率转换和回声消除，可以手动或自动使用。

**sample缓存**

PulseAudio 为命名的短批次样本实现了内存存储，这些样本可以上传到服务器一次，然后播放多次。

**流管理**

PulseAudio 管理所有桌面应用程序的所有输入和输出流，为它们提供时钟、缓冲和倒带等功能。

**时间管理**

PulseAudio 实现了基于每设备计时器的调度程序，可在声卡域中提供时钟，保持最佳延迟，并降低播放故障的可能性。

**省电**

PulseAudio 采用多种技术来减少 CPU 和电池使用量。

**自动设置和路由**

PulseAudio 自动设置卡、设备和流的参数，将流路由到设备，并执行其他内务操作。

**桌面集成**

PulseAudio 实现了将其集成到桌面环境中的多项功能。

**兼容层**

与其他音响系统有几个兼容层，因此现有应用程序无需修改即可自动在 PulseAudio 上运行。

## usecase

以下是如何在桌面上使用 PulseAudio 功能的一些实际示例：

- 智能热插拔处理。例如，在连接蓝牙或 USB 耳机时自动设置耳机，或者在耳机插入插孔时自动切换到耳机。
- 用于在立体声、环绕声或 S/PDIF 等各种模式之间轻松切换声卡的 GUI。
- 一个 GUI，用于轻松将音频流切换到任何可用的音频设备，如内置扬声器、有线耳机、蓝牙耳机或 HDMI 输出。
- 一个 GUI，用于使单个应用程序比其他应用程序更响亮，或将其静音，并在下次应用程序出现时记住此决定。
- 用于将音频路由到 LAN 中可用的远程设备的 GUI。例如，将笔记本电脑上播放音乐的浏览器连接到连接到 Raspberry Pi 的扬声器。
- 自动将音乐或语音从蓝牙播放器或移动电话路由到声卡或蓝牙扬声器或耳机。
- 透明地将各种声音处理工具添加到正在运行的应用程序中，例如向 VoIP 客户端添加回声消除。
- 通过自动动态调整延迟到当前正在运行的应用程序可接受的最大值，并禁用当前不必要的声音处理（如重新采样）来减少 CPU 和电池使用量。
- 智能 I/O 调度，可以结合播放的高延迟（以避免故障并降低 CPU 使用率）和用户操作（如音量更改）的低延迟（以提供更流畅的用户体验）。
- 自动将现有桌面应用程序集成到 PulseAudio 工作流程中，即使它们不知道 PulseAudio。



## 问题和缺点

使用 PulseAudio 有几个已知的缺点，包括基本问题和将来可能解决的实现问题：

- 额外的复杂性、开销和 bug（更多的代码总是意味着更多的 bug）
- 缺乏全面的文档
- 非直观的命令行工具和配置
- 奇怪的功能，如自动生成和内置看门狗
- 更高的最小延迟
- 在 802.11 （WiFi） 等不可靠的网络上服务质量差
- 没有硬件混合和重采样
- 使用 ALSA UCM 时没有硬件volume

## 高级组件

下图演示了示例 PulseAudio 设置的简化视图。

它显示了三个客户端（使用三个不同的 API）、一个本地 PulseAudio 服务器、两个远程 PulseAudio 服务器（通过“本机”和 RTP 协议连接）、一个远程 RTP 接收器、ALSA 后端以及为此设置提供服务所需的一组模块。

![img](images/random_name2/components.png)



## 关键抽象

本节讨论关键的服务器端对象类型。

###  Devices and streams 

PulseAudio 是围绕连接到流（源输出和接收器输入）的设备（源和接收器）构建的。下图说明了这些连接。

![img](images/random_name2/devices_and_streams.png)



### 对象层次结构

下图显示了服务器端对象的层次结构。

![img](images/random_name2/object_hierarchy.png)

































# 简介

ubuntu里，默认启动的pulseaudio是这样的：

```
/usr/bin/pulseaudio --start --log-target=syslog
```

PulseAudio是用于[Linux](https://so.csdn.net/so/search?from=pc_blog_highlight&q=Linux)，POSIX和Windows系统的网络低延迟声音服务器。

配置文件

```
~/.config/pulse/daemon.conf, 
/etc/pulse/daemon.conf
```



# 实时和高优先级计划

为了最大程度地降低播放过程中丢失的风险，

如果基础平台支持，建议使用实时调度运行PulseAudio。

这使PulseAudio守护程序的调度等待时间与系统负载分离，

因此是确保PulseAudio在需要其重新填充硬件播放缓冲区时始终获得CPU时间的最佳方法。

不幸的是，这在大多数系统上都是安全隐患，

因为PulseAudio是作为用户进程运行的，

并且为用户进程提供实时调度特权总是伴随着用户滥用其锁定系统的风险-这可能是由于创建进程而造成的。

实时有效地禁用了抢占。

为了最大程度地降低风险，PulseAudio默认情况下不会启用实时调度。

但是，建议在受信任的系统上启用它。

为此，请使用--realtime（请参见上文）启动PulseAudio或在daemon.conf中启用相应的选项。

由于获取实时调度是大多数系统上的特权操作，因此需要对系统配置进行一些特殊更改，以允许主叫用户使用它们。

有两个选项：

   在较新的Linux系统上，系统资源限制RLIMIT_RTPRIO（有关更多信息，请参见setrlimit（2））可用于允许特定用户获取实时调度。可以在/etc/security/limits.conf中进行配置，建议资源限制为9。

   或者，可以为PulseAudio二进制设置SUID根位。然后，守护程序将在启动时立即放弃root特权，但是保留CAP_NICE功能（在支持该功能的系统上），但前提是主叫用户是Pulse-rt组的成员（请参见上文）。对于所有其他用户，所有功能将立即删除。该解决方案的优势在于，实时特权仅授予PulseAudio守护程序，而不授予所有用户进程。

   或者，如果认为锁定机器的风险太大而无法启用实时调度，则可以启用高优先级调度（即，负好级别）。
   可以通过在启动PulseAudio时传递--high-priority（请参见上文）来启用它，也可以使用daemon.conf中的适当选项来启用它。只有设置了适当的资源限制RLIMIT_NICE（有关更多信息，请参见setrlimit（2））（可能在/etc/security/limits.conf中配置），才能启用负的尼斯级别。建议将资源限制为31（对应于不错的-11级）。



# 环境变量

```
   $ PULSE_SERVER：服务器字符串，指定客户端请求声音服务器连接且未明确要求特定服务器时要连接的服务器。服务器字符串是由空格分隔的服务器地址的列表，依次尝试。服务器地址由一个可选的地址类型说明符(unix:, tcp:, tcp4:, tcp6:)组成，后跟路径或主机地址。主机地址可以包括可选的端口号。服务器地址可以用{}中的字符串作为前缀。在这种情况下，以下服务器地址为ig-
   除非前缀字符串等于本地主机名或计算机ID（/ etc / machine-id），否则不进行操作。

   $ PULSE_SINK：当客户端创建回放流且未明确要求特定接收器时，要连接到的接收器的符号名称。

   $ PULSE_SOURCE：客户端创建记录流且未明确要求特定来源时要连接的来源的符号名称。

   $ PULSE_BINARY：使用服务器自动生成时运行的PulseAudio可执行文件的路径。

   $ PULSE_CLIENTCONFIG：用于客户端配置的应读取的文件路径，而不是client.conf（请参见上文）。

   $ PULSE_COOKIE：包含PulseAudio身份验证cookie的文件的路径。默认为~/.config/pulse/cookie。

   这些环境设置（如果已设置）优先于client.conf中的配置设置（请参见上文）。

```

# /etc/pulse/daemon.conf



```
   daemonize =
   启动后进行守护程序。布尔值，默认为no。--daemonize命令行选项优先。

   fail =
   如果配置脚本default.pa中的任何指令失败，则无法启动。采用布尔型参数，默认为yes。--fail命令行选项优先。

   allow-module-loading =
   启动后允许/禁止加载模块。这是一项安全功能，如果禁用此功能，请确保启动完成后，不能再将其他模块加载到PulseAudio服务器中。建议在启用系统实例时禁用此功能。请注意，如果启用此选项，某些功能（如自动热插拔支持）将无法使用。采用布尔型参数，默认为yes。--disallow-module-loading命令行选项优先。

   allow-exit =
   允许/禁止根据用户请求退出。默认为是。

   resample-method =
   要使用的重采样算法。使用src-sinc最佳质量，src-sinc-中等质量，src-sinc最快，src-零阶保持，src-linear，琐碎，speex-float-N，speex-fixed-N中的一种，ffmpeg，soxr-mq，soxr-hq，soxr-vhq。分别参见libsamplerate和speex的文档以获取有关不同src-和speex-方法的说明。琐碎的方法是最基本的算法。如果您的CPU紧张，请考虑使用此功能。另一方面，它们的质量最差。Speex重采样器采用整数质量设置，范围为0..10（不好...好）。它们以两种形式存在：固定和浮动。前者使用定点数，后者使用浮点数。在大多数台式机CPU上，浮点重采样器要快得多，而且它的质量也稍好一些。soxr系列方法基于libsoxr，libsoxr是SoX声音处理实用程序中的重采样器库。mq变体在这三个中表现最佳。Soq开发人员认为，hq较为昂贵，并且被认为是每个样本最多16位音频的最佳选择。vhq变量比hq精度更高，并且更适合于较大的样本。与其他重新采样器（例如speex）相比，Soxr重新采样器通常在更少的CPU上提供更好的质量。缺点是它们会给输出增加明显的延迟（通常最多20毫秒左右，在极少数情况下会更长）。有关所有可用重采样器的完整列表，请参见dump-resample-methods的输出。默认为speex-float-1。--resample-method命令行选项优先。

   prevent-resampling =
   如果设置，请尝试配置设备以避免重新采样。这仅在支持重新配置其速率的设备上以及没有其他流正在播放或捕获音频的设备上起作用。该设备的配置速率也不会低于默认采样率和备用采样率。

   enable-remixing =
   如果禁用，则永远不会将通道上混或下混到不同的通道映射。而是仅进行简单的基于名称的匹配。默认为是。

   remixing-use-all-sink-channels =
   如果启用，则在重新混合时使用所有接收器通道。否则，请重新混合到再现所有源通道所需的最小接收器通道集。（这对LFE混音没有影响。）默认为是。

   enable-lfe-remixing =
   如果在上混或下混时禁用，则忽略LFE通道。禁用此选项后，仅当输入LFE通道可用时，输出LFE通道也将获得信号。如果没有输入LFE通道可用，则输出LFE通道将始终为0。如果没有输出LFE通道可用，则将忽略输入LFE通道上的信号。默认为否。

   lfe-crossover-freq = 
   LFE滤波器的交叉频率（以Hz为单位）。将其设置为0以禁用LFE滤波器。预设为0。

   use-pid-file =
   在运行时目录中创建PID文件（$XDG_RUNTIME_DIR/pulse/pid）。如果启用此功能，则可以使用--kill或--check之类的命令。如果您计划每个用户启动一个以上的PulseAudio进程，则最好禁用此选项，因为它实际上会禁用多个实例。采用布尔型参数，默认为yes。--use-pid-file命令行选项优先。

   cpu-limit =
   如果禁用，则即使在受支持的平台上也不要安装CPU负载限制器。在调试/分析PulseAudio以禁用干扰的SIGXCPU信号时，此选项很有用。
   接受布尔参数，默认为no。--no-cpu-limit命令行参数优先。

   system-instance =
   作为系统级实例运行守护程序，需要root特权。接受布尔参数，默认为no。--system命令行参数优先。

   local-server-type =
   如果不需要，请不要使用此选项！当前仅当您希望D-Bus客户端使用远程服务器时，此选项才有用。在将来的版本中可能会删除此选项。如果只想在系统模式下运行PulseAudio，请使用system-instance选项。此选项将用户，系统之一或不作为参数。这本质上是system-instance选项的副本。不同之处在于none选项，当您要将远程服务器与D-Bus客户端一起使用时，该选项很有用。如果同时定义了this和system-instance，则此选项优先。默认为设置的系统实例。

   enable-shm =
   启用通过POSIX或memfd共享内存的数据传输。采用布尔型参数，默认为yes。--disable-shm命令行参数优先。

   enable-memfd =
   启用memfd共享内存。采用布尔型参数，默认为yes。

   shm-size-bytes =
   设置守护程序的共享内存段大小（以字节为单位）。如果未指定或设置为0，它将默认为某些系统特定的默认值，通常为64 MiB。请注意，通常不需要更改此值，除非您运行的OS内核不执行内存过量使用。

   lock-memory =
   将整个PulseAudio进程锁定到内存中。当与实时调度结合使用时，这可能会增加drop-out安全性，但这会占用其他进程大量的内存，因此可能会大大降低系统速度。默认为否。

   flat-volumes =
   启用“平坦”音量，即，在可能的情况下，使接收器音量等于与其连接的输入的最大音量。采用布尔型参数，默认为yes。

```

# client.conf

# 命令

## pactl

| 命令                     | 说明           |
| ------------------------ | -------------- |
| pactl list modules short | 列出安装的模块 |
|                          |                |
|                          |                |

以下是一些常用的 `pactl` 命令，帮助你管理和调试 PulseAudio。

**1. 列出所有加载的模块**

```bash
pactl list modules
```

**2. 加载一个模块**

```bash
pactl load-module <module-name> [arguments]
# 示例：加载 ALSA 输出模块
pactl load-module module-alsa-sink device=hw:1,0
```

**3. 卸载一个模块**

```bash
pactl unload-module <module-id>
# 示例：卸载模块 ID 为 12 的模块
pactl unload-module 12
```

**4. 列出所有设备**

```bash
pactl list sinks          # 列出所有输出设备
pactl list sources        # 列出所有输入设备
pactl list sink-inputs    # 列出所有输出设备的输入流
pactl list source-outputs # 列出所有输入设备的输出流
```

**5. 设置默认设备**

```bash
pactl set-default-sink <sink-name>
pactl set-default-source <source-name>
# 示例：设置默认输出设备
pactl set-default-sink alsa_output.pci-0000_00_1b.0.analog-stereo
```

**6. 调整音量**

```bash
pactl set-sink-volume <sink-name> <volume>
pactl set-source-volume <source-name> <volume>
# 示例：将输出设备的音量设置为 50%
pactl set-sink-volume 0 50%
```

**7. 静音/取消静音**

```bash
pactl set-sink-mute <sink-name> <mute>
pactl set-source-mute <source-name> <mute>
# 示例：静音输出设备
pactl set-sink-mute 0 1
# 取消静音
pactl set-sink-mute 0 0
```

**8. 移动音频流**

```bash
pactl move-sink-input <sink-input-id> <sink-name>
pactl move-source-output <source-output-id> <source-name>
# 示例：将 sink-input 3 移动到 alsa_output.pci-0000_00_1b.0.analog-stereo
pactl move-sink-input 3 alsa_output.pci-0000_00_1b.0.analog-stereo
```

**9. 列出客户端和服务器信息**

```bash
pactl list clients   # 列出所有客户端
pactl info           # 显示服务器信息
```

**10. 重新加载 PulseAudio 配置**

```bash
pactl unload-module module-cli-protocol-unix && pactl load-module module-cli-protocol-unix
```

这些命令应该能帮助你更好地管理 PulseAudio。如果你有特定需求或问题，请告诉我！

## pacmd

`pacmd` 是 PulseAudio 的另一个命令行工具，用于与 PulseAudio 服务器交互。以下是一些常用的 `pacmd` 命令：

**1. 获取 PulseAudio 信息**

```bash
pacmd stat
```

**2. 列出所有加载的模块**

```bash
pacmd list-modules
```

**3. 加载和卸载模块**

```bash
# 加载模块
pacmd load-module <module-name> [arguments]
# 示例：加载 ALSA 输出模块
pacmd load-module module-alsa-sink device=hw:1,0

# 卸载模块
pacmd unload-module <module-id>
# 示例：卸载模块 ID 为 12 的模块
pacmd unload-module 12
```

**4. 列出所有设备**

```bash
pacmd list-sinks          # 列出所有输出设备
pacmd list-sources        # 列出所有输入设备
pacmd list-sink-inputs    # 列出所有输出设备的输入流
pacmd list-source-outputs # 列出所有输入设备的输出流
```

**5. 设置默认设备**

```bash
pacmd set-default-sink <sink-name>
pacmd set-default-source <source-name>
# 示例：设置默认输出设备
pacmd set-default-sink alsa_output.pci-0000_00_1b.0.analog-stereo
```

**6. 调整音量**

```bash
pacmd set-sink-volume <sink-name> <volume>
pacmd set-source-volume <source-name> <volume>
# 示例：将输出设备的音量设置为 50%
pacmd set-sink-volume 0 32768  # 32768 = 50% (65536 is 100%)
```

**7. 静音/取消静音**

```bash
pacmd set-sink-mute <sink-name> <mute>
pacmd set-source-mute <source-name> <mute>
# 示例：静音输出设备
pacmd set-sink-mute 0 1
# 取消静音
pacmd set-sink-mute 0 0
```

**8. 移动音频流**

```bash
pacmd move-sink-input <sink-input-id> <sink-name>
pacmd move-source-output <source-output-id> <source-name>
# 示例：将 sink-input 3 移动到 alsa_output.pci-0000_00_1b.0.analog-stereo
pacmd move-sink-input 3 alsa_output.pci-0000_00_1b.0.analog-stereo
```

**9. 列出客户端和服务器信息**

```bash
pacmd list-clients  # 列出所有客户端
pacmd info          # 显示服务器信息
```

**10. 重新加载 PulseAudio 配置**

```bash
pacmd unload-module module-cli-protocol-unix && pacmd load-module module-cli-protocol-unix
```

以下是一个简单的表格，列出了一些常用命令：

| **命令**                                 | **说明**                   |
| ---------------------------------------- | -------------------------- |
| `pacmd stat`                             | 获取 PulseAudio 服务器状态 |
| `pacmd list-modules`                     | 列出所有加载的模块         |
| `pacmd load-module <module-name>`        | 加载指定模块               |
| `pacmd unload-module <module-id>`        | 卸载指定模块               |
| `pacmd list-sinks`                       | 列出所有输出设备           |
| `pacmd list-sources`                     | 列出所有输入设备           |
| `pacmd list-sink-inputs`                 | 列出所有输出设备的输入流   |
| `pacmd list-source-outputs`              | 列出所有输入设备的输出流   |
| `pacmd set-default-sink <sink-name>`     | 设置默认输出设备           |
| `pacmd set-default-source <source-name>` | 设置默认输入设备           |
| `pacmd set-sink-volume <sink-name>`      | 设置输出设备音量           |
| `pacmd set-source-volume <source-name>`  | 设置输入设备音量           |
| `pacmd set-sink-mute <sink-name>`        | 静音/取消静音输出设备      |
| `pacmd set-source-mute <source-name>`    | 静音/取消静音输入设备      |
| `pacmd move-sink-input <id> <sink>`      | 移动音频流到指定输出设备   |
| `pacmd move-source-output <id> <source>` | 移动音频流到指定输入设备   |
| `pacmd list-clients`                     | 列出所有客户端             |
| `pacmd info`                             | 显示服务器信息             |

## pactl和pacmd关系

`pactl` 和 `pacmd` 是 PulseAudio 提供的两个命令行工具，用于管理和控制 PulseAudio 服务器。它们在功能上有一些重叠，但也有一些区别。

**1. pactl**

- **用途**：`pactl`（PulseAudio Control）==主要用于发送简单的控制命令==给 PulseAudio 服务器。
- **适用场景**：适合用于脚本中自动化管理和控制 PulseAudio，如调整音量、切换设备、加载/卸载模块等。
- **接口**：基于 PulseAudio 的命令协议，通过 UNIX 套接字与服务器通信。
- **常用命令**：`pactl list`、`pactl load-module`、`pactl set-sink-volume` 等。

**2. pacmd**

- **用途**：`pacmd`（PulseAudio Command Line Interface）==提供一个更高级的交互式命令行界面==，用于实时管理 PulseAudio 服务器。
- **适用场景**：适合调试和实时管理 PulseAudio，特别是需要详细信息和更复杂操作时。
- **接口**：直接与 PulseAudio 的内部命令接口通信，提供更强大的功能。
- **常用命令**：`pacmd list-sinks`、`pacmd set-default-sink`、`pacmd load-module` 等。

**关系和区别**

| **特性**     | **pactl**                                 | **pacmd**                      |
| ------------ | ----------------------------------------- | ------------------------------ |
| **适用场景** | 简单控制命令，适合脚本自动化              | 高级调试和管理，适合实时交互   |
| **接口**     | PulseAudio 命令协议，通过 UNIX 套接字通信 | PulseAudio 内部命令接口        |
| **交互方式** | 非交互式命令行工具，适合一次性命令        | 交互式命令行界面，适合实时操作 |
| **功能**     | 调整音量、切换设备、加载/卸载模块等       | 提供更多详细信息和高级操作     |
| **复杂度**   | 简单，适合常规操作                        | 复杂，适合调试和高级管理       |

**总结**

- **pactl**：适合需要简单控制和自动化操作的场景。
- **pacmd**：适合需要详细信息和高级管理的场景，尤其是在调试时非常有用。

如果你是开发者，并且已经有 ALSA 背景，可以根据具体需求选择使用 `pactl` 或 `pacmd`。对于简单的日常管理和脚本控制，`pactl` 可能更方便；而在需要深入调试和管理时，`pacmd` 会提供更强大的功能和更详细的信息。



# 启动和退出

少数情况下PulseAudio在启动X11时没有自动启动，可运行下面的命令启动：

```
$ pulseaudio --start
```

运行下面的命令可以终止PulseAudio：

```
$ pulseaudio --kill
```

正如之前所说, 如果用户安装了桌面环境，PulseAudio很可能通过 `/etc/X11/xinit/xinitrc.d/pulseaudio`文件或者 `/etc/xdg/autostart/`目录下的文件自动启动



Linux 下的音频框架实在让人吐槽无力，OSS、eSound、aRts、ALSA、PulseAudio……这回又冒出来一个 JACK，实在是把人折磨死了。

不过，Linux 发展到今天，PulseAudio 已经足够好用了，

作为普通用户，只要把 PulseAudio 安装上之后，使用默认配置就好，

基本不会再遇到过去常见的各种软件不出声的问题了。

JACK 是为专业音频处理设计的，对于普通日常使用而言，它并不好用。

如果你不打算在 Linux 下做音频相关处理的话，坚持用 PulseAudio 就好。



Linux的声音系统或许是最无序的子系统部分！

作为Server来说，声音无足轻重，无人问津，

而作为桌面来说太多的实现方案，各有各的长出和不足，

ALSA经过多年的发展，基本统一了Linux声卡硬件驱动层的借口，

OSS日渐退出，但是在ALSA之上的各个应用层面，方案和软件之多让人咋舌！

ESD，aRts, JACK,GStreamer, 这些系统组件各个为战，实现了不同的功能，

ESD是GNOME的声音服务器，

而aRts是KDE的，

JACK可以处理一些底层的应用，

GStreamer是GNOME平台比较新的Code和Decode的中间层，向声音服务器输送解码后的RAW Audio，

还有很多程序，比如Xine和Mplayer，他们的声音处理完全是独自完成的，从编解码到输出到ALSA驱动，应用程序全包办了，不需其他的中间层！

这就使整个声音系统显的极其复杂和杂乱无章！

PulseAudio（以前叫Polypaudio）是一个跨平台的，可通过网络工作的声音服务，其一般使用于Linux和FreeBSD操作系统。

它可以用来作为一种简易改进的开放声音后台（ESD）替换。

PulseAudio声音服务器试图以全新的架构来提供新的声音处理架构，希望能像ALSA统一底层那样一统声音应用领域！



简单地说，Android是用了一个Google自己开发的中间层API来让APP和声音驱动（ALSA或者HAL封闭驱动）通信的。在早期，它是个ALSA的插件；现在则命名为AudioFlinger。

无论是什么方式，实际上APP是以访问中间层API的方式让自己发出声音的，而这个API，却成了Android整个音频系统的噩梦。



虽然PulseAudio是开源软件，但开源不等于免费，PulseAudio很可能是针对企业收费的。

这里会导致一个两头难的问题：

大厂商不掏钱 就用，可能会吃官司；而用了，会导致一系列连锁反应，这个会在后面介绍。

小厂商可以完全不鸟什么商业授权，但是本身的孱弱的开发能力不足以对 Android做二次开发。



# 软件模块

以前都是在pulseaudio里。

后面也进行模块化。把比较独立的部分分离出来。

```
pulseaudio-alsa 提供alsa支持
pulseaudio-bluetooth 添加bluez支持
pulseaudio-equalizer 均衡器
pulseaudio-jack 
pulseaudio-lirc 红外支持
pulseaudio-zeroconf mdns零配置支持
```

pulseaudio的前端

```
gtk gui: paprefs/pavucontrol
音量控制器：pulseaudio-ctl / pavolume-git
命令行混音器：ponymix/pamixer
网页音量控制：PaWebControl
系统托盘图标：pasystray

```

增加 `load-module <module-name-from-list>` 到文件 `/etc/pulse/default.pa`就可以启用对应的模块。

支持的所有模块：

https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/

大多数X11环境会在启动X11会话时自动启动PulseAudio。

正如之前所说, 如果用户安装了桌面环境，PulseAudio很可能通过 `/etc/X11/xinit/xinitrc.d/pulseaudio`文件或者 `/etc/xdg/autostart/`目录下的文件自动启动





# 架构





参考资料

https://magodo.github.io/PulseAudio/

https://developer.rokid.com/docs/rokidos-linux-docs/porting/audio/overview.html

https://www.jianshu.com/p/f55e7634140b

# volume入手分析

volume功能简单直观。适合作为分析的切入点。

# 简介

PulseAudio是一种开源的音频服务器系统，旨在提供强大而灵活的音频管理功能。

它最初由Lennart Poettering和其他开发者开发，

作为Linux和其他类Unix系统上的默认音频架构。

PulseAudio的设计目标是处理多种音频任务，

包括音频播放、录制、混合和路由。

它提供了一个高级的音频系统，允许多个应用程序同时访问音频设备，并对音频进行实时处理。

以下是PulseAudio的一些主要特点：

1. **软件混音和路由**：PulseAudio允许多个应用程序同时播放和录制音频，它可以混合这些音频流并将它们路由到适当的输出设备。

2. **网络透明性**：PulseAudio支持音频通过网络进行传输，这意味着您可以在本地计算机上播放远程计算机的音频，或者将音频从一个设备传输到另一个设备。

3. **模块化架构**：PulseAudio的架构是模块化的，允许用户根据需要加载和卸载不同的模块，以扩展其功能。

4. **音频效果处理**：PulseAudio支持实时音频效果处理，例如均衡器、回声消除和压缩器等。

5. **支持插件和扩展**：PulseAudio提供了各种插件和扩展，可以与其他音频系统（如ALSA和OSS）以及各种音频设备进行集成。

总体而言，PulseAudio提供了一个强大的音频管理框架，使用户能够更好地控制和处理音频。它在许多Linux发行版和其他类Unix系统中得到广泛使用，并逐渐成为标准的音频解决方案。

# 发展历史

PulseAudio的发展历史可以追溯到2004年，

当时它作为一个名为"Polypaudio"的项目启动。

Polypaudio最初是为了解决Linux系统中音频管理的一些问题而创建的，

比如应用程序之间的音频冲突、音频设备的独占性以及音频延迟等。



随着时间的推移，Polypaudio逐渐发展成为PulseAudio，并在2007年正式更名为PulseAudio。

该项目得到了广泛的关注和采用，并成为许多Linux发行版的默认音频架构，如Ubuntu、Fedora和Debian等。



==PulseAudio的发展受益于其灵活的架构和功能扩展性，==

允许开发者和社区为其添加新的功能和模块。

==它逐渐成为许多桌面环境的首选音频解决方案==，如GNOME和KDE等。



然而，在早期版本中，PulseAudio也面临了一些挑战和争议。一些用户报告了与特定硬件和应用程序的兼容性问题，并指出了一些性能和稳定性方面的困扰。然而，随着时间的推移，PulseAudio团队通过更新和改进不断解决了这些问题，并逐渐提升了其可靠性和功能性。



目前，PulseAudio仍然是许多Linux发行版的默认音频系统，并且在Linux桌面和嵌入式系统上广泛使用。它继续发展和演进，为用户提供更好的音频管理和处理功能。

# arch wiki的内容

默认情况下，PulseAudio 配置为自动检测所有声卡并对其进行管理。

它控制所有检测到的ALSA设备，并将所有音频流重定向到自身，

使PulseAudio守护程序成为中央配置点。

守护程序应该基本上是开箱即用的，只需要一些小的调整。



虽然PulseAudio通常开箱即用，只需要最少的配置，

但高级用户可以通过更改默认配置文件以禁用模块或从头开始编写自己的模块来更改守护程序的几乎每个方面。



PulseAudio作为服务器守护程序运行，

可以使用客户端/服务器体系结构在系统范围内运行或基于每个用户运行。



守护程序本身除了提供 API 和主机动态加载的模块之外，没有模块，什么都不做。

音频路由和处理任务都由各种模块处理，

包括PulseAudio的原生协议本身（由[module-native-protocol-unix](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/#index22h3)提供）。



客户端通过许多协议模块之一到达服务器，

这些模块将接受来自外部源的音频，通过PulseAudio路由它，并最终让它通过最后的其他模块出去。



输出模块不必是实际的声音输出：它可以将流转储到文件中，将其流式传输到[Icecast](https://wiki.archlinuxcn.org/wzh/index.php?title=Icecast&action=edit&redlink=1)等广播服务器，甚至只是丢弃它。



您可以在[Pulseaudio Loadable Modules](https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/)模块上找到所有可用模块的详细列表。



要启用它们，您只需向 `~/.config/pulse/default.pa` 中添加一行 `load-module *module-name-from-list*` 即可。



参考资料

1、

https://wiki.archlinuxcn.org/wiki/PulseAudio



# 竞争者PipeWire

PulseAudio与新出现的[PipeWire](https://zh.wikipedia.org/wiki/PipeWire)竞争，后者提供了一个兼容PulseAudio的服务组件（称为pipewire-pulse），PipeWire现在被许多Linux发行版默认采用以替换PulseAudio，包括[Fedora Linux](https://zh.wikipedia.org/wiki/Fedora_Linux)、[Ubuntu](https://zh.wikipedia.org/wiki/Ubuntu)和[Debian](https://zh.wikipedia.org/wiki/Debian)[[5\]](https://zh.wikipedia.org/wiki/PulseAudio#cite_note-5)[[6\]](https://zh.wikipedia.org/wiki/PulseAudio#cite_note-6)[[7\]](https://zh.wikipedia.org/wiki/PulseAudio#cite_note-7)。



开发版本的最新每日构建（代号为“Kinetic Kudu”）使用 Pipewire 代替了开箱即用的 Pulseaudio，

无需解决方法。 

Ubuntu 上次对其音频堆栈进行重大更改（恰如其分地）是在最后一个以“K”命名的版本 Ubuntu 9.10“Karmic Koala”中。



Ubuntu 在采用下一代声音服务器技术方面落后于其发行版竞争对手。 

PipeWire 的起源可以追溯到 2015 年。

该技术最初被构想为“用于视频的 PulseAudio”，但后来扩展到包括音频流。 

==Fedora 在 2021 年默认采用了该技术，其他桌面 Linux 发行版很快也纷纷效仿。==

从技术上讲，Ubuntu 已经包含了 PipeWire。 

Ubuntu 22.04 LTS 附带在默认映像上安装了 PipeWire 和 PulseAudio。

然而，前一个堆栈仅用于视频（主要是为了 Wayland 兼容性），而后者仍然负责音频职责。



除了“较新”且正在积极开发之外，PipeWire 还为 Ubuntu 桌面带来了许多好处。

据报道，这种实现的错误更少，硬件兼容性更好，CPU 使用率更低，代码库更现代。



许多 Linux 用户表示，与 PulseAudio 相比，现代蓝牙音频设备（例如 Apple Air Pods）在使用 PipeWire 时往往会“正常工作”。



目前尚不清楚 WirePlumber（PipeWire 的流行会话和策略管理器）是否也会进入 Ubuntu，但由于 PipeWire 独立运行并不是严格必要的，因此这只是一个小细节。更新：WirePlumber 现已上线！



https://www.omgubuntu.co.uk/2022/05/ubuntu-22-10-makes-pipewire-default

# 模块有哪些



https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/Modules/

# 模块编写

要编写一个模块，你必须得实现下面两个函数

```
int pa_init(pa_module* m);

void pa_done(pa_module* m);
```

看函数名称就可以知道

pa_init是在做初始化的工作，这个函数在load-module的时候被调用。

pa_done做一些资源释放的工作，在module被卸载的时候调用。


https://blog.csdn.net/cgipro/article/details/5703963

# 设计与实现

## 对象系统

| 对象      | 说明                                                         |
| --------- | ------------------------------------------------------------ |
| pa_object | 基础类。<br />refcnt。<br />free函数。<br />char *的类型<br />类型匹配函数。就这些东西。 |
|           | 配套的函数：<br />pa_object_new<br />pa_object_free<br />pa_object_ref<br />pa_object_unref<br />PA_DECLARE_PUBLIC_CLASS<br />PA_DEFINE_PUBLIC_CLASS<br />PA_DEFINE_PRIVATE_CLASS |
|           |                                                              |

https://www.jianshu.com/p/f55e7634140b

# 用户手册

https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/User/

# 开发手册



https://www.freedesktop.org/wiki/Software/PulseAudio/Documentation/Developer/

https://freedesktop.org/software/pulseaudio/doxygen/

# 嵌入式使用pulseaudio

https://blog.csdn.net/pengrui18/article/details/53747562

# 怎样支持蓝牙播放的

src\modules\bluetooth

这里是对应的代码。



# 参考资料

1、

https://blog.csdn.net/qq_42138566/article/details/108626378

2、

https://wiki.archlinux.org/title/PulseAudio_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

3、

http://edyfox.codecarver.org/html/jack_alsa_pulse_walkthrough.html

4、

https://www.liangzl.com/get-article-detail-184781.html

5、

https://www.linuxidc.com/Linux/2019-02/156865.htm

6、Android音频系统的改进设想和展望 PulseAudio介绍

https://blog.csdn.net/landishu/article/details/39481123

7、关于pulseaudio的一些总结

https://blog.csdn.net/cgipro/article/details/6089422