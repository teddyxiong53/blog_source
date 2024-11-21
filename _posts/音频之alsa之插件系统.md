---
title: 音频之alsa之插件系统
date: 2021-11-02 14:58:25
tags:
	- 音频

---

--

根据alsa-plugins目录下的代码来依次分析

这个是外部插件，主要用的还是内部插件。

# **ALSA 插件**

根据 [ALSA Plugins 文档](https://alsa.opensrc.org/ALSA_plugins)，ALSA 插件提供了一个灵活的机制，可以通过软件接口扩展和增强 ALSA 系统的功能。以下是关于 ALSA 插件的主要内容和类型总结：

---

### **ALSA 插件概述**

ALSA 插件是一个中间层，允许用户或应用程序通过它来扩展 ALSA 的功能。插件提供了多种功能，最常见的包括设备抽象、音效处理、格式转换、音频路由等。它们通过配置文件或环境变量进行管理，并能够在不修改应用程序的情况下，透明地在音频流中插入不同的处理模块。

### **插件的类型**

1. **硬件抽象插件**（如 `hw`, `plughw`, `dmix` 等）：
   - **`hw` 插件**：直接访问硬件设备。
   - **`plughw` 插件**：提供硬件访问的同时，可以进行格式转换（如采样率、声道数等的转换）。
   - **`dmix` 插件**：将多个音频流混合并输出到一个硬件设备，而不需要硬件支持混音功能。
   - **`dsnoop` 插件**：允许多个应用程序共享一个录音设备。

2. **音频格式转换插件**（如 `rate`, `channels`）：
   - 这些插件提供了自动的音频格式转换（如采样率转换、通道数转换等）。
   - 例如，**`rate` 插件**可以处理输入音频的采样率转换。

3. **音效插件**（如 `equal`，`echo`，`reverb`）：
   - 这些插件用于增强音频质量，提供不同的音效处理功能，如均衡器、回声、混响等。

4. **音频路由插件**：
   - 允许将音频流从一个设备路由到另一个设备。
   - **`multi` 插件**允许多个输出设备同时播放音频流。

5. **输入输出插件**：
   - 用于提供额外的音频接口，比如网络音频流、USB 音频设备、蓝牙音频设备等。
   - 例如，**`alsa_pcm` 插件**可以通过 PCM 协议处理输入输出数据流。

6. **网络插件**：
   - 允许音频流通过网络进行传输，例如 **`tcp`** 和 **`udp`** 插件可以用于通过网络传输音频数据。

### **插件配置**

插件通常通过配置文件来进行管理，配置文件一般位于 `/etc/asound.conf` 或 `~/.asoundrc`。在配置文件中，可以定义插件的参数和插件的组合。

例如，配置 `dmix` 插件：
```text
pcm.!default {
    type dmix
    ipc_key 1024
    slave.pcm "hw:0"
    bindings {
        0 0
        1 1
    }
}
```

### **插件管理命令**

- **`aplay` 和 `arecord`**：这些工具支持使用插件。可以通过 `-D` 参数选择不同的设备或插件。
  - 例如：
    ```bash
    aplay -D plughw:0,0 test.wav
    arecord -D plughw:1,0 test.wav
    ```
  
- **`alsamixer`**：用于管理设备音量等配置，支持加载和调整插件的设置。

### **常见的 ALSA 插件实例**

1. **`dmix` 插件**：将多个应用程序的音频输出混合到一个硬件设备。
   - 用于支持没有硬件混音功能的设备。
2. **`dsnoop` 插件**：允许多个应用程序共享一个录音设备。
   - 在没有硬件支持多个录音流的情况下使用。
3. **`rate` 插件**：提供采样率转换的功能。
   - 允许将音频流的采样率转换为目标设备支持的采样率。
4. **`equal` 插件**：提供简单的均衡器功能。
   - 用于调整音频的频率响应。

### **插件的组合和使用**
插件可以组合使用，创建一个功能强大的音频处理管道。例如，可以将 `dmix` 插件和 `rate` 插件结合使用，以实现多音频流混音并转换采样率：
```text
pcm.!default {
    type plug
    slave.pcm {
        type dmix
        ipc_key 1024
        slave.pcm "hw:0"
    }
    route_policy "default"
}
```

### **总结**
ALSA 插件提供了对音频设备的抽象和增强，使得应用程序可以更加灵活地管理和处理音频流。插件通过配置文件来管理，允许透明地执行硬件抽象、格式转换、音效处理、音频路由等功能。通过合理配置和选择插件，开发者能够根据需求定制和优化音频系统，增强音频处理能力。

# 插件的编写方法

外部插件在位于 /usr/lib/alsa-lib 下面的动态库。

命名规律是：libasound_module_pcm_xxx.so 

入口是通过一个宏来定义：

SND_PCM_PLUGIN_DEFINE_FUNC() 

以rate这个为例来分析。

对应文件rate_samplerate.c。

根据doc/samplerate.txt里的描述

这个插件的作用是：使用libsamplerate来进行码率采样率的变换。

这样来用：

```
pcm.my_rate {
	type rate
	slave.pcm "hw"
	converter "samplerate"
}
```

还可以在你的asoundrc里写上这一句：

```
defaults.pcm.rate_converter "samplerate"
```

在rate_samplerate.c的最后，定义了5个PLUGIN。

```
int SND_PCM_RATE_PLUGIN_ENTRY(samplerate) (unsigned int version, void **objp,
					   snd_pcm_rate_ops_t *ops)
{
	return pcm_src_open(version, objp, ops, SRC_SINC_FASTEST);
}
还有：
samplerate_best
samplerate_medium
samplerate_order
samplerate_linear
这4个。
都是调用的pcm_src_open函数，区别是最后一个参数不同。
```

实现了一个这样的结构体

```
static snd_pcm_rate_ops_t pcm_src_ops = {
	.close = pcm_src_close,
	.init = pcm_src_init,
	.free = pcm_src_free,
	.reset = pcm_src_reset,
	.adjust_pitch = pcm_src_adjust_pitch,
	.convert_s16 = pcm_src_convert_s16,
	.input_frames = input_frames,
	.output_frames = output_frames,
#if SND_PCM_RATE_PLUGIN_VERSION >= 0x010002
	.version = SND_PCM_RATE_PLUGIN_VERSION,
	.get_supported_rates = get_supported_rates,
	.dump = dump,
#endif
};
```

**调用的resample插件是SRC(secret rabbit code),其官网：**http://www.mega-nerd.com/SRC/

SRC能够进行任意的和时变的转换，

从256倍的下采样到相同因子的上采样。

这种情况下的任意性意味着输入和输出采样率之比可以是无理数。

转换率也可以随时间而变化，以加速和减速速效果。



参考资料

1、ALSA resample插件－SRC

https://blog.csdn.net/weixin_41965270/article/details/81272732

# a52

把S16的线性格式转成A52压缩stream，发送到spdif输出。

需要libavcodec来进行编码。

这样来使用：

```
pcm.myout {
	type a52
}
```

完整的写法：

```
	pcm.myout {
		type a52
		card 1
		rate 44100
		channels 4
		bitrate 256
		format S16_BE
	}
```



参考资料

alsa-plugins/doc/a52.txt

# oss

这个插件是实现alsa写的app可以直接在oss驱动上运行。

这样配置

```
	pcm.oss {
		type oss
		device /dev/dsp
	}
```

这样播放：

```
aplay -Dplug:oss foo.wav
```

# 内部插件

是指alsa-lib/pcm目录下的这些pcm_xx.c的文件。

以pcm_copy.c为例

```
typedef struct {
	snd_pcm_generic_t gen;
	snd_pcm_slave_xfer_areas_func_t read;
	snd_pcm_slave_xfer_areas_func_t write;
	snd_pcm_slave_xfer_areas_undo_func_t undo_read;
	snd_pcm_slave_xfer_areas_undo_func_t undo_write;
	int (*init)(snd_pcm_t *pcm);
	snd_pcm_uframes_t appl_ptr, hw_ptr;
} snd_pcm_plugin_t;	
```

这样定义：

```
typedef struct {
	/* This field need to be the first */
	snd_pcm_plugin_t plug;
} snd_pcm_copy_t;
```



支持的插件类型：

```
enum _snd_pcm_type {
	/** Kernel level PCM */
	SND_PCM_TYPE_HW = 0,
	/** Hooked PCM */
	SND_PCM_TYPE_HOOKS,
	/** One or more linked PCM with exclusive access to selected
	    channels */
	SND_PCM_TYPE_MULTI,
	/** File writing plugin */
	SND_PCM_TYPE_FILE,
	/** Null endpoint PCM */
	SND_PCM_TYPE_NULL,
	/** Shared memory client PCM */
	SND_PCM_TYPE_SHM,
	/** INET client PCM (not yet implemented) */
	SND_PCM_TYPE_INET,
	/** Copying plugin */
	SND_PCM_TYPE_COPY,
	/** Linear format conversion PCM */
	SND_PCM_TYPE_LINEAR,
	/** A-Law format conversion PCM */
	SND_PCM_TYPE_ALAW,
	/** Mu-Law format conversion PCM */
	SND_PCM_TYPE_MULAW,
	/** IMA-ADPCM format conversion PCM */
	SND_PCM_TYPE_ADPCM,
	/** Rate conversion PCM */
	SND_PCM_TYPE_RATE,
	/** Attenuated static route PCM */
	SND_PCM_TYPE_ROUTE,
	/** Format adjusted PCM */
	SND_PCM_TYPE_PLUG,
	/** Sharing PCM */
	SND_PCM_TYPE_SHARE,
	/** Meter plugin */
	SND_PCM_TYPE_METER,
	/** Mixing PCM */
	SND_PCM_TYPE_MIX,
	/** Attenuated dynamic route PCM (not yet implemented) */
	SND_PCM_TYPE_DROUTE,
	/** Loopback server plugin (not yet implemented) */
	SND_PCM_TYPE_LBSERVER,
	/** Linear Integer <-> Linear Float format conversion PCM */
	SND_PCM_TYPE_LINEAR_FLOAT,
	/** LADSPA integration plugin */
	SND_PCM_TYPE_LADSPA,
	/** Direct Mixing plugin */
	SND_PCM_TYPE_DMIX,
	/** Jack Audio Connection Kit plugin */
	SND_PCM_TYPE_JACK,
	/** Direct Snooping plugin */
	SND_PCM_TYPE_DSNOOP,
	/** Direct Sharing plugin */
	SND_PCM_TYPE_DSHARE,
	/** IEC958 subframe plugin */
	SND_PCM_TYPE_IEC958,
	/** Soft volume plugin */
	SND_PCM_TYPE_SOFTVOL,
	/** External I/O plugin */
	SND_PCM_TYPE_IOPLUG,
	/** External filter plugin */
	SND_PCM_TYPE_EXTPLUG,
	/** Mmap-emulation plugin */
	SND_PCM_TYPE_MMAP_EMUL,
	SND_PCM_TYPE_LAST = SND_PCM_TYPE_MMAP_EMUL
};
```

