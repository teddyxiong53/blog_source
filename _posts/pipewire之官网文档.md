---
title: pipewire之官网文档
date: 2024-05-27 15:27:17
tags:
	- 音频

---

--

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