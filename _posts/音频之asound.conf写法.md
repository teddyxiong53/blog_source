---
title: 音频之asound.conf写法
date: 2018-09-28 13:58:17
tags:
	- 音频

---



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