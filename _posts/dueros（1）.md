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







#参考资料

1、这里有些基本教程。

https://dueros.baidu.com/didp/news/technicalclass

2、

https://baike.baidu.com/item/DuerOS/20369004?fr=aladdin

3、听清、听懂、满足：DuerOS 整体架构最全解剖

https://www.leiphone.com/news/201707/UD9mEB4sooFYx3Ml.html

4、DuerOS轻量级设备解决方案，让机器对话就这么简单

http://baijiahao.baidu.com/s?id=1577897914444654794&wfr=spider&for=pc