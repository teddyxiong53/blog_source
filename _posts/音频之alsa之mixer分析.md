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



# 参考资料

1、

https://stackoverflow.com/questions/19489343/set-alsa-master-volume-in-db-from-c-code

2、Linux音频编程（三）混音器介绍

https://www.cnblogs.com/L-102/p/11526525.html

3、ALSA编程之libasound2库的使用——controls篇

这个里面的鱼骨图画得不错。值得学习。

接口梳理也清楚，示例代码不错。不过示例代码跟alsa-lib下面的test的control.c的差不多。

https://blog.csdn.net/oyoung_2012/article/details/79664491