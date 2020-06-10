---
title: 音频之alsa.conf写法
date: 2018-09-28 13:58:17
tags:
	- 音频

---

1

配置文件是在snd_pcm_open的时候，会进行调用。

代码是这样：

```
int snd_pcm_open(snd_pcm_t **pcmp, const char *name, 
		 snd_pcm_stream_t stream, int mode)
{
	snd_config_t *top;//这个结构体存放配置。这个存放一个配置项，多个组成链表。
	int err;

	assert(pcmp && name);
	err = snd_config_update_ref(&top);//这里面读取配置。
	if (err < 0)
		return err;
	err = snd_pcm_open_noupdate(pcmp, top, name, stream, mode, 0);
	snd_config_unref(top);
	return err;
}
```

```
snd_config_update_r
	configs = getenv(ALSA_CONFIG_PATH_VAR);//先从环境变量里读取这个ALSA_CONFIG_PATH路径。
	如果没有，那么就从，默认路径找。
	sprintf(s, "%s/alsa.conf", topdir);
	//找到用户自定义的配置文件。
	err = snd_user_file(name, &local->finfo[k].name);
	//读取配置。
	snd_config_load
```

```
上面的主要说明点：
    .asoundrc和asound.conf的引入提供用户定制化
    /usr/share/alsa/alsa.conf为alsa-api的主要入口点
```

**在alsa.conf中，通常还会引用 /etc/asound.conf 和 ~/.asoundrc这两个配置文件，**

这两个文件通常是放置你个人需要特殊设置的相关参数。

按照Alsa官方文档的说法，1.0.9版本以后，这两个文件就不再是必要的，甚至是不应该需要的。

至少是不推荐使用吧。

不过，对于我来说，在嵌入式系统中使用，为了简单和方便测试，恰恰是需要修改这两个文件 

配置蓝牙播放。

```
# device for bluetooth
pcm.bluetooth{
        type bluetooth
        device 00:02:5B:00:C1:A0
}
 
然后调用 aplay –D bluetooth sample.wav 播放。
```

需要注意，为了使用该设备，你需要 /usr/lib/alsa-lib/libasound_module_pcm_bluetooth.so 这一个蓝牙plugin的库文件。

这是在Bluez相关的包里，和Alsa本身没有关系。

从这里，我们也可以看出alsa的外部plugin和配置文件之间的名字关系规则： libasound_module_pcm_####.so 这里的#### 就是你在conf文件中pcm.xxxx 里所写的名字。

```
snd_pcm_open_conf
```

```
static const char *const build_in_pcms[] = {
	"adpcm", "alaw", "copy", "dmix", "file", "hooks", "hw", "ladspa", "lfloat",
	"linear", "meter", "mulaw", "multi", "null", "empty", "plug", "rate", "route", "share",
	"shm", "dsnoop", "dshare", "asym", "iec958", "softvol", "mmap_emul",
	NULL
};
```

```
sprintf(buf1, "%s/libasound_module_pcm_%s.so", ALSA_PLUGIN_DIR, str);
```



```
type hw 
	这个是用来做alias的。With the 'PCM hw type' you are able to define aliases for your devices.
```

例如，我们常用的指定default的。

```
pcm.!default {
	type hw
	card 0
	device 0
}
```

这个default，我们也可以替换成其他的名字，例如：

```
pcm.primary {
	type hw
	card 0 
	device 0
}
```

录音的时候，我们就这样：

```
arecord -D primary 1.wav
```



alsa-lib的库文件：

```
/usr/lib/alsa-lib # ls                         
libasound_module_ctl_arcam_av.so               
libasound_module_ctl_bluealsa.so               
libasound_module_ctl_oss.so                    
libasound_module_pcm_bluealsa.so               
libasound_module_pcm_oss.so                    
libasound_module_pcm_upmix.so                  
libasound_module_pcm_usb_stream.so             
libasound_module_pcm_vdownmix.so               
libasound_module_rate_samplerate.so            
libasound_module_rate_samplerate_best.so       
libasound_module_rate_samplerate_linear.so     
libasound_module_rate_samplerate_medium.so     
libasound_module_rate_samplerate_order.so      
libasound_module_rate_speexrate.so             
libasound_module_rate_speexrate_best.so        
libasound_module_rate_speexrate_medium.so      
```



一个最简单的配置文件写法是：

```
pcm.!default {
	type hw
	card 1
	device 7
}

ctl.!default {
	type hw
	card 1
	device 7
}
```

card表示声卡号，device表示设备号。

default前的**感叹号用于替代**alsa api 中默认的default配置



首先，无论是用户是.asoundrc还是系统的asound.conf都不是alsa一定要的。

大多数情况下，没有这些配置文件，还是可以正常工作的。

因为默认给了一个合理配置。

配置文件一般是做一些扩展功能。

alsa-lib的配置文件框架。

/usr/share/asla/asla.conf是主入口文件。

```
/usr/share/alsa # ls
alsa.conf         init              speaker-test
alsa.conf.d       pcm               topology
cards             sndo-mixer.alisp  ucm
```

这些文件都写得非常长。

```
cat /proc/asound/cards
 0 [AMLAUGESOUND   ]: AML-AUGESOUND - AML-AUGESOUND
                      AML-AUGESOUND
```

```
/proc/asound # ls
AMLAUGESOUND  cards         hwdep         timers
card0         devices       pcm           version
/proc/asound #
```



使用#号作为注释。

键值对语法。

```
key [
	"value0";
	"value1";
]
```

等价于：

```
key.0 "value0";
key.1 "value1";
```

```
key {
	subkey0 value0;
	subkey1 value1
}
```

等价于：

```
key.subkey0 value0;
key.subkey1 value1;
```



操作模式

```
用前缀来表示。默认是merge and create模式。
有4种模式。
+ ： merge and create。
- ： merge
？ ： 不要覆盖。
！：覆盖。
```





配置文件的位置

```
/usr/share/alsa
```

这个目录下的文件有：

```
alsa.conf        
alsa.conf.d      
cards            
init             
pcm              
sndo-mixer.alisp 
speaker-test     
topology         
ucm              
```

主配置文件就是这个alsa.conf文件。内容比较多。

首先是读取/etc/asound.conf和~/.asoundrc这2个文件的内容。

```

```



声卡设备的编号。

在/dev/snd目录下，看到这些char设备文件。

```
controlC0  ：control开头的，表示用于声卡的控制，例如通道选择，混音，麦克风控制。C表示Card。
controlC1  
controlC7  
pcmC0D0c   C0D0：card 0 device 0 。最后的c表示录音（capture）。前面的pcm表示pcm设备。对应的还有midi设备。
pcmC0D0p   p表示播放，play。
pcmC1D0c   
pcmC1D0p   
pcmC7D0c   
pcmC7D0p   
pcmC7D1c   
pcmC7D1p   
timer      
```

另外在/proc/asound/目录下，有这些：

```
/proc/asound # ls
Loopback         card7            pcm              timers
card0            cards            rockchiprk3308p  version
card1            devices          rockchiprk3308v
```

查看devices文件。

```
/proc/asound # cat devices
  0: [ 0]   : control
 16: [ 0- 0]: digital audio playback
 24: [ 0- 0]: digital audio capture
 32: [ 1]   : control
 33:        : timer
 48: [ 1- 0]: digital audio playback
 56: [ 1- 0]: digital audio capture
224: [ 7]   : control
240: [ 7- 0]: digital audio playback
241: [ 7- 1]: digital audio playback
248: [ 7- 0]: digital audio capture
249: [ 7- 1]: digital audio capture
```



pcm逻辑设备

我们习惯称之为pcm中间层，或者pcm native。



alsa用card、device和subdevice的分层结构来表示audio硬件设备和它们的组件。

层次关系是这样。

```
card0
	device0
		subdevice0
	device1
	
card1
	device0
```



这个分层结构是alsa看待硬件设备结构和能力的视角。

card和硬件上的声卡是一一对应的。

大部分的alsa硬件访问发生在device这个层级。

一个card上有多个device。

card+device的组合，基本可以说清楚，一个声音从哪里来，到哪里去。

subdevice，一般是对应一个通道。



alsa几乎都是由plugin构成的。

plugin列表不等同于alsa device列表。

有些device的名字跟plugin的名字一样，有些不一样。

最重要的plugin就是hw plugin。

它本身不做任何任何处理。

仅仅访问硬件驱动。



alsa.conf最终被解释为一棵树，它的节点是struct _snd_config结构，





# defaults

一般alsa设置了一个defaults设备，音频播放软件默认使用defaults设备输出声音。defaults设备定义在alsa.conf中。

defaults会默认匹配card number和device number比较小的声卡。

alsa的配置文件是alsa.conf位于/usr/share/alsa目录下，通常还有/usr/share/alsa/card和/usr/share/alsa/pcm两个子目录用来设置card相关的参数，别名以及一些PCM默认设置。以上配置文件，我等凡夫从不用修改，修改它们是大神的工作。



# plugin插件写法

插件是用来扩展pcm设备的功能和特性的。

插件可以做的事情：

```
采样率转化
通道之间复制。

```

往树莓派的.asoundrc里加几行配置，启动录音。报错。

```
pi@raspberrypi:~ $ arecord 2.wav
ALSA lib conf.c:1887:(_snd_config_load_with_include) _toplevel_:22:0:Unexpected char
ALSA lib conf.c:3650:(config_file_open) /home/pi/.asoundrc may be old or corrupted: consider to remove or fix it
ALSA lib conf.c:3572:(snd_config_hooks_call) function snd_config_hook_load returned error: Invalid argument
ALSA lib conf.c:4026:(snd_config_update_r) hooks failed, removing configuration
arecord: main:828: audio open error: Invalid argument
```

在asoundrc里加上这个。

```
pcm_slave.test123 {
    pcm "hw:1,0"
    format S16_LE
    rate 48000
}
pcm.rate_convert {
    type rate
    slave test123
}
```

录音命令：-v表示verbose。

```
arecord -vD rate_convert  3.wav
```

打印的输出：

## asym

*asym* is an ALSA PCM plugin that combines **half-duplex** PCM plugins like *dsnoop* and *dmix* into one **full-duplex** device

asym是asymmetrically的缩写。这个单词的意思是非对称。也就是播放和录音分开设置。

asym是一个插件，作用是把半双工的插件（比如dsnoop、dmix）转换成全双工的设备。

主要用来配置模式的录音和播放设备。



## dsnoop

dsnoop是d + snoop（探听）。

d表示：direct。

arecord -L，查看树莓派。

有一行是这样的打印的：

```
dsnoop:CARD=CAMERA,DEV=0
    USB2.0 PC CAMERA, USB Audio
    Direct sample snooping device
```

https://alsa.opensrc.org/Dsnoop

这样来使用：

```
arecord -f cd -c 2 -D dsnoop foobar.wav
```





## hw

这种插件是直接跟alsa的kernel 驱动通信。

这个一个raw的通信，没有任何转换。



## dmix

```
pcm.card0 {
	type hw
	card 0
}
pcm.!default {
	type plug
	slave.pcm "dmixer"
}

pcm.dmixer {
	type dmix
	ipc_key 1025
	slave {
		pcm "hw:0,0"
		period_time 0
		period_size 4096
		buffer_size 16384
		periods 128
		rate 44100
	}
	bindings {
		0 0 
		1 1
	}
}
```





播放增益设置

录音声道转换



数字音频有几个参数是我们需要关注的：

采样率、通道数、格式。

如果你用过oss编程。你可能是在播放某个文件前，一个一个设置过这些参数。

在alsa里，你会碰到一个概念：Configuration space。配置空间。

这个具体指什么呢？

这个产生的原因是：现实中声卡差别比较大，事情就变得复杂了。

参数不是独立的。

alsa通过一个多维度的参数集来描述。

其中一个维度对应采样率，一个维度对应格式，等等。



alsa设备，是各种插件的wrapper。

alsa设备由字符串来描述。

设备是在配置文件里定义的。

很多alsa设备是通用的。

alsa设备列表跟插件列表不一样。

毫不夸张地说，alsa完全是由插件构成的。

每当播放器或者其他程序使用alsa设备的时候，是插件来完成实际的工作。



最重要的插件就是hw插件。

它不进行自己的处理，而只是访问硬件驱动程序。

hw插件的用法：

```
-D hw:0,0
```



如果使用hw插件时，给定的参数，是硬件所不支持的，则hw插件会返回错误。



所以下一个最重要的插件是plug插件。plug插件会进行通道复制、格式转化和重采样。

用法是：

```
-D plughw:0,0
```

另外一个非常有用的插件是file插件。

常见的用法是：

```
aplay -D tee:\'plughw:0,0\',/tmp/1.out,raw 1.wav
```

可以在听到声音的同时，把播放的声音保存起来。



snd_open的时候，都会重新解析配置文件，所以修改配置文件后，程序执行你的程序，就可以生效的。



# 播放设备名

default：对于大部分应用，用这个就够了。一般使用pulseaudio或者dmix。这样就可以多个应用同时使用声卡了。

front：直接访问硬件，模拟输出。2个通道。通道图：front-left、front-right。

rear：单词意思是后面，跟front相对。直接访问硬件。模拟输出。2个通道。通道图：rear-left、rear-right。

center_lfe：

side

surround40：4个通道。front-left、front-right、rear-left、rear-right。

spdif

hdmi

hw

plughw



设备名前面可以加上`plug:`

例如：

```
plug:front
```

作用是实现参数转化。



# 录音设备名

default 

hw



# alsa.conf文件分析

```
@hooks [ # 这个是默认就会调用的。是一个数组，里面可以有多个对象。
		# 对应的代码函数是：snd_config_hook_load_for_all_cards
	{ # 当前只放了一个对象。
		func load
	}
]
```



参考资料

1、asound.conf配置

https://blog.csdn.net/zhangxu365/article/details/8449118

2、官方配置文件说明

http://www.alsa-project.org/main/index.php/Asoundrc

3、

https://wiki.archlinux.org/index.php/Advanced_Linux_Sound_Architecture_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

4、理解和使用Alsa的配置文件

https://blog.csdn.net/colorant/article/details/2598815

5、

http://www.voidcn.com/article/p-dsamalpt-bht.html

6、Linux ALSA 音频系统：逻辑设备篇

https://blog.csdn.net/zyuanyun/article/details/59180272

7、深入了解ALSA

https://blog.csdn.net/kickxxx/article/details/8291598

8、

https://blog.csdn.net/MyArrow/article/details/8230231?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task

9、

https://www.alsa-project.org/wiki/Asoundrc

10、Flask与pyaudio实现音频数据流的传输(电话会议语音交互式应用)

https://blog.csdn.net/weixin_30699831/article/details/99924273

11、alsa设置默认声卡

https://blog.csdn.net/samssm/article/details/53157210

12、alsa-lib的alsa.conf

https://www.pianshen.com/article/684731740/

13、alsa

https://www.volkerschatz.com/noise/alsa.html

14、DeviceNames

https://alsa-project.org/wiki/DeviceNames