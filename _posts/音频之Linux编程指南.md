---
title: 音频之Linux编程指南
date: 2019-05-16 14:45:11
tags:
	- 音频

---

1

音频信号是连续的模拟信号。

计算不能处理模拟信号。

所以需要把模拟信号经过AD转化，计算机才能处理。

音频数字化，经过2个大的步骤：

1、采样。就是每隔一段时间，就读取一次声音信号的幅值。是时间上的数字化。指标是采样频率。频率越高，就越接近原始效果。

2、量化。把采集到的幅值转化为数字值。幅度上的数字化。指标是量化位数。有8位、16位，32位。位数越多，可表示的就越精细，就越接近原始效果。



三个指标：

1、采样频率。

2、量化位数。

3、声道数。



syscall接口：

```
open
close
read
write 
ioctl
```



音频设备文件：

```
/dev/sndstat
	驱动提供的最简单的一个文件。只读的。
	表示声卡当前的状态。
	一般是用来检测声卡的。
	可以cat。
	不一定有这个文件。
/dev/dsp
	用于数字采样和录音的设备文件。
	这个文件非常重要，对它进行写操作，表示进行播放。
	而从它读，表示进行录音。
	一般有多个，用dps1、dsp2这样来编号。
/dev/audio
	类似与/dev/dsp。
	主要是兼容老的。不用这个 。
/dev/mixer
	mixer是硬件上的混音器。
	把多个信号叠加在一起。
	
/dev/sequencer
	很少用。
```



alsa可以截获oss调用，然后转化成alsa调用。

/dev/dsp。这个是oss里的标准。

如果没有安装alsa对oss的模仿层，就会缺少这个文件。



alsa在安装后，各个声道默认都是静音的。



参考资料

1、Linux音频编程指南

https://www.ibm.com/developerworks/cn/linux/l-audio/index.html

2、Advanced Linux Sound Architecture (简体中文)

https://wiki.archlinux.org/index.php/Advanced_Linux_Sound_Architecture_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)