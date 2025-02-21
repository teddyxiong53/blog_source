---
title: 音频之jack
date: 2019-06-20 16:48:37
tags:
	- 音频
---

--

在Linux的音频架构里，为了混音，一般是有一个音频守护进程。

例如pulseaudio就是这样一个守护进程。

jackd也是一个类似的程序。但是是对于音乐制作这种专业场景的。

当前我的笔记本上，默认运行了pulseaudio。

jackd也是安装了的。如果没有安装，这样安装：

```
sudo apt-get install jackd 
```

还需要安装另外一个软件：

```
sudo apt-get install qjackctl
```

你需要把自己添加到audio这个组。

查看自己当前在哪些组里。

```
$ groups teddy
teddy : teddy adm dialout cdrom sudo dip plugdev lpadmin sambashare
```

并没有在audio这个组里。

加入到这个组。

```
sudo usermod -a -G audio teddy
```

还需要注销一下才能生效。

# 和pulseaudio的共存

当你启动jackd之后，声卡就被jackd独占了。

而你的浏览器等的声音，是靠pulseaudio来工作的。pulseaudio是gnome桌面默认的声音服务器。

需要想办法让jackd跟pulseaudio共存。

```
sudo apt-get install pulseaudio-module-jack
```



# 简介

### Jack2 代码框架分析

#### 1. 概述
Jack2 是一个开源的音频服务器，支持低延迟音频处理，广泛应用于专业音频和音乐制作。它是 Jack Audio Connection Kit (JACK) 的继任者，提供了更高的性能和更好的跨平台支持。

#### 2. 代码结构
Jack2 的代码结构主要分为以下几个部分：

- **核心库 (`libjack`)**: 提供音频处理的核心功能。
- **服务器 (`jackd`)**: 负责管理音频设备和客户端连接。
- **客户端库 (`libjackclient`)**: 提供客户端应用程序与服务器通信的接口。
- **工具和实用程序**: 包括命令行工具和 GUI 工具，用于管理和监控 JACK 服务器。

#### 3. 核心库 (`libjack`)
核心库是 Jack2 的核心部分，负责音频流的处理和管理。主要模块包括：

- **音频缓冲区管理**: 管理音频数据的缓冲区，确保低延迟和高效率。
- **端口管理**: 管理音频输入输出端口，支持多通道音频。
- **客户端管理**: 管理连接到服务器的客户端，处理客户端的请求和事件。
- **时间管理**: 提供精确的时间管理功能，确保音频同步。

#### 4. 服务器 (`jackd`)
服务器是 Jack2 的核心组件，负责与音频硬件交互，并管理客户端连接。主要功能包括：

- **音频设备管理**: 支持多种音频设备，包括 ALSA、CoreAudio、PortAudio 等。
- **客户端连接管理**: 管理客户端的连接和断开，处理客户端的请求。
- **实时调度**: 提供实时调度功能，确保音频处理的低延迟。

#### 5. 客户端库 (`libjackclient`)
客户端库提供了一组 API，供客户端应用程序与 JACK 服务器通信。主要功能包括：

- **端口创建和管理**: 客户端可以创建和管理音频端口。
- **音频数据处理**: 客户端可以读取和写入音频数据。
- **事件处理**: 客户端可以注册回调函数，处理服务器事件。

#### 6. 工具和实用程序
Jack2 提供了一些工具和实用程序，用于管理和监控 JACK 服务器：

- **`jack_control`**: 命令行工具，用于启动、停止和管理 JACK 服务器。
- **`qjackctl`**: GUI 工具，提供图形界面管理 JACK 服务器和连接。
- **`jack_lsp`**: 列出当前 JACK 服务器的端口和连接。

#### 7. 编译和安装
Jack2 使用 `waf` 构建系统进行编译和安装。主要步骤包括：

1. **配置**: 运行 `./waf configure` 配置编译选项。
2. **编译**: 运行 `./waf build` 编译代码。
3. **安装**: 运行 `./waf install` 安装编译后的二进制文件和库。

#### 8. 开发资源
- **代码仓库**: [Jack2 GitHub 仓库](https://github.com/jackaudio/jack2)
- **社区支持**: [Jack Audio 邮件列表](https://lists.linuxaudio.org/listinfo/jack-devel)

#### 9. 总结
Jack2 是一个功能强大且灵活的音频服务器，适用于专业音频和音乐制作。通过分析其代码框架，可以更好地理解其工作原理和实现细节，为开发和定制提供基础。

# net和netone的区别

`net` 和 `netone` 是 JACK 中用于网络音频传输的两种不同后端（backend）。它们的设计目标和实现方式有所不同，适用于不同的场景。以下是它们的详细对比和关系说明：

---

### 1. **`net` 后端**
   - **设计目标**：
     - `net` 后端是 JACK 的原始网络音频实现，支持多客户端连接和复杂的音频路由。
     - 它允许多个 JACK 客户端通过网络连接到一个 JACK 服务器，并共享音频数据。
   - **特点**：
     - 支持多对多连接：多个发送端和接收端可以同时连接。
     - 灵活性高：可以配置多个输入/输出通道和复杂的路由。
     - 延迟较高：由于设计复杂，延迟通常比 `netone` 高。
     - 配置复杂：需要手动设置输入/输出端口数量和缓冲区大小。
   - **适用场景**：
     - 需要多客户端连接的复杂音频网络。
     - 专业音频制作环境，如分布式音频处理。

---

### 2. **`netone` 后端**
   - **设计目标**：
     - `netone` 后端是 JACK 的简化网络音频实现，专注于低延迟和简单的一对一连接。
     - 它专门用于在两个 JACK 实例之间传输音频数据，适合点对点的音频传输。
   - **特点**：
     - 一对一连接：只支持一个发送端和一个接收端。
     - 低延迟：设计简单，延迟通常比 `net` 低。
     - 配置简单：无需手动设置端口数量和缓冲区大小。
     - 灵活性较低：不支持多客户端连接或复杂路由。
   - **适用场景**：
     - 简单的点对点音频传输。
     - 需要低延迟的实时音频应用，如现场表演或远程录音。

---

### 3. **`net` 和 `netone` 的关系**
   - **共同点**：
     - 两者都基于 JACK 的网络音频协议，用于通过网络传输音频数据。
     - 都需要在发送端和接收端分别启动 JACK，并配置网络连接。
   - **区别**：
     - `net` 支持多客户端连接和复杂路由，适合专业音频网络。
     - `netone` 专注于低延迟和简单的一对一连接，适合点对点传输。
   - **选择建议**：
     - 如果需要连接多个设备或进行复杂的音频路由，选择 `net`。
     - 如果只需要在两个设备之间传输音频，并且对延迟要求较高，选择 `netone`。

---

### 4. **配置示例**
#### 使用 `net` 后端
- **接收端**：
  ```bash
  jackd -d net -l 4 -i 2 -o 2 -C 2 -P 2 -p 2048
  ```
- **发送端**：
  ```bash
  jackd -d net -l 4 -i 2 -o 2 -C 2 -P 2 -p 2048 -H <接收端IP地址>
  ```

#### 使用 `netone` 后端
- **接收端**：
  ```bash
  jackd -d netone
  ```
- **发送端**：
  
  ```bash
  jackd -d netone -H <接收端IP地址>
  ```

---

### 5. **性能对比**
| 特性       | `net` 后端   | `netone` 后端  |
| ---------- | ------------ | -------------- |
| 连接方式   | 多对多       | 一对一         |
| 延迟       | 较高         | 较低           |
| 配置复杂度 | 复杂         | 简单           |
| 适用场景   | 复杂音频网络 | 点对点音频传输 |

---

### 6. **总结**
- `net` 和 `netone` 是 JACK 中两种不同的网络音频后端，分别适用于复杂音频网络和简单点对点传输。
- 如果你的场景需要低延迟和简单配置，选择 `netone`。
- 如果需要多客户端连接和复杂路由，选择 `net`。

根据你的需求选择合适的后端，并按照上述配置示例进行设置即可。如果有更多问题，欢迎继续讨论！

# jack的各种工具

是在这里：

example-clients\wscript

```
jack_alias                  jack_net_master
jack_bufsize                jack_net_slave
jack_connect                jack_netsource
jack_control                jack_property
jack_cpu                    jack_rec
jack_cpu_load               jack_samplerate
jack_disconnect             jack_server_control
jack_evmon                  jack_session_notify
jack_freewheel              jack_showtime
jack_iodelay                jack_simdtests
jack_latent_client          jack_simple_client
jack_load                   jack_simple_session_client
jack_lsp                    jack_test
jack_metro                  jack_thru
jack_midi_dump              jack_transport
jack_midi_latency_test      jack_unload
jack_midiseq                jack_wait
jack_midisine               jack_zombie
jack_monitor_client         jackd
jack_multiple_metro
```



# jackd的参数

```

Usage: jackdmp [ --no-realtime OR -r ]
               [ --realtime OR -R [ --realtime-priority OR -P priority ] ]
      (the two previous arguments are mutually exclusive. The default is --realtime)
               [ --name OR -n server-name ]
               [ --timeout OR -t client-timeout-in-msecs ]
               [ --loopback OR -L loopback-port-number ]
               [ --port-max OR -p maximum-number-of-ports]
               [ --slave-backend OR -X slave-backend-name ]
               [ --internal-client OR -I internal-client-name ]
               [ --internal-session-file OR -C internal-session-file ]
               [ --verbose OR -v ]
               [ --clocksource OR -c [ h(pet) | s(ystem) ]
               [ --autoconnect OR -a <modechar>]
                 where <modechar> is one of:
                   ' ' - Don't restrict self connect requests (default)
                   'E' - Fail self connect requests to external ports only
                   'e' - Ignore self connect requests to external ports only
                   'A' - Fail all self connect requests
                   'a' - Ignore all self connect requests
               [ --replace-registry ]
               [ --silent OR -s ]
               [ --sync OR -S ]
               [ --temporary OR -T ]
               [ --version OR -V ]
         -d master-backend-name [ ... master-backend args ... ]
       jackdmp -d master-backend-name --help
             to display options for each master backend

Available backends:
      alsa (master)
      alsarawmidi (slave)
      dummy (master)
      loopback (slave)
      net (master)
      netone (master)
      proxy (master)

Available internals:
      audioadapter
      netadapter
      netmanager
      profiler
```

## -d alsa的参数

```
# jackd -d alsa --help
jackdmp 1.9.14
Copyright 2001-2005 Paul Davis and others.
Copyright 2004-2016 Grame.
Copyright 2016-2019 Filipe Coelho.
jackdmp comes with ABSOLUTELY NO WARRANTY
This is free software, and you are welcome to redistribute it
under certain conditions; see the file COPYING for details
        -d, --device    ALSA device name (default: hw:0)
        -C, --capture   Provide capture ports.  Optionally set device (default: none)
        -P, --playback  Provide playback ports.  Optionally set device (default: none)
        -r, --rate      Sample rate (default: 48000)
        -p, --period    Frames per period (default: 1024)
        -n, --nperiods  Number of periods of playback latency (default: 2)
        -H, --hwmon     Hardware monitoring, if available (default: false)
        -M, --hwmeter   Hardware metering, if available (default: false)
        -D, --duplex    Provide both capture and playback ports (default: true)
        -s, --softmode  Soft-mode, no xrun handling (default: false)
        -m, --monitor   Provide monitor ports for the output (default: false)
        -z, --dither    Dithering mode (default: n)
        -i, --inchannels        Number of capture channels (defaults to hardware max) (default: 0)
        -o, --outchannels       Number of playback channels (defaults to hardware max) (default: 0)
        -S, --shorts    Try 16-bit samples before 32-bit (default: false)
        -I, --input-latency     Extra input latency (frames) (default: 0)
        -O, --output-latency    Extra output latency (frames) (default: 0)
        -X, --midi-driver       ALSA MIDI driver (default: none)
```

## -d net的参数

```
# jackd -d net --help
jackdmp 1.9.14
Copyright 2001-2005 Paul Davis and others.
Copyright 2004-2016 Grame.
Copyright 2016-2019 Filipe Coelho.
jackdmp comes with ABSOLUTELY NO WARRANTY
This is free software, and you are welcome to redistribute it
under certain conditions; see the file COPYING for details
        -a, --multicast-ip      Multicast address, or explicit IP of the master (default: 225.3.19.154)
        -p, --udp-net-port      UDP port (default: 19000)
        -M, --mtu       MTU to the master (default: 1500)
        -C, --input-ports       Number of audio input ports. If -1, audio physical input from the master (default: -1)
        -P, --output-ports      Number of audio output ports. If -1, audio physical output from the master (default: -1)
        -i, --midi-in-ports     Number of MIDI input ports. If -1, MIDI physical input from the master (default: -1)
        -o, --midi-out-ports    Number of MIDI output ports. If -1, MIDI physical output from the master (default: -1)
        -n, --client-name       Name of the jack client (default: 'hostname')
        -s, --auto-save         Save/restore connection state when restarting (default: false)
        -l, --latency   Network latency (default: 5)
```



这篇文章不错。

https://www.cnblogs.com/daochenshi/p/4389797.html



关于jack网络音频的，目前整理了这几条命令。

还不能工作，但是至少可能需要这些命令。

```
===========sender：

jackd -d net -a 10.28.70.125 &
jack_load netmanager 

alsa_in -j jack_in -d hw:0,1 -c 2 

============receiver：
jackd -d alsa -d hw:0,1 -r 48000 &
jack_load netadapter


jack_connect netadapter:capture_1 system:playback_1
jack_connect netadapter:capture_2 system:playback_2

```

https://manpages.debian.org/buster/jackd2/



http://www.orford.org/assets/jack-idiots_guide.txt

音频质量：----------------- Jackd 专为挑剔的音频使用而设计，没有音频质量问题。它全程使用 32 位浮点数，这被认为对于绝大多数工作来说是足够的。

在时间精度方面，由于音频处理的阻塞性质，事件时间可能最多偏差 10 毫秒（4096，44.1k），例如在速度变化的情况下。

延迟：-------- 在大多数情况下，Jackd 提供的延迟与竞争系统相当或更好。针对 2.6 内核的最新补丁可以实现大约 1ms 的延迟，这超过了内置声卡的延迟。这个往返声卡延迟可以高达 4ms。相比之下，你离扬声器每远一米，就会增加 3ms 的延迟。

典型 Jackd 延迟约为 6 毫秒。这是针对一个包含 2 个周期，每个周期大小为 128，运行在 44.1kHz 的系统。

可扩展性：------------ 由于上下文切换，随着客户端数量的增加，开销也在不断增加。提到 20 个客户端作为一个大致的最大值。这可能是某些用途（如构建模块化合成器）的一个实际限制。

多张声卡：-------------------- 如果它们同步在一起，同一台机器上的多张卡可以一起使用。这可以通过使用中央晶振时钟或通过从一个卡向另一个卡提供数字音频输入并将其置于从模式来实现。为了让 Jack 访问它们，必须使用 alsa 配置文件将它们抽象为单个'设备'。

多台 Jack 服务器：---------------------- 现在可以在同一台机器上同时运行多个服务器，使用不同的声卡。没有任何同步，每个服务器都有自己的独立进程图和传输状态。单个客户端应用程序可以访问每个服务器。可以使用 Netjack 或 jack_diplomat 在它们之间路由信号。

# netjack2

这个文档写得还算详细。

https://github.com/jackaudio/jackaudio.github.com/wiki/WalkThrough_User_NetJack2

```
jack_load netmanager -i "-h"
```

这样-i来传递参数，查看对应的帮助信息。

想象一下，你拥有两台计算机（Linux、OSX、Windows 或 Solaris），

它们在音频方面完全运行。

你在第一台计算机上运行你最喜欢的合成器、采样器和其它设备，它拥有快速的处理器和大量的内存；

然后在另一台计算机上启动你最喜欢的音频/MIDI 编曲软件，这台计算机拥有大容量硬盘和优秀的音频硬件。

你可能想知道，我该如何将这两套系统连接起来，而不需要任何音频线路或数字/模拟转换？

Netjack2 基于主/从通信。

一个主节点可以处理多个从节点。

实际上，一个独立的软件元素管理所有从节点。

这个元素被称为网络管理器，是您必须启动以激活 Netjack2 的唯一东西。

在从节点方面，您只需启动一个经典的 jack 服务器。

唯一的区别是这个服务器将以"net"后端启动。

这意味着驱动程序不是像 ALSA、coreaudio 等其他音频硬件驱动程序，而是一个直接处理网络的驱动程序。



Netjack2 基于 Jackmp，

因此服务器可以以两种运行模式运行后端：同步或异步。

在同步模式下，数据在图执行后立即写入驱动程序的输出端口。

这意味着计算出的数据可以直接在当前周期结束时可用。

因此，在 Netjack2 中，数据只是直接发送回主节点，没有额外的延迟。

如果你在从节点上创建一个循环（简单地将驱动程序的输出连接到输入），你将在同一周期内将音频流返回到主节点。

作为补偿，主节点必须在其自己的进程中等待这些流。

在同步模式下，主节点在其进程中阻塞，直到从节点发送数据。



发送数据通过网络意味着额外的延迟。

让我们尝试在这个情况下量化它... 

我们在这里讨论的是网络带宽，这是网络一次能携带的数据量。

如果我们以一个音频周期作为时间单位，

我们就有一种网络音频带宽，

以每周期字节数表示。

这意味着如果我们有一个每音频周期 500k 字节的网络音频带宽，

而我们只有 500k 字节的数据要发送到这个网络上，发送这 500k 字节将占用所有的时间单位，即所有的音频周期持续时间。

这意味着我们有一个额外的网络延迟，可以达到一个音频周期。



需要两台具有网络功能的计算机（Linux、Macosx 或 Windows）（100Mbit/s 是一个良好的起点）。

Netjack2 需要一个 UDP 端口（默认为 19000），

还需要多播网络（默认 IP 为 225.3.19.154），

因此首先检查您的网络设备不会阻止多播或过滤 UDP。

这一点非常重要，您的防火墙不要阻止您使用的 ICMP 消息或 UDP 端口。

阻止 ICMP 会使系统在出现网络故障（物理断开或严重网络错误）时无法做出反应。

Netjack2 使用低级错误检测以保持实时行为。

我们不能使用基于确认和其他事物的整个系统连接错误检测，这就是为什么我们只在网络操作（发送或接收）失败时检测连接故障。阻止 ICMP 会禁用检测此类错误的网络操作功能。



无线和互联网使用不受支持，因为它们不能被视为实时。

在 Netjack 中，您可以设置额外的延迟，这允许您防止由于使用具有某种随机投递的网络（如无线或互联网网络）而导致的较大传输延迟。

Netjack2 目前不包括此功能。这就是我们推荐使用经典有线网络的原因。



网络管理器是一个将在服务器进程空间中运行的内部客户端。一旦您的 Jack 服务器启动，只需用以下方式加载网络管理器：

```
 jack_load netmanager
```


这将加载网络管理器到您的 JACK 服务器中。这就是您需要做的全部。您不需要设置任何名称或参数。

如果您需要，出于特别原因设置另一个组播地址或 UDP 端口，可以使用：

```
  jack_load netmanager -i "-a xxx.xxx.xxx.xxx -p port"
```

# jack2源代码分析

https://github.com/jackaudio/jackaudio.github.com/wiki/jack2-source-code-guide



# 一个windows的网络问题

https://github.com/jackaudio/jack2/issues/336

我在 Windows 上也有同样的问题，这似乎与 Windows 特有的网络怪异现象有关，但我还没有确切地定位到。例如，禁用 Windows 防火墙甚至不能纠正这个问题。我确实在 Wireshark 中验证了从从机发出的多播数据包已经到达主节点，但看起来它们并没有被传递给 jackd 进程。
我通过不在从节点（ `jackd -R -d net -a $MASTER_IP` ）上使用多播来解决这个问题。

# 参考资料

1、关于linux音频JACK的那些事情……

https://blog.csdn.net/zhang_danf/article/details/25405381

2、漫谈Linux下的音频问题

https://www.cnblogs.com/little-ant/p/4016172.html