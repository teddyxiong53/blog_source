---
title: amlogic之halaudio分析
date: 2021-05-24 17:33:11
tags:
	- amlogic

---

--

看halaudio/src/audio_hal目录下的，这个是主要的代码。

先看Makefile，看看输出的是什么东西。

TARGET=libhalaudio.so

是一个名为libhalaudio.so的动态库。

依赖了这些库：

```
LDLIBS += -ltinyalsa -lamaudioutils -lstdc++ -lsupc++ -lcjson -lspeex_rate
```

所以说是基于tinyalsa的接口来做的。

还使用了c++和cjson。已经从webrtc里弄出来的speex_rate。

对外输出的头文件有这些：

```
EXPORT_API = $(SRC)/../include/audio_base.h \
	$(SRC)/../include/audio_core.h \
	$(SRC)/../include/audio_effect_hal.h \
	$(SRC)/../include/audio_effect.h \
	$(SRC)/../include/audio_effect-base.h \
	$(SRC)/../include/audio_hal.h \
	$(SRC)/../include/hardware.h \
	$(SRC)/../include/bitops.h
```

先看这些头文件的接口

```
audio_base.h 
	全部是枚举定义。
audio_core.h 
	看版权信息，是从Android代码里弄出来的。
	下面的太差了。
audio_effect_hal.h 
audio_effect.h 
audio_effect-base.h 
audio_hal.h 
	audio_hw_device_open 这个在audioservice里有用到。
hardware.h 
bitops.h
```

看看C文件

```
alsa_config_parameters.c
	就一个函数get_hardware_config_parameters。pcm_config是tinyalsa的结构体。
alsa_device_parser.c
	就3个函数。判断card的index。名字。
alsa_manager.c
	有几个接口。主要是alsa的input和output。
aml_ac3_parser.c
	是dolby相关的。
aml_anti_drift.c
	防止漂移。
aml_audio_delay.c
	这个用途是什么？
aml_audio_ease.c
	ease是减轻的意思。
aml_audio_level.c
	？
aml_audio_resample_manager.c
	支持的resample有3种：simple、Android、speex。
	
aml_audio_spdifdec.c
	spdif解码。
aml_audio_stream.c
	
aml_audio_volume.c

aml_avsync_tuning.c
	音视频同步？
aml_bm_api.c
	bass management。
aml_callback_api.c
	
aml_channel_map.c

aml_config_parser.c
	json解析。
aml_datmos_api.c
	dolby全景声相关。
aml_dca_dec_api.c
	
aml_dcv_dec_api.c
aml_dec_api.c
aml_hw_mixer.c
aml_input_manager.c
aml_mat_parser.c
aml_output_manager.c
aml_pcm_dec_api.c
aml_sample_conv.c
aml_spdif_in.c
audio_format_parse.c
audio_hw.c
	audio_hw_device_get_module 这个是返回一个静态全局变量的指针。
audio_hw_dtv.c
audio_hw_ms12.c
audio_hw_profile.c
audio_hw_utils.c
audio_hwsync.c
audio_policy.c
audio_post_process.c
audio_route.c
audio_simple_resample_api.c
audio_speex_resample_api.c
audio_trace.c
dolby_lib_api.c
pulse_manager.c
spdif_encoder_api.c
standard_alsa_manager.c
```

# 实现了什么功能

做了这么复杂的封装，最终这个模块提供的价值是什么？

仅仅是对alsa的封装吗？

是可以做到linux和Android的通用？

封装了对atmos的支持？

除了标准的alsa接口，也自己封装了一套跟alsa接口并列的实现。

```
#if 1//def USE_ALSA_PLUGINS
    aml_output_function.output_open  = standard_alsa_output_open;
    aml_output_function.output_close = standard_alsa_output_close;
    aml_output_function.output_write = standard_alsa_output_write;
    aml_output_function.output_getinfo = standard_alsa_output_getinfo;
#else
    aml_output_function.output_open  = aml_alsa_output_open;
    aml_output_function.output_close = aml_alsa_output_close;
    aml_output_function.output_write = aml_alsa_output_write;
#endif
```





# audio_hal.h

这个是对外的主要接口。

```
struct audio_stream
struct audio_stream_out 
struct audio_stream_in 
struct audio_module 
struct audio_hw_device 
```

# audio_hw.h

```
struct aml_audio_device
	继承了struct audio_hw_device
struct aml_stream_out
struct aml_stream_in
```



```
audio_hw.h 头文件分析

aml_audio_device
	audio_hw_device
		hw_device_t 这个是主要的内容。
			set_parameters
			open_output_stream
			open_input_stream
			create_audio_patch
			set_audio_port_config
			install_callback_audio_patch
			add_stream_effect
	audio_devices_t in_device; //就是一个id。int32类型
	audio_devices_t out_device;
	aml_stream_in *active_input;
	aml_stream_out *active_output[] 可以多个输出。
	aml_stream_out *hwsync_output; 这个是什么输出？
	aml_hal_mixer hal_mixer  还有mixer。
	pcm *pcm;  一个pcm结构体。
	audio_config output_config; 输出音频的配置。
	aml_stream_out *active_outputs[] 又是stream输出。
	aml_audio_patch *audio_patch; 这里的patch，就相当于pipeline，我理解为胶布，一级一级粘贴起来。
	aml_hw_mixer hw_mixer; 又是一个mixer。
	
aml_stream_out 结构体的构成
	audio_stream_out stream 相当于audio_stream_out的子类。
		这个类的主要构成也是函数指针。
		write
		pause
		resume
		drain
		flush
		start
	write：这一层也有一个write函数，参数跟audio_stream_out的write函数完全一样。
	
另外还定义了一个全局的write_func指针类型。

aml_stream_in 结构体构成
	audio_stream_in stream 
		也是相当于这个的子类。
		read
		start 
		stop
		
```



# 提交日志分析

现在通过git提交日志来看代码的演进过程。

## ==

从第一个提交信息看

```
* audio: Linux Audio Framework [1/2]

PD#SWPL-110

Problem:
 we need unify the hal audio code for linux & Android

Solution:
 Merge the original Android 8.1 hal audio code to Linux
```

对应jira单上有对应的设计文档和接口文档，但是不是太详细。

## ==

```
PD#SWPL-2579

Problem:
  HDMI input doesn't support different samplerate

Solution:
  Add ALSA plugins to support different audio samplerate

```

之前都没有使用标准alsa api。这里才添加了。

是在这里注册的

```
void aml_output_init(void)
{

    ALOGD("Init the output module\n");
#ifndef USE_PULSE_AUDIO
#if 1//def USE_ALSA_PLUGINS
    aml_output_function.output_open  = standard_alsa_output_open;//这里
    aml_output_function.output_close = standard_alsa_output_close;
    aml_output_function.output_write = standard_alsa_output_write;
    aml_output_function.output_getinfo = standard_alsa_output_getinfo;
#else
    aml_output_function.output_open  = aml_alsa_output_open;
    aml_output_function.output_close = aml_alsa_output_close;
    aml_output_function.output_write = aml_alsa_output_write;
#endif
#else
    aml_output_function.output_open  = aml_pa_output_open;
    aml_output_function.output_close = aml_pa_output_close;
    aml_output_function.output_write = aml_pa_output_write;
#endif
    return;
}
```

而input的，则仍然只使用了tinyalsa的接口。

halaudio相当于把tinyalsa和alsa的揉在了一起。

优先使用tinyalsa，搞不定部分用alsa来做。

# 对alsa和tinyalsa的使用

input是用tinyalsa接口。
output是用alsa接口。

这个可以从代码中看出来：

```
size_t aml_alsa_input_read(void *handle, void *buffer, size_t bytes)
这个函数里使用的是：
pcm_read 这种tinyalsa接口。
open里也是pcm = pcm_open

```

```
size_t standard_alsa_output_write(void *handle, const void *buffer, size_t bytes)
这个用的snd_pcm_writei这种alsa接口。
其实也可以用aml_alsa_output_open，但是没有用。
```

主要是output的场景更复杂一些。



patch可以理解为pipeline。

create_patch的时候，创建了2个线程，要给input，一个output。



input的数据，写入到patch->aml_ringbuffer这个ringbuffer里。

