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



# ==

用aplay -l查看，看看有没有loopback的设备，

如果没有，使用modprobe snd-aloop来进行插入。



使用ALSA Loopback方式内录音频，可以录取声卡输出的音频而不影响正在播放的音频。

播放音频
aplay -fS16_LE -r16000 xxxx.pcm

录取输出音频
arecord -fS16_LE -r16000 -D "hw:Loopback,1,0" -c2 xxxx.pcm







# 参考资料

1、Redirect an audio stream with aloop

https://blog.getreu.net/projects/snd-aloop-device/body.html

2、Linux上用ALSA aloop driver实现录制其他程序播放的声音

https://blog.csdn.net/lsheevyfg/article/details/116799564