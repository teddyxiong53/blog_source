---
title: alsa之alsactl用法
date: 2022-05-10 13:49:01
tags:

	- alsa

---

--

```
/etc # cat alsactl.conf
MASTERVOL{"Master Playback Volume" 0 100}
MUTENAME{ "switch playback mute" 0 1}
```

# alsactl 命令用法

`alsactl` 是一个命令行工具，用于管理 ALSA（Advanced Linux Sound Architecture）的音频设置。它提供了一些用于查看、修改和操作音频设置的命令。

以下是 `alsactl` 常用命令的用法：

1. `alsactl init`: 初始化 ALSA 音频设置。它会加载默认的音频设置，并将其应用到当前的 ALSA 环境中。

2. `alsactl store`: 将当前的音频设置保存到状态文件中。通常情况下，状态文件保存在 `/var/lib/alsa/asound.state`。

3. `alsactl restore`: 从状态文件中还原音频设置。它会读取指定的状态文件，并将保存的音频设置应用到当前的 ALSA 环境中。

4. `alsactl kill <card>`: 停止指定声卡的 ALSA 控制器。这会导致当前的音频设置被丢弃，并重新加载默认的音频设置。

5. `alsactl monitor`: 监听 ALSA 控制器的变化，并实时显示音量和音频设置的改变。

6. `alsactl --file <file> <command>`: 指定自定义的状态文件进行操作。可以替换 `<file>` 为状态文件的路径，执行指定的 `<command>`。

这些是 `alsactl` 常用的命令，可以用于管理 ALSA 的音频设置。根据需要，你可以结合其他选项和参数来进行更详细的操作。你可以通过 `alsactl --help` 命令查看更多关于 `alsactl` 的帮助信息和可用选项。

# alsactl restore

`alsactl restore` 是一个命令行工具，用于还原 ALSA（Advanced Linux Sound Architecture）的音频设置。

在 Linux 系统中，ALSA 是用于提供音频支持的软件架构。它包含了驱动程序、库和工具，用于管理和控制音频设备的输入和输出。`alsactl restore` 命令用于从之前保存的状态文件中还原音频设置。

当执行 `alsactl restore` 命令时，它会读取指定的状态文件（通常是 `/var/lib/alsa/asound.state`）中保存的音频设置，并将这些设置应用到当前的 ALSA 环境中。这样可以确保在每次系统启动时或需要恢复音频设置时，都能够还原之前保存的状态。

通过运行 `alsactl restore` 命令，可以方便地还原之前的音频设置，包括音量、音频通道、音频效果等。这对于保持音频配置的一致性和避免手动重新配置音频设备非常有用。

需要注意的是，执行 `alsactl restore` 命令通常需要管理员权限，因为它涉及对系统的音频设置进行修改。

# /var/lib/alsa/asound.state内容举例

# 参考资料

1、

https://askubuntu.com/questions/50067/howto-save-alsamixer-settings