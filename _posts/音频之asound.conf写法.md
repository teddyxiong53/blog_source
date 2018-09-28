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



参考资料

asound.conf配置

https://blog.csdn.net/zhangxu365/article/details/8449118

官方配置文件说明

http://www.alsa-project.org/main/index.php/Asoundrc