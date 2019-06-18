---
title: 音频（3）alsa-utils
date: 2018-05-31 22:54:16
tags:
	- 音频

---



alsa-utils是一套linux下的命令行工具。

主要包括：

1、alsactl。设置。

2、aconnect。

3、alsamixer。是amixer的图形化（ncurses）版本。

4、amidi。

5、amixer。命令行方式进行mixer设置。

6、aplay。

7、aplaymidi。

8、arecord。

9、arecordmidi。

10、aseqnet。

11、iecset。

12、speaker-test。



proc目录下的相关信息。

```
teddy@teddy-ubuntu:/proc/asound$ tree
.
├── AudioPCI -> card0
├── CAMERA -> card1
├── card0
│   ├── audiopci
│   ├── codec97#0
│   │   ├── ac97#0-0
│   │   └── ac97#0-0+regs
│   ├── id
│   ├── midi0
│   ├── pcm0c
│   │   ├── info
│   │   └── sub0
│   │       ├── hw_params
│   │       ├── info
│   │       ├── prealloc
│   │       ├── prealloc_max
│   │       ├── status
│   │       └── sw_params
│   ├── pcm0p
│   │   ├── info
│   │   └── sub0
│   │       ├── hw_params
│   │       ├── info
│   │       ├── prealloc
│   │       ├── prealloc_max
│   │       ├── status
│   │       └── sw_params
│   └── pcm1p
│       ├── info
│       └── sub0
│           ├── hw_params
│           ├── info
│           ├── prealloc
│           ├── prealloc_max
│           ├── status
│           └── sw_params
├── card1
│   ├── id：里面的内容就是CAMERA。
│   ├── pcm0c
│   │   ├── info
│   │   └── sub0
│   │       ├── hw_params
│   │       ├── info
│   │       ├── status
│   │       └── sw_params
│   ├── stream0
│   ├── usbbus
│   ├── usbid
│   └── usbmixer
├── cards
├── devices
├── hwdep
├── modules
├── oss
│   ├── devices
│   └── sndstat
├── pcm
├── seq
│   ├── clients
│   ├── drivers
│   ├── queues
│   └── timer
├── timers
└── version
```

我们重点看看card1的，就是CAMERA的。

```
teddy@teddy-ubuntu:/proc/asound/card1$ cat stream0 
Generic USB2.0 PC CAMERA at usb-0000:02:03.0-1, high speed : USB Audio

Capture:
  Status: Stop
  Interface 3
    Altset 1
    Format: S16_LE
    Channels: 1
    Endpoint: 3 IN (NONE)
    Rates: 48000
    Data packet interval: 1000 us
```

```
teddy@teddy-ubuntu:/proc/asound/card1$ cat usbmixer 
USB Mixer: usb_id=0x19082310, ctrlif=2, ctlerr=0
Card: Generic USB2.0 PC CAMERA at usb-0000:02:03.0-1, high speed
  Unit: 2
    Control: name="Mic Capture Volume", index=0
    Info: id=2, control=2, cmask=0x1, channels=1, type="S16"
    Volume: min=0, max=5328, dBmin=0, dBmax=2081
  Unit: 2
    Control: name="Mic Capture Switch", index=0
    Info: id=2, control=1, cmask=0x1, channels=1, type="INV_BOOLEAN"
    Volume: min=0, max=1, dBmin=0, dBmax=0
```

```
teddy@teddy-ubuntu:/proc/asound/card1/pcm0c$ cat info 
card: 1
device: 0
subdevice: 0
stream: CAPTURE
id: USB Audio
name: USB Audio
subname: subdevice #0
class: 0
subclass: 0
subdevices_count: 1
subdevices_avail: 1
```



```
amixer contents
```

查看笔记本的声卡有哪些。 是有三张。

```
teddy@teddy-ThinkPad-SL410:/dev/snd$ cat /proc/asound/cards 
 0 [Intel          ]: HDA-Intel - HDA Intel
                      HDA Intel at 0xf2600000 irq 34
 1 [HDMI           ]: HDA-Intel - HDA ATI HDMI
                      HDA ATI HDMI at 0xf2110000 irq 35
29 [ThinkPadEC     ]: ThinkPad EC - ThinkPad Console Audio Control
                      ThinkPad Console Audio Control at EC reg 0x30, fw 6JHT52WW-1.172000
```

我的板子是有两张。

```
/dev/snd # cat /proc/asound/cards
 0 [rockchiprk3308a]: rockchip_rk3308 - rockchip,rk3308-acodec
                      rockchip,rk3308-acodec
 7 [Loopback       ]: Loopback - Loopback
                      Loopback 1
```

查看声卡0有哪些控件。

```
teddy@teddy-ThinkPad-SL410:/dev/snd$ amixer -c 0 controls 
numid=21,iface=CARD,name='Headphone Jack'
numid=19,iface=CARD,name='Internal Mic Phantom Jack'
numid=20,iface=CARD,name='Internal Mic Phantom Jack',index=1
numid=18,iface=CARD,name='Mic Jack'
numid=22,iface=CARD,name='Speaker Phantom Jack'
numid=17,iface=MIXER,name='Master Playback Switch'
numid=16,iface=MIXER,name='Master Playback Volume'
numid=2,iface=MIXER,name='Headphone Playback Switch'
numid=1,iface=MIXER,name='Headphone Playback Volume'
numid=25,iface=MIXER,name='PCM Playback Volume'
numid=14,iface=MIXER,name='Mic Boost Volume'
numid=7,iface=MIXER,name='Mic Playback Switch'
numid=6,iface=MIXER,name='Mic Playback Volume'
numid=11,iface=MIXER,name='Capture Source'
numid=13,iface=MIXER,name='Capture Switch'
numid=12,iface=MIXER,name='Capture Volume'
numid=5,iface=MIXER,name='Loopback Mixing'
numid=10,iface=MIXER,name='Auto-Mute Mode'
numid=26,iface=MIXER,name='Digital Capture Volume'
numid=15,iface=MIXER,name='Internal Mic Boost Volume'
numid=9,iface=MIXER,name='Internal Mic Playback Switch'
numid=8,iface=MIXER,name='Internal Mic Playback Volume'
numid=4,iface=MIXER,name='Speaker Playback Switch'
numid=3,iface=MIXER,name='Speaker Playback Volume'
numid=24,iface=PCM,name='Capture Channel Map'
numid=23,iface=PCM,name='Playback Channel Map'
```

查看控件的内容。

```
amixer -c 0 contents 
```

设置音量。

上面看到音量对应的numid是16。

获取当前音量。

```
teddy@teddy-ThinkPad-SL410:/dev/snd$ amixer cget numid=16
numid=16,iface=MIXER,name='Master Playback Volume'
  ; type=INTEGER,access=rw---R--,values=1,min=0,max=64,step=0
  : values=56
  | dBscale-min=-64.00dB,step=1.00dB,mute=0
```

修改音量。之所以要2个值，是一个左声道音量，一个右声道音量。

```
amixer cset numid=16 30,30 
```

这种写法显得比较复杂。

amixer有个子命令，叫sset。是Simple  set的缩写。

查看一下

```
teddy@teddy-ThinkPad-SL410:/dev/snd$ amixer scontrols 
Simple mixer control 'Master',0
Simple mixer control 'Headphone',0
Simple mixer control 'Speaker',0
Simple mixer control 'PCM',0
Simple mixer control 'Mic',0
Simple mixer control 'Mic Boost',0
Simple mixer control 'Capture',0
Simple mixer control 'Auto-Mute Mode',0
Simple mixer control 'Digital',0
Simple mixer control 'Internal Mic',0
Simple mixer control 'Internal Mic 1',0
Simple mixer control 'Internal Mic Boost',0
Simple mixer control 'Loopback Mixing',0
```

我们获取一下master的音量。

```
teddy@teddy-ThinkPad-SL410:/dev/snd$ amixer sget Master
Simple mixer control 'Master',0
  Capabilities: pvolume pvolume-joined pswitch pswitch-joined
  Playback channels: Mono
  Limits: Playback 0 - 64
  Mono: Playback 30 [47%] [-34.00dB] [on]
```

设置一下master的音量。

```
amixer sset Master 40
```



# 参考资料

1、alsa-utils工具包的使用

http://www.docin.com/p-1930060117.html

2、linux alsa音频架构的配置与使用

https://soilhead.cn/linux/17.html

3、The field ipc_gid must be a valid group (create group audio)

https://blog.csdn.net/guet_kite/article/details/80396546