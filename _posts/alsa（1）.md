---
title: alsa（1）
date: 2018-05-09 23:01:22
tags:
	- alsa

---

--

# 资源收集

这个alsalib的文档，比官方的可读性要好。
https://vovkos.github.io/doxyrest/samples/alsa/group_PCM_Dump.html

# 框架

![img](../images/random_name/v2-323ca01cf89d720b04b7df3d1f3026e3_720w.jpg)



ALSA分为两部分：

一部分是在Linux Kernel的声卡驱动，

主要是对声卡硬件（支持的采样率、声道、格式等）的描述和抽象；

另一部分是在User Space的alsa-lib，

有一套插件机制，包括resampling、mixing、channel mapping等功能都可以通过插件实现。



有ALSA还不够，

比如说，对多个应用同时播放的支持，

虽然可以通过ALSA的dmix插件实现，但不够好。

所以PulseAudio作为一个Sound Server登场了，

PulseAudio来接管各种音频的输入输出，

包括ALSA音频、蓝牙音频、网络音频等；

**会自动切换声卡，比如有USB声卡接入，播放自动切到USB声卡；**

还有控制每个应用独立的音量，等等。

**现在Linux桌面发行版大多都默认安装了PulseAudio。**



另一个类似PulseAudio的Sound Server是JACK Audio Connection Kit，

JACK针对的是实时性高、低延时的**专业音频应用**。

还有一个正在火热开发的新项目叫PipeWire，

其设计目标是集合PulseAudio + Jack两者的优点，

加入权限管理的安全机制，另外添加了对视频（摄像头设备）分发和管理的支持。

PipeWire看起来很有前景，值得关注一下。



有了PulseAudio、JACK和PipeWire，

他们都有提供各自的API，那么我们先要录音和播放，到底选择用哪种API呢？



**对于大部分应用，最佳的选择依然是用ALSA的API。**



PCM设备与声卡设备有所不同，PCM设备可以由ALSA的插件产生。

系统安装PulseAudio之后，

ALSA pulse插件会生成名为`pulse`的PCM设备，且这pulse会被设为默认设备。

 如果不用PulseAudio，想实现同时多个应用播放和录音可以使用`dmix`和`dsnoop`插件，

这两个插件支持采样频率、通道和格式有限，

通常会在这俩之上加上`plug`插件，多个插件可以（有限的）级联在一起使用的 。



个人来说，最推荐前面直接用`aplay`和`arecord`重定向的方式，

没什么依赖， 稳定可靠，重定向的pipe提供缓冲功能，而且是多进程跑。





在alsa驱动这一层，目前为止，抽象出了4层设备：

一是hw:0,0；

二是plughw:0,0；

三是default:0；

四是default。

至于一是清楚了，

二和二以上可以做数据转换，以支持一个动态的范围，

比如你要播放7000hz的东西，那么就可以用二和二以上的。

而你用7000hz作为参数，去设置一，就会报错。

三和四，支持软件混音。

我觉得default:0表示对第一个声卡软件混音，default表示对整个系统软件混音。



这里提出两点：

1.1.1 一般为了让所有的程序都可以发音，为使用更多的默认策略，我们选用三和四，这样少一些控制权，多一些方便。

1.1.2 对不同的层次的设备，相同的函数，结果可能是不一样的。

比如，设置Hardware Parameters里的period和buffer size，这个是对硬件的设置，

所以，default和default:0这两种设备是不能设置的。

如果直接操作hw:0,0，那么snd_pcm_writei只能写如8的倍数的frame，比如16、24等，

否则就会剩下一点不写入而退回，而 default，就可以想写多少就写多少，我们也不必要关心里面具体的策略。



交叉模式，interleaved。就是左右声道数据交叉存储，而不是先全部放左声道，然后全部放右声道的方式。

snd_pcm_readi，这个i就是表示interleaved模式。



xrun包括两种情况：

overrun，就是录音的时候可能会出现。应用层取数据太慢了。

underrun：就是播放的时候出现。应用层写得快，硬件层来不及处理。



EPIPE错误表示overrun错误。



# plugin

alsa的plugin是个什么概念？

https://alsa.opensrc.org/ALSA_plugins

这里有说明。

什么是plugin？

是用来创建虚拟设备，这些虚拟设备可以当成硬件设备来用。



在/etc/asound.conf和~/.asoundrc这2个配置文件里进行配置。

一个基本的插件配置样式是：

```
pcm.SOMENAME {
    type PLUGINTYPE
    slave {
        pcm SLAVENAME
    }
}
```

上面的语句，创建了一个名字叫SOMENAME的插件。类型是PLUGINTYPE。**一个插件相当于一个pipe，它的后端就是slave里的东西。**

插件的名字，有些是已经被预定义了的，例如default，dmix 。

**slave，可以是另一个插件，也可以是硬件设备。例如可以是hw:0,0**

（我是否可以这么理解：插件就是在硬件前面的预处理？）

```
插件1 -> 插件2 -> ... -> 插件N -> 硬件
```

一个.asoundrc的写法：

```
pcm.myplugdev {
	type plug
	slave {
		pcm default
		rate 44100
	}
}
```

然后我们播放命令这样写：

```
aplay -D myplugdev 1.wav
```



hw也是一种插件。它表示直接跟Linux驱动通信的插件。

```
pcm.myplugdev {
	type hw
	card 0
	subdevice 0
}
```

有一个特别的插件，类型是plug。

经常用到，它的作用是进行通道、采用率、格式的转化。



## hw

这个类型主要是给声卡设备起别名用的。

With the 'PCM hw type' you are able to define aliases for your devices.

```
pcm.primary {
        type hw
        card 0
        device 0
}
```

## plug

type plug的对type rate等几种类型的综合。

## dmix

在没有dmix之前，Linux上软件混音，只能靠artsd、esd、jack这些应用来完成。

dmix就是提供一个底层的混音方案。

实际上，还没有多少应用使用了这个特性。

dmix插件不是基于client/server架构。

它直接写入到声卡的DMA缓冲区。



插件类型在alsalib代码里的体现：

在alsalib/include/pcm.h里。

```
/** PCM type */
enum _snd_pcm_type {
	/** Kernel level PCM */
	SND_PCM_TYPE_HW = 0,
	/** Hooked PCM */
	SND_PCM_TYPE_HOOKS,
	/** One or more linked PCM with exclusive access to selected
	    channels */
	SND_PCM_TYPE_MULTI,
	/** File writing plugin */
	SND_PCM_TYPE_FILE,
	/** Null endpoint PCM */
	SND_PCM_TYPE_NULL,
	/** Shared memory client PCM */
	SND_PCM_TYPE_SHM,
	/** INET client PCM (not yet implemented) */
	SND_PCM_TYPE_INET,
	/** Copying plugin */
	SND_PCM_TYPE_COPY,
	/** Linear format conversion PCM */
	SND_PCM_TYPE_LINEAR,
	/** A-Law format conversion PCM */
	SND_PCM_TYPE_ALAW,
	/** Mu-Law format conversion PCM */
	SND_PCM_TYPE_MULAW,
	/** IMA-ADPCM format conversion PCM */
	SND_PCM_TYPE_ADPCM,
	/** Rate conversion PCM */
	SND_PCM_TYPE_RATE,
	/** Attenuated static route PCM */
	SND_PCM_TYPE_ROUTE,
	/** Format adjusted PCM */
	SND_PCM_TYPE_PLUG,
	/** Sharing PCM */
	SND_PCM_TYPE_SHARE,
	/** Meter plugin */
	SND_PCM_TYPE_METER,
	/** Mixing PCM */
	SND_PCM_TYPE_MIX,
	/** Attenuated dynamic route PCM (not yet implemented) */
	SND_PCM_TYPE_DROUTE,
	/** Loopback server plugin (not yet implemented) */
	SND_PCM_TYPE_LBSERVER,
	/** Linear Integer <-> Linear Float format conversion PCM */
	SND_PCM_TYPE_LINEAR_FLOAT,
	/** LADSPA integration plugin */
	SND_PCM_TYPE_LADSPA,
	/** Direct Mixing plugin */
	SND_PCM_TYPE_DMIX,
	/** Jack Audio Connection Kit plugin */
	SND_PCM_TYPE_JACK,
	/** Direct Snooping plugin */
	SND_PCM_TYPE_DSNOOP,
	/** Direct Sharing plugin */
	SND_PCM_TYPE_DSHARE,
	/** IEC958 subframe plugin */
	SND_PCM_TYPE_IEC958,
	/** Soft volume plugin */
	SND_PCM_TYPE_SOFTVOL,
	/** External I/O plugin */
	SND_PCM_TYPE_IOPLUG,
	/** External filter plugin */
	SND_PCM_TYPE_EXTPLUG,
	/** Mmap-emulation plugin */
	SND_PCM_TYPE_MMAP_EMUL,
	SND_PCM_TYPE_LAST = SND_PCM_TYPE_MMAP_EMUL
};
```







**alsa采用环形队列来存放输出和输入的数据。**



如果要支持多个应用同时打开声卡，需要支持混音功能。

**大多数的声卡不支持硬件混音。只有专业的声卡才支持。**

**所以需要软件混音。**

alsa自带了一个很简单的混音器dmix。

dmix的字母d，是Direct的意思。

使用dmix的方法，是把dmix作为默认设备。

我们先输出给dmix，让dmix去处理各个不同声音的混音。



alsa的接口分为：

```
control interface
	对应设备节点：/dev/snd/controlCX
	在我的笔记本上，有controlC0、controlC1、controlC7 这3个节点。
	功能：
		注册声卡。
		请求可用设备。
pcm interface
	对应节点：/dev/snd/pcmCXDX
	我的笔记本上有：pcmC0D0c  pcmC0D0p  pcmC1D3p 这3个节点。
	这个是最常用的接口。管理录音和播放。
	C代表Card。D代表Device。
raw midi interface
	设备节点：midiCXDX
	提供对声卡上midi总线的访问。
	我的笔记本没有对应的节点。
	
timer interface
	对应设备节点：/dev/snd/timer
	这个名字是固定的。
	
seq interface
	设备节点：/dev/snd/seq
	时序器接口。
mixer interface
	设备节点：/dev/snd/mixerCXDX
	笔记本没有。
	一般都没有这个节点，是硬件混音？
	
```



看alsa的应用层的缓冲区。
buffer是以时间为衡量单位的，例如500ms。
这个buffer相对来说有大，会有用户可以感知的延迟，所以在这个基础，再分出一个period的概念。
例如，我们可以简单的把buffer时间除以4 。
period_time = buffer_time / 4;
一个period的数据就是alsa应用往驱动传递的基本单元。



# 接口列表

```
/proc/asound
	信息接口。
/dev/snd/controlC0
	控制接口。
/dev/snd/mixerC0D0
	mixer接口。
/dev/snd/pcmC0D0
	pcm接口。
/dev/snd/midiC0D0
	rawmidi接口。
/dev/snd/seq
	时序器接口。
/dev/snd/timer
	时钟接口。
	
不一定要所有接口都有。seq、mixer很多时候可以没有。
```



https://www.alsa-project.org/wiki/ALSA_Library_API





对于上面的架构，在某一时刻只能有一个程序打开声卡并占有它，此时其它程序打开的话，会返回busy.如要支持同时可 以多个应用程序打开声卡，需要支持混音功能，有些声卡支持硬件混音，但大部分声卡不支持硬件混音，需要软件混音。

alsa自带了一个很简单的混音器dmix



# snd_interval理解

```
// openmin和openmax表示开集,如果2个全为1,那么就表示,range范围为(min,max)即2个开区间
// openmin为1,openmax为0,range范围为(min,max] 即开区间和闭区间
// integer等于1,表示it不是一个范围区间,而是一个固定的interger整型值
// dir等于0,表示为interger设置,dir < 0表示(min-1,max),dir > 0表示(min, max-1)
struct snd_interval {
    unsigned int min, max;
    unsigned int openmin:1,
             openmax:1,
             integer:1,
             empty:1;
};
```



```
struct snd_interval {
		unsigned int min, max;
		//openmin和openmax代表开集：
		//openmin和openmax都为1时，代表开区间，range范围为(min,max)
		//openmin=1,openmax=0时，range范围为(min,max] 即开区间和闭区间
		unsigned int openmin:1,
					 openmax:1,
					 //integer等于1,表示it不是一个范围区间,而是一个固定的interger整型值
					 integer:1,
					 empty:1;
}
```



https://blog.csdn.net/dengdun6257/article/details/102283475

# near接口问题



`__old_snd_pcm_hw_params_get_rate` 只能接收2个参数，val是一个内部变量，从而导致返回值错误，但是为什么动态链接和静态链接调用堆栈不同还不清楚

解决办法
目前想到的就是不用这些接口，即`__OLD_GET，__OLD_GET1，__OLD_NEAR，__OLD_NEAR1`修饰的接口都不用，包括官网的例子也没用这样的接口，如下：



https://blog.csdn.net/u010687717/article/details/103704419



# snd_pcm_hw_refine

```
changed = snd_mask_refine(m, constrs_mask(constrs, k));
                //changed masks，如果成功重定义了参数，cmask记录下是哪个参数被改变
                if (changed)
                        params->cmask |= 1 << k;
                if (changed < 0)
                        return changed;
```



```
snd_pcm_hw_refine函数里面有个很重要的参数：constrs = &substream->runtime->hw_constraints
hw_constraints即硬件约束条件，这里是在哪里赋值的呢？
其实是在snd_pcm_hw_constraints_complete函数里面：
```



https://blog.csdn.net/Guet_Kite/article/details/114314003



# 调试方法

```
export LIBASOUND_DEBUG=1
	这个环境变量控制了这些打印：
	hw_params配置有问题时的打印，靠这个来控制。
	--with-debug=no 会关闭这个特性。
	只在dump_hw_params函数里使用了这个环境变量。
	
REFINE_DEBUG
	这个是在refine函数调整参数把调整的细节打印出来。
	
```



```
#define ALSA_PCM_OLD_HW_PARAMS_API
#define ALSA_PCM_OLD_SW_PARAMS_API
#include <alsa/asoundlib.h>
```

# --with-versioned   

```
--with-versioned        shared library will be compiled with versioned
                          symbols (default = yes)
```

我在yocto下编译得到的alsa-lib总是有问题。

而buildroot的没有问题。

经过对比发现是这个选项不一样。

buildroot默认带上了这个选项：

```
--without-versioned
```

这个选项对代码的实际影响是什么？

```
VERSIONED_SYMBOLS 
```



```
#if defined(PIC) && defined(VERSIONED_SYMBOLS) /* might be also configurable */
#define USE_VERSIONED_SYMBOLS
#endif
```



```
#ifdef USE_VERSIONED_SYMBOLS
#define use_symbol_version(real, name, version) \
		symbol_version(real, name, version)
#define use_default_symbol_version(real, name, version) \
		default_symbol_version(real, name, version)
#else
#define use_symbol_version(real, name, version) /* nothing */
```



参考资料

https://blog.csdn.net/njuitjf/article/details/40544659



https://www.cnblogs.com/arnoldlu/p/13552504.html



# 参考资料

1、深入了解ALSA

https://www.cnblogs.com/lifan3a/articles/5553664.html

2、alsa-lib, alsa-utils交叉编译及在嵌入式上使用

https://blog.csdn.net/luckywang1103/article/details/45626201

3、ALSA编程细节分析

https://blog.csdn.net/azloong/article/details/6277457

4、怎样使用alsa API

https://blog.csdn.net/weixin_34123613/article/details/86122554

5、

https://blog.csdn.net/reille/article/details/5855859

6、Linux音频编程

https://www.cnblogs.com/hzl6255/p/8245578.html

7、

这篇文章特别好。

https://www.cnblogs.com/cslunatic/p/3677729.html

8、

https://blog.csdn.net/isunbin/article/details/81503152

9、alsa的 snd_pcm_readi 和 snd_pcm_writei

https://blog.csdn.net/junjun5156/article/details/70169912

10、alsa声卡驱动原理分析

https://wenku.baidu.com/view/29edc08a680203d8ce2f2408.html

11、ALSA声音编程介绍+underrun

https://blog.csdn.net/zhang_danf/article/details/39005767

12、音频出现Xrun（underrun或overrun）的原因与解决办法

https://blog.csdn.net/Qidi_Huang/article/details/53100493

13、

https://stackoverflow.com/questions/26545139/alsa-cannot-recovery-from-underrun-prepare-failed-broken-pipe

14、Softvol

https://alsa.opensrc.org/Softvol

15、利用alsa dmix实现混音

https://blog.csdn.net/Swallow_he/article/details/80456759

16、

https://blog.csdn.net/cnclenovo/article/details/47106743

17、这个系列文章可以。

https://www.cnblogs.com/jason-lu/tag/ALSA/

18、Linux音频编程

https://www.cnblogs.com/hzl6255/p/8245578.html

19、ALSA中PCM的使用

https://blog.csdn.net/explore_world/article/details/51013942

20、

https://blog.csdn.net/sssuperqiqi/article/details/97033472

21、Linux下录音和播放

这篇文章非常好。

https://zhuanlan.zhihu.com/p/58834651

22、A Guide Through The Linux Sound API Jungle

http://0pointer.de/blog/projects/guide-to-sound-apis.html