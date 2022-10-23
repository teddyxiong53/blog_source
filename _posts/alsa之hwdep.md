---
title: alsa之hwdep
date: 2022-10-17 19:50:33
tags:
	- alsa

---

--

可以看出hwdep的本意主要是用于download dsp image，

但通过它也可实现类似于其他字符设备的ioctl。

我说过音频大多控制是通过snd_kcontrol，但有些功能如果使用这种方式会比较繁琐且模块太过耦合。



举个例子：

电话语音通路，它不同于音乐回放通路，通话时才需要打开。

如果用snd_kcontrol，则上层需要调用多个control.set，并且更换CODEC芯片的话，上层也要跟着修改control name；

如果使用hwdep ioctl的话，就没有这个问题，

只需要保证命令字cmd一致，底层如何管理通话通路的一系列部件开关，上层都不需要关心。





参考资料

1、

https://blog.csdn.net/gjy938815/article/details/9175711