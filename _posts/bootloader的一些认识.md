---
title: bootloader的一些认识
date: 2018-04-16 16:42:33
tags:
	- bootloader

---



我以前做单片机开发，完全没有bootloader这个概念。

后面做linux开发，用的bootloader一直是uboot。

现在看esp8266的板子。这里也有bootloader的概念在。

要在bootloader里，做到这些：
1、初始化flash，提供读写接口。
2、初始化串口，从CH340接收数据。

如果有jtag，可以不依赖软件，就完成数据传输和写入的操作。

我以前的单片机开发就是这个。

esp8266的bootloader的固化了的。一般不让改。有bootloader，就可以不用jtag来辅助开发，下载程序就方便很多。



