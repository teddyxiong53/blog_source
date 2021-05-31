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



struct aml_audio_device  

这个是核心数据结构。

看test.c里的内容。

```
//1、拿到mod
audio_hw_device_get_module(&mod);
//2、拿到dev。
audio_hw_device_open(mod, &dev);
//3、设置参数。
dev->set_parameters(dev, "speakers=lr:c:lfe:lrs:lre");
```

