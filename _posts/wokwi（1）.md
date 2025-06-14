---
title: wokwi（1）
date: 2023-05-28 20:55:11
tags:
	- 嵌入式
---

--

在问chatgpt有哪些开源的智能手表os的时候，发现了wokwi这个公司。

发现他们有做不少有意思的东西。

# wokwi公司

Wokwi 是一个开发硬件仿真和教育工具的公司。他们的目标是为硬件开发者和教育工作者提供创新的虚拟仿真环境，使他们能够更轻松地设计、调试和教授硬件系统。

Wokwi 公司创建了一系列基于 Web 的硬件仿真器和模拟器，以帮助开发者和学生进行实验、学习和测试。他们的仿真器库包括 AVR8js 和 RP2040js，用于模拟 AVR 微控制器和 Raspberry Pi RP2040 微控制器。

这些仿真器库提供了一种交互式的仿真环境，通过 Web 浏览器就可以进行硬件系统的仿真和调试。它们支持实时执行指令、观察和修改寄存器和内存状态，以及与外部设备进行交互，从而提供了一个真实且易于使用的硬件开发平台。

Wokwi 的仿真器库广泛应用于教育领域，为学生提供了一个无需实际硬件的实验环境，使他们能够学习和实践电子和嵌入式系统的设计与编程。此外，开发者也可以利用这些仿真器库来加速原型开发、调试代码和验证硬件设计。

Wokwi 的仿真器库是开源的，其源代码可在 GitHub 上找到。除了开源项目外，Wokwi 还提供了一些额外的高级功能和工具，用于商业和教育用途。

通过提供创新的硬件仿真解决方案，Wokwi 公司致力于推动硬件开发和教育领域的进步，并为开发者和学生带来更好的学习和开发体验。

# avs8js

avr8js 是一个基于 JavaScript 的 AVR 8 位微控制器仿真器库。

它允许开发者使用 JavaScript 来模拟 AVR 微控制器的行为，

并且可以在 Web 浏览器中进行仿真和调试。

该库提供了一组功能强大的 API，

使得开发者可以创建 AVR 微控制器的虚拟实例，

并对其进行编程和仿真。

它支持模拟多种常见的 AVR 微控制器型号，如 ATmega328P、ATmega2560 等。

avr8js 提供了一个交互式的仿真环境，

可以实时执行 AVR 微控制器的指令，

并且可以观察和修改寄存器、内存以及其他外设的状态。

它还提供了断点调试功能，

使得开发者可以在特定的代码行上设置断点，并逐步调试程序执行过程。



此外，avr8js 还提供了一个简单易用的图形用户界面，

使得开发者可以直观地观察和修改 I/O 引脚的状态，

从而模拟外部设备与 AVR 微控制器的交互。



通过将 avr8js 集成到 Web 应用程序或在线教育工具中，

开发者可以创建 AVR 微控制器的虚拟实验环境，

从而提供一种交互式的学习和开发平台。

该库还支持与其他 JavaScript 库和框架的集成，使得开发者可以更进一步扩展和定制仿真环境。

你可以在 avr8js 的 GitHub 仓库中找到更多关于该库的详细信息、示例代码和文档：[https://github.com/wokwi/avr8js](https://github.com/wokwi/avr8js)

# rp2040js



rp2040js 是一个基于 JavaScript 的 Raspberry Pi RP2040 微控制器仿真器库。它允许开发者使用 JavaScript 来模拟 RP2040 微控制器的行为，并在 Web 浏览器中进行仿真和调试。

这个库提供了一组功能强大的 API，使开发者可以创建 RP2040 微控制器的虚拟实例，并对其进行编程和仿真。它模拟了 RP2040 的核心功能，包括 GPIO、UART、SPI、I2C、PWM 和时钟等外设，以及内置的 ARM Cortex-M0+ 处理器。

rp2040js 提供了一个交互式的仿真环境，可以实时执行 RP2040 微控制器的指令，并观察和修改寄存器、内存以及其他外设的状态。它还支持断点调试功能，允许开发者在代码的特定行上设置断点，并逐步调试程序执行过程。

该库还提供了一个简单易用的图形用户界面，使开发者可以直观地观察和修改 GPIO 引脚的状态，模拟外部设备与 RP2040 微控制器的交互。

通过将 rp2040js 集成到 Web 应用程序或在线教育工具中，开发者可以创建 RP2040 微控制器的虚拟实验环境，提供一种交互式的学习和开发平台。该库还支持与其他 JavaScript 库和框架的集成，使开发者能够进一步扩展和定制仿真环境。

你可以在 rp2040js 的 GitHub 仓库中找到更多关于该库的详细信息、示例代码和文档：[https://github.com/wokwi/rp2040js](https://github.com/wokwi/rp2040js)

# Wokwi GDB Server

https://github.com/wokwi/wokwi-gdbserver

# rp2040js-circuitpython

https://github.com/wokwi/rp2040js-circuitpython

Raspberry Pi Pico 模拟器上的一个简单的 CircuitPython，构建在 rp2040js 库之上。

您可以使用此模拟器在您的计算机上运行 CircuitPython 的发布固件，即使您无法访问物理硬件。您可以将其用于自动化测试（例如在 CI 环境中），以及用于教育目的。

如果您正在寻找一个成熟的、用户友好的 CircuitPython 模拟器，请查看 Wokwi：在 Wokwi 上启动一个新的 CircuitPython 项目。

# 支持的硬件

## mcu

avr

esp32

stm32

rp2040

## sensor





https://wokwi.com/projects/356530577106394113



# 自己定制一个芯片

https://wokwi.com/projects/429751083103298561

参考这个教程写的：https://docs.google.com/document/u/0/d/1wM7MTHtDus0j7P3BcJ_VE-ZeElnK84arpiW3qVIg0S4/mobilebasic?pli=1&tab=t.0&_immersive_translate_auto_translate=1#heading=h.kf24or4t82pq



https://stackblitz.com/edit/avr8js-minimal?file=index.ts

# 参考资料

1、

https://docs.wokwi.com/zh-CN/