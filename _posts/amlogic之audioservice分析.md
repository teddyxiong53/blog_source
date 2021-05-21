---
title: amlogic之audioservice分析
date: 2021-05-21 16:47:11
tags:
	- amlogic

---

--

src目录下

```
aml_event.c
	函数以AmlEvent_为前缀。
	核心数据结构：AmlEvent_t和AmlEventHandler_t
	AmlEvent_t：
		id。时间戳。void *的参数。next指针。
	AmlEventHandler_t
		包含一个AmlEvent_t链表。
		thread/mutex/cond。这一套线程来处理。
		2个函数指针：
			event_handler。2个参数：id和param。
			add_event_func。这个所有的调用地方，都是彻底了null。所以都是使用默认的。
				这个就是分配一个event，赋值，挂到链表上。
	对外提供的接口：
		AmlEvent_Open
			把event_handler和event_add函数指针传递进来，创建线程跑起来。
			被as_client.c、bt_client.cpp、halaudio.c、resource_manager.c、usb_player.c这5个文件调用了。
			as_client.c里的这个的对应的调用栈是：
				homeapp的main函数
					AS_Client_Init
						AmlEvent_Open
			事件的处理回调是homeapp里的asclient_callback
			as_client.c里这个event id固定是0，是notify处理。
			notify有多种，有一个枚举。void * 的param是一个json字符串。
			最后处理这些notify是这样做：
				input chn改变：
				音量改变
				音频格式改变
			homeapp里的相当于总的，它的回调最后调用了InputMgr_CallbackHandler
			相当于把事件进行了继续分发。
			这个里面会遍历InputHandler_list。调用对应的ASCallback_handler进行处理。
		AmlEvent_Close
		AmlEvent_AddEvent
			这个相当于trigger的含义。
		AmlEvent_DelEvent
aml_syslog.c
as_alsa.c
	对外接口：alsa_init
	调用栈：
	AS_Volume_Init
		alsa_init
	主要是amixer接口处理音量。
as_client.c
	对外接口：AS_Client_Init
	主要处理作为dbus client的事务。
as_client_shm.c
as_config.c
as_external_wrap.c
asplay.c
as_volume.c
audioservice.c
data_player.c
dolby_decoder.c
ffmpeg_decoder.c
halaudio.c
	这个很重要。是音频的硬件抽象层。
	重要结构体：
	一个共用体。
		AmlHalAudioEventParam_u，就是各种事件param。
		入口是HalAudio_Init
		调用栈是：
			audioservice.c main函数
				AS_Input_Init 参数是配置文件名。
					HalAudio_Init(NULL, codec_config);
						codec_config是这样：
						"audio_codec_config":	{
                            "ffmpeg": ["mp3", "wav", "flac"]
                            },
halaudio_spdif.c
halhdmicec.c
halhdmicec_control.c
hardware_buildroot.c
input_mgr.c
pa_config.c
pa_volume.c
```

homeapp目录下

```
airplay_client.c
avs_client.c
halaudio_client.c
homeapp.c
	这个是入口文件。
input_manage.c
led.c
ota_upgrade.c
resource_manage.c
sh_cmd.c
simulate_key.c
speaker_process.c
syskey.c
tm1640_anode.c
tm2_external.c
usb_player.c
```



btHandleEvents.h

这个头文件找不到。

