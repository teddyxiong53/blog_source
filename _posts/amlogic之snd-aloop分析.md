---
title: amlogic之snd-aloop分析
date: 2022-01-027 16:39:01
tags:

	- sound

---

--

之前一直都是用music_vol来作为播放设备的。

```

pcm.mixoutput {
    type dmix
    ipc_key 1024
    slave {
        pcm "hw:1,0,0"
        period_time 0
        period_size 1024
        buffer_size 4096
        rate 48000
        format "S16_LE"
        channels 2
    }

    bindings {
        0 0
        1 1
    }
}

pcm.music_48K {
    type rate
    slave.pcm "mixoutput"
    slave.rate 48000
    converter "speexrate_medium"
}

pcm.music_vol {
    type plug
    slave.pcm "music_48K"
}
```

是通过snd-aloop模块产生的hw:1,0,0作为播放设备。

snd-aloop具体是怎么工作的？

对应的配置项和文件是

```
obj-$(CONFIG_SND_ALOOP) += snd-aloop.o
```

snd-aloop对于你录制mic之外的其他音频源的声音很有用。例如录制某个应用的声音。

load snd-aloop的方法，

手动方式

```
modprobe snd-aloop
```

开机自动加载

```
echo 'snd-aloop' >> /etc/modules
```



```
snd-aloop provides 2 pass-through devices:
card 1, device 0 and
card 1, device 1.
```



hw:1,0,0是播放设备，这样来播放

```
aplay -D hw:1,0,0 1.wav
```

hw:1,1,0是录音设备，这样录音

```
arecord -D hw:1,1,0 1.wav 
```

可以同时录音和播放。验证通路。





用aplay -l查看，看看有没有loopback的设备，

如果没有，使用modprobe snd-aloop来进行插入。



使用ALSA Loopback方式内录音频，可以录取声卡输出的音频而不影响正在播放的音频。

播放音频
aplay -fS16_LE -r16000 xxxx.pcm

录取输出音频
arecord -fS16_LE -r16000 -D "hw:Loopback,1,0" -c2 xxxx.pcm





# 以aloop为例分析snd驱动框架

```
struct loopback
	aloop声卡对应的结构体。
	下面包含一个snd_card指针。相当于继承了snd_card。
	loopback_cable：有8x2个，8个subdevice，play/capture这2个方向。
		相当于连接device跟card的线缆吗？
		线缆有什么特性？2个pcm stream（为什么要有这个？）
		还有一个snd_pcm_hardware成员。（为什么要有这个？）
		3个flag变量：running/pause/valid。（分别什么用途？）
		
	loopback_setup：也有8x2个。
		这个主要是formate/rate/channels这3个。配套snd_ctl_elem_id。
	aloop还有一个mutex的cable_lock。主要在什么情况下进行lock呢？
	还有2个snd_pcm指针。（表示了什么？）
	
	
struct loopback_pcm
	1、持有一个loopback指针。
	2、struct snd_pcm_substream。相当于继承了这个？
	3、struct loopback_cable指针。
	4、其他int变量。还有一个timer_list。
	
snd_pcm_substream
snd_pcm_runtime

aloop在设备树里不存在。不需要任何设备树配置。
驱动是一个platform_driver。
通过platform_device_register_simple接口创建了8个device。
然后把指针存放到全局的struct platform_device *devices[SNDRV_CARDS];指针数组里。
全局的数组还有：
int index[8];
char *id[8];
bool enable[8];
int pcm_substreams[8];//默认是0，创建时，给1
int pcm_notify[8];

每创建一个device，则loopback_probe函数会被调用一次。

loopback_probe函数的逻辑
1、snd_card_new创建一个snd_card结构体，多分配的额外内存给loopback结构体。
2、loopback_pcm_new，调用2次。
3、loopback_mixer_new。
4、loopback_proc_new。调用2次。


loopback_playback_ops
loopback_capture_ops
这2个ops结构体是主要的函数实现。

loopback_open
	就是创建一个loopback_pcm。
	整个操作都用cable_lock锁起来。
	创建了一个loopback_timer_function定时器函数。
		函数的操作是：调用snd_pcm_period_elapsed
	snd_pcm_hw_rule_add依次添加format/rate/channels的约束。
```



# 参考资料

1、Redirect an audio stream with aloop

https://blog.getreu.net/projects/snd-aloop-device/body.html

2、Linux上用ALSA aloop driver实现录制其他程序播放的声音

https://blog.csdn.net/lsheevyfg/article/details/116799564

3、

https://blog.csdn.net/weixin_38387929/article/details/122411732

4、

