---
title: 音频之alsa配置输出到fifo
date: 2020-06-11 17:25:08
tags:
	- 音频

---

1

因为需要把蓝牙的播放，也可以通过snapcast进行发送。

要达到这个目标，有两种思路：

1、修改bluealsa的代码，把本来通过snd_pcm_writei写入到声卡的数据，修改为写入snapfifo。这个通路我已经实现。但是按照之前的设计，进入到snapfifo里的数据，都要是48000/16/2的格式的。这就需要我在蓝牙sbc解码的时候进行重采样。这个有点麻烦。

2、直接把alsa配置为全部写入到snapfifo。

这个就简单一些，按道理不用改其他播放器的内容，只需要修改配置文件就可以。

在snapcast的issue讨论里有这样一个配置，看他们说，都是可以正常工作的。

```
pcm.!default {
	type plug
	slave {
		pcm rate48000Hz # Direct default output to the below converter
	}
}
pcm.rate48000Hz {
	type rate
	slave {
		pcm writeFile # Direct to the plugin which will write to a file
		format S16_LE
		#channels 2
		rate 48000
	}
	#route_policy copy
}

pcm.writeFile {
	type file
	slave {
		#pcm card0 # Now write to the actual sound card
		pcm null
	}
	file "/tmp/snapfifo"
	format "raw"
}

```

但是在我的Ubuntu笔记本上，没有起作用。

我用aplay和speaker-test测试，都还是直接从笔记本上发声。按道理应该把声音发送到我的手机上发出来的。

而这个配置在我的板端，则问题更加严重。

```
Playback device is default
Stream parameters are 48000Hz, S16_LE, 1 channels
Using 16 octaves of pink noise
Rate set to 48000Hz (requested 48000Hz)
Buffer size range from 1 to 206158430
Period size range from 0 to 206158431
Using max buffer size 206158428
Periods = 4
ALSA lib pcm_mmap.c:399:(snd_pcm_mmap) malloc failed: Cannot allocate memory
Unable to set hw params for playback: Cannot allocate memory
Setting of hwparams failed: Cannot allocate memory
```

我还是先在我的笔记本上调通。

这样改是可以的：

```
pcm.!snapcast {
	//..
}
```

就是把default改成snapcast。然后播放的时候：

```
aplay -D snapcast 1.wav
```

这样就可以达到预期的效果。



下面看看板端的问题。

板端的音频配置，看看/usr/share/alsa下面的配置有什么不同。

没有什么大的不同。

其实是正常的。

speaker-test不能正常工作而已。

aplay播放一首歌曲，是正常的。



现在正式把这些修改放到板端运行。发现问题：

```
/userdata # amixer sget Master
amixer: Unable to find simple control 'Master',0
```

找不到Master这个控制音量的control了。

我加上这个还是不行：

```
defaults.pcm.rate_converter "speexrate_medium"

pcm.!default
{
    type asym
    playback.pcm {
        type plug
        slave.pcm "softvol"
    }
    capture.pcm {
        type plug
        slave {
            pcm "hw:0,0"
        }
    }
}
pcm.softvol {
    type softvol
    slave.pcm "snapcast"
    control {
        name "Master Playback Volume"
        card 0
    }
    min_dB -40.0
    max_dB 0.0
    resolution 100
}
```

amixer scontrols 这个命令查看也没有看到Master的。

在我的笔记本上，则是可以看到的。

在我改动之前，板端的音量也还是正常的。

需要把驱动看一下。看看这些control是如何被注册到系统里的。

驱动里的确是没有Master的。

看来这个要靠应用层配置文件里注册。



经过测试，发现这样的现象：

1、rootfs里，先不改/etc/asound.conf，维持之前的样子。

2、靠before_app.sh里，启动app之前，先mount --bind我改后的。

3、这样就amixer sget Master正常。

先这样跑起来再说。

现在mpd播报错误：

```
ERROR: Failed to open "My ALSA Device" [alsa]; Failed to open ALSA device "snapcast": Invalid argument
```

我还是把mpd的继续自己直接写入fifo，而不是写入alsa。

现在mpd可以播放。可以调节音量。

我把asound.conf里，还是改回default设备。蓝牙也使用default设备来播放。

但是这个导致了几个问题：

1、提示音播放一直失败。

2、蓝牙播放无法调节音量。



所以还是改回之前的。用snapcast这个pcm来播放，而不是default。

但是这个还是有几个问题。

1、提示音的音量特别大。这个先不管。

2、蓝牙播放有卡顿和杂音。

卡顿和杂音是怎么来的？

我直接在板端用aplay播放歌曲。

歌曲都是44100/2/16格式的。这个没有杂音。

不对，我把snapclient杀掉，用aplay播放。



当前这种修改音频配置的方式，感觉有些不清楚的地方，难以解决。

所以还是回头再看看对sbc数据进行重采样。



暂时不管44100采样率之外的情况。

先把我系统里所有的地方，都从48000调整为44100的。

这样蓝牙播放是正常的。没有杂音。







参考资料

1、

https://github.com/badaix/snapcast/issues/45

2、How to use softvol to control the master volume

https://alsa.opensrc.org/How_to_use_softvol_to_control_the_master_volume