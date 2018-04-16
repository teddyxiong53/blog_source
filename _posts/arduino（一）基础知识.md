---
title: arduino（一）
date: 2018-04-14 11:01:39
tags:
	- arduino
typora-root-url: ..\
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

2018年4月15日19:30:48

板子到了。看看怎么跑起来。

![](/images/arduino（一）-esp8266正面.jpg)

![](/images/arduino（一）-esp8266背面.jpg)

可以看到，上面是自带了CH340G的usb转串口芯片的。

# 上手步骤

1、上电。

先找到资料，看看如何供电。

没有资料说明。我把usb线接到电脑上，wifi模组旁边有个蓝色灯闪了一下，电脑上弹出在安装usb转串口驱动。

我们选择跳过。

到网上搜索CH340的驱动。

我用这个。

http://www.wch.cn/download/CH341SER_EXE.html

安装很简单，就是一个INF文件。

现在我的电脑上可以看到对应的com6 了。

2、在arduino的IDE里下载一个示例程序进去。

我们打开arduino IDE。

依次点击：菜单，首选项，设置标签里的附加开发板管理器网址。输入：

```
http://arduino.esp8266.com/stable/package_esp8266com_index.json
```

然后我们点击：工具，开发板，开发板管理器，拉到最下面，看到“esp8266 by ESP8266 Community”，点击安装。

然后就会下载板子相关的内存。稍微等一下。要下载大概150M的东西。速度不快。我下载失败了2次，选择代理方式。选择ssr的方式翻墙。还是很慢。找到一个好的 ssr服务器，**我选择安装2.3版本的esp相关文件。这个下载就比较顺利。**

arduino IDE工具还是写得不够健壮。是用java写的。所以安装目录带了一个java环境，所以很大。

安装完成后，我们就可以在板子列表里看到esp8266的板子了。是在Generic ESP8266 Module下面的WeMos D1 。

3、我们现在可以下载一个sample进去了。

依次点击：文件，示例，ESP8266Wifi，wifiscan的。

然后点击：项目，编译，

然后点击：项目，上传。

```
Archiving built core (caching) in: C:\Users\Administrator\AppData\Local\Temp\arduino_cache_353064\core\core_esp8266_esp8266_d1_mini_CpuFrequency_80,UploadSpeed_921600,FlashSize_4M3M_6d0fcb228d55700a74e17ca29b8b5f72.a
项目使用了 226745 字节，占用了 (21%) 程序存储空间。最大为 1044464 字节。
全局变量使用了31952字节，(39%)的动态内存，余留49968字节局部变量。最大为81920字节。
Uploading 230896 bytes from C:\Users\Administrator\AppData\Local\Temp\arduino_build_901449/WiFiScan.ino.bin to flash at 0x00000000
................................................................................ [ 35% ]
................................................................................ [ 70% ]
..................................................................               [ 100% ]
```

然后点击arduino ide的右上角的串口监视器，设置波特率为115200，然后就可以看到对应的串口6上在打印扫描出来的WiFi热点的名字。

到这里了，一个基础示例就跑起来了。

#arduino程序的构成

我们看看WiFiScan这个程序的代码。

```
/*
 *  This sketch demonstrates how to scan WiFi networks. 
 *  The API is almost the same as with the WiFi Shield library, 
 *  the most obvious difference being the different file you need to include:
 */
#include "ESP8266WiFi.h"

void setup() {
  Serial.begin(115200);

  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  Serial.println("Setup done");
}

void loop() {
  Serial.println("scan start");

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0)
    Serial.println("no networks found");
  else
  {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i)
    {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE)?" ":"*");
      delay(10);
    }
  }
  Serial.println("");

  // Wait a bit before scanning again
  delay(5000);
}
```

一个arduino程序的构成非常简单，就是一个setup函数，用来初始化，一个loop函数，用来循环。

我下载的esp8266的库文件在这里：

C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0

我现在需要搞清楚，esp8266的启动过程。

我把这个目录的内容拷贝出来，建立source insight工程，先阅读一遍。需要把ino文件解析为C文件。

我还是先把WiFiScan相关文件都过一遍。

底层用到了C++，Serial，这个就是一个类。

类继承关系是这样的。

```
Print
	Stream
		HardwareSerial
```

最底层跟串口寄存器打交道的还是用C语言写的。





# 参考资料

1、[选型指南]如何选择你的第一块Arduino?

http://mc.dfrobot.com.cn/forum.php?mod=viewthread&tid=809

2、nodemcu (一) 刷固件

https://www.plotcup.com/2016/11/26/nodemcu-1/



