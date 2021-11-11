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
	这个是显示状态信息的。
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



libasexternal_input.so

这个动态库包含了哪些内容？起什么作用？

symbolic link to libasexternal_m6350.so

对应的就是src/external下面的文件。

外面用一个结构体进行包装，把这个动态库load进来，把一些接口函数抽取出来赋值给包装结构体。

AS_Config_GetEDID

在conf文件里，是这样写的内容：

```
"edid": [
        "0x35",
        "0x09", "0x7f", "0x07",
        "0x0f", "0x7f", "0x07",
        "0x15", "0x07", "0x50",
        "0x3d", "0x1e", "0xc0",
        "0x57", "0x07", "0x03",
        "0x5f", "0x7e", "0x01",
        "0x67", "0x7e", "0x03"
        ],
```

创建了一个线程来跟hdmi repeater来通信。

mcuinfochange_int_thread

```
//使用epoll来等待事件
external_input_interrupt_poll
```

是把这个加入到epoll的监听中。

```
#define GPIO_I2S_INT  "/sys/class/gpio/gpio415/value"
#define GPIO_I2S_MUTE_INT  "/sys/class/gpio/gpio455/value"
```

这个本质还是靠gpio的变化来通知的。

这里感知到gpio变化，然后就去读取i2c的数据。得到详细的信息。



我还是觉得这里的事件机制非常坑。导致逻辑非常不清晰。

主要是没有必要。

而且dbus的方式很难读。

换成jsonrpc就会清晰多了。



```
AM_CONDITIONAL([HALAUDIO_ENABLE], [test x$halaudio = xtrue])
```



当前各种枚举太多了。感觉相互关系很不清晰。

audioservice.h里的枚举

```
AS_Input_e
特点是：
INPUT_XX_ALL = 0x18100
INPUT_XX_1 = 0X18101
INPUT_XX_2 = 0X18102
可以用下面这样的宏来判断是否属于这一类。
其实也是挺别扭的。
#define IsLINEINInput(a)  \
  (AML_AS_INPUT_LINEIN_ALL == ((a) & (~AML_AS_INPUT_INDEX_MASK)))
  
  

AS_Output_e
	输出有Speaker、headphone、arc、spdif、bt这5种。
	
AML_AS_AudioFormat_e
	pcm、ac3、dts、MP3
	MP3、aac、flac、dolby true hd
	
AML_AS_NOTIFYID_e
	通知有这些：
	用100的间隔来分割不同的通知。
	0:3个，audio format、volume、mute改变。
	100：4个。src改变前，src改变后，halaudio切换完成，input chn改变
	300:2个。解码开始，解码ringbuf的状态。
	400：1个。dbus的状态。
	500:2个，SD卡插入、移除。
	600:1个。mcu变化。
	700：3个。日志优先级变化、日志级别变化、trace级别变化。
	900：4个。电源变化。
	2000:1个。有ota升级。
	
```

event，很多都是在一个文件内部，自己产生，自己处理。

主要应该是为了不阻塞。

# usb player

这个逻辑比较集中。适合用来做分析入口。

# 用shm做了什么

DataPlayerRingbufHead_t

AS_Client_Play函数里调用了client_shm_init

client_shm_init的流程：

```
shmget(key, size, 0666);
```

用来把文件读取到这里来进行播放。

具体用法有点没看懂。不知道头部的长度怎么来的。

# 硬件图和音频通路分析

现在对照着D621的硬件框图和audioservice的配置文件一起看，就对得上了。

例如，板端aplay -l，信息是这样：

```
aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: AMLAUGESOUND [AML-AUGESOUND], device 0: TDM-A-dummy multicodec-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 1: TDM-B-dummy-alsaPORT-i2sCapture dummy-1 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 2: TDM-C-tas5782m multicodec-2 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 4: SPDIF-A-dummy dummy-4 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
```

在audioservice的配置文件里是这样：

```
"speaker_8ch": {
        "MAX_CHANNELS": 8,
        "ALSA_Config": {
            "HDMI_IN": {
                "card": 0,
                "device": 1
            },
            "SPDIF_IN": {
                "card": 0,
                "device": 4
            },
            "LINE_IN": {
                "card": 0,
                "device": 1
            },
            "BT_IN": {
                "card": 0,
                "device": 0
            },
            "LOOPBACK_IN": {
                "card": 1,
                "device": 1
            },
            "Speaker_Out": {
                "card": 0,
                "device": 2
            },
            "Spdif_out": {
                "card": 0,
                "device": 4
            }
        },
```

可以看到hdmi输入的对应hw:0,1，spdif in的对应hw:0,4

而在D621（hdmi repeater板）的硬件框图上，是这样：

![image-20211111162324898](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20211111162324898.png)

可以看到，hdmi in是连接到了tdmb这个口上。

这个在aplay -l里看到的是：

```
card 0: AMLAUGESOUND [AML-AUGESOUND], device 1: TDM-B-dummy-alsaPORT-i2sCapture dummy-1 []
```

而蓝牙的，是连到了tdma上，就是hw:0,0了。

而spdif的，是对应hw:0,4的。

# homeapp分析

这个还可以把avs和gva的对接进来？

对应的函数实现在这里：

```
./multimedia/avs/Client/AvsClient.c
```

是在avs的源代码里，自己写了一个c文件。输出一个动态库。

先不细看。



homeapp里的内容还比较多。

包括了对mcu进行在线升级的内容。

把目录梳理一下

```
├── airplay_client.c 对接AirPlay
├── airplay_client.h
├── aml_uart   这个没有被编译。
│   ├── aml_uart.c
│   ├── aml_uart.h
│   ├── Android.mk
│   ├── cmd_define.h
│   ├── device_status.c
│   ├── device_status.h
│   ├── dsp_sendback.c
│   ├── dsp_sendback.h
│   ├── mcu_cmds.c
│   ├── mcu_cmds.h
│   ├── ringqueue.c
│   ├── ringqueue.h
│   ├── syscfg.c
│   ├── syscfg.h
│   ├── sys_tool.c
│   ├── sys_tool.h
│   ├── tcl_ota
│   │   ├── aml_downloader.c
│   │   ├── aml_downloader.h
│   │   ├── aml_gethostbyname.c
│   │   ├── aml_md5.c
│   │   ├── aml_md5.h
│   │   ├── Android.mk
│   │   ├── common.h
│   │   ├── Makefile
│   │   ├── swupdate-md5check.sh
│   │   ├── tcl_ota.c
│   │   ├── tcl_ota.h
│   │   ├── tcl_ota_test.c
│   │   ├── upgrade_config_file
│   │   └── upgrade_test.c
│   ├── uartcmd.c
│   ├── uartcmd.h
│   ├── uart_mcu_upgrade
│   │   ├── Android.mk
│   │   └── mcu_upgrade.c
│   ├── wifi_mgr.c
│   └── wifi_mgr.h
├── Android.mk
├── avs_client.c 
├── avs_client.h
├── bt_client.cpp
├── bt_client.h
├── gen_simulate_key_h.sh
├── gva_castcontrol.h
├── gva_client.cpp
├── gva_client.h
├── halaudio_client.c
├── halaudio_client.h
├── homeapp.c
├── input_manage.c
├── input_manage.h
├── led.c
├── led_char_16.h
├── led.h
├── Makefile.am
├── ota_upgrade.c
├── resource_manage.c
├── resource_manage.h
├── sh_cmd.c
├── simulate_key.c
├── speaker_process.c
├── syskey.c
├── syskey.h
├── tm1640_anode.c
├── tm1640_anode.h
├── tm2_external.c
├── tm2_external.h
├── usb_player.c
└── usb_player.h
```

当前只编译了这些

```
homeapp_SOURCES = homeapp.c syskey.c tm1640_anode.c led.c \
                  resource_manage.c input_manage.c
```

还是可以选配编译uart的。

```
if AML_UART_ENABLE
homeapp_SOURCES += \
	aml_uart/dsp_sendback.c \
	aml_uart/mcu_cmds.c \
	aml_uart/ringqueue.c \
	aml_uart/sys_tool.c \
	aml_uart/syscfg.c \
	aml_uart/uartcmd.c \
	aml_uart/aml_uart.c \
	aml_uart/device_status.c
```

resource request，资源管理

包括了改变CPU的频率。

例如这个：

```
case INPUT_NOTIFY_TYPE_RES_CHANGE:
       if (!IsHDMIInput(param->input_id)) {
         halaudio_switch_cpu_frequency(_HALAUDIO_CPU_1_2_G_);
       }
       break;
```

bt_client.cpp没有编译。里面的函数也是找不到的。

android.mk的有加。所以是只对GVA的有使用。

