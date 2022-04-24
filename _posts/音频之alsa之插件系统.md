---
title: 音频之alsa之插件系统
date: 2021-11-02 14:58:25
tags:
	- 音频

---

--

根据alsa-plugins目录下的代码来依次分析

这个是外部插件，主要用的还是内部插件。

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

