---
title: 音频（3）alsa-utils
date: 2018-05-31 22:54:16
tags:
	- 音频

---



alsa-utils是一套linux下的命令行工具。

主要包括：
1、alsactl。

2、aconnect。

3、alsamixer。

4、amidi。

5、amixer。

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





# 参考资料

1、alsa-utils工具包的使用

http://www.docin.com/p-1930060117.html

2、linux alsa音频架构的配置与使用

https://soilhead.cn/linux/17.html