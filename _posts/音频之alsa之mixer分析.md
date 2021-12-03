---
title: 音频之alsa之mixer分析
date: 2020-04-27 17:52:08
tags:
	- 音频

---

--



什么是mixer？主要起什么作用？

mixer从字面含义看，是混音器的意思。那么起的作用就是把多路音频混合到一起的。

我现在是希望通过db值来设置音量，网上找了一个资料，就是使用了mixer的接口来做的。

但是我对mixer并不太了解，所以就以此为契机，进行一下了解。



mixer:

用来控制多个输入、输出的音量,

也控制输入(microphone,line-in,CD)之间的切换，

可以将多个信号组合或者叠加在一起。

声卡上的混音器由**多个混音通道组成**，

它们可以通过声卡驱动程序提供的设备文件/dev/mixer进行编程（对混音器进行操作的软件接口），

混音器主要是对声卡的输入增益和输出增益进行调节。

**混音器的操作不符合典型的读/写操作模式，**

**除了open和close系统调用，大部分通过ioctl系统调用来完成的。**

与/dev/dsp不同，/dev/mixer允许多个应用程序同时访问，

并且混音器的设置值会一直保持到对应的设备文件被关闭为止。

Linux上的声卡驱动程序大多都支持将混音器的ioctl操作直接应用到声音设备上，

也就是说如果已经打开了/dev /dsp，那么就不用再打开/dev/mixer来对混音器进行操作，

而是可以直接用打开/dev/dsp时得到的文件标识符来设置混音器。

常用的mixer控制有

```
SOUND_MIXER_VOLUME 主音量调节
SOUND_MIXER_BASS 低音控制
SOUND_MIXER_TREBLE 高音控制
SOUND_MIXER_SYNTH FM 合成器
SOUND_MIXER_PCM 主D/A 转换器
SOUND_MIXER_SPEAKER PC 喇叭
SOUND_MIXER_LINE 音频线输入
SOUND_MIXER_MIC 麦克风输入
SOUND_MIXER_CD CD 输入
SOUND_MIXER_IMIX 放音音量
SOUND_MIXER_ALTPCM 从D/A 转换器
SOUND_MIXER_RECLEV 录音音量
SOUND_MIXER_IGAIN 输入增益
SOUND_MIXER_OGAIN 输出增益
SOUND_MIXER_LINE1 声卡的第1 输入
SOUND_MIXER_LINE2 声卡的第2 输入
SOUND_MIXER_LINE3 声卡的第3 输入
```

alsa框架下的是/dev/snd/controlC0这样的文件名来打开mixer。

```
snprintf(fn, sizeof(fn), "/dev/snd/controlC%u", card);
    fd = open(fn, O_RDWR);
```







打开alsa-lib的代码，在src/mixer目录下，放的就是mixer相关代码。

看simple.c这个文件。这个是封装的简单接口。主要就是使用这里的接口。



```
struct _snd_mixer_class 
	主要就是包括了一个snd_mixer_t。
```

```
struct _snd_mixer 
	3个list：
		slaves
		classes
		elems
	snd_mixer_elem_t **pelems
		所有的elem
	
```

```
struct _snd_mixer_elem
	主要就是包括一个snd_mixer_class_t。
	
```



以amixer info命令执行的为例进行分析。

```
/dev/snd # amixer info                                     
Card default 'rockchiprk3308a'/'rockchip,rk3308-acodec'    
  Mixer name    : ''                                       
  Components    : ''                                       
  Controls      : 80                                       
  Simple ctrls  : 64                                       
/dev/snd #                                                 
```

用到的数据结构有：

```
snd_ctl_t *handle;
snd_mixer_t *mhandle;
```



```
Card default 'rockchiprk3308a'/'rockchip,rk3308-acodec'  
	这一行信息是：printf("Card %s '%s'/'%s'\n", card, snd_ctl_card_info_get_id(info),
	       snd_ctl_card_info_get_longname(info));
```



mixer的相关接口：

```
err = snd_mixer_open(&mhandle, 0)
	打开，得到一个snd_mixer_t的handler指针。
snd_mixer_selem_register
	这个注册是起什么作用？
snd_mixer_attach(mhandle, "default")
	把mixer跟声卡绑定起来。
err = snd_mixer_load(mhandle);
	载入。	
snd_mixer_get_count(mhandle)
	获取control的个数。
	就是上面的Simple ctrls  : 64   
snd_mixer_close(mhandle);
	关闭。
```



从上面的内容，目前涉及到这些概念：

```
mixer
elem
simple elem
```



自己编译amixer的代码，方便加代码调试。名字之所以叫simple_test，是因为我加在buildroot里的测试project就叫simple_test，我把amixer的代码拷贝过来编译的。

```
/userdata # ./simple_test -d sset Master 50% 
Simple mixer control 'Master',0              
  Capabilities: pvolume                      
  Playback channels: Front Left - Front Right
  Limits: Playback 0 - 255                   
  Mono:                                      
  Front Left: Playback 128 [50%] [-25.40dB]  
  Front Right: Playback 128 [50%] [-25.40dB] 
```

-d这个表示debug，但是只对cset的场景有用。

对应全局变量是debugflag。基本没怎么用。所以debug是形同虚设的。



看上面命令的调用函数情况。

```
snd_mixer_open(&handle, 0)
snd_mixer_attach(handle, card)
snd_mixer_selem_register(handle, smixer_level > 0 ? &smixer_options : NULL, NULL)
err = snd_mixer_load(handle);
elem = snd_mixer_find_selem(handle, sid);
snd_mixer_selem_has_playback_channel
snd_mixer_selem_has_playback_volume
snd_mixer_selem_get_playback_volume_range
snd_mixer_selem_get_playback_volume
snd_mixer_selem_set_playback_volume
```



现在看我通过db值来获取和设置音量的情况。

```
snd_mixer_selem_get_playback_volume(m_elem, SND_MIXER_SCHN_FRONT_LEFT, &vol);
```

这样获取的是0到255的值，不是百分比。



```
snd_mixer_selem_id_get_name(sid)
snd_mixer_selem_id_get_index(sid)
	用这2个函数里获取name和index，直接访问属性会访问不到，因为没有在对外的头文件里暴露。
```



50%的值，显示的dB值为-25.40。实际值是-2540 。在显示的时候进行除以100的操作了。

从get_range看，dB值的范围是

```
min:-5100, max:0
```



# ctl和mixer是什么关系

一个mixer上可以挂一个ctl链表。

一个ctl，是通过name来打开的。例如default这样的名字。

一个mixer内部，是没有明确包含哪个网卡的信息的。

靠mixer里的slaves链表来包含。



ctl也有element。

mixer也有element。

ctl的type有hw、shm。

mixer的type只有一个simple。

二者建立关联的地方，就是attach的时候，

```
snd_mixer_attach
```

这个函数的实现是：

```
int snd_mixer_attach(snd_mixer_t *mixer, const char *name)
{
	snd_hctl_t *hctl;
	int err;

	err = snd_hctl_open(&hctl, name, 0);
	if (err < 0)
		return err;
	err = snd_mixer_attach_hctl(mixer, hctl);
	if (err < 0)
		return err;
	return 0;
}
```

就是这里，把private指针设置为了mixer。

```
snd_hctl_set_callback(hctl, hctl_event_handler);
snd_hctl_set_callback_private(hctl, mixer);
```

poll fd，是哪个fd的？这个是open pcm设备的fd。

```
pcm->poll_fd = fd;
pcm->poll_events = info.stream == SND_PCM_STREAM_PLAYBACK ? POLLOUT : POLLIN;
```



还有这样一个函数，把mixer的element和ctl的element关联起来，作用是什么？

```
int snd_mixer_elem_attach(snd_mixer_elem_t *melem,
			  snd_hctl_elem_t *helem)
```



ctl和mixer都是对应clt设备的，而不是pcm设备的。

open pcm设备的时候，也会打开clt设备，例如在snd_pcm_hw_open里，就调用了snd_ctl_hw_open

不过就用了一下，然后就close了。

```
ret = snd_ctl_pcm_prefer_subdevice(ctl, subdevice);
```



snd_hctl_throw_event 这个函数里，调用hctl的callback函数。

可以有的event是这些：

```
add
remove
tlv
info
value
```

例如snd_hctl_elem_add的时候，就throw了add event。

snd_mixer_handle_events调用了snd_hctl_handle_events，遍历slave链表。

snd_mixer_handle_events就是被用户代码调用的。在wait之后调用。

会有哪些mixer event产生呢？也就是ctl event了。

读取事件是这个函数：

```
static int snd_ctl_hw_read(snd_ctl_t *handle, snd_ctl_event_t *event)
```

通过读取pcmcontrol节点的

```
read(hw->fd, event, sizeof(*event));
```

读取到event如何处理？

snd_hctl_handle_event这个公共处理。

例如add，通过snd_hctl_elem_add来处理。

对于remove和value事件，会调用到snd_hctl_elem_throw_event，里面会通过回调调用到用户代码注册进来的回调。当前注册进去的回调是处理volume和mute发生变化时的处理。



snd_mixer_class_t

这个结构体的作用是什么？

每个snd_mixer_elem_t都有一个snd_mixer_class_t指针，表示elem的类型？

每种class的elem处理event不一样。

```
err = class->event(class, mask, helem, melem);
```

class的event处理函数在哪里指定的？

snd_mixer_class_register

默认都注册了一个simple_event的处理函数。

```
	snd_mixer_class_set_event(class, simple_event);
	snd_mixer_class_set_compare(class, snd_mixer_selem_compare);
	err = snd_mixer_class_register(class, mixer);
```

有必要再读一下amixer的代码。



# 参考资料

1、

https://stackoverflow.com/questions/19489343/set-alsa-master-volume-in-db-from-c-code

2、Linux音频编程（三）混音器介绍

https://www.cnblogs.com/L-102/p/11526525.html

3、ALSA编程之libasound2库的使用——controls篇

这个里面的鱼骨图画得不错。值得学习。

接口梳理也清楚，示例代码不错。不过示例代码跟alsa-lib下面的test的control.c的差不多。

https://blog.csdn.net/oyoung_2012/article/details/79664491