---
title: 音频延迟latency（1）
date: 2024-11-22 19:34:35
tags:
	- 音频

---

--

# 系统梳理

以下是基于ALSA接口和工具测试及优化音频延迟的方法，分为**测试准备**、**测试音频延迟**和**优化音频延迟**三个部分：

---

**1. 测试准备**

| 步骤         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| **硬件环境** | 使用具备音频输入（麦克风）和输出（耳机或音箱）的设备。       |
| **工具安装** | 确保系统安装了 `alsa-utils`（包含 `arecord` 和 `aplay`）、`jackd` 和 `latencytop` 等工具。 |
| **确认配置** | 使用 `aplay -l` 和 `arecord -l` 确认音频设备，指定测试使用的设备号（如 `hw:0,0`）。 |

---

**2. 测试音频延迟**

| 方法             | 工具及步骤                                                   |
| ---------------- | ------------------------------------------------------------ |
| **静态延迟测试** | 1. 使用 `arecord` 录制音频：<br>`arecord -D hw:0,0 -f cd -d 10 test.wav`<br>2. 回放：<br>`aplay -D hw:0,0 test.wav`<br>3. 主观感知延迟。 |
| **回环延迟测试** | 1. 将音频输入连接到输出（硬件或软件方式）；<br>2. 使用 [jack_iodelay](https://jackaudio.org/faq/latency_tests.html) 测量。 |
| **软件延迟分析** | 使用 `latencytop` 或 `strace` 分析 `aplay` 或 `arecord` 系统调用的延迟来源：<br>`strace -tt -T aplay test.wav` |
| **实时延迟测量** | 编写实时音频处理程序，使用 `snd_pcm_writei` 和 `snd_pcm_readi` 的返回时间戳计算延迟。 |

---

**3. 优化音频延迟**

| 优化点             | 方法                                                         |
| ------------------ | ------------------------------------------------------------ |
| **降低Buffer大小** | 修改ALSA缓冲区参数：<br>在代码中调整 `snd_pcm_hw_params_set_buffer_size()` 和 `snd_pcm_hw_params_set_period_size()`。 |
| **优化调度优先级** | 将音频应用程序设置为实时优先级：<br>`chrt -f 99 ./your_audio_app` 或使用 `set_rtprio`。 |
| **禁用省电功能**   | 禁用CPU C状态和音频设备的省电模式（通过 `/sys/module/snd_hda_intel/parameters/power_save`）。 |
| **内核优化**       | 确保使用低延迟内核（`CONFIG_PREEMPT` 和 `CONFIG_HZ_1000`），并优化 `tickless`。 |
| **调节采样率**     | 保证输入和输出设备采样率一致，避免重采样开销（可通过 `arecord` 和 `aplay` 参数指定）。 |
| **排除干扰**       | 禁用可能影响音频性能的服务（如NetworkManager），通过 `htop` 或 `top` 查看系统负载。 |

---

**附加建议**

1. 使用 [rt-tests](https://rt.wiki.kernel.org/index.php/RT-tests) 测试系统实时性能。
2. 如果使用的是USB音频设备，检查并优化 `snd-usb-audio` 模块参数（如 `nrpacks`）。
3. 将关键路径日志（dmesg、ALSA debug）启用，分析具体延迟来源。

# latencytop

https://www.latencytop.org/

延迟有多种类型和原因。LatencyTOP 专注于导致音频跳帧、桌面体验卡顿或服务器过载（即使你还有大量的 CPU 功率）的那类延迟。

LatencyTOP 专注于应用程序希望运行并执行有用代码的情况，但在某些资源当前不可用时（内核随后阻止进程）。这既在系统级别也针对每个进程级别进行，以便您可以了解系统发生的情况，以及哪个进程正在遭受延迟或导致延迟。