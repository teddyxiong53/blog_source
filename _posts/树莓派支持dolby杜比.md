---
title: 音频之ac3音频格式
date: 2021-11-11 14:31:43
tags:
	- 音频

---

--

# x600扩展板

用来给树莓派增加dolby支持。

```
 - 真正高清无损 完美音质 从树莓派HDMI信号里的声音解码分离
 - 支持模拟音频2.1声道输出
 - 支持数字音频5.1声道光纤和同轴输出
 - 彻底解决树莓派主板自带声卡音质差的问题
 - 可通过RCA莲花座或3.5mm 标准耳机插孔外接音响设备
 - 可实现音频同步分离输出，有PASS、2 0CH、5.1CH三种音频模式可选择
 - 支持杜比数码AC-3、DTS、LPCM等多种数字音频格式输出
 - 支持HDMI 输出（视频和音频信号与HDMI输入端完全相同)
```

修改config.txt

```
hdmi_force_hotplug=1       设定 HDMI 热拔插功能为开启状态
hdmi_group                            选择显示输出设备为 DMT 类型 (电脑显示器) 或 CEA 类型 (电视机)
hdmi_mode                            选择显示分辨率
```

hdmi_group=2           
(选择 "1" 为电视机, 选择 "2" 为电脑显示器)



如何用树莓派4b 实现DVD功能？

比如播放内存卡的hdr视频，就输出hdr信号，播放dolby vision视频就输出dolby vision信号。 只播放内存卡里面的，不考虑DVD光驱。



# mplayer来播放dolby

这个是把5.1转成立体声来播放的：

```
mplayer --ac=a52 --channels=6 -ao alsa:device=51to20 dolbyaurora.vob
```

MPLAYER 预计能够解码以 Dolby Digital 5.1 编码的声音流，并将 6 个声道发送到 ALSA 虚拟设备。 Alsa 虚拟设备会将 6 通道音频缩混为 2 通道。



参考资料

1、

https://www.instructables.com/Play-Dolby-Digital-51-Audio-on-Raspberry-Pi/

# raspBMC 

尽管 Raspberry Pi 的真正目标是教育，但其强大的 GPU 使该设备在 HTPC 爱好者和爱好者中非常受欢迎。

我已经在 Raspbmc 上工作了一年，现在很高兴宣布最终版本，并祝贺 XBMC 发布了如此出色的新版本。 Raspbmc 是一个自我更新的 Linux 发行版，通过简单的安装将 XBMC 带到 Raspberry Pi。它可以通过 SD 卡、USB 驱动器甚至 NFS 共享运行，并且完全支持开箱即用的 WiFi。

Raspbmc 具有 AirPlay、PVR、1080p 播放等功能。您可以在 www.raspbmc.com/about 上了解有关 Raspbmc 功能的更多信息，并在 20 分钟内启动并运行。



OSMC 和 Kodi 有什么区别？
Kodi 是一个媒体中心应用程序，OSMC 是运行 Kodi 并将其带到您的设备的操作系统。 OSMC 不是 Kodi 的一个分支，而是一个以 Kodi 作为主要应用程序的 Linux 发行版。
这与在 Windows 或 Android 上运行的 Kodi 的概念类似。 OSMC 基于 Debian（GNU/Linux 的一种风格），并经过大量优化以提供最佳的电视体验。

OSMC 负责：

让您的系统保持最新状态
硬件管理（处理遥控器、键盘、WiFi 适配器等设备）
管理系统资源
OSMC 通过 Debian 存储库和 App Store 提供了超过 40,000 个软件包





https://www.raspberrypi.com/news/raspbmc-final-version-released/

# 参考资料

1、	X600 扩展板

http://www.suptronics.com/Xseries/x600_cn.html