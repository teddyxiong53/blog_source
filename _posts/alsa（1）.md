---
title: alsa（1）
date: 2018-05-09 23:01:22
tags:
	- alsa

---

1

在alsa驱动这一层，目前为止，抽象出了4层设备：

一是hw:0,0；

二是plughw:0,0；

三是default:0；

四是default。

至于一是清楚了，二和二以上可以做数据转换，以支持一个动态的范围，比如你要播放7000hz的东西，那么就可以用二和二以上的。而你用7000hz作为参数，去设置一，就会报错。三和四，支持软件混音。我觉得default:0表示对第一个声卡软件混音，default表示对整个系统软件混音。

这里提出两点：

1.1.1 一般为了让所有的程序都可以发音，为使用更多的默认策略，我们选用三和四，这样少一些控制权，多一些方便。

1.1.2 对不同的层次的设备，相同的函数，结果可能是不一样的。比如，设置Hardware Parameters里的period和buffer size，这个是对硬件的设置，所以，default和default:0这两种设备是不能设置的。

如果直接操作hw:0,0，那么snd_pcm_writei只能写如8的倍数的frame，比如16、24等，否则就会剩下一点不写入而退回，而 default，就可以想写多少就写多少，我们也不必要关心里面具体的策略。



交叉模式，interleaved。就是左右声道数据交叉存储，而不是先全部放左声道，然后全部放右声道的方式。

snd_pcm_readi，这个i就是表示interleaved模式。



xrun包括两种情况：

overrun，就是录音的时候可能会出现。应用层取数据太慢了。

underrun：就是播放的时候出现。应用层写得快，硬件层来不及处理。



EPIPE错误表示overrun错误。





alsa的plugin是个什么概念？

https://alsa.opensrc.org/ALSA_plugins

这里有说明。

什么是plugin？

是用来创建虚拟设备，这些虚拟设备可以当成硬件设备来用。

常见的plugin有：

```
adpcm
	
```

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

上面的语句，创建了一个名字叫SOMENAME的插件。类型是PLUGINTYPE。一个插件相当于一个pipe，它的后端就是slave里的东西。

插件的名字，有些是已经被预定义了的，例如default，dmix 。

slave，可以是另一个插件，也可以是硬件设备。例如可以是hw:0,0

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
aplay -Dmyplugdev 1.wav
```





pcm插件扩展了pcm设备的特性和功能。



还是要把官方文档仔细看一遍。

配置文件语法

```
简单格式，支持现代数据描述，例如嵌套和数组支持。
空白。如果有有用的空白，用"A B"。引号来包含。
注释用# 。

标点符号：
大括号
中括号
,
;
=
.
''
""

```

等号不是必须的，因为主要是靠空白进行分割的。

```
a 1 # is equal to
a=1 # is equal to
a=1;    # is equal to
a 1,
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