---
title: avs之笔记本环境搭建
date: 2018-10-27 01:52:25
tags:
	- avs

---



这个是《avs之Linux搭建》的延续，之前是在虚拟机里搭建的。

不能语音交互。

所以现在我要在笔记本上搭建。

整个过程如下。

我总结一下：

1、我的笔记本的录音功能有问题。我试了各种录音工具都不行，才确认这一点。

所以我只能采用usb摄像头来做录音工具。

2、关键就是把usb的作为录音的default设备。这就需要写配置文件来改。



```
teddy@teddy-ThinkPad-SL410:~/work/avs/sdk-folder$ cat /proc/asound/cards
 0 [Intel          ]: HDA-Intel - HDA Intel
                      HDA Intel at 0xf2600000 irq 34
 1 [HDMI           ]: HDA-Intel - HDA ATI HDMI
                      HDA ATI HDMI at 0xf2110000 irq 35
29 [ThinkPadEC     ]: ThinkPad EC - ThinkPad Console Audio Control
                      ThinkPad Console Audio Control at EC reg 0x30, fw 6JHT52WW-1.172000
```

用Python脚本录音也没有内容。

https://segmentfault.com/a/1190000013854294

用audacity录音也没有声音。试一下用外部usb的看看。

查看了设备hw的号。然后录音可以。播放正常。

我怎么来修改默认的声卡到usb声卡呢？

根据这篇文章这么改了。还是不行。还是要指定-Dhw:2,0才行。

https://blog.csdn.net/latticer/article/details/79969468?utm_source=blogxgwz0

```
teddy@teddy-ThinkPad-SL410:~$ cat /etc/asound.conf 
pcm.!default {
    type hw
    card 2

}
ctl.!default {
    type hw
    card 2
}
```

按照这个改，还是不行。

```
$ sudo vim /etc/asound.conf   
defaults.pcm.card 2 
defaults.pcm.device 0  
defaults.ctl.card 2
```

```
teddy@teddy-ThinkPad-SL410:~$ arecord -l
**** CAPTURE 硬體裝置清單 ****
card 0: Intel [HDA Intel], device 0: ALC269 Analog [ALC269 Analog]
  子设备: 0/1
  子设备 #0: subdevice #0
card 2: CAMERA [USB2.0 PC CAMERA], device 0: USB Audio [USB Audio]
  子设备: 1/1
  子设备 #0: subdevice #0
```

参考这篇文章来做。

https://blog.csdn.net/w598753468/article/details/62223119?utm_source=blogxgwz8

还是不行。



https://wiki.archlinux.org/index.php/Advanced_Linux_Sound_Architecture_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

看这篇。

把/etc/asound.conf删掉。

在主目录下，新建.asoundrc文件。

```
teddy@teddy-ThinkPad-SL410:~$ cat .asoundrc 
pcm.!default {
    type asym
        playback.pcm {
            type plug
            slave.pcm "hw:0,0"
        }
    capture.pcm {
        type plug
        slave.pcm "hw:2,0"
    }
}
```

这样可以了。

```
teddy@teddy-ThinkPad-SL410:~$ arecord  -d 3 -f S16_LE -r 44100 1.wav
正在录音 WAVE '1.wav' : Signed 16 bit Little Endian, 频率44100Hz， Mono
teddy@teddy-ThinkPad-SL410:~$ aplay 1.wav 
正在播放 WAVE '1.wav' : Signed 16 bit Little Endian, 频率44100Hz， Mono
```

然后果然就可以了。



# 唤醒词加入

默认都是按键的方式进行交互的。看看怎么加入唤醒词。

