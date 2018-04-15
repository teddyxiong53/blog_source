---
title: arduino（一）
date: 2018-04-14 11:01:39
tags:
	- arduino

---



很早就听说了arduino，但是以前看网上总是说，技术含量不高。不如树莓派。

所以就一直没有考虑入手arduino。

但是我最近看youtube上的视频，很多的视频都是用arduino在做东西。我觉得arduino很有意思。

我自己在电子制作方便非常欠缺，也是希望从arduino入手，提高自己电子制作的能力。可以做出一些有意思的设备出来。



#如何购买

既然要入手，那么第一个问题就是，到哪里买。

我先到arduino的论坛上看看情况。

https://www.arduino.cn/thread-6513-1-1.html

这篇文章说了，价格相差非常大。因为arduino的电路的确不复杂，所以其实是可以自己做的。

但是我觉得我还是先用现成的，熟练之后，再考虑自己做一个。

而且如果用便宜的非官方版本，成本应该比自己做还要低一些。

https://openjumper.taobao.com/?v=1

这个是官方授权的店。我不买。但是这里很全。我们可以看看有哪些有意思的配件。

我看卖得不多，对这个感兴趣的，大部分都清楚行情，没那么容易上当。

http://www.zaixinjian.com/index

这个网站似乎不错。

# 选型

我发现还是需要先对arduino的型号做一个梳理。

官方就有十几款，淘宝上有很多非官方的。

选择的原则有：

1、性能。

2、特性。

3、尺寸。

arduino是来自意大利的项目，所以命名有很多意大利风格。



## Uno

处理器：atmega 328， 8位的CPU，16M的主频，2K ram，32K flash。

gpio：14个。6个adc。

价格：30刀。（抢钱啊。树莓派才35刀）。

uno这个名字是个拉丁文，表示第一的意思。最适合初学者上手的。

兼容性是最好的。CPU是两排针脚的封装，可以很容易更换。

## Leonardo

我就认为这个名字是表示达芬奇吧。

处理器：atmega32u4， 8位，16M主频，2.5Kram，32K flash。

价格：25刀。

是uno的小升级。

板子支持usb，可以模拟成鼠标和键盘。

## Due

处理器：atmel SAM3X8E Cortex M3的，32位，84M主频，96K ram，512K Flash。

支持usb。

价格50刀。还是贵。

这个有个问题，就是电压是3.3V的，之前的都是5V的。导致扩展板的兼容问题。要注意。

## Micro

跟Leonardo差不多。就是尺寸更小。

##Esplora

这个是意大利语。表示探索。

跟Leonardo差不多。增加了一些外设。

## Yun

这个是中文拼音了。就是云的拼音。表示的就是物联网相关。

主芯片是8位单片机，但是上面集成了一个AR9331芯片，这个很厉害，里面带了一个openwrt的系统。

AR9331是Atheros的芯片。mips架构，400M主频。

https://wikidevi.com/wiki/Atheros_AR9331

价格65刀。

## Robot

2颗8位单片机。

带显示屏，有轮子。

价格到了275刀。



这么看下来，感觉就是贵贵贵。很贵。

我先看Uno的电路图看看。

找一下便宜货。

这个叫WeMos D1的板子，是arduino Uno兼容的。带ESP8266 WiFi芯片的。

https://item.taobao.com/item.htm?spm=a230r.1.14.20.43fb6558DyZN84&id=525088572403&ns=1&abbucket=3#detail



# wemos D1

看看这个板子的详细信息。我觉的如果没有特别的不好的地方，就选择这个了。

公司官网在这里：https://www.wemos.cc/

https://github.com/wemos

github上提供了不少的参考程序。



乐鑫又推出了新的ESP32，比ESP8266要强大。



NodeMCU又是个什么鬼？是基于ESP的一块板子。

官网在这：

http://www.nodemcu.com/index_cn.html

nodemcu是一个开源的物联网平台。使用lua作为主要的编程语言。这个我不喜欢。

暂时不买这个，观察一下再说。

NodeMCU-32S的价格是39元。加入购物车。过段时间再买。



这个是看到的最便宜的一个。16块。深圳还免邮。不能更便宜了。反正就是一个盒饭钱。

https://item.taobao.com/item.htm?spm=a1z02.1.2016030118.d2016038.5fba782dzTMQxv&id=531755241333&scm=1007.10157.81291.100200300000000&pvid=7250a532-8e28-4b0f-b63c-e8c1eece0fc8

老板要下单才给你发链接。

ModeMcu ：**<https://pan.baidu.com/s/1hsgp3mO> 
链接：**<http://pan.baidu.com/s/1c2fJwsw> 

密码：c9t9 
Arduino IDE教程：**<http://www.windworkshop.cn/?p=758%20(%EF%BD%80%E3%83%BB%CF%89%E3%83%BB%C2%B4)> 
使用方法 **<https://www.plotcup.com/2016/11/26/nodemcu-1/> 
switch 4.1系统正式告破**<http://bbs.a9vg.com/thread-5336030-1-1.html> 
不亦的博客：**<https://so.csdn.net/so/search/s.do?q=NodeMCU&t=blog&u=leytton> 
驱动下载： **<http://pan.baidu.com/s/1qY5p6fq>



这些先放着，等板子到了再看。





# 参考资料

1、[选型指南]如何选择你的第一块Arduino?

http://mc.dfrobot.com.cn/forum.php?mod=viewthread&tid=809





