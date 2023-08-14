---
title: alsa（2）
date: 2019-12-16 09:35:22
tags:
	- alsa

---

--

跟音频相关的重要目录有：

```
/dev/snd
/proc/asound/card0
/sys/kernel/debug/asoc
```



/dev/snd目录下的设备的含义：

```
controlC0 -->                 用于声卡的控制，例如通道选择，混音，麦克风的控制等
midiC0D0  -->                用于播放midi音频
pcmC0D0c --〉            用于录音的pcm设备，C0D0表示card 0的device 0，最后的c表示capture录音。
pcmC0D0p --〉               用于播放的pcm设备
seq  --〉                        音序器
timer --〉                       定时器
```

通常，我们更关心的是pcm和control这两种设备。

看一下驱动代码。



以pxa2xx_ac97.c代码为例。

在sound/arm/目录下。

我的板子上有2个card，card0是真的，card7是loopback回采的。

```
/proc/asound/card0/pcm0c/sub0 # ls -lh                             
-r--r--r--    1 root     root           0 Jan  1 08:13 hw_params    
-r--r--r--    1 root     root           0 Jan  1 08:13 info         
-rw-r--r--    1 root     root           0 Jan  1 08:13 prealloc     
-r--r--r--    1 root     root           0 Jan  1 08:13 prealloc_max 
-r--r--r--    1 root     root           0 Jan  1 08:13 status       
-r--r--r--    1 root     root           0 Jan  1 08:13 sw_params    
```

当前hw_params内容是这样：

```
/proc/asound/card0/pcm0c/sub0 # cat hw_params
access: RW_INTERLEAVED                       
format: S16_LE                               
subformat: STD                               
channels: 8                                  
rate: 16000 (16000/1)                        
period_size: 512                             
buffer_size: 32768                           
```

info的内容：

```
/proc/asound/card0/pcm0c/sub0 # cat info   
card: 0                                    
device: 0                                  
subdevice: 0                               
stream: CAPTURE                            
id: dailink-multicodecs rk3308-hifi-0      
name:                                      
subname: subdevice #0                      
class: 0                                   
subclass: 0                                
subdevices_count: 1                        
subdevices_avail: 0                        
```

status的内容：

```
/proc/asound/card0/pcm0c/sub0 # cat status  
state: RUNNING                              
owner_pid   : 405                           
trigger_time: 10.608632296                  
tstamp      : 0.000000000                   
delay       : 162                           
avail       : 162                           
avail_max   : 512                           
-----                                       
hw_ptr      : 15729840                      
appl_ptr    : 15729678                      
```

sw_params内容：

```
/proc/asound/card0/pcm0c/sub0 # cat sw_params   
tstamp_mode: NONE                               
period_step: 1                                  
avail_min: 512                                  
start_threshold: 1                              
stop_threshold: 32768                           
silence_threshold: 0                            
silence_size: 0                                 
boundary: 4611686018427387904                   
```



Control接口主要让用户空间的应用程序（alsa-lib）可以访问和控制音频codec芯片中的多路开关

对于Mixer（混音）来说，Control接口显得尤为重要，从ALSA 0.9.x版本开始，所有的mixer工作都是通过control接口的API来实现的。



ALSA已经为AC97定义了完整的控制接口模型，如果你的Codec芯片只支持AC97接口，你可以不用关心本节的内容。



```
1、在线查看/更改CODEC寄存器
mount -t debugfs none /d  //挂载debugfs文件系统
cd /d/asoc/WMT_WM8994/wm8994-codec //进入wm8994调试目录
cat codec_reg //查看wm8994寄存器
echo 6 0010 > codec_reg //写0x0010到reg[0006h]
```



在移动设备中，codec的作用可以归纳为4点：

1、对pcm等信号进行D/A转换。

2、对mic、linein或者其他输入源的模拟信号进行A/D转换。

3、对音频通路进行控制。例如播放音乐、收听FM节目、接听电话，音频信号在codec中的流通路线是不同的。

4、对音频信号做出处理，例如音量控制、功率放大、EQ控制。



alsa的逻辑，总体上可以分为两大块：

1、录音播放流控 。

​	这个相当于操作oss的/dev/dsp设备。可以设置音频三大参数。

​	aplay等工具，调用alsa lib的snd_pcm_xx函数，操作/dev/snd/pcmC0D0c等设备节点。

​	进行：设置音频三大参数、dma buffer大小设置，预缓冲阈值设置。

​	不通read/write，而是用ioctl来做。

2、mixer。

​	相当于oss驱动里的/dev/mixer设备节点。

​	在alsa里是/dev/snd/controlC0节点。

​	可以控制音量、静音、通道切换。



参考资料

1、Linux ALSA声卡驱动之一：ALSA架构简介

这个是系列文章，很好。

https://blog.csdn.net/DroidPhone/article/details/6271122

2、WM8994调试要点记录

https://www.xuebuyuan.com/597049.html

3、alsa-lib应用层接口分析

https://blog.csdn.net/yuhuqiao/article/details/82785234

4、Alsa中PCM参数设置

https://www.cnblogs.com/lifan3a/articles/4939828.html