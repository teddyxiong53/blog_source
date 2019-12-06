---
title: Linux驱动之音频
date: 2018-02-27 22:24:22
tags:
	- Linux驱动

---



在linux系统中，先后出现了音频设备的3种框架：oss、alsa、asoc。



# 音频设备的硬件接口

出现了3种主要的接口，就是cpu跟音频编解码芯片之间的接口。

1、pcm。脉冲编码调制。

```
1、是最简单的一种接口。
2、由4根线组成：时钟脉冲bclk，帧同步信号fs，数据发送dx，数据接收dr。
3、帧同步信号频率跟采样率一样。
4、pcm接口很容易实现，理论上可以支持任何的数据方案和采样率。
```

2、I2S接口。

```
1、Philips在1980年代发明。
2、由3根线组成，lrclk、bclk、sd。sd是数据收发，半双工的。lrclk为高，左声道，lrclk为低，右声道。
3、I2S更加适合立体声系统。
```

3、ac97接口。

```
1、是1997年，由Intel主导提出的一个方案。
2、比较复杂，但是功能强大。
3、用4根线就可以实现9个音频通道。
```

接口的适用场景：

1、mp3播放器用I2S。

2、移动电话用PCM接口。

3、智能手机、电脑用ac97接口。



# oss音频设备驱动

oss标准中有2个最基本的音频设备：

1、mixer。对应/dev/mixer

驱动重点是ioctl的实现。

2、dsp。对应/dev/dsp

驱动重点是read、write、ioctl、poll的实现。

## oss用户空间编程的例子

实现了录音3秒然后再播放的功能。

```
#define LENGTH 3 //录音的秒数
#define RATE 8000 //采样频率
#define SIZE 8 //量化位数
#define CHANNELS 1 //单声道

unsigned char buf[LENGTH * RATE * SIZE *CHANNELS /8];

int main()
{
    int fd;
    int arg;
    int status;
    fd = open("/dev/dsp", O_RDWR);
    arg = SIZE ;
    ioctl(fd, SOUND_PCM_WRITE_BITS, &arg);
    
    arg = CHANNELS;
    ioctl(fd, SOUND_PCM_WRITE_CHANNELS, &arg);
    
    arg = RATE;
    ioctl(fd, SOUND_PCM_WRITE_RATE, &arg);
    
    while(1) {
        printf("say something...\n");
        read(fd, buf, sizeof(buf));
        printf("what you said: \n");
        write(fd, buf, sizeof(buf));
        
        //等待播放录音完毕、
        ioctl(fd, SOUND_PCM_SYNC, 0);
    }
    return 0;
}
```



# alsa音频设备驱动

##为什么需要alsa？

因为oss虽然成熟，但是是商业软件，没有开源的。所以linux不再包含它的更新了。

alsa是Advanced Linux Sound Architecture就用来替代oss的。而且比oss更加好用，为用户态编程提供了库文件alsa-lib，不再需要直接进行ioctl这种原始接口相关操作了。但是可以兼容oss。



##alsa组件

1、alsa-driver。非常庞大，代码量达到几十万行以上。

2、alsa-libs。开发包。用户include asoundlib.h，链接libasound.so。

3、alsa-libplugins。插件。

4、alsa-utils。管理工具包。aplay、arecord这些工具。

5、alsa-tools。小程序包。

6、alsa-firmware。特殊音频固件支持包。

7、alsa-oss。兼容oss的模拟层。

上面这些组件只有alsa-driver是必须的。其余都是可选的。



## alsa的用户接口

1、信息接口。/proc/asound。这个是个目录，下面有大概80个文件。

2、控制接口。/dev/snd/controlCX，X取值是0,1等值。

```
树莓派上的情况是这样的。
pi@raspberrypi:/dev/snd$ ls
by-id  by-path  controlC0  controlC1  pcmC0D0p  pcmC0D1p  pcmC1D0c  seq  timer
```

3、音序器接口。seq。

4、定时器接口。timer。

5、pcm接口。

用户程序不要直接使用这些设备，这些是给alsa-lib用的，用户用alsa-lib就好了。



# asoc音频设备驱动

asoc是alsa在soc上的发展和演变。

本质上仍然是alsa，但是进行了这些改动：

1、传统的alsa架构下，同一个音频芯片在不同的CPU下，驱动不同。这个是不符合代码重用的。

2、所以对cpu相关代码和codec相关代码进行了分离。

在嵌入式设备上，推荐用asoc架构的。



## asoc组成

由3个部分组成：

1、codec部分。

2、平台驱动。只关心CPU。

3、板级驱动。

1和2都是可以通用的。



看Linux源代码，可以看到音频相关的驱动，没有像所有其他的驱动那样，放在drivers目录下。

而是在单独的一个sound底层子目录下。

为什么音频驱动这么特立独行呢？

看Linux的历史提交情况看，这个变化是在内核2.5版本开始变化的。

这个时候，开始引入alsa框架，负责人也发生了变化。





参考资料

1、为什么Linux的音频驱动位于sound目录下而不是driver/sound？

http://blog.chinaunix.net/uid-30374564-id-5571674.html