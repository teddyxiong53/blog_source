---
title: 物联网之PlatformIO
date: 2018-12-22 11:26:17
tags:
	- 物联网
---

--

# 基本信息

什么是platformio？

https://platformio.org/

官网上说是：一个开源生态系统，针对物联网开发。

vscode可以集成platformio。



platformio要解决的是这样的问题：

做stm32开发，一般用Keil。

做arduino开发，用Arduino IDE。

而且这2个IDE 做得都不行。体验非常差。

另外esp32的，一般基于eclipse。

能不能把这些乱七八糟的统一为一种方式呢？

可以。platformio就是要做到这个。

# 介绍

PlatformIO（PIO）是一个开源的、跨平台的、集成式的开发平台，专注于嵌入式系统和物联网（IoT）应用程序的开发。它旨在简化嵌入式开发的复杂性，提供了一个统一的开发环境，可以用于多种不同的硬件平台和开发框架。以下是 PlatformIO 的主要特点和介绍：

1. **支持多种硬件平台：** PlatformIO 支持多种嵌入式硬件平台，包括Arduino、Raspberry Pi、ESP8266、ESP32、STM32等。这意味着您可以使用 PlatformIO 来开发多种不同硬件上的嵌入式应用程序。

2. **支持多种开发框架：** PlatformIO 提供了对多种开发框架的支持，包括Arduino、Mbed、Espressif、ST STM32等。这意味着您可以使用 PlatformIO 来开发使用不同框架的应用程序，而无需更改开发环境。

3. **跨平台：** PlatformIO 是一个跨平台的开发环境，支持 Windows、macOS 和 Linux 操作系统。这使得开发者可以在不同的操作系统上使用相同的工具。

4. **集成式开发环境：** PlatformIO 提供了一个集成式的开发环境，包括代码编辑器、代码构建、上传固件、库管理和调试工具。这使得开发过程更加流畅，并减少了不同工具之间的集成问题。

5. **强大的库管理：** PlatformIO 提供了一个强大的库管理系统，使得查找、安装和更新库变得非常容易。开发者可以方便地使用其他人创建的开源库，以加速开发过程。

6. **自动依赖解析：** PlatformIO 能够自动解析项目的依赖关系，包括库和框架，以确保构建和上传过程的顺利进行。

7. **调试支持：** PlatformIO 集成了多种调试工具，支持硬件调试器，可以用于查找和修复应用程序中的问题。

8. **嵌入式单元测试：** PlatformIO 支持嵌入式系统的单元测试，帮助开发者编写更可靠的代码。

9. **丰富的社区支持：** PlatformIO 拥有庞大的用户社区和活跃的开发团队，因此您可以轻松找到帮助和支持。

PlatformIO 是一个强大的工具，适用于嵌入式系统和物联网应用程序的开发，它使开发者能够更轻松地管理硬件和软件复杂性，加速开发过程，并提供了丰富的功能和生态系统支持。

# 发展历史

PlatformIO（PIO）的发展历史可以追溯到2014年，自那时以来，它经历了多个版本和改进，逐渐演变成为今天的嵌入式开发生态系统。以下是 PlatformIO 的主要发展历史里程碑：

1. **2014年：** PlatformIO 的初始版本问世。最初，它是一个独立的命令行工具，专注于提供更好的嵌入式开发体验。

2. **2015年：** PlatformIO 开始支持 Arduino 平台，使得使用 PlatformIO 开发 Arduino 应用变得更加方便。

3. **2016年：** PlatformIO 引入了对 Espressif ESP8266 平台的支持，这是一个流行的 Wi-Fi 模块和开发平台。这进一步扩展了 PlatformIO 的应用范围。

4. **2017年：** Espressif 的 ESP32 平台也得到了支持，将 PlatformIO 带入了更高级的嵌入式应用领域。

5. **2018年：** PlatformIO 引入了对不同嵌入式平台和框架的更广泛支持，包括 STM32、Mbed 等。这增加了 PlatformIO 的多样性和适用性。

6. **2019年：** PlatformIO 的社区开始快速扩展，吸引了更多开发者和贡献者。它成为了一个备受欢迎的开发工具，得到了更多用户的认可。

7. **2020年：** PlatformIO 4.0 发布，引入了许多新功能和改进，包括用户界面的升级、自动依赖解析、更好的库管理等。此版本增加了 PlatformIO 的易用性。

8. **2021年：** PlatformIO 继续快速发展，引入了更多硬件平台和框架的支持，以及更多的开发者工具和集成式调试支持。

PlatformIO 的发展历史充满了创新和不断改进，使得嵌入式系统的开发更加容易和高效。它的成功得益于强大的社区支持和开发团队的不断努力，成为了嵌入式开发领域的一款受欢迎的工具。这一生态系统的不断扩展也为未来的嵌入式开发提供了更多可能性。

# platformio跟keil比较

PlatformIO 和 Keil MDK（Microcontroller Development Kit）都是嵌入式系统开发的工具，但它们在很多方面有着不同的特点和应用场景。下面是它们之间的一些比较：

**1. 开发生态系统和硬件支持：**

- **PlatformIO：** PlatformIO 是一个开源工具，支持多种硬件平台和框架，包括Arduino、ESP8266、ESP32、STM32、Raspberry Pi等。它的生态系统非常广泛，适用于不同的嵌入式项目和硬件选择。

- **Keil MDK：** Keil MDK 是由ARM开发的集成开发环境，主要面向ARM Cortex-M系列微控制器。它在ARM平台上提供了高度集成的开发工具，但支持的硬件范围相对较窄。

**2. 价格和许可证：**

- **PlatformIO：** PlatformIO 是开源的，免费使用，无需付费许可证。它适用于个人开发者和小型项目。

- **Keil MDK：** Keil MDK 提供了不同版本，包括免费版本（MDK-Lite）和付费版本（MDK-Professional）。付费版本包括更多高级功能，并且在商业项目中使用时通常需要购买许可证。

**3. 可扩展性和自定义性：**

- **PlatformIO：** PlatformIO 非常灵活，可以通过插件来扩展其功能。它支持多种编程语言（C、C++、Python等），并且可以轻松自定义构建流程。

- **Keil MDK：** Keil MDK在某些方面较为封闭，更专注于ARM Cortex-M平台。自定义性相对较低，主要用于ARM Cortex-M开发。

**4. 跨平台支持：**

- **PlatformIO：** PlatformIO 支持多个操作系统，包括Windows、macOS和Linux，因此适用于不同开发者的工作环境。

- **Keil MDK：** Keil MDK主要面向Windows操作系统，虽然可以通过虚拟机等方式在其他操作系统上运行，但在跨平台方面有一些限制。

**5. 社区支持和生态系统：**

- **PlatformIO：** PlatformIO 有一个庞大的开发者社区，拥有广泛的文档、教程和插件。这使得开发者可以轻松找到帮助和资源。

- **Keil MDK：** Keil MDK也有一定的社区支持，但相对于PlatformIO来说，生态系统规模较小。

**6. 适用场景：**

- **PlatformIO：** PlatformIO 适用于广泛的嵌入式项目，特别是那些使用不同硬件平台和框架的项目。它对于初学者和开源项目非常友好。

- **Keil MDK：** Keil MDK主要适用于专注于ARM Cortex-M系列微控制器的项目，尤其是在商业和工业领域中。它提供了针对ARM架构的高度优化工具链和调试支持。

总的来说，PlatformIO 和 Keil MDK 都是强大的嵌入式开发工具，但它们在硬件支持、定制性、许可证和适用场景方面有所不同。选择哪个工具取决于您的项目需求和偏好。如果您需要跨多个硬件平台进行开发，或者正在进行开源项目，PlatformIO 可能是更好的选择。如果您主要关注ARM Cortex-M系列微控制器，并且需要高度优化的工具链和商业支持，那么 Keil MDK 可能更适合您。



# 参考资料

1、PlatformIO IDE搭建统一的物联网嵌入式开发环境

https://blog.csdn.net/gu332523602/article/details/77836955

2、官网

https://docs.platformio.org/en/latest/integration/ide/pioide.html

