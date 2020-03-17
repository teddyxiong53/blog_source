---
title: 音频之aux接口
date: 2020-03-16 09:48:11
tags:
	- 音频
---

1

aux是auxiliary的缩写。这个单词的意思是辅助的意思。

表示一种音频输入接口。

在一般的音响设备上，除了正常的输入输出接口外，通常还会配备几个标有aux的**输出入端口**。

是用来做预备的接续端。

当你有特别的需求，例如要做额外的声音输入和输出时，就可以使用aux端口。

简单来说，就是你有一个手机，希望用音箱来输出这个声音，就拿一个两头都的3.5mm耳机接口的线，把手机跟音箱的aux口连接起来就行了。



一般aux就是line in，最好接其他设备的line out(LO口）

line in对应的就是line out，**一般传输的是没有经过放大的模拟信号**

aux，音频输入接口。

**一般用在车上，接受模拟信号，放大过的没放大过的都可以。**

可以耳机口3.5线直接aux接，高级点的播放器有line out 直接aux接也可以。

一般随身听只有放大后的模拟信号，就是耳机口，专业点的有单独的line out 口



amixer，是alsamixer的文本模式,即命令行模式，需要用amixer命令的形式去配置你的声卡的各个选项，

可以这么说，你也许会直接修改Linux内核音频驱动源码来满足您的需求，比如选择音频输入通道是Mic输入，还是Line 输入，需要修改WM9714的寄存器来决定，

而amixer可以从应用层来修改音频芯片的寄存器值，决定采用Mic输入或者Line输入。

这样就大大简化了代码修改的难度，毕竟比直接修改Linux Kernel ALSA会简单些。






这里使用的是Ubuntu12.04的Line-in功能(实现立体声功能):



参考资料

1、AUX接口

https://baike.baidu.com/item/AUX%E6%8E%A5%E5%8F%A3

2、

https://jingyan.baidu.com/article/219f4bf70dde589e442d38f0.html

3、AUX和line in什么区别？

http://www.erji.net/forum.php?mod=viewthread&tid=1992296&page=1

4、ALSA --- amixer控制声卡驱动实现Line-in功能

https://blog.csdn.net/yimiyangguang1314/article/details/7755815