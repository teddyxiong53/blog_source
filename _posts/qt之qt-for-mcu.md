---
title: qt之qt-for-mcu
date: 2021-06-09 10:02:11
tags:
	- qt

---

--

Qt for MCU 将能够在没有操作系统的设备上运行，

允许开发人员在具有成本效益的单片机上创建流畅的用户界面，

基于 Qt 的应用程序现在可以部署在运行传统操作系统的系统以及基于 ARM Cortex M7 的微控制器上。



**Qt for MCU 是如何实现的呢？答案是 Qt Quick。**

Qt Quick 是一个用于开发移动应用程序的框架，其核心是 QML，它是一种用于描述用户界面的声明性语言。从语法上看，它有一种 JSON 感觉，低开销运行时使 QML GUI 能够与后端 C/C++ 代码绑定，使 GUI 可以跨多个平台进行移植。

Qt for MCU 应用程序是使用新的运行时呈现的，

该运行时提供高性能和低内存消耗。

这是通过一个新的 QML 到 C++ 的转换，

再加上一个新的声明性属性绑定引擎来实现的。

此外，新的运行时允许应用程序在没有操作系统的情况下直接在处理器上运行，被称为“在裸金属上运行”。

还可以使用标准 Qt 库在运行 Linux、Windows 等操作系统的功能更强大的设备上部署应用程序。

![img](../images/random_name/aHR0cHM6Ly9pbWcuaXRob21lLmNvbS9uZXdzdXBsb2FkZmlsZXMvMjAxOS84LzIwMTkwODI2MjE1ODM5XzYxOTIuanBn)

**Qt for MCU 硬件兼容性**

目前，Qt for MCU 是专门为 ARM Cortex-M 单片机开发的，具有有限的测试硬件平台，如下所述：

- [STM32F769i-DISCO](https://www.cnx-software.com/2016/06/01/stmicro-unveils-two-low-cost-stm32f7-arm-cortex-m7-development-boards/#32f746g-discovery-board)
- STM32F7508-DK
- I.MX RT1050-EVKB
- Renesas RH850



参考资料

1、Qt宣布新工具包 Qt for MCU，支持单片机

https://blog.csdn.net/z609932088/article/details/100094650