---
title: 音频之alsa之mixer分析
date: 2020-04-27 17:52:08
tags:
	- 音频

---

1

什么是mixer？主要起什么作用？

mixer从字面含义看，是混音器的意思。那么起的作用就是把多路音频混合到一起的。

我现在是希望通过db值来设置音量，网上找了一个资料，就是使用了mixer的接口来做的。

但是我对mixer并不太了解，所以就以此为契机，进行一下了解。

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



参考资料

1、

https://stackoverflow.com/questions/19489343/set-alsa-master-volume-in-db-from-c-code