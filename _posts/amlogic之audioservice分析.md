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

## homeapp.c文件

这个相当于跟用户交互的前端部分。

asclient_callback 这个是处理后端的通知消息的回调。

audioservice调用了这个来发送通知：

```
snprintf(notify_str, 64,
            "{\"id\": %d,"
            "\"input_chs\": %d}",
            AML_AS_NOTIFY_INPUT_CHS_NUM_CHANGE, pHandle->channel_num);
      audioservice_notify_system_update(notify_str);
```

led的显示，都是靠这个来做的。

```
收到AML_AS_NOTIFY_AUDIO_FORMAT_CHANGED消息，调用show_audioinfo

```



# 打开日志调试

编译层面：

```
#ifdef AML_LOG_ENABLE
#include "aml_log.h"
#endif
```

AML_LOG_ENABLE这个宏是定义了的。

用加编译错误的方式确认了。

那么日志函数就是这样的：

```
#ifdef AML_LOG_ENABLE
#define AML_SYSLOG(priority, args...)                                          \
  do {                                                                         \
    AML_LOG(priority_to_level(priority), ##args);                              \
  } while (0)
#else
```

AML_LOG在哪里定义？

应该是这个头文件

```
#include "aml_log.h"
```

在这个目录下./vendor/amlogic/aml_commonlib/aml_log/aml_log.h

```
#define AML_LOG(level, fmt, ...) AML_LOG_CAT(DEFAULT, level, fmt, ##__VA_ARGS__)
```

```
#define AML_LOG_CAT(cat, level, fmt, ...)                                                          \
    do {                                                                                           \
        if (AML_LOG_CAT_ENABLE(&(AML_LOG_GET_CAT_(cat)), level)) {                                 \
            aml_log_msg(&(AML_LOG_GET_CAT_(cat)), level, __FILE__, __func__, __LINE__, fmt,        \
                            ##__VA_ARGS__);                                                        \
        }                                                                                          \
    } while (0)
```

AML_LOG_CAT_ENABLE这个决定了级别。

aml_log_msg这个的实现是怎样的？

```
    va_start(ap, fmt);
    vsnprintf(&buf[len], sizeof(buf) - len, fmt, ap);
    va_end(ap);
    fprintf(log_fp ?: stdout, "%s", buf);
```

如果没有log_fp，那么打印到stdout上。



当前在/tmp目录下，有这2个以AML_LOG开头的文件。

```
AML_LOG_audioservice 
AML_LOG_homeapp      
```

里面内容是：

```
# cat AML_LOG_homeapp
all:LOG_ERR
```

那么看起来是基本配置。

这个是在aml_log.c里默认生成的。

动态监听了这2个配置文件的。

我修改一下看看。

改成LOG_DEBUG。

现在从运行层面看看。

当前怎么启动的audioservice和homeapp。

```
/usr/bin/audioservice /etc/default_audioservice.conf&
/usr/bin/homeapp -r /dev/input/event0 -a /dev/input/event3 -D music_vol -s &
```

都是后台运行。

我改成手动前台运行的，就可以看到在stdout上打印的日志了。

对于默认启动的，可以加重定向到文件的方式来记录日志。

不过，log_fp为什么没有是有效值呢？

是需要调用这个aml_log_set_output_file函数才有效。

## asplay设置set-logpriority和set-loglevel过程

trace level是指什么？跟loglevel有什么区别？

都是被audioservice的on_handle_system_command函数处理。

sys_command_setloglevel函数处理。

调用了这个函数aml_log_set_from_string

是设置给了aml_log.c里的函数。

有这么两个函数

```
void aml_log_set_from_string(const char *str);
void aml_trace_set_from_string(const char *str);
```

区别是这样：

```
void aml_log_set_from_string(const char *str) {
    if (!strncmp(level_str, str, strlen(str))) return;
    strncpy(level_str, str, 256);
    aml_log_sync_config_file(str);
    get_setting_from_string(AML_DEBUG_LOG, str);
}

void aml_trace_set_from_string(const char *str) {
    get_setting_from_string(AML_TRACE_LOG, str);
}
```

AML_SYSLOG展开是这样

```
AML_SYSLOG(LOG_INFO, "aaa");
展开得到：
AML_LOG_CAT(DEFAULT,  LOG_INFO, "aaa")
进一步展开：
do {                                                                                           \
        if (AML_LOG_DEFAULT->log_level > LOG_INFO) {                                 \
            aml_log_msg(&(AML_LOG_DEFAULT), LOG_INFO, __FILE__, __func__, __LINE__, "aaa");                                                        \
        }                                                                                          \
    } while (0)
	
static struct AmlLogCat AML_LOG_LAST = {NULL, 0, 0, NULL};
struct AmlLogCat AML_LOG_DEFAULT = {"default", 1, 1, &AML_LOG_LAST};
aml_log_msg里面就是把buf构造处理，然后调用fprintf打印。

```

LOG_INFO 这个宏是从syslog里借用来的。

```
#define LOG_EMERG   0
#define LOG_ALERT   1
#define LOG_CRIT    2
#define LOG_ERR     3
#define LOG_WARNING 4
#define LOG_NOTICE  5
#define LOG_INFO    6
#define LOG_DEBUG   7
```

当前这么设计，没有看出什么特别的用处来，是可以分文件、分模块来设置吗？怎么配置呢？



下面这个是控制halaudio层的打印

```
echo "AML_AUDIO_DEBUG=1" >/tmp/AML_AUDIO_DEBUG
echo "AML_AUDIO_DEBUG=2" >/tmp/AML_AUDIO_DEBUG
echo "AML_AUDIO_DEBUG=3" >/tmp/AML_AUDIO_DEBUG
echo "AML_AUDIO_DEBUG=4" >/tmp/AML_AUDIO_DEBUG
echo "AML_AUDIO_DEBUG=5" >/tmp/AML_AUDIO_DEBUG
1=LEVEL_INFO  2=LEVEL_DEBUG  3=LEVEL_WARN  4=LEVEL_ERROR 5=LEVEL_FATAL
```

文件是被动态监听的，所以修改可以实时生效。



这样来按模块控制日志级别。

```
AML_LOG_DEFINE(USBPlayer)
#define AML_LOG_DEFAULT AML_LOG_GET_CAT(USBPlayer)
```

目前audioservice里，只有2个单独定义的。

```
halaudio_client.c (homeapp) line 41 : AML_LOG_DEFINE(halaudio_client)
usb_player.c (homeapp) line 40 : AML_LOG_DEFINE(USBPlayer)
```

```
AML_LOG_DEFINE(USBPlayer)
展开是：
struct AmlLogCat AML_LOG_USBPlayer = {
	"USBPlayer",
	AML_LOG_LEVEL_INVALID,
	AML_LOG_LEVEL_INVALID,
	NULL
};
```

如果要单独关闭USBPlayer的日志，应该这样配置

```
aml_log_set_from_string("USBPlayer:LOG_ERR,halaudio_client:LOG_INFO");

aml_log_set_from_string("USBPlayer:LOG_QUIET");
```

```
echo all:LOG_ERR,USBPlayer:LOG_INFO > /tmp/AML_LOG_homeapp
```



参考资料

https://confluence.amlogic.com/pages/viewpage.action?pageId=74514632

https://confluence.amlogic.com/display/SW/BR-AML_LOG

# 当前的日志分析

开头的一段：注意这个声卡的分配情况。

```
audio_hw_device_get_module 
it is TV
max channel 8
Device name=HDMI_IN card=0 device=1
Device name=SPDIF_IN card=0 device=4
Device name=LINE_IN card=0 device=1
Device name=BT_IN card=0 device=0
Device name=LOOPBACK_IN card=1 device=1
Device name=Speaker_Out card=0 device=2
Device name=Spdif_out card=0 device=4
```

然后有一个这个错误

```
6.786332 audioservice[2333] default ERR tid:2333 (as_volume.c 1107 in_AS_Volume_ParseVolumeConfig): unable to open pcm device(tas5782m): No such file or directory
```

然后设置了halaudio的音量

```
6.809002 audioservice[2333] default DEBUG tid:2333 (as_volume.c 566 in_HalAudio_SetVolume): Set hal master volume soft = 100.000000, hardware = 0.000000
6.811026 audioservice[2333] default DEBUG tid:2333 (halaudio_spdif.c 453 HalAudio_SetCommand):  cmd = master_vol=1.000000
```

然后调用了

```
(external/mcu6350_func.c 80 mcu6350_set_update): type:2
```

然后设置了settings里的各个配置项。

一连串的这个打印

```
6.818988 audioservice[2333] default DEBUG tid:2333 (halaudio_spdif.c 416 allinput_halaudio): set halaudio config=file=/etc/dap_tuning_files.xml:endpoint=internal_speaker:virt-enable
6.820516 audioservice[2333] default DEBUG tid:2333 (halaudio.c 127 HalAudio_InputSet): enter6.820540 audioservice[2333] default DEBUG tid:2333 (halaudio_spdif.c 656 halaudio_input_set): setting type = speakers
```

然后打印了

```
(input_mgr.c 1327 AS_Input_Init): Input init successfully
```



# 完整测试环境

现在打算用树莓派4b来作为hdmi输出。

当前的情况是：

1、切换到hdmi输出，没有声音出来。

2、切换到bt的。手机连上来播放，有声音。

3、切换到hdmi arc，会打印内核错误，但是没有死机。

4、直接在板子上执行speaker-test -t pink，有声音输出到外部Speaker。

5、树莓派的耳机孔，接到板子的LINEIN，且板子这边切到LINEIN输入方式，可以正常听到声音。



是树莓派的hdmi输出有问题？

我用电脑试一下。也是不行。



现在是所有的板子的HDMI输入都没有声音。

另外再找了一块板子，这个就可以了。电脑这边连接是有显示声音设备的，播放声音也可以正常出来。



# event机制

就是一个异步机制，跟我一般用的Executor是类似的，相当于提交一个任务到专门的线程来处理，避免阻塞。

# IT66321

电平变化，外面不知道有没有进行一个电平反转。



# audioservice和homeapp的通信协议

收到

```
Method call: GetInputSettings
{"name": "volume"}
```

返回

```
{"name": "volume", "return": 60.0}
```

然后从这个json里解析出需要的60.0这个值。

协议是很简单，但是实现真的很麻烦。主要cjson使用太麻烦了。



在xml里是这样定义的：

```
    <method name="GetInputSettings">
      <arg name="input" direction="in" type="s"/>
      <arg name="settings" direction="out" type="s"/>
      <arg name="reply" direction="out" type="i"/>
    </method>
```

# atmos调试

这里有一些经验文章

https://confluence.amlogic.com/pages/viewpage.action?pageId=74514632



# audioservice的文档

在这里有详细的文档。

https://confluence.amlogic.com/display/SW/aml_log

```
asplay set-loglevel “all:LOG_ERR” or  asplay set-logpriority LOG_ERR
```

# AS resource管理

当前资源管理只管理了alsa device。

尽管当前使用了dmix插件来避免冲突，但是dmix可能导致延迟，导致某些GVA/C4A认证测试通不过。

![image-20211119141847864](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20211119141847864.png)



HalInput_Client: Manage the input like HDMI, AUX, SPDIF, ARC



## C4A



# bt_client

这个在buildroot下，并没有编译。只有c4a的android.mk里有加入编译。

但是buildroot下确实可以用蓝牙，那么具体是怎么实现的呢？

如果要替换为bluez，应该怎么替换呢？

是通过halaudio统一管理的？应该是。bt的是连接到tdma接口上的。反正都是当成声卡来处理的。

这一点从硬件层面怎么理解呢？

蓝牙模块上有pcm引脚，直接接到芯片的tdma引脚上，就这么回事。

所以当前蓝牙是一直开启的，即使没有切换到蓝牙模式。

那么这样播放音乐，蓝牙的声音会出来吗？

不会出来。

# ffmpeg

默认没有配置

```
# BR2_PACKAGE_AUDIOSERVICE_FFMPEG is not set
```

# main volume

这个的意义是什么？

就调节amixer的音量就够了吧。

另外弄一个软件音量，用在什么情况？

遥控能调到吗？



HALAUDIO_EXT_ARCVOLUME_CHANGE

这个是表示什么场景？

表示通过arc连接tv？tv遥控器修改了tv的音量？

把什么信息传递给soundbar了？

是mcu有中断来了。且当前是arc input的模式。

先拿到arc的音量值，然后跟当前的main volume比较，发现不同，就进行设置。

还把external_input_arc_setvolume再设回到tv。



