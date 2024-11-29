---
title: 音频之alsa.conf写法
date: 2018-09-28 13:58:17
tags:
	- 音频

---

--

配置文件是在snd_pcm_open的时候，会进行调用。

代码是这样：

```
int snd_pcm_open(snd_pcm_t **pcmp, const char *name, 
		 snd_pcm_stream_t stream, int mode)
{
	snd_config_t *top;//这个结构体存放配置。这个存放一个配置项，多个组成链表。
	int err;

	assert(pcmp && name);
	err = snd_config_update_ref(&top);//这里面读取配置。
	if (err < 0)
		return err;
	err = snd_pcm_open_noupdate(pcmp, top, name, stream, mode, 0);
	snd_config_unref(top);
	return err;
}
```

```
snd_config_update_r
	configs = getenv(ALSA_CONFIG_PATH_VAR);//先从环境变量里读取这个ALSA_CONFIG_PATH路径。
	如果没有，那么就从，默认路径找。
	sprintf(s, "%s/alsa.conf", topdir);
	//找到用户自定义的配置文件。
	err = snd_user_file(name, &local->finfo[k].name);
	//读取配置。
	snd_config_load
```

```
上面的主要说明点：
    .asoundrc和asound.conf的引入提供用户定制化
    /usr/share/alsa/alsa.conf为alsa-api的主要入口点
```

**在alsa.conf中，通常还会引用 /etc/asound.conf 和 ~/.asoundrc这两个配置文件，**

这两个文件通常是放置你个人需要特殊设置的相关参数。

按照Alsa官方文档的说法，1.0.9版本以后，这两个文件就不再是必要的，甚至是不应该需要的。

至少是不推荐使用吧。

不过，对于我来说，在嵌入式系统中使用，为了简单和方便测试，恰恰是需要修改这两个文件 

配置蓝牙播放。

```
# device for bluetooth
pcm.bluetooth{
        type bluetooth
        device 00:02:5B:00:C1:A0
}
 
然后调用 aplay –D bluetooth sample.wav 播放。
```

需要注意，为了使用该设备，你需要 /usr/lib/alsa-lib/libasound_module_pcm_bluetooth.so 这一个蓝牙plugin的库文件。

这是在Bluez相关的包里，和Alsa本身没有关系。

从这里，我们也可以看出alsa的外部plugin和配置文件之间的名字关系规则： libasound_module_pcm_####.so 这里的#### 就是你在conf文件中pcm.xxxx 里所写的名字。

```
snd_pcm_open_conf
```

```
static const char *const build_in_pcms[] = {
	"adpcm", "alaw", "copy", "dmix", "file", "hooks", "hw", "ladspa", "lfloat",
	"linear", "meter", "mulaw", "multi", "null", "empty", "plug", "rate", "route", "share",
	"shm", "dsnoop", "dshare", "asym", "iec958", "softvol", "mmap_emul",
	NULL
};
```

```
sprintf(buf1, "%s/libasound_module_pcm_%s.so", ALSA_PLUGIN_DIR, str);
```



```
type hw 
	这个是用来做alias的。With the 'PCM hw type' you are able to define aliases for your devices.
```

例如，我们常用的指定default的。

```
pcm.!default {
	type hw
	card 0
	device 0
}
```

这个default，我们也可以替换成其他的名字，例如：

```
pcm.primary {
	type hw
	card 0 
	device 0
}
```

录音的时候，我们就这样：

```
arecord -D primary 1.wav
```



alsa-lib的库文件：

```
/usr/lib/alsa-lib # ls                         
libasound_module_ctl_arcam_av.so               
libasound_module_ctl_bluealsa.so               
libasound_module_ctl_oss.so                    
libasound_module_pcm_bluealsa.so               
libasound_module_pcm_oss.so                    
libasound_module_pcm_upmix.so                  
libasound_module_pcm_usb_stream.so             
libasound_module_pcm_vdownmix.so               
libasound_module_rate_samplerate.so            
libasound_module_rate_samplerate_best.so       
libasound_module_rate_samplerate_linear.so     
libasound_module_rate_samplerate_medium.so     
libasound_module_rate_samplerate_order.so      
libasound_module_rate_speexrate.so             
libasound_module_rate_speexrate_best.so        
libasound_module_rate_speexrate_medium.so      
```



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

default前的**感叹号用于替代**alsa api 中默认的default配置



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



使用#号作为注释。

键值对语法。

```
key [
	"value0";
	"value1";
]
```

等价于：

```
key.0 "value0";
key.1 "value1";
```

```
key {
	subkey0 value0;
	subkey1 value1
}
```

等价于：

```
key.subkey0 value0;
key.subkey1 value1;
```



操作模式

```
用前缀来表示。默认是merge and create模式。
有4种模式。
+ ： merge and create。
- ： merge
？ ： 不要覆盖。
！：覆盖。
```





配置文件的位置

```
/usr/share/alsa
```

这个目录下的文件有：

```
alsa.conf        
alsa.conf.d      
cards            
init             
pcm              
sndo-mixer.alisp 
speaker-test     
topology         
ucm              
```

主配置文件就是这个alsa.conf文件。内容比较多。

首先是读取/etc/asound.conf和~/.asoundrc这2个文件的内容。

```

```



声卡设备的编号。

在/dev/snd目录下，看到这些char设备文件。

```
controlC0  ：control开头的，表示用于声卡的控制，例如通道选择，混音，麦克风控制。C表示Card。
controlC1  
controlC7  
pcmC0D0c   C0D0：card 0 device 0 。最后的c表示录音（capture）。前面的pcm表示pcm设备。对应的还有midi设备。
pcmC0D0p   p表示播放，play。
pcmC1D0c   
pcmC1D0p   
pcmC7D0c   
pcmC7D0p   
pcmC7D1c   
pcmC7D1p   
timer      
```

另外在/proc/asound/目录下，有这些：

```
/proc/asound # ls
Loopback         card7            pcm              timers
card0            cards            rockchiprk3308p  version
card1            devices          rockchiprk3308v
```

查看devices文件。

```
/proc/asound # cat devices
  0: [ 0]   : control
 16: [ 0- 0]: digital audio playback
 24: [ 0- 0]: digital audio capture
 32: [ 1]   : control
 33:        : timer
 48: [ 1- 0]: digital audio playback
 56: [ 1- 0]: digital audio capture
224: [ 7]   : control
240: [ 7- 0]: digital audio playback
241: [ 7- 1]: digital audio playback
248: [ 7- 0]: digital audio capture
249: [ 7- 1]: digital audio capture
```



pcm逻辑设备

我们习惯称之为pcm中间层，或者pcm native。



alsa用card、device和subdevice的分层结构来表示audio硬件设备和它们的组件。

层次关系是这样。

```
card0
	device0
		subdevice0
	device1
	
card1
	device0
```



这个分层结构是alsa看待硬件设备结构和能力的视角。

card和硬件上的声卡是一一对应的。

大部分的alsa硬件访问发生在device这个层级。

一个card上有多个device。

card+device的组合，基本可以说清楚，一个声音从哪里来，到哪里去。

**subdevice，一般是对应一个通道。**



alsa几乎都是由plugin构成的。

plugin列表不等同于alsa device列表。

有些device的名字跟plugin的名字一样，有些不一样。

最重要的plugin就是hw plugin。

它本身不做任何任何处理。

仅仅访问硬件驱动。



alsa.conf最终被解释为一棵树，它的节点是struct _snd_config结构，





# defaults

一般alsa设置了**一个defaults设备，**音频播放软件默认使用defaults设备输出声音。defaults设备定义在alsa.conf中。

**defaults会默认匹配card number和device number比较小的声卡。**

alsa的配置文件是alsa.conf位于/usr/share/alsa目录下，通常还有/usr/share/alsa/card和/usr/share/alsa/pcm两个子目录用来设置card相关的参数，别名以及一些PCM默认设置。以上配置文件，我等凡夫从不用修改，修改它们是大神的工作。



# plugin插件写法

插件是用来扩展pcm设备的功能和特性的。

插件可以做的事情：

```
采样率转化
通道之间复制。

```

往树莓派的.asoundrc里加几行配置，启动录音。报错。

```
pi@raspberrypi:~ $ arecord 2.wav
ALSA lib conf.c:1887:(_snd_config_load_with_include) _toplevel_:22:0:Unexpected char
ALSA lib conf.c:3650:(config_file_open) /home/pi/.asoundrc may be old or corrupted: consider to remove or fix it
ALSA lib conf.c:3572:(snd_config_hooks_call) function snd_config_hook_load returned error: Invalid argument
ALSA lib conf.c:4026:(snd_config_update_r) hooks failed, removing configuration
arecord: main:828: audio open error: Invalid argument
```

在asoundrc里加上这个。

```
pcm_slave.test123 {
    pcm "hw:1,0"
    format S16_LE
    rate 48000
}
pcm.rate_convert {
    type rate
    slave test123
}
```

录音命令：-v表示verbose。

```
arecord -vD rate_convert  3.wav
```

打印的输出：

## asym

*asym* is an ALSA PCM plugin that combines **half-duplex** PCM plugins like *dsnoop* and *dmix* into one **full-duplex** device

asym是asymmetrically的缩写。这个单词的意思是非对称。也就是播放和录音分开设置。

asym是一个插件，作用是把半双工的插件（比如dsnoop、dmix）转换成全双工的设备。

主要用来配置模式的录音和播放设备。



`type asym` 是 ALSA 提供的一种插件，用于实现非对称音频设备配置。它允许分别定义播放（`playback.pcm`）和录音（`capture.pcm`）的设备，从而使它们独立工作。

### **关键点**

- **作用**：将播放和录音设备分开使用，适用于播放设备和录音设备不同的情况。

- 语法

  ：

  ```plaintext
  pcm.asym_example {
      type asym
      playback.pcm "playback_device"
      capture.pcm "capture_device"
  }
  ```

  - `playback.pcm`：指定播放使用的 PCM 设备。
  - `capture.pcm`：指定录音使用的 PCM 设备。

------

### **当前配置中的应用**

```plaintext
pcm.!default {
  type asym
  playback.pcm "plug:stereo2quad"
  capture.pcm "plug:dnsoop"
}
```

#### 解读：

1. **播放路径**：
   - 使用 `plug:stereo2quad` 作为播放设备，提供立体声到四声道的路由功能，并最终输出到 `quad`。
   - 适合需要混合模拟和数字音频的场景。
2. **录音路径**：
   - 使用 `plug:dnsoop` 作为录音设备。
   - 这里 `dnsoop` 可能是另一个插件设备（未定义），需要查看其具体实现。

------

### **应用场景**

1. 单独配置录音和播放设备

   ：

   - 硬件录音和播放设备不同，例如使用独立的 USB 麦克风和音响。

2. 特殊信号处理需求

   ：

   - 录音和播放需要不同的信号处理链路。

------

### **常见问题**

1. `playback.pcm` 或 `capture.pcm` 未定义时

   ：

   - 如果没有指定，可能会导致音频路径不可用或默认使用硬件设备。

2. 性能问题

   ：

   - 如果播放和录音的设备同步性要求较高，可能需要进一步优化缓冲设置。

------

### **推荐实践**

- 确保 `playback.pcm` 和 `capture.pcm` 的设备定义符合实际硬件。

- 通过 

  ```
  aplay
  ```

   和 

  ```
  arecord
  ```

   测试播放和录音路径是否正常：

  ```bash
  aplay -D plug:default test.wav
  arecord -D plug:default -f cd test_capture.wav
  ```

## dsnoop

dsnoop是d + snoop（探听）。

**跟dmix类似，只不过dmix用在播放上，而dsnoop用在录音上。**

d表示：direct。

arecord -L，查看树莓派。

有一行是这样的打印的：

```
dsnoop:CARD=CAMERA,DEV=0
    USB2.0 PC CAMERA, USB Audio
    Direct sample snooping device
```

https://alsa.opensrc.org/Dsnoop

这样来使用：

```
arecord -f cd -c 2 -D dsnoop foobar.wav
```





## hw

这种插件是直接跟alsa的kernel 驱动通信。

这个一个raw的通信，没有任何转换。



## dmix

```
pcm.card0 {
	type hw
	card 0
}
pcm.!default {
	type plug
	slave.pcm "dmixer"
}

pcm.dmixer {
	type dmix
	ipc_key 1025
	slave {
		pcm "hw:0,0"
		period_time 0
		period_size 4096
		buffer_size 16384
		periods 128
		rate 44100
	}
	bindings {
		0 0 
		1 1
	}
}
```





播放增益设置

录音声道转换



数字音频有几个参数是我们需要关注的：

采样率、通道数、格式。

如果你用过oss编程。你可能是在播放某个文件前，一个一个设置过这些参数。

在alsa里，你会碰到一个概念：Configuration space。配置空间。

这个具体指什么呢？

这个产生的原因是：现实中声卡差别比较大，事情就变得复杂了。

参数不是独立的。

alsa通过一个多维度的参数集来描述。

其中一个维度对应采样率，一个维度对应格式，等等。



alsa设备，是各种插件的wrapper。

alsa设备由字符串来描述。

设备是在配置文件里定义的。

很多alsa设备是通用的。

alsa设备列表跟插件列表不一样。

毫不夸张地说，alsa完全是由插件构成的。

每当播放器或者其他程序使用alsa设备的时候，是插件来完成实际的工作。



**最重要的插件就是hw插件。**

**它不进行自己的处理，而只是访问硬件驱动程序。**

hw插件的用法：

```
-D hw:0,0
```



如果使用hw插件时，给定的参数，是硬件所不支持的，则hw插件会返回错误。



**所以下一个最重要的插件是plug插件。plug插件会进行通道复制、格式转化和重采样。**

用法是：

```
-D plughw:0,0
```

另外一个非常有用的插件是file插件。

常见的用法是：

```
aplay -D tee:\'plughw:0,0\',/tmp/1.out,raw 1.wav
```

可以在听到声音的同时，把播放的声音保存起来。



snd_open的时候，都会重新解析配置文件，所以修改配置文件后，程序执行你的程序，就可以生效的。



# 播放设备名

default：对于大部分应用，用这个就够了。一般使用pulseaudio或者dmix。这样就可以多个应用同时使用声卡了。

front：直接访问硬件，模拟输出。2个通道。通道图：front-left、front-right。

rear：单词意思是后面，跟front相对。直接访问硬件。模拟输出。2个通道。通道图：rear-left、rear-right。

center_lfe：

side

surround40：4个通道。front-left、front-right、rear-left、rear-right。

spdif

hdmi

hw

plughw



设备名前面可以加上`plug:`

例如：

```
plug:front
```

作用是实现参数转化。



# 录音设备名

default 

hw



# alsa.conf文件分析

```
@hooks [ # 这个是默认就会调用的。是一个数组，里面可以有多个对象。
		# 对应的代码函数是：snd_config_hook_load_for_all_cards
	{ # 当前只放了一个对象。
		func load
	}
]
```



```
aplay -D"plug:'dmix:RATE=44100'" <filename>

aplay -Dplug:\'dmix:SLAVE=\"hw:1,0\",RATE=44100\' <filename>

aplay -D"plug:'dmix:FORMAT=S32_LE'" <filename>
```

# 一个比较复杂的例子

https://unix.stackexchange.com/questions/511175/using-and-configuring-alsa-plugins-dmix-and-dsnoop-for-stereo-play-and-capture

这个例子是要实现一个比较复杂的输入输出。

```
I installed a new PCI based soundcard in my PC. It has 8 S/PDIF based I/O pairs with each line numbered 1 to 8 for input as well as output. And I'm trying to use lines 3-8 for input (mics) and 3-8 for output (play) in stereo with :

line 3 + line 4 = channel 1 (both input and output),
line 5 + line 6 = channel 2 (both input and output),
line 7 + line 8 = channel 3 (both input and output).
```

但是没有看到最终解决的。

# 一份比较好的文档

https://vovkos.github.io/doxyrest/samples/alsa/page_pcm_plugins.html

# route插件

`type route` 是 ALSA 的一个插件，用于重映射音频通道和调整信号流的音量比例。它允许灵活地将输入音频通道映射到输出音频通道，并可通过变换矩阵（`ttable`）定义通道之间的关系。

------

### **作用**

1. **通道重映射**：将输入通道的音频分配到不同的输出通道。
2. **音量调节**：通过 `ttable` 调整输入信号传递到输出通道的音量比例。
3. **音频路由**：在需要从多通道音频中选取部分通道或重新组合时非常有用。

------

### **语法**

```plaintext
pcm.route_example {
    type route
    slave.pcm "target_device"  # 目标设备
    slave.channels N          # 目标设备的通道数
    ttable {                  # 通道映射表
        0.0 1.0  # 输入通道 0 映射到输出通道 0，音量为 1.0
        0.1 0.5  # 输入通道 0 映射到输出通道 1，音量为 0.5
        1.0 1.0  # 输入通道 1 映射到输出通道 0，音量为 1.0
    }
}
```

#### **关键字段**

- `slave.pcm`：指定路由的目标设备。

- `slave.channels`：指定目标设备的通道数。

- ```
  ttable
  ```

  （通道映射表）：

  - 定义输入通道到输出通道的映射关系和音量比例。
  - 格式：`输入通道.输出通道 音量比例`。

------

### **当前配置中的应用**

```plaintext
pcm.stereo2quad {
  type route
  slave.pcm "quad"
  ttable [
    [ 1 0 1 0 ]  # 左声道 (输入通道 0) 映射到前左和后左 (输出通道 0 和 2)
    [ 0 1 0 1 ]  # 右声道 (输入通道 1) 映射到前右和后右 (输出通道 1 和 3)
  ]
}
```

#### 解读：

- **目标设备**：`quad`（一个四通道混合设备）。

- 映射逻辑

  ：

  - 左声道（输入通道 0）：
    - 输出到前左（通道 0），音量为 1。
    - 输出到后左（通道 2），音量为 1。
  - 右声道（输入通道 1）：
    - 输出到前右（通道 1），音量为 1。
    - 输出到后右（通道 3），音量为 1。

------

### **应用场景**

1. 立体声扩展为四声道或更多

   ：

   - 如家庭影院系统，需将左右声道复制到后置扬声器。

2. 音频信号分配

   ：

   - 将输入信号同时传递到多个输出设备。

3. 自定义通道映射

   ：

   - 某些硬件布局或应用需求需要特定的通道顺序。

------

### **常见问题**

1. 音量比例问题

   ：

   - 如果 `ttable` 中的比例设置不当，可能导致音量不均或过大/过小。

2. 通道数不匹配

   ：

   - 如果输入通道数或目标设备通道数配置错误，会导致设备无法工作。

------

### **推荐实践**

1. 确保目标设备支持所需的通道数，使用 

   ```
   speaker-test
   ```

    验证：

   ```bash
   speaker-test -D quad -c 4
   ```

2. 逐步调试 `ttable` 的映射关系，确保音频路由符合预期。

3. 测试完整路由链，验证从输入到输出的所有映射是否正常：

   ```bash
   aplay -D plug:stereo2quad test.wav
   ```



# dsnoop插件

`dsnoop` 是 ALSA 的一个插件，

用于捕获音频输入（录音）时

支持多个应用程序同时访问同一个音频输入设备。

通常情况下，直接访问硬件设备（如 `hw:0,0`）是独占的，

但通过 `dsnoop` 插件可以实现音频输入的共享。

------

### **dsnoop 插件的特点**

1. **多程序共享**：允许多个应用程序同时从同一音频输入设备录音。
2. **缓冲区管理**：通过内部缓冲区同步多个客户端，避免因采样速率或缓冲区大小不同引发冲突。
3. **透明性**：应用程序通过 `dsnoop` 访问设备，无需知道底层实现。

------

### **基本配置示例**

以下是一个典型的 `dsnoop` 配置：

```plaintext
pcm.dsnoop {
    type dsnoop
    ipc_key 2048
    ipc_perm 0666
    slave {
        pcm "hw:0,0"
        channels 2
        rate 44100
        period_size 1024
        buffer_size 4096
    }
}
```

------

### **配置解读**

| 配置项         | 说明                                                        |
| -------------- | ----------------------------------------------------------- |
| `type dsnoop`  | 指定插件类型为 `dsnoop`，实现音频输入的共享。               |
| `ipc_key`      | 共享内存的唯一标识符，用于不同客户端之间的通信。            |
| `ipc_perm`     | 设置 IPC（进程间通信）的权限，`0666` 表示所有用户均可访问。 |
| `slave`        | 定义底层设备的参数。                                        |
| `pcm "hw:0,0"` | 底层音频输入设备（如声卡的麦克风通道）。                    |
| `channels 2`   | 输入通道数量（通常为立体声，2 个通道）。                    |
| `rate 44100`   | 采样率（如 44100Hz）。                                      |
| `period_size`  | 指定单个音频缓冲区的大小（以帧为单位）。                    |
| `buffer_size`  | 设置总缓冲区大小（应是 `period_size` 的整数倍）。           |

------

### **应用场景**

1. **多程序同时录音**：
   - 例如，需要同时运行一个实时语音处理程序和一个录音程序。
   - 默认情况下，硬件设备是独占的，无法被多个程序同时访问，`dsnoop` 解决了这一问题。
2. **音频监控**：
   - 一边录制音频，一边对音频进行实时分析或监控。

------

### **使用方法**

#### **1. 配置文件中定义 `dsnoop` 设备**

在 `/etc/asound.conf` 或 `~/.asoundrc` 中添加上述配置。

#### **2. 指定 `dsnoop` 设备录音**

通过应用程序使用 `dsnoop` 设备，例如：

```bash
arecord -D dsnoop -f cd test.wav
```

- `-D dsnoop`：指定设备为 `dsnoop`。
- `-f cd`：指定音频格式为 CD（16 位、44.1kHz、立体声）。

#### **3. 默认录音设备**

将 `dsnoop` 设置为默认设备：

```plaintext
pcm.!default {
    type plug
    slave.pcm "dsnoop"
}
```

这样可以让所有录音程序自动使用 `dsnoop`，无需手动指定。

------

### **常见问题**

1. **音频延迟**

   - `dsnoop` 插件引入了缓冲区，可能会导致轻微的音频延迟。
   - 可以尝试调整 `period_size` 和 `buffer_size` 的大小，减小延迟。

2. **参数不兼容**

   - 如果底层设备不支持指定的采样率或通道数，可能会报错。

   - 建议在 

     ```
     slave
     ```

      中使用 

     ```
     plug
     ```

      插件：

     ```plaintext
     slave.pcm "plughw:0,0"
     ```

3. **设备被占用**

   - 如果底层设备被独占（如另一个程序未通过 `dsnoop` 而直接访问设备），可能会导致 `dsnoop` 无法工作。

------

### **总结**

- **功能**：`dsnoop` 实现了音频输入设备的多应用共享，适用于同时录音或实时处理场景。
- **配置灵活**：通过调整缓冲区大小和其他参数，可以适配不同的需求。
- **使用简便**：通过指定 `dsnoop` 设备或将其设为默认设备即可透明使用。

# 参考资料

1、asound.conf配置

https://blog.csdn.net/zhangxu365/article/details/8449118

2、官方配置文件说明

http://www.alsa-project.org/main/index.php/Asoundrc

3、

https://wiki.archlinux.org/index.php/Advanced_Linux_Sound_Architecture_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

4、理解和使用Alsa的配置文件

https://blog.csdn.net/colorant/article/details/2598815

5、

http://www.voidcn.com/article/p-dsamalpt-bht.html

6、Linux ALSA 音频系统：逻辑设备篇

https://blog.csdn.net/zyuanyun/article/details/59180272

7、深入了解ALSA

https://blog.csdn.net/kickxxx/article/details/8291598

8、

https://blog.csdn.net/MyArrow/article/details/8230231?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task

9、

https://www.alsa-project.org/wiki/Asoundrc

10、Flask与pyaudio实现音频数据流的传输(电话会议语音交互式应用)

https://blog.csdn.net/weixin_30699831/article/details/99924273

11、alsa设置默认声卡

https://blog.csdn.net/samssm/article/details/53157210

12、alsa-lib的alsa.conf

https://www.pianshen.com/article/684731740/

13、alsa

https://www.volkerschatz.com/noise/alsa.html

14、DeviceNames

https://alsa-project.org/wiki/DeviceNames

15、ALSA子系统（二）------PCM (digital audio) plugins

这篇文章不错。

https://blog.csdn.net/Guet_Kite/article/details/108124585