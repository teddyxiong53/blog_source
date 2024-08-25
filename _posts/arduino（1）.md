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

# arduino库标准

https://arduino.github.io/arduino-cli/0.34/library-specification/

# arduino-cli命令行工具

安装：

```
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | BINDIR=~/local/bin sh
```

添加到PATH

运行：

```
aruduio-cli board list
```

这个命令是通过串口usb的方式来列举出当前电脑连接的板子。

生成的数据文件目录是：

```
~/.arduino15$ tree
.
├── inventory.yaml
├── library_index.json
├── library_index.json.sig
├── package_index.json
├── package_index.json.sig
├── packages
│   └── builtin
│       └── tools
│           ├── ctags
│           │   └── 5.8-arduino11
│           │       └── ctags
│           ├── dfu-discovery
│           │   └── 0.1.2
│           │       ├── dfu-discovery
│           │       └── LICENSE.txt
│           ├── mdns-discovery
│           │   └── 1.0.9
│           │       ├── LICENSE.txt
│           │       └── mdns-discovery
│           ├── serial-discovery
│           │   └── 1.4.1
│           │       ├── LICENSE.txt
│           │       └── serial-discovery
│           └── serial-monitor
│               └── 0.14.1
│                   ├── LICENSE.txt
│                   └── serial-monitor
├── staging
│   └── packages
│       ├── ctags-5.8-arduino11-pm-x86_64-pc-linux-gnu.tar.bz2
│       ├── dfu-discovery_v0.1.2_Linux_64bit.tar.gz
│       ├── mdns-discovery_v1.0.9_Linux_64bit.tar.gz
│       ├── serial-discovery_v1.4.1_Linux_64bit.tar.gz
│       └── serial-monitor_v0.14.1_Linux_64bit.tar.gz
└── tmp

16 directories, 19 files
```

Arduino CLI（命令行界面） 是一个面向 Arduino 生态系统的全功能工具，

旨在简化从命令行编译和上传代码到 Arduino 板的过程。

它集成了板管理器、库管理、编译器和上传工具等功能，

提供了一个统一的解决方案，

适用于 Windows 的命令提示符、以及 Linux 和 macOS 的终端用户。

Arduino CLI 对于那些偏好命令行操作或寻求自动化集成的开发者来说，是理想的选择。

它不仅支持标准的 Arduino 开发，也是 Arduino Create Web 编辑器的背后技术驱动力。

自动化

```
build_and_upload:
  script:
    - arduino-cli compile --fqbn Arduino:avr:uno my_project
    - arduino-cli upload --fqbn Arduino:avr:uno --port /dev/ttyACM0 my_project
```

它提供了ArduinoIDE的所有功能：

- 编写[sketch](https://so.csdn.net/so/search?q=sketch&spm=1001.2101.3001.7020)

- 上载sketch

- 库管理

- [开发板](https://so.csdn.net/so/search?q=开发板&spm=1001.2101.3001.7020)和核心管理

我们可以在命令行中使用所有这些功能，而无需使用Arduino IDE。

如果您熟悉Arduino IDE，那么迁移到Arduino cli不会有问题。即使这样，Arduino命令行界面中有一些重要的概念或关键字：

sketch草图：这是我们正在编写的应用程序的源代码

board开发板：它是我们正在使用的板，以及我们想要上传代码的位置。开发板由称为FQBN的唯一id标识。

code核心：它是开发板会使用的核心。可以有几个不同的开发板使用相同的内核。

library库：它是我们在草图中包含的一个软件，由其他人开发，负责管理特定任务：传感器库、LED库、协议库等



查看当前连接的nodemcu

```
arduino-cli board listall nodemcu
```



这篇文章不错

https://blog.csdn.net/chentuo2000/article/details/129472612

## 操作nodemcu wemos d1

https://gist.github.com/adi-g15/de41e96079a5b63045e86dc7c8c5c87e

```
$ arduino-cli board listall
$ arduino-cli sketch new blink2
$ cp -v blink2.ino ~/Arduino/blink2/
$ arduino-cli compile --fqbn esp8266:esp8266:d1 Arduino/blink2
$ arduino-cli upload -p /dev/ttyUSB0 --fqbn esp8266:esp8266:d1 Arduino/blink2
```

https://github.com/zoobab/arduino-cli-esp8266



Arduino CLI并不严格要求配置文件才能工作，

因为命令行界面提供了任何可能的功能。

但是，在发出命令时，拥有一个可以节省大量输入时间，因此让我们继续使用以下命令创建它：

```
$ arduino-cli config init
Config file written: /home/luca/.arduino15/arduino-cli.yaml
```

创建一个sketch

```
$ arduino-cli sketch new MyFirstSketch
Sketch created in: /home/luca/MyFirstSketch
```

得到这样的目录：

```
tree
.
└── MyFirstSketch
    └── MyFirstSketch.ino
```

ino文件里：

```
void setup() {
}

void loop() {
}
```

我们实现为blink程序。

```
void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
}
```

全新安装后要做的第一件事是通过运行以下命令来更新可用平台和库的本地缓存：

```
$ arduino-cli core update-index
Updating index: package_index.json downloaded
```

使用 USB 电缆将开发板连接到 PC 后，您应该能够通过运行以下命令来检查它是否已被识别：

```
$ arduino-cli board list
Port         Type              Board Name              FQBN                 Core
/dev/ttyACM1 Serial Port (USB) Arduino/Genuino MKR1000 arduino:samd:mkr1000 arduino:samd
```

如果您看到列出了`Unknown`板，只要您识别平台核心并使用正确的 FQBN 字符串，上传应该仍然可以进行。当由于某种原因未检测到主板时，您可以通过运行以下命令列出所有支持的主板及其 FQBN 字符串：

要安装`arduino:samd`平台核心，请运行以下命令：

```
arduino-cli core install arduino:samd
```

如果您的主板需要第 3 方核心包才能工作，您可以在 Arduino CLI 配置文件中列出其他包索引的 URL。

例如，要添加 ESP8266 内核，请编辑配置文件并更改`board_manager`设置，如下所示：

```
board_manager:
  additional_urls:
    - https://arduino.esp8266.com/stable/package_esp8266com_index.json
```

要编译草图，请运行`compile`命令，并传递正确的 FQBN 字符串：

> "FQBN 字符串"是一个在编程和软件开发领域中使用的专业术语，它代表了"Fully Qualified Board Name"的缩写。这个术语通常用于指代一个完全限定的板子名称，它包含了足够的信息来唯一识别一个硬件平台或开发板。
>
> 在编译代码时，特别是在嵌入式系统或微控制器编程中，你需要指定一个FQBN字符串来告诉编译器针对哪个具体的硬件平台进行编译。这个字符串通常包含了制造商、板子型号、处理器类型等信息，确保编译器可以生成适合特定硬件的固件。
>
> 例如，在Arduino IDE中，当你选择一个板子类型时，IDE会根据选择的板子自动设置FQBN字符串。这个字符串可能看起来像这样：`arduino:avr:uno`，其中"arduino"是制造商，"avr"是处理器架构，"uno"是具体的板子型号。

编译

```
arduino-cli compile --fqbn arduino:samd:mkr1000 MyFirstSketch
```

烧录：

```
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:samd:mkr1000 MyFirstSketch
```

如果您需要向草图中添加更多功能，

Arduino 生态系统中的一些可用库很可能已经提供了您所需的功能。

例如，如果您需要去抖策略来更好地处理按钮输入，您可以尝试搜索`debouncer`关键字：

```
 arduino-cli lib search debouncer
```

我们最喜欢的是`FTDebouncer` ，让我们通过运行来安装它：

```
 arduino-cli lib install FTDebouncer
```

Arduino CLI 可以通过`daemon`命令作为 gRPC 服务器启动。



当您运行[`arduino-cli board list`](https://arduino.github.io/arduino-cli/1.0/commands/arduino-cli_board_list/)时，您的主板不会显示。可能的原因：

你的主板是更便宜的衍生品，或者它是一块板，例如经典的 Nano，使用 USB 转串行转换器，例如 FTDI FT232 或 CH340。这些芯片总是向操作系统报告相同的 USB VID/PID，因此我们唯一知道的是主板安装了特定的 USB2Serial 芯片，但我们不知道该芯片位于哪块主板上。



# Arduino CLI 的三大支柱

Arduino CLI 是一个用[Golang](https://go.dev/)编写的开源命令行应用程序，

可以从终端使用它来编译、验证草图并将其上传到 Arduino 板，

并且能够管理该过程中所需的所有软件和工具。

但不要被它的名字所迷惑：Arduino CLI 的功能比普通控制台应用程序要多得多，如[Arduino IDE 2.x](https://github.com/arduino/arduino-ide)和[Arduino Cloud](https://cloud.arduino.cc/home)所示，它们都依赖它来实现类似的目的，但每个应用程序的方式都完全不同另一个。

在本文中，我们介绍了 Arduino CLI 的三大支柱，解释了我们如何设计该软件，以便在不同场景下有效利用它。

## 第一支柱：命令行界面

正如您所料，使用 Arduino CLI 的第一种方式是通过终端由人工操作，用户体验在这里起着关键作用。

用户体验正在持续改进过程中，因为我们希望该工具功能强大但又不太复杂。

我们严重依赖子命令来提供一组丰富的逻辑组合在一起的不同操作，

以便用户可以轻松探索界面，

同时获得非常具体的上下文帮助（即使是中文！）。

### 机器人控制台应用程序

人类并不是我们想要支持的唯一客户类型，

Arduino CLI 也被设计为以编程方式使用 - 想想自动化管道或[CI](https://en.wikipedia.org/wiki/Continuous_integration) / [CD](https://en.wikipedia.org/wiki/Continuous_deployment)系统。

当您编写在无人值守时易于运行的软件时，需要注意一些细节，特别是无需配置文件即可运行的能力。

这是可能的，因为您在 arduino-cli.yaml 配置文件中找到的每个配置选项都可以通过命令行标志或设置环境变量来提供。

举个例子，以下命令都是等效的，并且将获取 ESP32 平台的外部包索引：

## 第二支柱：gRPC 接口

[gRPC](https://grpc.io/)是一个高性能[RPC](https://en.wikipedia.org/wiki/Remote_procedure_call)框架，可以高效连接客户端和服务器应用程序。 

Arduino CLI 可以充当 gRPC 服务器（我们称之为[守护进程模式](https://arduino.github.io/arduino-cli/1.0/commands/arduino-cli_daemon/)），

公开一组实现与命令行界面完全相同的功能集的程序，

并等待客户端连接和使用它们。

为了给出一个想法，以下是一些能够检索远程运行的 Arduino CLI 服务器实例的版本号的[Golang](https://go.dev/)代码：

```go
package main

import (
    "context"
    "log"
    "time"

    rpc "github.com/arduino/arduino-cli/rpc/cc/arduino/cli/commands/v1"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
)

func main() {
    // Establish a connection with the gRPC server
    conn, err := grpc.NewClient("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        log.Println(err)
        log.Fatal("error connecting to arduino-cli rpc server, you can start it by running `arduino-cli daemon`")
    }
    defer conn.Close()

    // Create an instance of the gRPC clients.
    cli := rpc.NewArduinoCoreServiceClient(conn)

    // Now we can call various methods of the API...
    versionResp, err := cli.Version(context.Background(), &rpc.VersionRequest{})
    if err != nil {
        log.Fatalf("Error getting version: %s", err)
    }
    log.Printf("arduino-cli version: %v", versionResp.GetVersion())
}
```

## 第三个支柱：嵌入

Arduino CLI 是用[Golang](https://go.dev/)编写的，

代码的组织方式使得通过在编译时将您需要的模块包含在另一个 Golang 应用程序中，

可以轻松地将其用作库。

第一和第二支柱都依赖于基于 gRPC protobuf 定义的通用 Golang API：

一组抽象 Arduino CLI 提供的所有功能的函数，以便当我们提供修复或新功能时，它们会自动可用于命令行和 gRPC 接口。

实现此 API 的源模块是通过`commands`包实现的，并且可以将其导入其他 Golang 程序中以嵌入成熟的 Arduino CLI。

例如，这就是支持[Arduino Cloud 的](https://cloud.arduino.cc/home)某些后端服务编译草图和管理库的方式。

为了让您了解嵌入 Arduino CLI 的含义，以下介绍了如何使用 API 搜索内核：

嵌入 Arduino CLI 仅限于 Golang 应用程序，并且需要深入了解其内部结构。对于一般用例，gRPC 接口可能是更好的选择。尽管如此，这仍然是我们使用并提供支持的有效选项。

# arduino语言参考

https://docs.arduino.cc/language-reference/

# arduino所有的库

https://www.arduino.cc/reference/en/libraries/

# 写一个arduino库

https://docs.arduino.cc/learn/contributions/arduino-creating-library-guide/

库至少需要两个文件：头文件（扩展名为 .h）和源文件（扩展名为 .cpp）。

头文件包含库的定义：基本上是内部所有内容的列表；

而源文件有实际的代码。

我们将我们的库称为“Morse”，所以我们的头文件将是

```arduino
Morse . h
```

 。让我们看看里面有什么。

乍一看可能有点奇怪，但是一旦您看到它附带的源文件，就会更有意义。

```
#include "Arduino.h"
class Morse
{
  public:
    Morse(int pin);
    void begin();
    void dot();
    void dash();
  private:
    int _pin;
};
```

```
/*
  Morse.cpp - Library for flashing Morse code.
  Created by David A. Mellis, November 2, 2007.
  Updated by Jason A. Cox, February 18, 2023.
  Released into the public domain.
*/

#include "Arduino.h"
#include "Morse.h"

Morse::Morse(int pin)
{
  _pin = pin;
}

void Morse::begin()
{
  pinMode(_pin, OUTPUT);
}

void Morse::dot()
{
  digitalWrite(_pin, HIGH);
  delay(250);
  digitalWrite(_pin, LOW);
  delay(250);  
}

void Morse::dash()
{
  digitalWrite(_pin, HIGH);
  delay(1000);
  digitalWrite(_pin, LOW);
  delay(250);
}
```



```
#include <Morse.h>

Morse morse(13);

void setup()
{
  morse.begin();
}

void loop()
{
  morse.dot(); morse.dot(); morse.dot();
  morse.dash(); morse.dash(); morse.dash();
  morse.dot(); morse.dot(); morse.dot();
  delay(3000);
}
```

为此，请在 Morse 目录中创建一个名为**keywords.txt**的文件。它应该看起来像这样：

```arduino
Morse   KEYWORD1
begin   KEYWORD2
dash    KEYWORD2
dot KEYWORD2
```

KEYWORD1是对应数据类型。

KEYWORD2对应函数和方法。

LITERAL1对应常量。



# arduino上的脚本语言

https://blog.csdn.net/m0_46336441/article/details/122649821

# esp8266的arduino core实现

https://github.com/esp8266/Arduino

这个值得分析学习。



# 参考资料

1、
https://www.phodal.com/blog/arduino-modular/

2、
http://arduiniana.org/

3、
https://www.arduino.cc/reference/en/