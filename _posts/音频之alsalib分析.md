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

## latency.c

看看这个latency测试做了什么。

运行，不用任何参数就可以运行。

默认的播放和录音设备都是hw:0,1 



```
# ./latency 
Scheduler set to Round Robin with priority 99...
Playback device is hw:0,0
Capture device is hw:0,0
Parameters are 22050Hz, S16_LE, 2 channels, non-blocking mode
Poll mode: no
Loop limit is 661500 frames, minimum latency = 64, maximum latency = 4096
[ 1436.018134@2]  audio_ddr_mngr: frddrs[0] registered by device fe330000.audiobus:tdm@0
[ 1436.020639@2]  master_mode(0), binv(1), finv(1) out_skew(3), in_skew(3)
[ 1436.020981@2]  master_mode(0), binv(1), finv(1) out_skew(3), in_skew(3)
[ 1436.021635@2]  asoc-aml-card auge_sound: tdm prepare capture
Hardware PCM card 0 'AML-AUGESOUND' de[ 1436.022860@2]  asoc-aml-card auge_sound: TDM[0] Capture enable
vice 0 subdevice 0
Its setup is:
  stream       : PLAYBACK
  access       : RW_INTERLEAVED
  format       : S16_LE
  subformat    : STD
  channels     : 2
  rate         : 22050
  exact rate   : 22050 (22050/1)
  msbits       : 16
  buffer_size  : 64
  period_size  : 32
  period_time  : 1451
  tstamp_mode  : NONE
  tstamp_type  : MONOTONIC
  period_step  : 1
  avail_min    : 32
  period_event : 0
  start_threshold  : 2147483647
  stop_threshold   : 64
  silence_threshold: 0
  silence_size : 0
  boundary     : 1073741824
  appl_ptr     : 0
  hw_ptr       : 0
Hardware PCM card 0 'AML-AUGESOUND' device 0 subdevice 0
Its setup is:
  stream       : CAPTURE
  access       : RW_INTERLEAVED
  format       : S16_LE
  subformat    : STD
  channels     : 2
  rate         : 22050
  exact rate   : 22050 (22050/1)
  msbits       : 16
  buffer_size  : 64
  period_size  : 32
  period_time  : 1451
  tstamp_mode  : NONE
  tstamp_type  : MONOTONIC
  period_step  : 1
  avail_min    : 32
  period_event : 0
  start_threshold  : 2147483647
  stop_threshold   : 64
  silence_threshold: 0
  silence_size : 0
  boundary     : 1073741824
  appl_ptr     : 0
  hw_ptr       : 0
Trying latency 64 frames, 2902.494us, 2.902494ms (344.5312Hz)
[ 1437.656587@2]  sched: RT throttling activated
[ 1437.705841@0]  RT throttling on cpu:2 rt_time:951ms, curr:swapper/2/0 prio:120 sum_runtime:0ms
[ 1438.705842@0]  RT throttling on cpu:2 rt_time:950ms, curr:swapper/2/0 prio:120 sum_runtime:0ms
[ 1439.705829@0]  RT throttling on cpu:2 rt_time:953ms, curr:swapper/2/0 prio:120 sum_runtime:0ms
[ 1440.705832@0]  RT throttling on cpu:2 rt_time:952ms, curr:swapper/2/0 prio:120 sum_runtime:0ms
[ 1441.705853@0]  RT throttling on cpu:2 rt_time:952ms, curr:swapper/2/0 prio:120 sum_runtime:0ms
```

看代码里有这个：

```
snd_pcm_link(chandle, phandle)
```

snd_pcm_link的作用是什么？

把2个pcm连接起来。

可以调用到snd_pcm_hw_link

最后是调用SNDRV_PCM_IOCTL_LINK。



# async机制分析

是靠sigio来做的。

# alsa-ioctl-test

这个库似乎不错。

https://github.com/takaswie/alsa-ioctl-test

# alsalisp

lisp 和 alsa lisp 的区别

Alsa lisp 只是用一些简单的内在函数实现了 lisp 的基本语法。

但它不支持宏语法，太复杂了。

除了简单的语法之外，alsa lisp 还实现了自己特殊的内部函数来调用 alsa-lib 本机函数。 

alsa相关的内在函数包括：

```
static const struct intrinsic snd_intrinsics[] = {
        { "Acall", F_acall },
        { "Aerror", F_aerror },
        { "Ahandle", F_ahandle },
        { "Aresult", F_ahandle },
        { "Asnderr", F_snderr },
        { "Asyserr", F_syserr }
    };
```





https://medium.com/@zpcat/alsa-lisp-in-alsa-lib-eb2fd497ecb3

# aserver.c

`aserver.c` 是 ALSA（Advanced Linux Sound Architecture）项目中的一个文件，它是 ALSA 库的一部分。该文件实现了 ALSA 的音频服务器（Audio Server）功能。

音频服务器是 ALSA 中的一个重要组件，它提供了音频设备的管理和控制。aserver.c 文件包含了音频服务器的实现代码，其中包括与音频设备的连接、音频数据的传输、音频流的处理等功能。

通过音频服务器，应用程序可以与音频设备进行交互，实现音频的输入和输出。它提供了一个统一的接口，使应用程序能够以统一的方式访问不同的音频设备，包括声卡、虚拟音频设备等。

具体来说，aserver.c 文件可能包含了以下功能的实现：

1. 设备管理：与音频设备的连接和初始化，包括打开设备、设置采样率、通道数等。

2. 数据传输：音频数据的读取和写入，包括从应用程序读取音频数据并发送到音频设备，或从音频设备读取音频数据并传递给应用程序。

3. 音频流处理：对音频流进行处理，例如音频格式转换、音频效果处理、混音等。

4. 控制和同步：提供控制音频服务器的接口，例如启动、停止、暂停音频流，以及同步音频流的时钟等。

需要注意的是，aserver.c 只是 ALSA 音频服务器的一部分，整个 ALSA 项目包含了更多的组件和文件，用于提供全面的音频处理和音频设备管理功能。

## aserver过时了吗

根据我所了解的信息，`aserver` 在 ALSA 项目中已经过时了。在较新版本的 ALSA 中，`aserver` 不再被广泛使用或推荐作为音频服务器的实现。

替代 `aserver` 的是 PulseAudio，它是一个现代的音频服务器系统，提供了更强大和灵活的音频管理和处理功能。PulseAudio 在大多数 Linux 发行版中成为默认的音频服务器。它提供了高级的音频路由、音量控制、设备管理、混音以及网络音频功能等。

PulseAudio 具有更好的多应用程序支持、音频设备切换的灵活性以及更好的音频处理和混音能力。它还提供了强大的插件架构，可以扩展和自定义其功能。

虽然 `aserver` 过时了，但 ALSA 仍然是 Linux 和许多嵌入式系统上的音频架构的基础。应用程序可以直接使用 ALSA API 来与音频设备进行交互，而不必依赖于 `aserver`。

如果您需要在 Linux 系统上进行音频处理或音频管理，推荐使用 PulseAudio 或其他现代的音频服务器来替代 `aserver`。

# pcm_local.h



# alsa的namehint是什么

在ALSA（Advanced Linux Sound Architecture）中，==namehint是一种用于指定音频设备名称的机制。==它提供了==一种灵活的方式来标识和选择音频设备。==

通常情况下，ALSA会根据配置文件和硬件信息自动分配设备名称，例如"hw:0"、"hw:1"等。然而，有时候这些默认的设备名称可能不够直观或不够具有描述性。

==namehint允许用户为音频设备提供一个更具描述性的名称，以替代默认的设备名称。==这个名称可以是任意字符串，用于更好地标识和识别音频设备。例如，可以将namehint设置为"External USB Sound Card"，以更清晰地表示设备的身份和类型。

使用namehint可以提高音频设备的可识别性和可用性。它可以在ALSA配置文件中进行设置，或者通过ALSA库的API进行动态设置。通过指定namehint，用户可以更方便地选择和操作音频设备，而不仅仅依赖于默认的设备名称。



```
# show all name hints also for definitions without hint {} section
defaults.namehint.showall off
# show just basic name hints
defaults.namehint.basic on
# show extended name hints
defaults.namehint.extended off
```

这段代码片段是ALSA配置文件中的设置，用于控制在设备定义中显示和使用namehint的方式。

- `defaults.namehint.showall off`：该设置指示ALSA不显示没有namehint的设备定义。也就是说，只有带有namehint的设备定义会被显示。

- `defaults.namehint.basic on`：该设置指示ALSA显示基本的namehint。基本的namehint是指给设备定义提供的简单、常规的名称提示。

- `defaults.namehint.extended off`：该设置指示ALSA不显示扩展的namehint。扩展的namehint是指给设备定义提供更详细、更具描述性的名称提示。

通过这些设置，可以控制ALSA在设备定义中显示不同级别的namehint。可以根据实际需要，选择显示基本的名称提示还是更详细的名称提示。

# snd_ctl和snd_hctl区别

==h表示high level的意思。==

snd_hctl包含了snd_ctl的指针，相当于它的子类。

hclt的函数都是转而调用ctl的函数的。

==mixer里都是调用的hctl的接口。==

```
所以api层次是这样：
	我们使用mixer接口。
	mixer接口调用hctl接口。
	hctl接口调用clt接口。
	我们只需要关注mixer接口就可以了。
```



```
snd_mixer_selem_register
	snd_mixer_simple_none_register
		这个对应的simple_none.c，编译了的。
		simple_abst.c 这个是默认没有编译的。
		
```

```
simple.c 这个是接口层
	simple_none.c 这个是实现层。
```



# alsa mixer的simple_none.c和simple_abst.c 关系

`simple_none.c`和`simple_abst.c`是ALSA库中用于混音器（mixer）抽象层的两个不同实现文件。

`simple_none.c`是一个简单的混音器实现，它提供了最基本的混音器功能。它不依赖于任何特定的硬件或底层驱动程序，而是提供了一个虚拟的混音器接口，用于处理音频控制和调整音量等操作。这个实现适用于那些不需要硬件混音器支持的场景。

另一方面，`simple_abst.c`是一个更复杂和抽象的混音器实现。它建立在`simple_none.c`的基础上，并提供了更多的功能和灵活性。它可以与不同类型的硬件混音器进行交互，包括硬件混音器的控制和配置。这个实现可以根据底层硬件的不同进行定制和扩展。

总结起来，`simple_none.c`是一个简单的混音器实现，提供基本的混音器功能，而`simple_abst.c`是一个更复杂和抽象的混音器实现，提供更多的功能和与硬件混音器的交互。它们在ALSA库中属于混音器抽象层的不同实现文件，用于处理音频控制和调整音量等操作。

# alsa use case说明

ALSA（Advanced Linux Sound Architecture）中的 "use case" 表示一种特定的音频应用场景或用途，

其中定义了声卡和音频硬件的配置以满足该场景的需求。

使用案例通常包括特定的音频输入输出设置、采样率、通道数等参数，

以确保在特定的使用环境中获得最佳的音频性能。

在 ALSA 中，使用案例的定义涉及到配置音频通道、混音设置、音频输入输出设备的连接等。

通过指定使用案例，用户或应用程序可以告诉 ALSA 如何配置声卡以满足其特定的音频需求。

以下是一个典型的 ALSA 使用案例的配置示例：

```c
#include <alsa/asoundlib.h>

int main() {
    snd_pcm_t *handle;
    snd_pcm_hw_params_t *params;
    const char *device = "default";

    // 打开 PCM 设备
    snd_pcm_open(&handle, device, SND_PCM_STREAM_PLAYBACK, 0);

    // 初始化硬件参数
    snd_pcm_hw_params_alloca(&params);
    snd_pcm_hw_params_any(handle, params);

    // 设置使用案例的参数，例如采样率、通道数等
    snd_pcm_hw_params_set_access(handle, params, SND_PCM_ACCESS_RW_INTERLEAVED);
    snd_pcm_hw_params_set_format(handle, params, SND_PCM_FORMAT_S16_LE);
    snd_pcm_hw_params_set_channels(handle, params, 2);
    unsigned int rate = 44100;
    snd_pcm_hw_params_set_rate_near(handle, params, &rate, 0);

    // 应用参数到 PCM 设备
    snd_pcm_hw_params(handle, params);

    // ... 其他操作

    // 关闭 PCM 设备
    snd_pcm_close(handle);

    return 0;
}
```

在这个例子中，`snd_pcm_hw_params_set_format`、`snd_pcm_hw_params_set_channels` 和 `snd_pcm_hw_params_set_rate_near` 等函数设置了音频硬件的参数，以适应特定的使用案例（在这里是播放音频）。实际上，根据不同的使用案例，你可能需要调整这些参数以满足具体的需求。

使用案例的概念允许 ALSA 灵活地适应各种音频需求，例如音频播放、录制、VoIP 通信等。

==在 ALSA 中，你可以通过配置不同的使用案例来实现这些不同的音频应用场景。==

## ucm

alsaucm（ALSA 用例管理器）是一个使用 ALSA 用例接口的程序命令行。

在复杂的声卡上，设置音频路由并不简单，

混音器设置可以彼此冲突，导致声卡根本无法工作。

ALSA 用例管理器是一种用于控制复杂音频硬件的机制

在硬件配置和有意义的用例之间建立关系

最终用户可以与之联系。

用例管理器还可用于在必要时在用例之间切换一致的方式。



代码在alsa-utils的alsaucm\usecase.c

## 命令用法

`alsaucm` 是 ALSA（Advanced Linux Sound Architecture）工具中的一个用于管理使用案例（use case）的命令行工具。它允许用户配置和管理不同的音频使用场景，例如播放音频、录制音频等。以下是一些基本的用法示例：

1. **列出支持的使用案例：**
   ```bash
   alsaucm -c <card-id> list
   ```
   这将列出指定声卡 (`<card-id>`) 上支持的所有使用案例。

2. **选择使用案例：**
   
   ```bash
   alsaucm -c <card-id> set <use-case>
   ```
这将设置指定声卡 (`<card-id>`) 的当前使用案例为 `<use-case>`。
   
3. **列出当前使用案例的状态：**
   ```bash
   alsaucm -c <card-id> status
   ```
   这将显示指定声卡 (`<card-id>`) 上当前使用案例的状态信息。

4. **启动/停止使用案例：**
   
   ```bash
   alsaucm -c <card-id> start
   alsaucm -c <card-id> stop
   ```
   这将启动或停止指定声卡 (`<card-id>`) 上当前使用案例。

请注意，`<card-id>` 是你的声卡的编号，你可以通过 `aplay -l` 或 `arecord -l` 命令来查看。

下面是一个使用案例的完整示例：

```bash
# 列出支持的使用案例
alsaucm -c 0 list

# 设置使用案例为播放音频
alsaucm -c 0 set Playback

# 查看当前使用案例状态
alsaucm -c 0 status

# 启动使用案例
alsaucm -c 0 start
```

请根据你的实际需求和声卡配置，使用 `alsaucm` 工具进行相应的配置。确保你在使用该工具时了解你的声卡支持的使用案例和相应的配置选项。



https://manpages.ubuntu.com/manpages/focal/en/man1/alsaucm.1.html

# output的层次关系

可以看到也是有一个类的继承关系的。

面向接口编程的观念也是有的。

snd_output 这个是接口层。

它有2个实现的子类。

```
snd_output_stdio
snd_output_buffer
```

接口使用的数据结构是抽象的snd_output_t。

```
struct _snd_output {
	snd_output_type_t type;
	const snd_output_ops_t *ops;
	void *private_data;
};
```



snd_output的接口有：

| 接口              | 说明 |
| ----------------- | ---- |
| snd_output_close  |      |
| snd_output_printf |      |
| snd_output_puts   |      |
| snd_output_putc   |      |
| snd_output_flush  |      |

open有所不同：

```
snd_output_stdio_open

snd_output_stdio_attach
	这个不用open，直接把一个现成的FILE *指针跟output关联起来。

snd_output_buffer_open这个不用attach。
```

# snd_pcm_ops_t 和snd_pcm_fast_ops_t的关系

 `snd_pcm_fast_ops_t` 则是 `snd_pcm_ops_t` 的一种优化版本，旨在提高 PCM 设备操作的效率。

它包含了一组更快速、经过优化的函数指针，用于更快地执行音频设备的操作。

这些函数指针可能使用了一些技巧或者更高效的方法来完成相同的任务，从而提升了音频数据的处理速度。

# BUILD_PCM_PLUGIN_MMAP_EMUL

`BUILD_PCM_PLUGIN_MMAP_EMUL` 是 ALSA 库的一个编译选项，用于构建 PCM 插件的内存映射（mmap）模拟支持。

==在某些情况下，音频设备可能不支持真正的内存映射方式（mmap），而是通过模拟实现来提供对这种功能的支持。==这种情况下，可以使用 `BUILD_PCM_PLUGIN_MMAP_EMUL` 选项进行编译，以构建 ALSA PCM 插件的模拟内存映射支持。

该选项的启用可能会使 ALSA 库在运行时提供对那些并不实际支持 mmap 的设备提供某种模拟方式，让它们也能够使用 mmap 相关的功能，尽管实际上这只是一种模拟而非硬件级别的内存映射支持。

在编译 ALSA 库时启用 `BUILD_PCM_PLUGIN_MMAP_EMUL` 选项可以帮助处理一些特定设备不支持 mmap 的情况，使得这些设备也能够利用 ALSA 提供的 mmap 相关的特性和功能。

# alsa配置文件里的type plug和其他的插件有什么区别

在 ALSA 的配置文件中，`type plug` 是一个特殊的 PCM 类型，用于创建一个 PCM 转发（PCM forwarding）或者转换（PCM conversion）的插件。

与其他插件相比，`type plug` 允许你创建一个虚拟的 PCM 设备，对输入或输出的音频数据进行处理，然后将其传递到另一个 PCM 设备。

区别在于：

1. **转发和转换功能**：`type plug` 允许你创建一个中间层的 PCM 设备，可以将其配置为转发输入数据到输出设备，或者在中间进行特定的音频格式转换、采样率转换等处理。

2. **灵活性**：`type plug` 插件非常灵活，它可以用于许多不同的转换和处理场景。你可以配置它来适应不同的音频设备和需求，进行格式转换、通道映射、音频数据处理等操作。

3. **其他插件功能**：相比之下，其他插件可能有着特定的功能和目的。例如，`type hw` 用于直接连接到硬件设备，`type asym` 用于管理多个输入输出设备等。==而 `type plug` 则更像是一个通用的处理器，可以根据配置对音频数据进行处理和转发。==

总体来说，`type plug` 提供了更多的灵活性，允许对音频数据进行中间处理并将其发送到其他 PCM 设备。这种特性使其在需要音频转换或中间层处理时非常有用。

# pcm_multi.c这个的作用是什么

`pcm_multi.c` 是 ALSA 源代码中的一个文件，用于实现 ALSA PCM（脉冲编码调制）设备的多路复用功能。该文件主要包含了用于创建和管理多路复用 PCM 设备的相关代码。

在 ALSA 中，多路复用 PCM 设备允许多个客户端应用程序同时访问同一个 PCM 设备，实现了多个客户端同时使用音频设备的功能。这对于一些场景，比如需要多个应用同时播放音频或进行音频录制时非常有用。

`pcm_multi.c` 文件中的代码实现了管理多个客户端对同一个 PCM 设备的访问，包括对音频数据的路由、同步、缓冲区管理等功能。它允许多个应用程序通过相同的 PCM 设备来传输音频数据，从而实现了音频设备的共享和多路复用。

这种功能对于需要多个应用程序同时访问同一个音频设备的场景非常有用，比如音频会议、多媒体应用等。它确保了这些应用程序能够同时使用音频设备，而不会发生资源冲突或数据混乱。

# struct snd_pcm_direct



*Direct Stream Mixing*

就是dmix。

这里也有一个server的概念在的。

snd_pcm_direct_server_create

在snd_pcm_dmix_open里被调用。

# SNDRV_PCM_IOCTL_DELAY

`SNDRV_PCM_IOCTL_DELAY` 是 ALSA 中 PCM 设备相关的一个 ioctl 命令。它用于获取 PCM 设备的延迟信息。

使用该 ioctl 命令，可以向 ALSA PCM 设备发送一个请求以获取当前音频流中的延迟。延迟信息对于需要实时音频处理的应用程序非常重要，例如需要音频和视频同步的多媒体应用程序等。

这个 ioctl 命令需要通过调用 `ioctl()` 系统调用并传递相应的参数来使用。在 C 语言中的使用可能类似以下示例：

```c
#include <alsa/asoundlib.h>

snd_pcm_t *pcm_handle; // 假设已经打开了 PCM 设备

snd_pcm_sframes_t delay;
if (ioctl(snd_pcm_file_descriptor(pcm_handle), SNDRV_PCM_IOCTL_DELAY, &delay) == 0) {
    printf("PCM device delay: %lu frames\n", (unsigned long)delay);
} else {
    printf("Failed to get PCM device delay\n");
}
```

这个 ioctl 命令通过将 `SNDRV_PCM_IOCTL_DELAY` 作为命令参数传递给 PCM 设备的文件描述符来获取当前的延迟值。`delay` 是一个返回参数，表示当前 PCM 设备中的延迟帧数。

这个值对于确保音频和视频同步、实现低延迟音频处理以及确保实时应用程序的正确功能非常重要。

## 这个延迟是怎么算出来的

PCM 设备的延迟指的是在音频数据流中经过的时间或样本帧数量，通常用于描述数据在从应用程序发送到音频设备或从音频设备接收到应用程序之间的时间差。

延迟的计算可以根据具体的应用场景和硬件设备的不同而有所不同。一般来说，有两种类型的延迟：

1. **输入延迟（Capture Delay）**：指的是从音频输入设备捕获数据到应用程序处理数据之间的时间差。
   
2. **输出延迟（Playback Delay）**：指的是从应用程序发送数据到音频输出设备播放之间的时间差。

对于 ALSA 中的 PCM 设备，可以通过 `SNDRV_PCM_IOCTL_DELAY` ioctl 命令来获取当前 PCM 设备的延迟信息。这个延迟通常以采样帧数的形式表示，表示在数据流中经过的采样帧数量。

这个延迟值的计算可能涉及多个因素，包括：

- **硬件缓冲区**：音频设备通常有自己的缓冲区用于数据的传输和处理。延迟值可以受到这些缓冲区的大小和设备内部处理的影响。

- **数据处理时间**：数据在应用程序和设备之间的传输和处理所需的时间。这包括数据在缓冲区中等待、处理器的处理时间等等。

- **硬件时钟**：硬件时钟的精确性和同步性对延迟的计算也有影响。

延迟的准确计算可能是一个复杂的过程，取决于设备和应用程序的特性。`SNDRV_PCM_IOCTL_DELAY` 通过 ALSA 提供了一种获取延迟信息的方式，但延迟的实际计算可能还受到其他因素的影响，需要结合具体的设备和应用场景来理解和衡量延迟值。

# buildroot默认没有编译alsalib的test

需要在test/Makefile.am里加上：

```
bin_PROGRAMS = latency pcm
```

以及其他你需要编译的。这样默认make就会编译出来你要的测试程序。

默认的check_PROGRAMS，需要make check才会生成。

# alsa里的refine是什么概念

在 ALSA 中，"refine" 是一个==用于优化和调整音频设备参数的概念==。

在 ALSA 的 PCM 设备中，通常有一组硬件参数（hardware parameters），比如采样率、通道数、数据格式等等。

这些参数需要在应用程序与音频设备之间进行匹配和协商，以确保数据能够正确地传输和处理。

"Refine" 在 ALSA 中的上下文中表示对这些硬件参数进行优化和调整的过程。这包括但不限于：

- **参数匹配和协商**：将应用程序的参数与音频设备的参数进行匹配和协商，选择最合适的参数配置。

- **参数修正和补充**：在参数不匹配或不完整的情况下，根据设备的特性和应用程序的需求对参数进行修正和补充，以确保数据传输的准确性和稳定性。

- **设备能力检测**：检测音频设备的能力和特性，以确定设备支持的最佳参数范围，并尝试调整应用程序的参数以适应设备的能力。

"Refine" 的过程可以发生在 PCM 设备的准备阶段，例如在打开 PCM 设备之后，应用程序可能需要对设备的参数进行优化和调整，以确保音频数据的正常传输和处理。

## 用实际的数字来举例

好的，让我们假设有一个 PCM 设备，支持的参数为：

- 采样率：8000 Hz、16000 Hz、32000 Hz、44100 Hz、48000 Hz
- 通道数：1（单声道）或 2（立体声）
- 数据格式：16 位 Little-Endian

现在你有一个音频文件，它的参数为：

- 采样率：44100 Hz
- 通道数：2（立体声）
- 数据格式：16 位 Little-Endian

你的应用程序需要将这个音频文件播放到 PCM 设备上。在这个情况下可能会进行的 "refine" 过程如下：

1. **打开 PCM 设备**：使用 ALSA API 打开 PCM 设备。

2. **设置设备参数**：设置 PCM 设备的参数为：

   - 采样率：44100 Hz
   - 通道数：2（立体声）
   - 数据格式：16 位 Little-Endian

3. **参数优化**：检查设备能否完全支持这些参数。假设设备支持全部参数，则无需额外的参数修正。

4. **数据传输**：开始将音频文件数据传输到 PCM 设备。由于参数完全匹配，音频文件的数据可以直接传输到设备，保证音频的播放。

在这个例子中，"refine" 过程主要涉及设置 PCM 设备的参数，并确保这些参数与音频文件的参数相匹配，以确保音频文件能够在 PCM 设备上正确播放。

# 参考资料

1、how to compile test examples alsa

https://stackoverflow.com/questions/14355488/how-to-compile-test-examples-alsa

2、

https://blog.csdn.net/eydwyz/article/details/72577196

3、

https://blog.csdn.net/kickxxx/article/details/8291598