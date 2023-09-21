---
title: zig之microzig
date: 2023-09-15 18:47:11
tags:
	- zig
---

--

仓库在这里：

https://github.com/ZigEmbeddedGroup/microzig

这个是直接用zig来写单片机程序。

这个是在rp2040上跑的。

https://github.com/ZigEmbeddedGroup/raspberrypi-rp2040

我觉得还是从单片机的开发这个角度，更加方便我去对比zig和c的区别。

这个是blinky闪灯的示例程序。

https://github.com/ZigEmbeddedGroup/raspberrypi-rp2040/blob/main/examples/blinky.zig

看起来也是比较直观简洁的。

这个是microzig的创始人的网站。

https://sycl.it/agenda/workshops/intro-to-zig-on-embedded/

强大的错误处理、编译时间和显式内存分配都使 Zig 成为创建嵌入式应用程序的出色工具。 

Felix 和 Matt 是 Zig Embedded Group 的创始人，致力于开发 MicroZig，

这是一个为您设置微控制器编程的所有先决条件的框架。

在本课程中，您将了解如何设置嵌入式 Zig 开发环境以及使用模拟和数字信号控制伺服电机。

在我们的会议期间，我们将简要介绍：

- Electronic Circuits
- Hardware Interrupts
- Programming and Debugging hardware
- Bootloaders
- Debugging techniques
- Peripherals:
  - General Purpose Input Output (GPIO)
  - Analog-to-Digital converter (ADC)
  - Pulse-Width Modulation (PWM)