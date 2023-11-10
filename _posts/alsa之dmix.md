---
title: alsa之dmix
date: 2020-06-10 17:15:08
tags:
	- 音频

---

--

pcm插件扩展了pcm device的功能。

让pcm device可以允许底层sample转换，通道数据的copy。

dmix插件提供了对多个stream的直接mix。

对于不支持硬件mixing的声卡，dmix默认使能了。



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
        period_time 0 us单位
        period_size 4096 字节
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

测试混音，就在命令行，有2个命令分别播放音乐，要可以听出2个音乐，而不是杂音。



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





# ipc_key_add_uid

`ipc_key_add_uid` 是 Advanced Linux Sound Architecture (ALSA) 的一个参数，通常在 `/etc/asound.conf` 或 `~/.asoundrc` 配置文件中使用，用于配置 ALSA 的 dmix 插件。这个参数的目的是为了指定一个共享 IPC (Inter-Process Communication) 键值，以便多个用户能够共享 dmix 插件。

当多个用户在同一台计算机上共享 ALSA dmix 插件时，`ipc_key_add_uid` 参数可以确保这些用户之间的音频数据分离。这对于多用户系统非常有用，以防止一个用户的音频数据被其他用户访问或混合。

通常，你可以在 ALSA 配置文件中添加如下的配置来设置 `ipc_key_add_uid`：

```shell
pcm.dmix {
    type dmix
    ipc_key_add_uid <UID>
    slave.pcm "hw:0,0"
}
```



请注意，`ipc_key_add_uid` 只在多用户共享 ALSA dmix 插件时才需要设置，==对于单用户系统通常不需要。==确保你有足够的权限来编辑 ALSA 配置文件，并小心操作，以避免破坏声音配置。



# alsa的dmix插件混音的优缺点

ALSA 的 dmix 插件是用于实现音频混音的重要组件，特别是在多个应用程序需要访问音频硬件设备的情况下。以下是 dmix 插件的一些优点和缺点：

**优点：**

1. **多应用程序支持**：dmix 插件允许多个应用程序同时访问音频硬件设备，而不需要它们争夺访问权。这使得在同一时间播放多个音频流变得容易。

2. **无需硬件混音**：dmix 插件通过在内存中混合音频数据来避免要求音频硬件支持混音。这意味着即使音频硬件不支持混音，也可以实现多应用程序音频播放。

3. **低延迟**：dmix 插件通常具有较低的音频延迟，因为音频数据可以被实时混合而不需要等待硬件。

4. **易于配置**：dmix 插件可以通过 ALSA 配置文件进行配置，使其适应不同的硬件设备和需求。

**缺点：**

1. **质量问题**：虽然 dmix 插件可以实现音频混音，但在某些情况下可能会影响音频质量。==这尤其在混合多个不同采样率或位深度的音频流时可能出现。==

2. **有限的功能**：dmix 插件主要用于基本的音频混音需求，但在某些高级音频应用中可能无法满足特定需求。==对于专业音频生产等用途，可能需要更复杂的混音解决方案。==

3. **配置复杂性**：尽管配置 dmix 插件相对容易，但仍然需要一定的了解和配置，特别是在需要处理多个音频设备或混音需求复杂的情况下。

总的来说，dmix 插件是一个非常有用的工具，可以让多个应用程序同时访问音频硬件设备，特别是在桌面和娱乐应用中。但在专业音频领域，可能需要更高级的混音解决方案，以确保音频质量和精确的控制。

# 参考资料

1、利用alsa dmix实现混音

https://blog.csdn.net/Swallow_he/article/details/80456759

2、

https://blog.csdn.net/jzjhome/article/details/73250450

3、这里有个配置值得参考

https://github.com/Arkq/bluez-alsa/issues/4

4、这里有个fifo配置。

https://github.com/voice-engine/alsa_plugin_fifo

5、这里有markdown文档，挺好的。

https://github.com/opensrc/alsa/tree/master/lib/md