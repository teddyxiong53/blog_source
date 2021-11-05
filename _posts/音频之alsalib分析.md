---
title: 音频之alsalib分析
date: 2021-04-02 15:58:41 
tags:
	- 音频

---

--

test目录怎么编译？

直接进入到test目录下，你要编译xx.c，则执行：

```
make xx
```



运行出现这个错误

```
cannot access '/usr/lib/alsa-lib/libasound_module_conf_pulse.so': No such file or directory
```

这个很容易，就是ln -s 把对于的目录软链接到/usr/lib/alsa-lib/目录就好了。



我现在需要深入阅读和调试alsalib的代码。

怎么搭建环境呢？

我的电脑上，实际上在这个位置。

/usr/lib/x86_64-linux-gnu/alsa-lib/libasound_module_conf_pulse.so

所以需要configure的时候，配置一下。

最好是纯静态的方式来编译。

所有代码都在本地。

我重新这样configure一下看看。

```
./configure \
--enable-static \
--enable-debug \
--with-pic \
--with-debug   
```

这样编译得到的还是要到/usr/lib/alsa-lib/目录下去找库。

我这样来运行吧。至少先跑起来。

```
LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/alsa-lib ./timer 
```

看test/lsb/config.c这个测试程序。

alsalib的config做得很强大。

值得学习一下。

```
snd_config_top
	创建一个配置根节点。
```



"@hook"关键字可以由第三方编写共享库来扩充功能。

而在alsa.conf中开头的部分，则是用于load其他配置文件：

```
@hooks [  
    {  
        func load  
        files [  
            "/etc/asound.conf"  
            "~/.asoundrc"  
        ]  
        errors false  
    }  
]  
```

这里没有指定第三方共享库，则会调用snd_config_hook_load这个函数，

其中调用snd_config_load装载/etc/asound.conf和~/.asoundrc这2个特定的配置文件。

另外一点，可以用“<>”, 包含其他配置文件。

如：

`<confdir:pcm/surround.conf>`



当在web上搜索关于ALSA的答案时，我发现都是提问和自相矛盾的声明，鲜有确切的答案。

我想有两个原因：

首先，有些声音问题不像看起来那么简单，

此外ALSA文档简直是一团糟。

本文会尝试解决这些声音问题，并矫正一团糟的ALSA文档。



ALSA用cards，device和subdevices的分层结构

表示audio硬件设备和他们的组件。

这个分层结构是ALSA看待硬件设备结构和能力的视角。

如果声卡这个分层结构和声卡的文档有差别，那么可能是由于驱动没有支持所有的功能。

ALSA cards和声卡硬件是一一对应的。

ALSA cards的主要保存每块卡上的设备列表。

一个card可以通过一个ID（字符串）或者从0开始的数字表示。



大部分ALSA硬件访问发生在device级别。

可以从0开始枚举每个卡的devices，

不同的devices可以独立的打开和使用。

典型的，**声卡和设备这两个标识足以决定声音信号从哪里读取，送到哪里**。



Subdevices是ALSA能够区分的更细粒度的对象。

最常见的场景是一个device的每个channel都对应一个subdevice

或者总共只有一个subdevice。



一个device的subdevice理论上可以单独使用，

但是在一个subdevice上播放multi-channel信号时，也会使用其余的subdevices。

和device一样，subdevices索引标识从0开始。



**PCM参数和配置空间**

数字化声音有一定数目的参数：

采样率，通道数和采样值存储格式。

如果你已经使用OSS编程，那么你可能习惯于在播放音乐文件之前设置这些参数。类似于ALSA文档中所提到的配置空间。

现实的答案没有那么简单：

比如一些声卡无法结合所有支持的采样格式，采样率和通道数。

所以这些参数不是独立的。

ALSA考虑到了这种情况，使用一个n维空间的参数集，

每一维对应着采样率，采样格式，通道数等等。

如果一个给定声卡的参数是独立的，那么所有合法配置就在一个n维盒子中，在这种情况下，我们需要做的就是描述每一维的取值范围。

如果参数之间不是独立的，那么允许的配置集比较复杂了。



当一个硬件设备通过ALSA访问，参数并不总是独立的。

进一步说，一个设备由于某些特定参数的限制，它的合法配置空间被相应的压缩小了。

这就使得我们可以使用一个较小空间而不是确定的数值。

此外，还导致依赖于参数设置顺序的问题。

也就是说ALSA plugin能够自动选择最合适的硬件参数并执行格式转换。

我们在接下来的小节中会讨论这个plugin和其他的plugin



**ALSA devices and plugins**

为了避免混淆，我们先简单介绍一下ALSA device。

这里说的ALSA device和上面提到的hardware devices完全不同。

ALSA device用字符串表示。

他们定义在ALSA的一个配置文件中。

更复杂的是，一些标准的ALSA devices是：属类:card,devicce,subdevice。

但是硬件card和device的规范不能做为ALSA设备，

事实上有些ALSA devices的参数不是硬件相关的。



不夸张的说ALSA几乎都是由plugins组成的。

不论什么时候一个player或者程序使用ALSA设备时，plugins做脏活累活。

plugins的完整列表在ALSA library doxygen 文档的pcm_plugins.html中。

**注意plugins列表并不等同于ALSA devices列表。**

一些标准devices的名字和他们使用的plugins同名，

但是有些devices并不是这样，

有时不同的ALSA devices使用相同的plugin。

因此本节我们会给出每一个plugin的名字，如果可能，还会给出特定硬件设备使用这个plugin允许的名字。



最重要的plugin无疑是hw plugin。

它本身不做任何处理，仅仅访问硬件驱动。

如果应用选择硬件不支持的PCM参数(sampling rate, channel count或者sample format)，

hw plugin返回出错信息。

因此下一个重要的plugin是'plug' plugin，

plug plugin执行channel复制，采样率转换以及必要的重采样。

不像hw plugin被device hw:0,0使用，

plug plugin对应的device命名是不同的：plughw:0,0。

但二者的设备名都包含要访问的硬件cards，device以及subdevice。

（事实上，plug device也存在，也使用plug plugin，并且它的参数SLAVE指明数据要发送到哪里，因此这个plugin一定和其他的plugins链接到一起）



此外一个很有用的plugin是file plugin，它会把采样数据写到一个文件中。

它有两个ALSA devices：file 和 tee。

前者有两个参数，文件名和格式。

后者传送数据到另外一个device以便写到一个文件中，第一个参数就是那个device。如果第二个设备有任何参数（比如 "plughw:0,0"），那么你要把他的名字用引号括起来，以防止被命令行解释。假定你想使用第一个声卡上的第一个设备播放声音，你可以用如下方式获取输出声音的copy。

```
aplay -Dtee:\'plughw:0,0\', /tmp/alsatee.out, rawxy.wav
```

得承认这看起来没什么意义（因为你可以简单的copy xy.wav或者转换为sox），

然而使用这个方法，基于ALSA的movie player可以抽取声音内容。

tee's 输出是raw 采样数据没有任何文件头。

file plugin也可以用来从文件中读取数据，但是没有预定义的设备使用这种方式。



现存的许多plugins用来mixer和rerouting channels。

由于这些plugins需要大量的参数，

没有预定以的ALSA devices使用他们。

route plugin是一个mixing矩阵。

channels不仅仅可以被交换或者任意赋值，而且可以被混音。

多个plugin仅仅允许reroute channels，

但是可以有几个slave devices，因此可以在不同声卡的channels上播放。

dmix和dshare plugins允许一个device被多个clients(player application)使用。

dshare plugin把可用channels分配给需要的clients，

而dmix则是把多个clients播放的内容混音到一个channels。



# test代码分析

## audio_time

没看懂这个有什么用。统计时间的？

## chmap

这个的意义又是什么？

是指声道布局。

就是这些东西

```
enum {
	SNDRV_CHMAP_UNKNOWN = 0,
	SNDRV_CHMAP_NA,		/* N/A, silent */
	SNDRV_CHMAP_MONO,	/* mono stream */
	/* this follows the alsa-lib mixer channel value + 3 */
	SNDRV_CHMAP_FL,		/* front left */
	SNDRV_CHMAP_FR,		/* front right */
	SNDRV_CHMAP_RL,		/* rear left */
	SNDRV_CHMAP_RR,		/* rear right */
```



## control

```
	snd_ctl_t *handle;
	snd_ctl_card_info_t *info;
	snd_pcm_info_t *pcminfo;
	snd_rawmidi_info_t *rawmidiinfo;
```

# async机制分析

是靠sigio来做的。

# alsa-ioctl-test

这个库似乎不错。

https://github.com/takaswie/alsa-ioctl-test

# 参考资料

1、how to compile test examples alsa

https://stackoverflow.com/questions/14355488/how-to-compile-test-examples-alsa

2、

https://blog.csdn.net/eydwyz/article/details/72577196

3、

https://blog.csdn.net/kickxxx/article/details/8291598