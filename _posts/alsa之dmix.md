---
title: alsa之dmix
date: 2020-06-10 17:15:08
tags:
	- 音频

---

1

alsa自带了一个很简单的混音器dmix

应用程序不需要做任何修改，只需要修改asound.conf

dmix的字母d，是Direct 的意思。

一个典型的dmix配置：

```
pcm.myplugdev {
	type dmix
	ipc_key 112233
	ipc_key_add_uid yes
	ipc_perm 0660
	slave {
		pcm "hw:0,0"
		channels 2
		format S16_LE
		rate 48000
		period_size 1024
		buffer_size 4096
	}
}
```



一个例子。

```
pcm.!default {
    type plug
    slave.pcm "dmixer"
}
pcm.dmixer  {
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



```
# Adapted via http://stackoverflow.com/a/14398926/6268583
#
# Enceinte
pcm.dmixed {
    type dmix
    ipc_key 1024
    ipc_key_add_uid 0
    ipc_perm 0666     # mixing for all users
    slave.pcm "hw:1,0"
}
# Micro
pcm.dsnooped {
    type dsnoop
    ipc_key 1025
    slave.pcm "hw:1,0"
}

pcm.duplex {
    type asym
    playback.pcm "dmixed"
    capture.pcm "dsnooped"
}

# Instruct ALSA to use pcm.duplex as the default device
pcm.!default {
    type plug
    slave.pcm "duplex"
}

# tell ALSA to use hw:0 to control the default device (alsamixer and so on)
ctl.!default {
    type hw
    card 0
}
```







参考资料

1、利用alsa dmix实现混音

https://blog.csdn.net/Swallow_he/article/details/80456759

2、

https://blog.csdn.net/jzjhome/article/details/73250450

3、这里有个配置值得参考

https://github.com/Arkq/bluez-alsa/issues/4

4、这里有个fifo配置。

https://github.com/voice-engine/alsa_plugin_fifo