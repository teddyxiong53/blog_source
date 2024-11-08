---
title: 音频之MPRIS
date: 2022-04-09 21:04:11
tags:
	- 音频

---

--

看hifiberry里，有MPRIS这个概念，就了解一下。

MPRIS是Media Player Remote Interfacing Specification的缩写。

基于dbus的协议，用来做播放器控制的一套协议。

用来发现、查询、控制播放器。

# 简介

MPRIS（Media Player Remote Interfacing Specification）是一种用于媒体播放器的==接口标准==，

主要用于在Linux和其他Unix-like系统中==实现==媒体播放器的==远程控制==和信息传递。

它允许不同的媒体播放器之间进行交互，以及与桌面环境或其他应用程序进行集成。

### MPRIS的主要特点

1. **统一接口**：MPRIS定义了一个标准化的接口，允许开发者创建兼容的媒体播放器和控制应用程序。

2. **远程控制**：通过MPRIS，用户可以使用一个应用程序控制另一个媒体播放器的播放、暂停、跳过等功能。

3. **元数据获取**：MPRIS允许应用程序访问当前播放的媒体信息，如标题、艺术家、专辑封面等。

4. **事件通知**：媒体播放器可以通过MPRIS向其他应用程序发送状态更新，例如播放状态变化或媒体变化。

### MPRIS的版本

MPRIS有多个版本，最常用的是MPRIS 2.0。这个版本提供了对多种媒体控制功能的支持，包括：

- 播放、暂停、停止、跳转
- 媒体信息的获取
- 播放列表管理
- 音量控制

### 应用实例

- **桌面环境集成**：许多桌面环境（如KDE和GNOME）都集成了MPRIS，使用户可以通过系统托盘或媒体控制面板控制播放。
- **第三方应用**：开发者可以创建支持MPRIS的应用程序，以便与现有媒体播放器无缝集成。

### 总结

MPRIS是一种强大的协议，极大地提高了媒体播放的灵活性和用户体验。通过标准化的接口，它促进了不同媒体应用程序之间的互操作性，是现代多媒体应用开发中不可或缺的一部分。

# mpris规范主要内容说明

MPRIS（Media Player Remote Interfacing Specification）规范的主要内容涵盖了媒体播放器的远程控制和信息交互。以下是其主要组成部分的说明：

### 1. **基本概念**

- **接口**：MPRIS 定义了一组标准接口，允许应用程序与媒体播放器进行通信。
- **对象模型**：基于 D-Bus 的对象模型，允许通过 D-Bus 进行方法调用和信号传递。

### 2. **核心接口**

- **Player**：主要接口，提供控制媒体播放的基本功能，如播放、暂停、停止、跳过等。
- **TrackList**：管理当前播放列表，允许用户获取和修改播放列表中的曲目。
- **Metadata**：提供当前播放媒体的元数据，如标题、艺术家、专辑、持续时间等。

### 3. **重要方法**

- **Play()**：开始播放当前曲目。
- **Pause()**：暂停当前曲目。
- **Stop()**：停止播放。
- **Next()**：跳到下一曲目。
- **Previous()**：返回到上一曲目。

### 4. **信号通知**

- **PropertiesChanged**：当播放器状态或元数据变化时，发送此信号以通知监听者。
- **Playing**、**Paused**、**Stopped**：状态变化的信号，允许应用程序根据播放状态进行更新。

### 5. **元数据属性**

- **mpris:trackid**：当前曲目的唯一标识符。
- **mpris:length**：曲目的长度，单位为毫秒。
- **mpris:artUrl**：曲目的封面艺术 URL。
- **mpris:artist**、**mpris:title**、**mpris:album**：曲目的艺术家、标题和专辑信息。

### 6. **版本支持**

- MPRIS 2.0 和 2.2 版本的规范主要增加了一些新特性和改进，确保更好的兼容性和功能性。

### 7. **扩展性**

- MPRIS 允许开发者根据需要扩展接口以支持特定功能，但必须遵循基本的协议规范。

### 总结

MPRIS 规范通过提供统一的接口和方法，使得不同的媒体播放器和控制应用程序能够相互沟通，从而提高用户体验。开发者可以利用这些接口实现丰富的媒体控制功能，促进跨平台和跨应用的无缝集成。欲了解更多详细信息，建议查阅[官方规范文档](https://specifications.freedesktop.org/mpris-spec/latest/)。

# 用python实现一个demo

下面是一个简单的 Python 示例，展示如何使用 `dbus` 库来与 MPRIS 兼容的媒体播放器进行交互。这个示例将连接到一个正在运行的媒体播放器，并执行播放、暂停和获取元数据的操作。

### 安装依赖

确保安装了 `dbus-python` 库。可以通过以下命令安装：

```bash
pip install dbus-python
```

### 示例代码

```python
import dbus
import dbus.mainloop.glib
from gi.repository import GLib

def get_mpris_player():
    session_bus = dbus.SessionBus()
    try:
        # 尝试获取 MPRIS 兼容的媒体播放器
        player = session_bus.get_object('org.mpris.MediaPlayer2.Player', '/org/mpris/MediaPlayer2')
        return player
    except dbus.exceptions.DBusException:
        print("没有找到 MPRIS 媒体播放器")
        return None

def play(player):
    player.Play()

def pause(player):
    player.Pause()

def get_metadata(player):
    metadata = player.Get("org.mpris.MediaPlayer2.Player", "Metadata", dbus_interface=dbus.INTROSPECTABLE)
    return metadata

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    player = get_mpris_player()
    if player:
        # 播放
        print("播放中...")
        play(player)

        # 暂停
        print("暂停中...")
        pause(player)

        # 获取元数据
        metadata = get_metadata(player)
        print("当前曲目元数据:")
        for key, value in metadata.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
```

### 运行示例

1. 确保有一个支持 MPRIS 的媒体播放器正在运行，如 VLC、Rhythmbox 等。
2. 将上述代码保存为 `mpris_demo.py`。
3. 在终端中运行：

   ```bash
   python mpris_demo.py
   ```

### 说明

- 该代码首先尝试连接到 MPRIS 媒体播放器。
- 然后，它调用播放和暂停功能，并获取当前播放的元数据。
- `dbus` 库用于与 D-Bus 进行通信，`gi.repository` 用于事件循环的支持。

请确保在运行此代码之前，已安装并运行好相应的媒体播放器。

# linux哪些播放器支持mpris

我只列我感兴趣的。

 **VLC Media Player**

MPD 

# 用python实现一个支持mpris协议的播放器

下面是一个简单的 Python 示例，展示如何实现一个基本的 MPRIS 兼容媒体播放器。这个示例将使用 `dbus` 和 `gi` 库来创建一个简单的播放器，支持播放、暂停和获取元数据。

### 安装依赖

确保安装了以下库（如果尚未安装）：

```bash
pip install dbus-python
pip install PyGObject
```

### 示例代码

这是一个简单的 MPRIS 媒体播放器的实现：

```python
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import random
import time

class SimpleMPRISPlayer:
    def __init__(self):
        self.loop = GLib.MainLoop()
        self.player_state = "Stopped"
        self.current_track = {
            'mpris:trackid': '/track/1',
            'mpris:length': 300000,  # 300 seconds
            'mpris:artist': 'Artist Name',
            'mpris:title': 'Track Title',
            'mpris:album': 'Album Name',
            'mpris:artUrl': 'http://example.com/art.jpg'
        }

        # D-Bus setup
        self.bus = dbus.SessionBus()
        self.bus_name = dbus.service.BusName('org.mpris.MediaPlayer2.SimplePlayer', bus=self.bus)
        self.player_obj = dbus.service.Object(self.bus_name, '/org/mpris/MediaPlayer2')

        # Register MPRIS interfaces
        self.player_obj.add_signal_receiver(self.handle_play, dbus_interface='org.mpris.MediaPlayer2.Player', signal_name='Play')
        self.player_obj.add_signal_receiver(self.handle_pause, dbus_interface='org.mpris.MediaPlayer2.Player', signal_name='Pause')
        self.player_obj.add_signal_receiver(self.handle_stop, dbus_interface='org.mpris.MediaPlayer2.Player', signal_name='Stop')
        self.player_obj.add_signal_receiver(self.handle_next, dbus_interface='org.mpris.MediaPlayer2.Player', signal_name='Next')
        self.player_obj.add_signal_receiver(self.handle_previous, dbus_interface='org.mpris.MediaPlayer2.Player', signal_name='Previous')

        # Register properties
        self.player_obj.add_property('org.mpris.MediaPlayer2.Player', 'PlaybackStatus', self.get_playback_status)
        self.player_obj.add_property('org.mpris.MediaPlayer2.Player', 'Metadata', self.get_metadata)

    def get_playback_status(self):
        return self.player_state

    def get_metadata(self):
        return self.current_track

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='', out_signature='')
    def Play(self):
        self.player_state = "Playing"
        print("Playing track...")

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='', out_signature='')
    def Pause(self):
        self.player_state = "Paused"
        print("Paused track.")

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='', out_signature='')
    def Stop(self):
        self.player_state = "Stopped"
        print("Stopped track.")

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='', out_signature='')
    def Next(self):
        print("Next track (not implemented).")

    @dbus.service.method('org.mpris.MediaPlayer2.Player', in_signature='', out_signature='')
    def Previous(self):
        print("Previous track (not implemented).")

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        print("MPRIS Player is running...")
        self.loop.run()

if __name__ == "__main__":
    player = SimpleMPRISPlayer()
    player.run()
```

### 运行示例

1. 将上述代码保存为 `simple_mpris_player.py`。
2. 在终端中运行此脚本：

   ```bash
   python simple_mpris_player.py
   ```

### 说明

- **D-Bus 接口**：该示例通过 D-Bus 注册了一个名为 `org.mpris.MediaPlayer2.SimplePlayer` 的媒体播放器。
- **播放控制**：实现了基本的播放、暂停和停止方法。
- **元数据**：提供了一些示例元数据，如艺术家、曲目标题和专辑。
- **信号接收**：使用 D-Bus 信号接收器来处理播放、暂停、停止等操作。

### 注意

- 这是一个简单的示例，未实现完整的播放器逻辑，如实际音频播放和播放列表管理。
- 您可以根据需要扩展功能，例如添加实际的音频播放支持、播放列表管理等。

# 参考资料

1、

https://wiki.archlinux.org/title/MPRIS