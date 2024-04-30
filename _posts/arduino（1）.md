---
title: arduino（1）
date: 2023-02-03 16:13:17
tags:
	- arduino

---

--

# 简介

Arduino是一种==开源电子原型平台，==

用于创建各种交互式项目。

它由一个易于使用的硬件和一个基于简化版C/C++的软件开发环境组成。

Arduino的核心是一个单片机（通常是Atmel AVR系列或者ARM系列的芯片），

它可以通过简单的电路连接和编程来控制各种传感器和执行器。

Arduino平台的特点包括：

1. **开源性**: Arduino硬件和软件是开源的，这意味着任何人都可以自由查看、修改和分享设计和代码。

2. **易用性**: Arduino具有简单的开发环境和编程语言，使得即使是初学者也可以轻松上手。

3. **灵活性**: 通过连接各种传感器、执行器和其他电子组件，您可以创建几乎任何想法的原型。

4. **社区支持**: Arduino拥有一个活跃的全球社区，您可以在这里获取帮助、分享项目和与其他Arduino用户交流经验。

5. **低成本**: Arduino硬件相对便宜，因此非常适合学习和原型开发。

Arduino可用于各种项目，包括物联网（IoT）、机器人、传感器应用、艺术装置等等。无论您是想要学习电子制作的基础知识，还是希望实现自己的创意项目，Arduino都是一个很好的选择。

# 发展历史

Arduino的发展历史可以追溯到2005年，当时一群意大利的学生和教授在设计一款简单易用的开源硬件平台，用于教育目的。以下是Arduino的主要发展里程碑：

1. **2005年**: 首个Arduino原型诞生。这个项目由Massimo Banzi、David Cuartielles、Tom Igoe、Gianluca Martino和David Mellis等人共同创立。他们的目标是设计一个简单的电子原型平台，使非专业人士能够轻松地制作电子项目。

2. **2005年**: 第一款Arduino原型板发布。这个板子使用了Atmel公司的8位AVR微控制器，由于其易用性和开放性，很快受到了开发者和爱好者的欢迎。

3. **2007年**: Arduino Diecimila发布。这是第一个广泛使用的Arduino板，具有USB接口和自动重置功能，使得与计算机的连接更加方便。

4. **2008年**: Arduino Uno发布。Uno是目前为止最受欢迎和广泛使用的Arduino板之一，它引入了一些新特性，如更大的Flash存储器和更多的数字输入/输出引脚。

5. **2010年**: Arduino Mega 2560发布。Mega 2560是一款功能更强大的Arduino板，具有更多的引脚和更多的存储器，适用于需要更多输入/输出和更复杂项目的开发者。

6. **2012年**: Arduino Due发布。Due是第一款基于32位ARM架构的Arduino板，具有更高的性能和更多的功能，适用于需要处理更复杂任务的项目。

7. **至今**: Arduino平台不断发展壮大，推出了许多不同类型的板子和扩展模块，以满足不同需求的开发者和项目。同时，Arduino社区也不断壮大，为用户提供支持、教程和丰富的资源。

总的来说，Arduino通过其简单易用的设计和开放的生态系统，已经成为了世界上最受欢迎的开源电子原型平台之一，为无数人实现了他们的创意和想法。

# 常见的Arduino型号及其相关信息

以下是一些常见的Arduino型号及其相关信息：

| Arduino型号                 | 微控制器芯片      | 上市年份 | RAM大小 | Flash大小 |
| --------------------------- | ----------------- | -------- | ------- | --------- |
| Arduino NG                  | ATmega8           | 2005     | 1 KB    | 8 KB      |
| Arduino Diecimila           | ATmega168         | 2007     | 1 KB    | 16 KB     |
| Arduino Duemilanove         | ATmega328         | 2009     | 2 KB    | 32 KB     |
| Arduino Uno                 | ATmega328P        | 2010     | 2 KB    | 32 KB     |
| Arduino Mega 2560           | ATmega2560        | 2010     | 8 KB    | 256 KB    |
| Arduino Leonardo            | ATmega32U4        | 2012     | 2.5 KB  | 32 KB     |
| Arduino Due                 | ATSAM3X8E         | 2012     | 96 KB   | 512 KB    |
| Arduino Pro Mini            | ATmega328P        | 2012     | 2 KB    | 32 KB     |
| Arduino Micro               | ATmega32U4        | 2012     | 2.5 KB  | 32 KB     |
| Arduino Nano                | ATmega328P        | 2015     | 2 KB    | 32 KB     |
| Arduino MKR1000             | SAMD21 Cortex-M0+ | 2016     | 32 KB   | 256 KB    |
| Arduino MKR Zero            | SAMD21 Cortex-M0+ | 2017     | 32 KB   | 256 KB    |
| Arduino MKR WiFi 1010       | SAMD21 Cortex-M0+ | 2018     | 32 KB   | 256 KB    |
| Arduino Nano Every          | ATmega4809        | 2019     | 6 KB    | 48 KB     |
| Arduino Uno WiFi Rev2       | ATmega4809        | 2019     | 6 KB    | 48 KB     |
| Arduino Nano 33 IoT         | nRF52840          | 2019     | 256 KB  | 1 MB      |
| Arduino Nano RP2040 Connect | RP2040 Cortex-M0+ | 2021     | 264 KB  | 2 MB      |

这是一些常见的Arduino型号及其所使用的微控制器芯片、上市年份以及RAM和Flash的大小。

# 有哪些基于arduino的著名项目

基于Arduino的项目非常广泛，涵盖了各种领域，包括物联网（IoT）、机器人技术、艺术装置、教育、医疗健康等等。以下是一些著名的基于Arduino的项目：

1. **3D打印机和CNC机器人**: 许多DIY 3D打印机和数控雕刻机（CNC）项目都基于Arduino控制系统。

2. **智能家居系统**: 使用Arduino控制传感器和执行器来构建智能家居系统，如温度监控、灯光控制、智能门锁等。

3. **自动植物浇水系统**: 基于Arduino的自动植物浇水系统可以根据土壤湿度和环境条件自动为植物浇水，保持植物的健康生长。

4. **无人机**: 一些DIY爱好者使用Arduino构建无人机，实现飞行控制和自动导航功能。

5. **健身追踪器**: Arduino可以用于制作简单的健身追踪器，监测步数、心率、睡眠质量等健康数据。

6. **交互艺术装置**: 许多艺术家和创意工作者使用Arduino构建交互式艺术装置，如光雕、声音装置、动态雕塑等。

7. **智能车辆**: 基于Arduino的智能车辆项目包括自动驾驶小车、避障车、线追踪车等。

8. **教育项目**: Arduino被广泛应用于教育领域，用于教授学生电子制作、编程和物联网等知识。

9. **医疗设备**: 一些低成本的医疗设备项目使用Arduino，如心率监测器、血压监测器等。

10. **环境监测系统**: Arduino可以用于构建环境监测系统，监测空气质量、水质、土壤湿度等环境参数。

这只是一小部分基于Arduino的项目示例，实际上还有许多其他有趣和创新的项目正在不断涌现。Arduino的灵活性和易用性使其成为许多创客、工程师和艺术家的首选平台。

## 基于arduino的3D打印机开源代码

基于Arduino的3D打印机通常使用开源的固件和软件来控制打印机的运行。其中，最著名和常用的开源固件是Marlin，它是一款专门为3D打印机设计的固件，支持多种类型的打印机硬件和功能。

你可以在Marlin团队的GitHub仓库中找到他们的开源代码：[Marlin GitHub仓库](https://github.com/MarlinFirmware/Marlin)

Marlin固件使用C++编写，提供了丰富的功能和配置选项，可以适配各种类型的3D打印机。通过对固件的配置和编译，您可以根据自己的打印机硬件和需求进行定制。

除了Marlin固件之外，还有其他一些基于Arduino的3D打印机固件和软件，例如Repetier Firmware、Smoothieware等。您可以根据自己的需求和偏好选择合适的固件来控制您的3D打印机。

## 基于arduino的智能家居系统

基于Arduino的智能家居系统可以通过连接传感器、执行器和网络模块来实现远程监控和控制家居设备。以下是智能家居系统可能涉及的一些功能和组件：

1. **温度和湿度监测**: 使用温湿度传感器（如DHT系列）监测室内环境的温度和湿度，并将数据发送到Arduino控制器。

2. **光线传感器**: 使用光线传感器监测室内光照强度，可以根据光照强度控制灯光的开关。

3. **人体红外感应器**: 通过人体红外感应器检测人体活动，可以实现智能照明和安防功能，如当有人进入房间时自动开灯。

4. **智能插座**: 使用可控插座和继电器模块，可以远程控制家电的开关，实现远程电源控制功能。

5. **门窗传感器**: 安装在门窗上的磁性传感器可以监测门窗的开关状态，实现智能安防和节能功能。

6. **液位传感器**: 用于监测水箱、水槽等容器的液位，可以实现智能水源管理和漏水检测功能。

7. **风扇和空调控制**: 使用继电器模块控制风扇和空调的开关，可以根据室内温度和湿度自动调节风扇和空调的运行状态。

8. **声音和视频监控**: 使用麦克风和摄像头模块可以实现声音和视频监控功能，可以远程查看家中的情况。

这些功能可以通过Arduino控制器和各种传感器、执行器以及网络模块来实现，您可以根据自己的需求和偏好选择合适的组件来构建智能家居系统。同时，您也可以使用开源的智能家居平台和库来简化开发过程，例如Home Assistant、OpenHAB等。

# 架构分析

以x-track的ArduinoAPI目录为切入点进行分析。

D:\study\X-TRACK\Software\X-Track\ArduinoAPI

这个是为了使用arduino的相关的开源库而封装的适配层。





arduino ide 1.x版本是java写的。

2.x版本就改成electron的方案了。基于vscode了。

# c++代码分析

## 重载new操作符

```
void *operator new (size_t size)
{
  return malloc(size);
}

void *operator new[](size_t size)
{
  return malloc(size);
}
```

这是C++中的内存分配运算符重载函数，用于在动态内存分配时调用。

当使用`new`关键字分配内存时，会自动调用`operator new`函数进行内存分配，

在这里，`operator new`函数被重载为调用`malloc`函数来分配内存。

同样地，当使用`new[]`关键字分配数组内存时，会自动调用`operator new[]`函数进行内存分配，

在这里，`operator new[]`函数也被重载为调用`malloc`函数来分配内存。

`size`参数表示需要分配的内存大小，函数返回值为指向分配的内存块的指针。

由于`malloc`函数返回的是一个`void*`类型的指针，因此这里`operator new`和`operator new[]`的返回值也是`void*`类型的指针。

这种重载运算符的方式使得内存分配操作可以自定义，从而可以在程序中实现更加灵活、高效的内存管理。

**同时，这种运算符重载也使得C++中的内存分配操作与C语言中的内存分配操作（如`malloc`和`free`）兼容，方便与C语言代码的交互。**

## 虚函数处理

```
extern "C" void __cxa_pure_virtual(void) __attribute__((__noreturn__));
extern "C" void __cxa_deleted_virtual(void) __attribute__((__noreturn__));

void __cxa_pure_virtual(void)
{
  // We might want to write some diagnostics to uart in this case
  //std::terminate();
  while (1)
    ;
}

void __cxa_deleted_virtual(void)
{
  // We might want to write some diagnostics to uart in this case
  //std::terminate();
  while (1)
    ;
}
```

这段代码定义了两个函数`__cxa_pure_virtual`和`__cxa_deleted_virtual`，这两个函数都是C++中的异常处理函数，用于在发生虚函数调用错误时进行处理。

`__cxa_pure_virtual`函数用于处理纯虚函数调用错误，**即在没有实现虚函数的情况下调用该函数。**

该函数的实现是一个死循环，它会一直等待程序中止。

在这个死循环中可以添加一些诊断信息或者其他处理方式，例如向串口打印错误信息，以便在调试时进行分析。

`__cxa_deleted_virtual`函数用于处理已删除的虚函数调用错误，即在已删除的虚函数上调用该函数。

该函数的实现与`__cxa_pure_virtual`函数类似，也是一个死循环，它会一直等待程序中止。

**这两个函数都被声明为`extern "C"`，这是为了告诉编译器这是一个C语言函数，而不是C++语言函数。**

**这是因为C++中的函数名会经过名称重整（name mangling）处理，导致在链接时无法正确地找到函数的符号。**

通过使用`extern "C"`声明，可以避免这个问题，并使得这两个函数可以被其他编程语言（例如C语言）调用。同时，这两个函数也使用了`__attribute__((__noreturn__))`属性，表示它们不会返回任何结果，而是永远阻塞在循环中，以确保程序中止。

这些函数通常由编译器自动生成，用于处理一些C++异常和错误的情况。

**如果用户在程序中显式地声明了一个纯虚函数，但没有对其进行实现，或者将一个已删除的虚函数进行调用，那么就会触发这些异常处理函数的调用。**

在这些处理函数中，可以添加一些额外的处理逻辑，以便在发生异常时进行诊断和调试。

## main函数

```
int main(void)
{
  initVariant();

  setup();

  for (;;) {
#if defined(CORE_CALLBACK)
    CoreCallback();
#endif
    loop();
    serialEventRun();
  }

  return 0;
}
```

# arduino库标志



https://arduino.github.io/arduino-cli/0.34/library-specification/

# 参考资料

1、
https://www.phodal.com/blog/arduino-modular/

2、
http://arduiniana.org/

3、
https://www.arduino.cc/reference/en/