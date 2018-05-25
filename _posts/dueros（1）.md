---
title: dueros（1）
date: 2018-05-07 21:22:00
tags:
	- dueros
typora-root-url: ..\
---



基于dueros的设备有：

1、小度在家。

这个是百度和小鱼合作的产品。带屏幕。

唤醒词是小度小度。价格是599元。

这个是2018年3月26日发布的。



可以应用的解决方案有：

智能音箱、智能电视、智能冰箱、智能故事机、家庭机器人。



dueros整体架构

分为3大部分：

1、应用层。这个反而是对底层设备的。

2、核心层。语音识别、语音播报、屏幕显示。

3、能力层。就是各种skill。

标准版开发套件完全按照 产品级要求研发，包括 4Mic 拾音板、MTK8516 主板，Wi-Fi/BT+喇叭，终端软件为 Linux+DuerOS SDK+终端应用，它的目标是开箱即用。



开发套件轻量级的。是基于Cortex M系列新品，1秒开机，用rtos的。



dueros对话服务协议。



音箱设备的skill相当于手机的app。

dueros的sdk相当于Android SDK。

# 轻量级设备

轻量级设备是指运行FreeRTOS、mbedOS等轻量级操作系统的智能硬件，它们具有低成本、低功耗、便携式等特点，在儿童故事机、便携音箱、智能小家电等领域有广泛应用。

DuerOS轻量级设备方案为开发者提供整体的解决方案，支持快速的改造和接入。普通设备经过简单改造即可成为语音交互的智能硬件，其成本只有一碗阳春面的价格。

接入的DuerOS轻量级硬件最低标准是ARM Cortex-M3内核的MCU，主频120Mhz，Flash容量>256KB, SRAM>64KB，这些MCU通常都采用mbedOS或者FreeRTOS。目前主流的智能家居产品普遍采用的WIFI SoC芯片，例如RDA、Realtek、MTK、乐鑫等都能够支持。百度会向合作伙伴提供接DuerOS智能语音服务的SDK源代码，方便客户定制轻量级设备的各种功能。

目前设备端SDK支持mbedOS和FreeRTOS两个主流平台，APP端 SDK和open api可以支持开发者Android、IOS、Web的开发需求。

目前固件在不断迭代和优化中，当前频率两周一个小版本发布，每两个月一个大版本发布。

开发者可以通过开放平台的控制台直接对设备做OTA升级，并支持OTA发布策略的管理。可以随时支持用户的新需求。

开发者可以从哪几方面入手，参与到这一解决方案的实施中来？
个人开发者可以通过DuerOS开放平台上的链接购买RDA的Lite设备开发板，下载SDK后即可开始基于mbedOS开发（RDA芯片相关资料要通过其官方论坛获得）。

# Lite SDK

这个的demo是基于RDA的UNO 91H的板子的。

![](/images/dueros（1）-uno板子.png)

然后看代码里。

```
const unsigned int RDA_FLASH_SIZE     = 0x400000;   // Flash Size
    const unsigned int RDA_SYS_DATA_ADDR  = 0x18204000; // System Data Area, fixed size 4KB
    const unsigned int RDA_USER_DATA_ADDR = 0x18205000; // User Data Area start address
    const unsigned int RDA_USER_DATA_LENG = 0x3000;     // User Data Area Length
```

这个适合用来理解dueros的整体结构。

demo的流程：

```
1、媒体管理器初始化。
duer::MediaManager::instance().initialize();
2、连接到wifi。
s_net_stack.connect(CUSTOM_SSID, CUSTOM_PASSWD, NSAPI_SECURITY_NONE) == 0)
3、启动循环。
duer::DuerApp app;
app.start();
duer::event_loop();
```

我们看涉及到的主要数据结构。

1、MediaManager媒体管理器。

定义在duer-os-light下面的baidu_media_manager.h里。

这个class的重要方法有：play_url、set_volume。采用的是单例的模式。

2、s_net_stack

static WiFiStackInterface s_net_stack;

3、DuerApp。





智能语音系统是如何组成的？麦克风阵列、AEC、唤醒、ASR、VAD、NLU、自定义Bot是什么意思？

百度的DuerOS从开发者的角度看，是怎样的一种形态？能够提供怎样的能力？

亚马逊的AVS是什么？百度的AVS兼容协议是什么？百度的DCS协议跟前两者又有什么区别？

认证授权是什么？OAuth2.0是什么？

Http2.0是什么？为什么选择Http2.0，而不是Http1.1或Http1.0？

什么是设备发现？什么是配网？什么是登陆？

DuerOS中的长链接建立，Ping机制，Directive下发，Event上传是什么？

这个博客系列主要针对初级的开发者，一步一步的展示一个基于DuerOS平台的智能语音交互系统具体实现，在实现的过程中也会逐步解释背后的实现原理。希望能够通过这个博客系列，普通的开发者能够顺利搭建属于自己的智能语音系统。



硬件平台：树莓派3B+DuerOS阵列版

编程语言：Python



后期会从零开始搭建基于DuerOS的智能语音助手，大概会遵从如下的步骤：

智能语音系统的系统组成

DuerOS开发者个人注册

树莓派硬件环境搭建

DuerOS系统组成

OAuth2.0认证授权

DuerOS中长链接建立，Ping机制，Directive下发，Event上传

设备发现，配网，认证

自定义Bot认证
欢迎搭建提出更多的问题，我会在后续的博客中进行补充。



麦克风阵列

麦克风用来将模拟的声音信号转换为数字信号，核心器件是ADC（Analog to Digital Controller）控制器，我们在日常生活中常见的麦克风大多是单麦克风，外形如下图所示：

首先麦克风阵列具有更好的远场拾音效果，举个不太严谨的例子，使用单麦克风打电话，手机需要放在半米的范围之内，对方才能听清说话的声音；但使用麦克风阵列，手机放在3~5米的范围之内，对方也能清晰的听到语音。
其次，麦克风阵列能够获取声源的角度信息，也就是说能够辨别声音的来源，但单麦克风做不到。
所以，在大多的智能语音系统中均采用麦克风阵列，而百度的DuerOS个人开发套件使用的就是麦克风阵列（包含两个麦克风）。



最显著的缺点就是麦克风阵列的成本相比于单麦克风而言，价格会高出很多。



技术点
麦克风选型：驻极体/数字麦克风

麦克风一致性

AEC

波束合成

盲源分离
对具体的技术细节感兴趣的同学可以逐条了解下，这里就不逐一展开了。



语音唤醒

语音唤醒的常见场景就是用户使用唤醒词（如百度的“小度小度”，亚马逊的“Alex”）将设备激活。
实际上设备在通过唤醒词激活之前也是一直在工作的，设备一直在录音，并检查录音的数据中是否包含预设的唤醒词（如“小度小度”、“Alexa”），当检测到有唤醒词，设备便进入唤醒状态。
当前对于个人开发者相对友好的免费的唤醒引擎主要有：

SnowBoy (https://snowboy.kitt.ai/)

Pocketsphinx (https://cmusphinx.github.io/wiki/tutorialpocketsphinx/)

Sensory (http://www.sensory.com)
目前，百度已全资收购了KITTAI（SnowBoy是KITTAI旗下产品），建议开发者直接使用SnowBoy作为唤醒引擎，同时，SnowBoy的唤醒词训练，及唤醒引擎的集成使用也很简洁方便。



语音识别（ASR）
语音识别（ASR）简单的说就是讲语音转化为文本，目前几乎所有的语音系统都是先将语音转化为文本，然后再基于文本进行后续的语义理解和处理的。



自然语言处理（NLP/NLU）
有了语言识别（ASR）获取的文本信息，后面就进入了自然语言处理单元了，可以说这个步骤是最接近我们概念上理解的人工智能了。这个部分会从输入文本中获取用户的意图和对应的关键信息。举个例子，对应用户输入请求：“我想听周杰伦的歌”，NLU会将请求拆解成如下的结构化结果：

意图：听歌

词槽：周杰伦
有了NLU的处理结果，就可以获取用户请求的结果了。



内容召回
假设你有两个资源库，其中，一个是电影库，一个是歌曲库。当接收NLU的处理结果后，从意图（听歌）上，你可以判别用户希望从歌曲库中获取资源，从词槽（周杰伦）可以判断用户想听歌曲的类别。有了意图和词槽就能从资源库中检索到用户期望的结果，并将结果按请求的路径返回。

完整过程

下面我们将上面的各个核心部分连贯起来，想象茶几上放着一个智能音响，用户坐在两米外的沙发上，用户通过语音发出请求“小度小度”，音响的提示灯亮起指示激活状态，用户说“我想听周杰伦的歌”，稍后，音响播放周杰伦的青花瓷。

满足远场（3~5米）拾音：麦克风阵列

提示灯亮起指示设备激活：唤醒引擎

语音请求转化为文本：语音识别（ASR）

从文本中识别出意图（听歌）和词槽（周杰伦）：自然语言处理（NLU）

通过意图和词槽返回结果：内容召回



从这个地址http://open.duer.baidu.com/doc/device-devkit/intro_markdown

下载镜像问题。先烧录看看效果。



Python版本当前支持的功能。

当前版本支持功能：

- 完成OAuth 2.0认证
- 通过[Enter]键触发唤醒状态
- 通过[小度小度]触发唤醒状态
- 支持天气、百科等TTS播放功能
- 支持音乐播放功能
- 支持闹铃功能
- 云端下发Directive显示

后续会支持跟多的功能，比如，

- 接入百度的技能平台，完成自定义功能
- 接入百度的配网、配对、设备控制能力

希望大家把使用过程中遇到的问题提出来，便于后续的优化

#参考资料

1、这里有些基本教程。

https://dueros.baidu.com/didp/news/technicalclass

2、

https://baike.baidu.com/item/DuerOS/20369004?fr=aladdin

3、听清、听懂、满足：DuerOS 整体架构最全解剖

https://www.leiphone.com/news/201707/UD9mEB4sooFYx3Ml.html

4、DuerOS轻量级设备解决方案，让机器对话就这么简单

http://baijiahao.baidu.com/s?id=1577897914444654794&wfr=spider&for=pc

5、Step by Step带你玩转DuerOS - 内容目录

https://dueros.baidu.com/forum/topic/show/244800?pageNo=1