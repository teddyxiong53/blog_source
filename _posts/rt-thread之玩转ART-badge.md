---
title: rt-thread之玩转ART-badge
date: 2021-12-19 16:48:25
tags:
	- rt-thread

---

--

最近参加rt-thread开发者大会，大会给每个参会者发了一个ART badge作为身份卡，这个实际是一个电路板，带一个小的显示屏。主控芯片是Realtek的。运行的rt-thread的系统。

屏幕开机后显示2个二维码：一个是小程序二维码，一个是普通二维码（用来扫描获取蓝牙名字的）。

带来一个300mAh的电池供电，有micro usb口可以进行充电，续航8个小时没有问题。够一天的会议使用了。

现在会议已经结束，这个牌子显示的信息就没有什么意义了。那么就可以看看能够做什么好玩的东西。

他们的微信小程序上有加QQ群的连接，qq群是：178686826

从芯片的丝印看，是RTL8762DW。群里倒是有一些手册。

板子是丝印来看，是使用的柿饼UI。

显示屏的型号是TFT9K1884FPC-A1-E

先看看当前的rt-thread里有没有对应个bsp代码。

代码在这里

https://github.com/ART-Badge

网站在这里

https://art-badge.github.io/website/#/

反正是可以自己进行开发的。

我可以把它改成自己的名片。

RTL8762D作为主控芯片，MCU主频为90MHZ，运行RT-Thread 操作系统，并整体使用睿赛德科技的湃心穿戴OS，外扩了8M的PSRAM，以及16M的片外flash 。

ART-Badge主要使用到串口（用于调试和控制台输出），GPIO（用于驱动按键、蜂鸣器和ADC采集），I2C接口（用于和板载的 SC7A20 三轴加速度传感器通信）。

底板的PCB采用2层Layout。板载的IC主要有：

- 半反半透明屏幕，分辨率 240 X 240，颜色格式 RGB565，在关闭背光的情况下依旧能有出色的可视度。
- APS6404L-3SQR，PSRAM（动态随机存取存储器），用于动态加载图形资源，8M的容量十分富裕。
- ch340e，USB转串口芯片，也很常用，通过 USB 线把 ART-Badge 连接电脑之后，就可以直接用串口控制台使用shell了，后面的二次开发也是使用到了串口工具 UDB 下载。
- BS814A-1，电容触摸 IC，用于 ART-Badge 正面的按键交互。
- SC7A20，士兰微出的一款高精度12bit数字三轴加速度传感器芯片，内置功能丰富，功耗低，体积小，测量精确。

硬件搞定之后就开始**移植软件**啦，ART-Badge 运行的是基于RT-Thread 的湃心穿戴OS。

这里科普一下 湃心穿戴OS，它是一个超轻量级、已量产的产品级穿戴操作系统平台。中间层的模块包括 GUI 引擎、通讯组件、NFC、存储类工具等。中上层是由 JavaScript 搭建的应用程序框架，最上层则是轻量级系列众多的小程序。



参考资料

1、开源一个电子胸牌项目，很棒！

这个是2020年的版本。

https://www.eet-china.com/mp/a96505.html