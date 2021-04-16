---
title: alsa之插件C代码写法
date: 2020-06-10 17:52:08
tags:
	- 音频

---

1

https://github.com/voice-engine/alsa_plugin_fifo

这里是一个fifo插件。

是一个语音项目。

https://wiki.voicen.io/voicen_os/



asound.conf配置文件，是alsa-lib的默认配置文件，

路径在 /etc/，可以用来配置alsa库的一些附加功能。

这个文件不是alsa库运行时所必须的，

没有它alsa库也可以正常运行。

asound.conf允许对声卡或者设备进行更高级的控制，

提供访问alsa-lib中的pcm插件方法，

允许你做更多的复杂的控制，

比如可以把声卡组合成一个或者多声卡访问多个I/O。



在ALSA中，PCM插件扩展了PCM设备的功能和特性。

插件可以自动处理诸如：

命名设备、采样率转换、通道间的采样复制、写入文件、为多个输入/输出连接声卡/设备（不同步采样）、使用多通道声卡/设备等工作。



hw插件

```
pcm.!default {
        type hw
        card 0
}
 
ctl.!default {
        type hw           
        card 0
}
```

名字为default的声卡，指向card0，也就是hw：0，0，测试命令：aplay -D default test.wav



在ALSA中，PCM插件扩展了PCM设备的功能和特性。

插件可以自动处理诸如：

命名设备、采样率转换、通道间的采样复制、写入文件、为多个输入/输出连接声卡/设备（不同步采样）、使用多通道声卡/设备等工作。

要使用它们，开发者需要创建一个虚拟从属设备（slave device）。



```
pcm_slave.sl2 {
    pcm "hw:0,0"
    rate 48000
}
pcm.rate_convert {
    type rate
    slave sl2
}
```

这个可以把其他的rate的音频，统一转成48K的来播放。

aplay -D rate_convert test.wav

也可以这样写：

```
pcm.rate_convert {
	type rate
	slave {
		pcm "hw:0,0"
		rate 48000
	}
}
```



在~/.asoundrc或者/etc/asound.conf文件

加入default.pcm.rate_convert "samplerate"

 或者default.pcm.rate_convert "speexrate" ，

是两种不同的rate转换的plugin

然后在播放的时候使用命令行

aplay -v -D "plug:SLAVE='hw:0,0'" 1.wav 

进行播放

或者

```
pcm.my_rate {
    type rate
    slave {
        pcm "hw"
        rate 48000
    }
    converter "samplerate" # or converter "speexrate"
}
```

aplay -D my_rate 1.wav

查看硬件实际播放的sample rate

可以通过`cat /proc/asound/card0/pcm0p/sub0/hw_params`查看实际硬件播放时候的sample rate





参考资料

1、ALSA resample插件－SRC

https://blog.csdn.net/weixin_41965270/article/details/81272732

2、【ALSA】 asound.conf 插件讲解

https://blog.csdn.net/sssuperqiqi/article/details/97033472

3、

https://blog.csdn.net/luckywang1103/article/details/79271238