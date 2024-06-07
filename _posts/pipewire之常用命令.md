---
title: pipewire之常用命令
date: 2024-05-27 14:42:17
tags:
	- 音频

---

--

# pipewire的核心进程

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



# 常用 PipeWire 命令

| 命令          | 描述                                                |
| ------------- | --------------------------------------------------- |
| `pw-cli`      | PipeWire 通用命令行工具，用于与 PipeWire 管道交互。 |
| `pw-play`     | 播放音频文件。                                      |
| `pw-record`   | 录制音频到文件。                                    |
| `pw-dump`     | 输出当前 PipeWire 的所有对象信息。                  |
| `pw-top`      | 类似 `top` 的工具，显示 PipeWire 的实时状态。       |
| `pw-cat`      | 从输入设备捕获音频并输出到标准输出。                |
| `pw-link`     | 管理 PipeWire 节点之间的链接。                      |
| `pw-profiler` | 显示实时性能数据。                                  |
| `pw-dump`     | 生成 PipeWire 当前状态的 JSON 转储。                |
| `pw-jack`     | 提供 JACK 兼容层的命令，用于与 JACK 客户端交互。    |

## 具体命令及其使用示例

### 1. `pw-cli`

`pw-cli` 是与 PipeWire 交互的通用工具。

- 查看所有节点信息：

  ```sh
  pw-cli info all
  ```

- 列出所有节点：

  ```sh
  pw-cli list Node
  ```

- 获取特定节点的信息：

  ```sh
  pw-cli info <node-id>
  ```

### 2. `pw-play`

`pw-play` 用于播放音频文件。

- 播放音频文件：

  ```sh
  pw-play path/to/audiofile.wav
  ```

- 使用特定设备播放音频：

  ```sh
  pw-play --target <device-id> path/to/audiofile.wav
  ```

### 3. `pw-record`

`pw-record` 用于录制音频到文件。

- 录制音频到文件：

  ```sh
  pw-record output.wav
  ```

- 从特定设备录制音频：

  ```sh
  pw-record --target <device-id> output.wav
  ```

### 4. `pw-dump`

`pw-dump` 用于生成当前 PipeWire 状态的 JSON 文件。

- 生成 PipeWire 状态转储：

  ```sh
  pw-dump > pipewire-dump.json
  ```

### 5. `pw-top`

`pw-top` 显示 PipeWire 的实时状态，类似 `top` 命令。

- 显示实时状态：

  ```sh
  pw-top
  ```

### 6. `pw-cat`

`pw-cat` 从输入设备捕获音频并输出到标准输出。

- 捕获音频并保存到文件：

  ```sh
  pw-cat > output.raw
  ```

- 使用特定设备捕获音频：

  ```sh
  pw-cat --target <device-id> > output.raw
  ```

### 7. `pw-link`

`pw-link` 用于管理 PipeWire 节点之间的链接。

- 列出所有链接：

  ```sh
  pw-link -i
  pw-link -o
  ```

- 创建链接：

  ```sh
  pw-link <output-node-id> <input-node-id>
  ```

- 删除链接：

  ```sh
  pw-link -d <output-node-id> <input-node-id>
  ```



# pw-loopback

pw-loopback 程序是一个 PipeWire 客户端，它使用 PipeWire 环回模块创建环回节点，并通过命令行选项进行配置。

`pw-loopback` 是 PipeWire 中用于创建环回（loopback）设备的工具。

它可以将一个音频源的输出连接到另一个音频源的输入，从而实现音频的环回。

例如，你可以将麦克风的输入环回到扬声器的输出，

或者将应用程序的音频输出环回到另一个应用程序的音频输入。

创建一个loopback设备，自动连接到speaker

```
$ pw-loopback -m '[[FL FR]]' --capture-props='[media.class=Audio/Sink]'
```

创建一个loopback设备，自动连接到mic

```
$ pw-loopback -m '[[FL FR]]' --playback-props='[media.class=Audio/Source]'
```

创建一个dummy的loopback设备，不会自动连接到任何东西。

```
$ pw-loopback -m '[[FL FR]]' --capture-props='[media.class=Audio/Sink]' --playback-props='[media.class=Audio/Source]'
```

创建一个loopback设备，自动连接到speaker，并且交换左右声道。

```
$ pw-loopback --capture-props='[media.class=Audio/Sink audio.position=[FL FR]]' --playback-props='[audio.position=[FR FL]]'
```

创建一个loopback设备，自动连接到mic，并且交换左右声道。

```
$ pw-loopback --capture-props='[audio.position=[FR FL]]' --playback-props='[media.class=Audio/Source audio.position=[FL FR]]'
```

参考资料

1、

https://linuxcommandlibrary.com/man/pw-loopback

# pw-config

从效果看，就是查看配置文件的位置。

```
# pw-config 
{
  "config.path": "/usr/share/pipewire/pipewire.conf",
  "override.2.0.config.path": "/etc/pipewire/pipewire.conf.d/10-wireplumber.conf"
}
```

看代码里的写法，这个是因为默认查看的name是pipewire.conf。所以是上面的效果。

可以指定-n名字。

```
pw-config -n pipewire-pulse.conf
{
  "config.path": "/usr/share/pipewire/pipewire-pulse.conf"
}
```

还可以list

```
# pw-config -n pipewire-pulse.conf list
{
  "config.name": "pipewire-pulse.conf",
  "config.path": "/usr/share/pipewire/pipewire-pulse.conf",
  "context.properties": {
    ## Configure properties in the system.
    #mem.warn-mlock  = false
    #mem.allow-mlock = true
    #mem.mlock-all   = false
    #log.level       = 2

    #default.clock.quantum-limit = 8192
},
  "context.spa-libs": {
    audio.convert.* = audioconvert/libspa-audioconvert
    support.*       = support/libspa-support
},

```

# pw-metadata

pw-metadata -l

```
# pw-metadata -l
Found "settings" metadata 31
Found "default" metadata 37
Found "route-settings" metadata 38
```



```
pw-metadata -n settings                  # list settings
pw-metadata -n settings 0                # list server settings
pw-metadata -n settings 0 log.level 2    # modify a server setting
```



```
# pw-metadata -n settings
Found "settings" metadata 30
update: id:0 key:'log.level' value:'2' type:''
update: id:0 key:'clock.rate' value:'48000' type:''
update: id:0 key:'clock.allowed-rates' value:'[ 48000 ]' type:''
update: id:0 key:'clock.quantum' value:'1024' type:''
update: id:0 key:'clock.min-quantum' value:'32' type:''
update: id:0 key:'clock.max-quantum' value:'2048' type:''
update: id:0 key:'clock.force-quantum' value:'0' type:''
update: id:0 key:'clock.force-rate' value:'0' type:''
```



# pw-cat

pw-cat 是一个简单的工具，

用于在 PipeWire 服务器上播放或捕获原始或编码的媒体文件。

它理解 libsndfile 支持的所有音频文件格式，用于 PCM 捕获和播放。

捕获 PCM 时，文件扩展名用于猜测文件格式，默认为 WAV 文件格式。

它理解用于播放和录音的标准 MIDI 文件。

该工具不会渲染 MIDI 文件，它只会使 MIDI 事件可用于图表。

您需要 MIDI 渲染器（例如 qsynth、timidity 或硬件 MIDI 渲染器）才能听到 MIDI。

DSF 文件格式支持 DSD 播放。该工具仅适用于支持 DSD 的原生硬件，并且在未找到此类硬件时会产生错误。

当 FILE 为 - 时，输入和输出将分别是来自 STDIN 和 STDOUT 的原始数据。

# pw-cli

与 PipeWire 实例交互。

当给出命令时，pw-cli 将执行该命令并退出

如果未给出命令，pw-cli 将启动与默认 PipeWire 实例 pipeline-0 的交互式会话。

可以连接到其他远程实例。提示符下会显示当前实例名称。

请注意，pw-cli 还会创建本地 PipeWire 实例。有些命令在当前（远程）实例上运行，有些命令在本地实例上运行，例如模块加载。



# spa-acp-tool 

用于执行 ALSA 卡配置文件探测代码的调试工具，无需运行 PipeWire。

可用于调试 PipeWire 的 ALSA 卡配置文件功能不正确的问题。

这个工具很有用。

操作上类似bluetoothctl工具，有自己的子命令。

```
>>>list
card 0: profiles:5 devices:10 ports:2
    profile 0: name:"off" prio:0 (available: yes)
    profile 1: name:"output:stereo-fallback+input:stereo-fallback" prio:5151 (available: unknown)
    profile 2: name:"output:stereo-fallback" prio:5100 (available: unknown)
    profile 3: name:"input:stereo-fallback" prio:51 (available: unknown)
  * profile 4: name:"pro-audio" prio:1 (available: yes)
    port 0: name:"analog-input" direction:capture prio:10000 (available: unknown)
    port 1: name:"analog-output" direction:playback prio:9900 (available: unknown)
  * device 0: direction:playback name:"pro-output-0" prio:0 flags:00000001 devices: "hw:0,0" 
  * device 1: direction:playback name:"pro-output-1" prio:0 flags:00000001 devices: "hw:0,1" 
  * device 2: direction:playback name:"pro-output-3" prio:0 flags:00000001 devices: "hw:0,3" 
  * device 3: direction:capture name:"pro-input-0" prio:0 flags:00000001 devices: "hw:0,0" 
  * device 4: direction:capture name:"pro-input-1" prio:0 flags:00000001 devices: "hw:0,1" 
  * device 5: direction:capture name:"pro-input-2" prio:0 flags:00000001 devices: "hw:0,2" 
  * device 6: direction:capture name:"pro-input-3" prio:0 flags:00000001 devices: "hw:0,3" 
  * device 7: direction:capture name:"pro-input-4" prio:0 flags:00000001 devices: "hw:0,4" 
    device 8: direction:capture name:"stereo-fallback" prio:51 flags:00000000 devices: "hw:%f" 
    device 9: direction:playback name:"stereo-fallback" prio:51 flags:00000000 devices: "hw:%f" 
```



```
./spa/plugins/alsa/acp/alsa-mixer.c:4461:        { "stereo-fallback",        N_("Stereo") },
```

