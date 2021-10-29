---
title: 树莓派pico了解
date: 2021-10-29 11:35:25
tags:
	- 树莓派

---

--

Raspberry Pi Pico SDK（以下简称 SDK）

提供了使用 C、C++ 或汇编语言为基于 RP2040 的设备（例如 Raspberry Pi Pico）

编写程序所需的头文件、库和构建系统。

SDK 旨在提供非嵌入式 C 开发人员和嵌入式 C 开发人员都熟悉的 API 和编程环境。

一个程序以传统的 main() 方法启动。

支持标准 C/C++ 库以及 C 级库/API，用于访问 RP2040 的所有硬件，包括 PIO（可编程 IO）。

此外，SDK 提供了用于处理定时器、同步、USB (TinyUSB) 和多核编程以及各种实用程序的更高级别的库。

SDK 可用于构建任何东西，从简单的应用程序到成熟的运行时环境（如 MicroPython），再到低级软件（如 RP2040 的片上 bootrom 本身）。

尚未准备好包含在 SDK 中的其他库/API 可以在 pico-extras 中找到



Raspberry Pi Pico是具有灵活数字接口的低成本，高性能微控制器板。

它集成了Raspberry Pi自己的RP2040微控制器芯片，

运行速度高达133 MHz的双核Arm Cortex M0 +处理器，

嵌入式264KB SRAM和2MB板载闪存以及26个多功能GPIO引脚。

对于软件开发，可以使用Raspberry Pi的C / C ++ SDK或MicroPython。





参考资料

1、sdk

https://github.com/raspberrypi/pico-sdk

2、官方文档

https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

3、

https://blog.csdn.net/weixin_40330033/article/details/117430765