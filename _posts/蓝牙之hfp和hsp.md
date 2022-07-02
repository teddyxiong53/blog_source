---
title: 蓝牙之hfp和hsp
date: 2022-04-21 19:41:11
tags:
	- 蓝牙

---

--

一、前言
有时，我们能看到有的蓝牙产品标明支持HFP/HSP，而有的产品却只标注了支持HFP，那么HFP or HSP是什么呢？又有什么样的关系呢？

二、HSP协议
HSP（Headset Profile），耳机模式
仅实现了最基本的通话操作：接听电话、挂断电话、调节音量、声音在手机/蓝牙耳机之间切换。
1
2
三、HFP协议
HFP(Hands-free Profile)，免提模式，
是在HSP上的扩展，除了上述功能以外，还包括控制三方通话、来电拒接、耳机端来电显示等高级功能，
不过实现的方式，和用于控制的AT CMD完全不一样。

目前HFP的使用场景有车载蓝牙，耳机和PDA，定义了AG和HFP两种角色。
AG（Audio Gate）音频网关—音频设备输入输出网关；
HF（Hands Free）免提—该设备作为音频网关的远程音频输入/输出机制，并可提供若干遥控功能。

在车载蓝牙中，手机侧是AG，车载蓝牙侧是HF，在android源代码中，将AG侧称为HFP/AG，将HF侧称为HFPClient/HF。

四、总结
HFP(Hands-free Profile)和HSP（Headset Profile）都是为了实现蓝牙通话而制定的，所实现的功能都和蓝牙通话相关。基本所有的蓝牙耳机、车载蓝牙都会支持这两个协议。

在Android设计上并没有将上述两个协议分开显示，而是均表述为“手机音频”，在使用的时候优先连接HFP，只有在对方仅支持HSP或HFP连接失败的时候才会尝试连接HSP。

参考资料

1、

https://blog.csdn.net/zhanghuaishu0/article/details/107198830