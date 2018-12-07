---
title: ama（1）
date: 2018-11-27 17:50:35
tags:
	- 智能音箱
typora-root-url: ..\
---



ama是Amazon Mobile Accessory的缩写。是智能音箱的衍生产品。

是基于蓝牙的，和手机配合使用。

具体的产品形态可以是车载手机支架，可以方便地进行语音导航、播放歌曲等操作。

还可以是耳机。

目前网上还是只能搜索到一些新闻。

小米的小爱蓝牙音箱就是这种类型的产品。

这个要2018年11月28日才开始卖。

主要操作逻辑是：

1、2个按键，一个电源键，一个语音键。

长按电源键2秒，开关机。

如果机器里没有配对信息，则开机后，自动进入到配对状态。

也可以在关机状态下，长按电源键6秒，强制进入到配对状态。

短按语音键：

唤醒小爱同学。



# AMA要求的蓝牙规格

1、蓝牙4.2以上。

2、标准的配对，授权，连接码，加密。

3、支持spp、A2DP、HFP、SDP、RFCOMM，SCO

# AMA的编码支持

支持：

1、opus。

2、mSBC。

# AMA的构成

由3个部分构成：

1、手机app。亚马逊官网提供一个。

2、一个第三方厂家的音箱（或者耳机等）。

3、第三方厂家的手机app。

框图是这样的：

![](/images/AMA框图.png)



使用步骤是：

1、用oem厂家的app，通过ble跟音箱配对。

2、亚马逊app通过SDP（Service Discovery Protocol）通过经典蓝牙连接到音箱。

3、

#参考资料

1、小米官网

https://www.mi.com/sound-carry/specs/

2、亚马逊官网资料

https://developer.amazon.com/zh/docs/ama-kit/alexa-mobile-accessory-kit-overview.html

