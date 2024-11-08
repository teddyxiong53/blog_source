---
title: 音频之hifiberry系统研究
date: 2021-12-02 19:58:33
tags:
	- 音频

---

--

官网：

https://www.hifiberry.com/

代码在这里：

https://github.com/hifiberry/hifiberry-os

hifiberryos是一个针对音频播放的最小的linux发行版。

主要目的不是添加更多的功能，而是保持足够小。

所以，基于buildroot来做，而且不能使用包管理工具来安装新的软件。

更新机制是通过不同的分区来实现的。

| partition | file system | use    |
| --------- | ----------- | ------ |
| p0        | fat         | /boot  |
| p1        | ext4        | root 1 |
| p2        | ext4        | root 2 |
| p3        | ext4        | /data  |

更新对应的package。

https://github.com/hifiberry/hifiberry-os/tree/master/buildroot/package/hifiberry-updater

用户界面是基于BeoCreate这个项目。

项目在这里

https://github.com/bang-olufsen/create

BeoCreate2是BeoCreate这个4ch放大器的板端软件。

配套的电脑软件是BeoCreate Connect，会自动发现网络里的BeoCreate声音系统。

这个软件是基于electron框架的。

浏览一下hifiberry的仓库，找到raspidmx，这个似乎有点意思。



把hifiberry代码下载下来，编译一下，就用rpi4的来编译。

就根据doc目录下的文档来操作。

```
 
# 这个会把buildroot的代码clone下来。
# 会在当前目录的上一层。
./get-buildroot
# 这个会在上一层目录生成一个buildroot-4的目录，作为编译的输出目录。
./build-config 4
# 进行编译
./compile 4 hifiberry
```

# 简介

HiFiBerry 是一个专为树莓派设计的高品质音频扩展板，

旨在提升树莓派的音频性能。

它提供了一系列不同的音频产品，适用于多种应用，包括音乐播放、数字音频播放和音频流媒体服务。

### 主要特点

1. **高品质音频输出**：
   - HiFiBerry 使用高质量的DAC（数模转换器），提供清晰、准确的音频输出。
   - 支持高分辨率音频，能够播放高达192kHz/24bit的音频格式。

2. **多种型号**：
   - HiFiBerry DAC+：适用于大多数音频应用，提供优质的模拟输出。
   - HiFiBerry DAC+ Pro：增加了更高质量的组件，支持更低的噪音和失真。
   - HiFiBerry Digi+：数字输出扩展板，适合需要数字音频输出的用户。

3. **简单的安装与配置**：
   - 兼容树莓派的标准接口，安装过程简单。
   - 支持多种操作系统，如Raspbian、Volumio和Moode等，用户可以轻松配置和管理音频播放。

4. **开源和社区支持**：
   - HiFiBerry 提供开源驱动程序，用户可以根据需要进行定制。
   - 拥有活跃的社区支持，用户可以在论坛上获取帮助和分享经验。

### 应用场景

- **家庭音频系统**：将树莓派与 HiFiBerry 结合，可以构建一个高保真音频播放系统。
- **网络音乐播放器**：利用流媒体服务（如Spotify、Tidal等）进行高质量音乐播放。
- **DIY 音频项目**：适合音频爱好者和开发者，进行各种音频相关的DIY项目。

### 总结

HiFiBerry 是树莓派用户提升音频体验的理想选择，无论是用于家庭娱乐系统还是个人项目，它都能提供卓越的音质和灵活的功能。通过简单的安装和配置，用户可以轻松享受高保真的音频体验。

# package分析

这个是自己写了很多的package。

## alsa-eq

这个是一个alsa eq均衡器。

## audiocontrol2

这个是核心应用。Python写的。

控制各种播放器的。

```
from ac2.data.mpd import MpdMetadataProcessor
from ac2.players.mpdcontrol import MPDControl
from ac2.players.vollibrespot import VollibspotifyControl
```



## beocreate

nodejs写的。

应该是用户控制界面。

# 官方文档

https://github.com/hifiberry/hifiberry-os/blob/master/doc/readme.md

https://www.hifiberry.com/docs/

# 音频测试

https://www.audiosciencereview.com/forum/index.php?threads/hifiberry-dac2-hd-review-rpi-hat.21034/

# 手册

https://gzhls.at/blob/ldb/8/8/1/2/d368e86e380de104a54edfe3586b75943e53.pdf

# 参考资料

1、更新机制

https://github.com/hifiberry/hifiberry-os/blob/master/doc/updater.md

2、***Beocreate 2*** is the software suite for *Beocreate 4-Channel Amplifier*

https://github.com/bang-olufsen/create

3、

https://blog.csdn.net/F8qG7f9YD02Pe/article/details/114957192