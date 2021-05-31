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
	共享内存，只被as_client.c调用。
	AS_Client_Play的时候，调用了client_shm_init，这里分配了一块shm。
	AS_Client_Play只被usb_player.c里调用了一次。
as_config.c
	大部分都是Get接口，用来获取json里的某个元素。
	还有init、save、restore。
as_external_wrap.c
	默认没有使能。
asplay.c
	命令行工具。地位相当于as_client.c。
as_volume.c
	通过amixer接口来设置音量。
audioservice.c
	audioservice的入口文件。作为dbus server端。
	处理各种消息。
data_player.c
	被audioservice.c里的函数调用。
dolby_decoder.c
	跟ffmpeg并列的。音频解码。
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
	这个是提供了接口，可以跟Android的接口进行兼容。Android就不需要编译这个文件。
input_mgr.c
	
pa_config.c
pa_volume.c
	portaudio接口方式。默认没有用。
```

homeapp目录下

```
airplay_client.c
avs_client.c
halaudio_client.c
homeapp.c
	这个是入口文件。
input_manage.c
	Install_Input_Apps 这个函数比较重要。
led.c
	这个是显示昨天信息的。
	可以显示文字。
ota_upgrade.c
resource_manage.c
	这个值得注意一下。
	这个res是指什么资源？有请求和释放这2种操作。
	被调用的地方还比较多。
	AMLResHandler 这个是句柄，就是一个void *的指针。
	例如蓝牙的，AMLResHandler bt_res_handler;是一个全局变量。
	
simulate_key.c
	这个的命令行工具，模拟按键操作。
speaker_process.c
	对音频进行处理。跟bt、halaudio是一个级别的东西。
syskey.c
	按键处理。
tm1640_anode.c
tm2_external.c
usb_player.c
```



btHandleEvents.h

这个头文件找不到。

