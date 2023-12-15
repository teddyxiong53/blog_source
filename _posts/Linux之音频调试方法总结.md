---
title: Linux之音频调试方法总结
date: 2023-12-07 10:38:51
tags:
	- 音频

---

--

# 查看设备是否打开

## aplay -l

```
 # aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: AMLAUGESOUND [AML-AUGESOUND], device 0: TDM-A-dummy-alsaPORT-i2sCapture soc:dummy-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 1: TDM-B-tas5707-alsaPORT-i2s multicodec-1 []
  Subdevices: 0/1
  Subdevice #0: subdevice #0
```

看Subdevices：0/1 

这个就是已经打开的状态的。

Subdevices: 1/1 这个是没有打开的状态的。

## 看proc下面的status

```
cat /proc/asound/card0/pcm0p/sub0/status
```

还可以这样看所有的：

```
cat /proc/asound/card0/pcm*p/sub0/status
```

显示是这样：

```
 # cat /proc/asound/card0/pcm*p/sub0/status
closed
closed
closed
closed
```

