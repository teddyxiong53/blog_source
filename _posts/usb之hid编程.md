---
title: usb之hid编程
date: 2020-10-29 10:42:30
tags:
	- usb
---

1

示例代码：

```
import hid

vid = 0x093a	# Change it for your device
pid = 0x2510	# Change it for your device

with hid.Device(vid, pid) as h:
	print(f'Device manufacturer: {h.manufacturer}')
	print(f'Product: {h.product}')
	print(f'Serial Number: {h.serial}')
```

运行报错，

```
Unable to load any of the following libraries hidapi.dll
```

https://github.com/libusb/hidapi/releases

这里下载压缩包，解压，把x86目录下的库文件放到到C:\Windows\System32。我尽量用win32的。

因为这样可以保证在32位和64位的电脑上都可以用。

但是下载运行还是提示找不到对应的库。



```
OSError: [WinError 193] %1 不是有效的 Win32 应用程序
```

Python调试出现OSError: [WinError 193] %1 不是有效的 Win32 应用程序，

一般来讲是因为python位数和dll位数不一样导致的，dll是32位的，而python是64位的。

我的系统是64位Win7安装了64位的python，当调用32位dll（比如32位的ODBC驱动）的时候，就报错。

如何解决：

1、安装64位的dll（一般很难找到）

2、安装32位的python



为了最好的兼容性，我考虑这种涉及底层硬件操作的。

python用2.7版本的，32位的。

```
from __future__ import print_function

import hid

vid = 0x093a	# Change it for your device
pid = 0x2510	# Change it for your device

with hid.Device(vid, pid) as h:
	print(h.manufacturer)
	print(h.product)
```

现在这样hid可以读出信息来。



HID设备的描述符除了5个USB的标准描述符（设备描述符、配置描述符、接口描述符、端点描述符、字符串描述符，见[百合电子工作室](http://www.baiheee.com/)的另一篇文章：[USB开发基础－－USB命令（请求）和USB描述符](http://www.baiheee.com/Documents/090518/090518112619.htm)）外，

还包括3个HID设备类特定描述符：

HID描述符、

报告描述符、

实体描述符。



HID设备的报告描述符比较复杂也比较难理解。

报告描述符的语法不同于USB标准描述符，

它是以项目（items）方式排列而成，无一定的长度。

HID的报告描述符已经不是简简单单的描述某个值对应某个固定意义了，

它已经能够组合出很多种情况，

并且需要PC上的HID驱动程序提供parser解释器来对描述的设备情形进行重新解释，

**进而组合生成出本HID硬件设备独特的数据流格式，**

所以我觉得可以把它理解为“报告描述符脚本语言”更为贴切。

我们使用“报告描述符”专用脚本语言，

让用户来自己定义他们的HID设备都有什么数据、以及这些数据各个位（bit）都有什么意义。



有关报告描述符的详细信息可参考USB HID协议，

*USB* 协会提供了一个*HID* 描述符编辑工具称作*HID Descriptor Tool，用它可方便生成我们的报告描述符。*

例如鼠标报告的就是位置信息，

```
@ 11:41:16 139 +8.0
Device[4]:  InputMouse
LB MB RB 4B 5B   Xcnts   Ycnts  Zdelta  Hdelta
1  0  0  0  0        0      -2       0       0

@ 11:41:16 147 +7.7
Device[4]:  InputMouse
LB MB RB 4B 5B   Xcnts   Ycnts  Zdelta  Hdelta
1  0  0  0  0       -1      -2       0       0
```



键盘报告的就是按键信息。

```
@ 11:39:56 350 +551.4
Device[2]:  InputKeyboard
Vkey   Event  E[1:0]  Scancode
50      Make      00        19

@ 11:39:56 531 +180.7
Device[2]:  InputKeyboard
Vkey   Event  E[1:0]  Scancode
50     Break      00        19

```



实体描述符被用来描述设备的行为特性。

实体描述符是可选的描述符，

HID设备可以根据其本体的设备特性选择是否包含实体描述符。



HID设备类特定的命令（请求）有6个，

它们分别是

Get_Report、

Get_Idle、

Get_Protocol、

Set_Report、

Set_Idle

Set_Protocol。



USB主机在请求HID设备的配置描述符时，

设备首先返回的描述符为：

配置描述符、接口描述符、HID描述符、端点描述符。

HID描述符里包含了其附属的描述的类型和长度（如报告描述符），

然后主机再根据HID描述符的信息请求其相关的描述符。



HID协议有其局限性，

但所有现代主流操作系统都识别标准USB HID设备（例如键盘和鼠标），而无需专门的驱动程序。

在设备安装时，屏幕上可能呈现“一个‘HID兼容设备’已安装”消息。



HID协议中有两个实体：主机（host）和设备（device）。

设备是直接与人类交互的实体，例如键盘或鼠标；

主机则是负责与设备通信并接收人类在设备上输入的数据。

输出数据则是主机传送给设备，设备再展现给人类。

最常见的主机就是PC，但有些手机和PDA也可作为主机。



HID协议使得设备的实现非常简单。

设备定义它们的数据包，然后向主机呈递“HID描述符”。

HID描述符是描述设备的数据包的硬编码字节数组，其中包括：

设备支持多少个数据包，数据包大小，以及数据包中各个字节和比特的目的。

例如，计算器程序的键盘按钮可以告诉主机，该按钮的按压/松开状态被存储为数据包4号中第6个字节中的第2比特（注意：这些位置仅为说明目的，并且依设备而不同）。

设备通常将HID描述符存储在ROM中，并且不需要本质上理解或解析HID描述符。

目前市场上的一些鼠标和键盘硬件仅使用8位[CPU](https://zh.wikipedia.org/wiki/中央处理器)来实现。



主机的预期是比设备更复杂的实体。

主机需要检索来自设备的HID描述符，并需要解析它才可以与设备进行完全通信。

解析HID描述符可能很复杂。

已知有多个操作系统的负责解析HID描述符的驱动程序在发布给公众几年后被发现存在缺陷。

但是，这种复杂性也成就了HID设备的快速创新。



上述机制描述了什么是HID“报告协议”。

因为可以理解并非所有主机都能够解析HID描述符，

HID还定义了“引导协议”（boot protocol）。

因为引导协议中使用固定的数据包格式，所以只支持特定功能的特定设备。

在该模式中不使用HID描述符，因此创新是有限的，但好处是可以在无法支持HID的主机上仍可实现有限的功能。



鼠标只有X轴、Y轴和前3个按钮可用。鼠标上的任何额外功能将不可用。



USB－HID是Human Interface Device的缩写，属于人机交互操作的设备，

如USB鼠标，USB键盘，USB游戏操纵杆，USB触摸板，USB轨迹球、电话拨号设备、VCR遥控等等设备。

 TPYBV101除了具有usb host功能以外，还可作为USB－HID设备来应用，

这里重点讲述如果作为鼠标和键盘使用。



TPYBV101作为鼠标的应用可以参考micropython官方实例中的usb-mouse应用。这里以官方实例为例。



而pc端上的”HID”一般指的是USB-HID标准，更多指微软在USB委员会上提议创建的一个人体学输入设备工作组。



**HID标准概念之后，**所有HID定义的设备驱动程序提供可包含任意数量数据类型和格式的自我描述包。计算机上的单个HID驱动程序就可以解析数据和实现数据[I/O](https://link.zhihu.com/?target=https%3A//zh.wikipedia.org/wiki/I/O%22%20%5Co%20%22I/O)与应用程序功能的动态关联。



HID attack 通过插入带有攻击向量的USB设备等方式，恶意代码直接就被加载执行，攻击操作也就瞬时发生。此类方式属于物理层面攻击。

相对来说，攻击者控制了用户的键盘，则就可以说控制了对方主机的权限。



既然，USB插得有可能是移动储存设备，也有可能是类似键盘鼠标的输入设备，那么计算机是如何分辨的呢？



答案就是 HID协议中的定义的HID设备标识符。

就我们人类而言，键盘之所以是键盘，是因为能打字，

鼠标之所以能是鼠标，是因为能控制光标的移动

U盘之所以是U盘，是因为他能长得像U盘，能传入传输文件。

但是计算机不是人，他只认识0和1，Device Class Definition for Human Interface Devices是一个公开的国际标准，用于规定HID设备的类型。

当任何一个HID设备在接入电脑时，操作系统就首先会读取其设备标识符，



**你如果具备U盘的标识，那我就给你挂载一个盘符。**

**你如果具备键盘的标识符，我就接受你给我输入的信息。**

原则上HID 是一出厂，就被设定好了的，出厂了就不能再更改了。



老生常谈的一句话“**互联网本身是安全的，自从有了安全的人，互联网就变得不安全了。**”

但是HID规范和协议是公开，通过自定义HID标识，让计算机模拟了键盘的输入。

则达到了我们所说的HID攻击。



在USB设备中，HID设备的成本较低。另外，HID设备并不一定要有人机交互功能，只要符合HID类别规范的设备都是HID设备。

Wndows操作系统最先支持的HID设备。在windows 98以及后来的版本中内置有 HID设备的驱动程序，应用程序可以直接使用这些驱动程序来与设备通信。

![1601133666495](../images/random_name/1601133666495.png)



在设计一个USB接口的计算机外部设备时，如果HID类型的设备可以满足需要，可以将其设计为HID类型设备，

这样可以省去比较复杂的USB驱动程序的编写，直接利用Windows操作系统对标准的HID类型USB设备的支持。



交换的数据储存在称为报表（Report）的结构内，

设备的固件必须支持HlD报表的格式。

主机通过控制和[中断传输](https://www.bytekits.com/usb/usb-interrupt-transfer.html)中的传送和请求报表来传送和接收数据。报表的格式非常灵活。

每一笔事务可以携带小量或中量的数据。

> 低速设备每一笔事务最大是8B,一个报表可以使用多笔事务。
> 全速设备每一笔事务最大是64B
> 高速设备每一笔事务最大是1024B。

设备可以在未预期的时间传送信息给主机，例如键盘的按键或是鼠标的移动。

所以主机会定时轮询设备，以取得最新的数据。

HID设备的最大传输速度有限制。

主机可以保证低速的中断端点每10ms内最多1笔事务，每一秒最多是800B（8×100）。

保证全速端点每lms一笔事务，每一秒最多是64000B(64×1000)。

保证高速端点每125 us三笔事务，每一秒最多是24.576MB(1024×8000×3)。

HID设备没有保证的传输速率。

如果设备是设置在10ms的时距，事务之间的时间可能等于或小于10ms。除非设备是设置在全速时在每个帧传输数据，或是在高速时在每个微帧传输数据。这是最快的轮询速率，所以端点可以保证有正确的带宽可供使用。

HID设备除了传送数据给主机外，它也会从主机接收数据。只要能够符合HlD类别规范的设备都可以是HID设备。

设备除了HlD接口之外，它可能同时还包含有其他的USB接口。

例如影像显示设备可能使用HID接口来做亮度、对比度的软件控制，

而使用传统的影像接口来传送要显示的数据。

USB扩音器可以使用实时传输来播放语音，同时使用HID接口来控制音量、低音等。



HID类别设备的规范文件主要是以下两份：

- Device Class Definition for Human interface Devices
- HID Usage Tables

所有的HID传输都是使用默认控制管道或是一个中断管道，

HID设备必须有一个中断输入端点来传送数据到主机，中断输出端点则不是必需的。

主机与设备之间所交换的数据，可以分成两种类型：

- 低延迟的数据，必须尽快地到达目的；
- 配置或其他的数据，没有严格时间限制的需求。



主机的驱动程序要与HID设备通信，设备的固件必须符合下列需求：

- 设备的描述符必须识别该设备包含有HID接口。
- 除了默认控制管道外，固件必须另外支持一个中断输入管道。
- 固件必须包含一个[报表描述符](https://www.bytekits.com/hid/hid-report-descriptor.html)来定义要传送与接收的设备数据



Windows 中的 HID 驱动程序堆栈的体系结构基于名为 hidclass.sys 的类驱动程序。 

客户端和传输微型驱动程序从用户模式或内核模式下访问的类驱动程序。



HID设备连接到USB主机后，主机通过发送Get_Descriptor请求读取HID设备的描述符，了解描述符对了解USB设备是至关重要的。



![1601134116633](../images/random_name/1601134116633.png)



对于一个HID设备，[设备描述符](https://www.bytekits.com/usb/usb-device-descriptor.html)与[配置描述符](https://www.bytekits.com/usb/usb-configure-descriptor.html)没有HID特定的信息。其[设备描述符](https://www.bytekits.com/usb/usb-device-descriptor.html)的bDeviceClass和bDeviceSubClass字段的值为0，接口描述符的bInterfaceClass字段值为03，表示设备的该接口是HID类别。



在接口描述符中**子类别码字段**等于1表示此设备支持启动接口（Boot Interface）。

**如果设备有启动接口，即便主机的HID没有加载驱动程序，设备也可以使用。**

这种情形可能发生在计算机是由DOS直接启动，在启动时观看系统设置画面或使用Wndows的安全模式时。

在操作系统加载HlD驱动程序后会使用Set_Protocol请求，将设备由启动协议转换成报表协议。

| 偏移量 | 字段                   | 字节数 | 数值类型 | 说明                                                         |
| ------ | ---------------------- | ------ | -------- | ------------------------------------------------------------ |
| 0      | bLength                | 1      | Numeric  | 描述符字节数                                                 |
| 1      | bDescriptorType        | 1      | Constant | 0x21 = [HID描述符](https://www.bytekits.com/hid/hid-hiddescriptor.html) |
| 2      | bcdHID                 | 2      | Numeric  | HID规范版本号（BCD）                                         |
| 4      | bCountryCode           | 1      | Numeric  | 硬件设备所在国家的国家代码                                   |
| 5      | bNumDescriptors        | 1      | Numeric  | 类别描述符数目（至少有一个[报表描述符](https://www.bytekits.com/hid/hid-report-descriptor.html)） |
| 6      | bDescriptorType        | 1      | Constant | 类别描述符的类型                                             |
| 7      | wDescriptorLength      | 2      | Numeric  | [报表描述符](https://www.bytekits.com/hid/hid-report-descriptor.html)的总长度 |
| 9      | [bDescriptorType]...   | 1      | Constant | 附加的描述符的类型，可选的                                   |
| 10     | [wDescriptorLength]... | 2      | Numeric  | 附加的描述符的总长度，可选的                                 |



[报表描述符](https://www.bytekits.com/hid/hid-report-descriptor.html)定义了执行设备功能的数据格式和使用方法。

和USB的其他描述符是不一样的，它不是一个简单的表格，[报表描述符](https://www.bytekits.com/hid/hid-report-descriptor.html)是USB所有描述符中最复杂的。

[报表描述符](https://www.bytekits.com/hid/hid-report-descriptor.html)非常复杂而有弹性，**因为它需要处理各种用途的设备。**

报表的数据必须**以简洁的格式来储存**，这样才不会浪费设备内的储存空间以及数据传输时的总线时间。



报表描述符由item构成。

item可以分为两种：短item和长item。

短item

短item的第一个byte，可以分为3个部分：

bit0和bit1：bSize。表示数据部分的长度，取值0、1、2、3依次对应0、1、2、4个字节。

bit2和bit3：bType。0：Main。1：Global。2：Local。

bit4到bit7：bTag。

长item

长item的第一个byte是这样：1111   11  10 。这样说明这个item是长item。

第二个byte是bDataSize。所以数据长度最长是255字节。



USB规范官网提供了一个HID报告描述符工具，https://www.usb.org/document-library/hid-descriptor-tool

使用我们此工具，我们可以：

- 创建、编辑和验证HID报告描述符。

- 输出多种输出（.txt、.inc、.h等）

- 查看一些标准的设备报告描述符示例。

  > 该工具包中，包含有大量的常用设备的报告描述符。



有三种类型的 HID Api：设备发现和设置、数据移动和报表创建/解释。



# BUS hound工具

在USB的设计、调试中监听数据传输十分重要。监听USB数据可以使用USB总线分析仪，但这样的设备比较昂贵，于是我们可以用Bus Hound这个软件来监听总线数据。不过它只能看到传输成功的数据包，对于令牌包和应答包时看不到，但是足以满足大部分的应用场合了。这个强大的软件可以捕捉如鼠标、键盘、硬盘、串口等众多设备的数据。



# 协议分析

一个鼠标，3个按键，还有x和y轴。

1个bit代表一个按键。

一个char来表示移动的距离。

所以数据就是这样格式：

![image-20201029141643949](../images/random_name/image-20201029141643949.png)

对应的C数据结构

```
struct mouse_report_t
{
    uint8_t buttons;
    int8_t x;
    int8_t y;
}
```

描述符

第一个item就是描述按键。

```
USAGE_PAGE (Button)
USAGE_MINIMUM (Button 1)
USAGE_MAXIMUM (Button 3)
```

每个按键的状态一个bit。

```
LOGICAL_MINIMUM (0)
LOGICAL_MAXIMUM (1)
```

那就有3个bit

```
REPORT_COUNT (3)
REPORT_SIZE (1)
```

发送这些数据给电脑。

```
INPUT (Data,Var,Abs)
```

最后的就是这样：

```
USAGE_PAGE (Button)
USAGE_MINIMUM (Button 1)
USAGE_MAXIMUM (Button 3)
LOGICAL_MINIMUM (0)
LOGICAL_MAXIMUM (1)
REPORT_COUNT (3)
REPORT_SIZE (1)
INPUT (Data,Var,Abs)
```

没有使用的5个bit呢？

```
REPORT_COUNT (1)
REPORT_SIZE (5)
INPUT (Cnst,Var,Abs)
```

下面我们看X轴的移动

```
USAGE_PAGE (Generic Desktop)
USAGE (X)
LOGICAL_MINIMUM (-127)
LOGICAL_MAXIMUM (127)
```

使用了8个bit

```
REPORT_SIZE (8)
REPORT_COUNT (1)
```

发送相对位置给电脑

```
INPUT (Data,Var,Rel)
```

合并起来就是：

```
USAGE_PAGE (Generic Desktop)
USAGE (X)
LOGICAL_MINIMUM (-127)
LOGICAL_MAXIMUM (127)
REPORT_SIZE (8)
REPORT_COUNT (1)
INPUT (Data,Var,Rel)
```

Y轴也是类似。

所以是这样：

```
USAGE_PAGE (Button)
USAGE_MINIMUM (Button 1)
USAGE_MAXIMUM (Button 3)
LOGICAL_MINIMUM (0)
LOGICAL_MAXIMUM (1)
REPORT_COUNT (3)
REPORT_SIZE (1)
INPUT (Data,Var,Abs)
REPORT_COUNT (1)
REPORT_SIZE (5)
INPUT (Cnst,Var,Abs)
USAGE_PAGE (Generic Desktop)
USAGE (X)
USAGE (Y)
LOGICAL_MINIMUM (-127)
LOGICAL_MAXIMUM (127)
REPORT_SIZE (8)
REPORT_COUNT (2)
INPUT (Data,Var,Rel)
```

但是这还没有完。

为了让电脑知道这个设备是鼠标。

```
USAGE_PAGE (Generic Desktop)
USAGE (Mouse)
COLLECTION (Application)
    USAGE (Pointer)
    COLLECTION (Physical)
     
    ... What we wrote already goes here
     
    END COLLECTION
END COLLECTION
```

最后，一个标准的mouse的hid 报表描述符是这样：

```
0x05, 0x01,                    // USAGE_PAGE (Generic Desktop)
0x09, 0x02,                    // USAGE (Mouse)
0xa1, 0x01,                    // COLLECTION (Application)
0x09, 0x01,                    //   USAGE (Pointer)
0xa1, 0x00,                    //   COLLECTION (Physical)
0x05, 0x09,                    //     USAGE_PAGE (Button)
0x19, 0x01,                    //     USAGE_MINIMUM (Button 1)
0x29, 0x03,                    //     USAGE_MAXIMUM (Button 3)
0x15, 0x00,                    //     LOGICAL_MINIMUM (0)
0x25, 0x01,                    //     LOGICAL_MAXIMUM (1)
0x95, 0x03,                    //     REPORT_COUNT (3)
0x75, 0x01,                    //     REPORT_SIZE (1)
0x81, 0x02,                    //     INPUT (Data,Var,Abs)
0x95, 0x01,                    //     REPORT_COUNT (1)
0x75, 0x05,                    //     REPORT_SIZE (5)
0x81, 0x03,                    //     INPUT (Cnst,Var,Abs)
0x05, 0x01,                    //     USAGE_PAGE (Generic Desktop)
0x09, 0x30,                    //     USAGE (X)
0x09, 0x31,                    //     USAGE (Y)
0x15, 0x81,                    //     LOGICAL_MINIMUM (-127)
0x25, 0x7f,                    //     LOGICAL_MAXIMUM (127)
0x75, 0x08,                    //     REPORT_SIZE (8)
0x95, 0x02,                    //     REPORT_COUNT (2)
0x81, 0x06,                    //     INPUT (Data,Var,Rel)
0xc0,                          //   END_COLLECTION
0xc0                           // END_COLLECTION
```





![img](../images/random_name/924267-20170515162120057-1295459680.png)

USAGE_PAGE

相当于一个namespace。

INPUT

Data,Var,Abs

Add the above data variables to the report

Cnst,Var,Abs

Add the above constant variables to the report (e.g. padding bits to byte align for the next data section)



# python代码

这个库看起来操作简单。

https://github.com/ahtn/python-easyhid

对外的类，就2个：

```
HIDDevice
	open()
	close()
	write(data, report_id=0)
	read(size=64, timeout=None)
	set_nonblocking(block)
	is_open()
	is_connected()
	send_feature_report(data, report_id=0)
	get_feature_report(size, report_id=0)
	get_error()
	get_manufactory_string()
	get_production_string()
	get_serial_number()
	get_indexed_string()
	description()
	
Enumeration
	这个就2个函数。
	一个是find。
	一个是show。
	代码不长。
```

操作都是对hdiapi.dll里的函数的调用。

使用cffi来跟C混合编程。

总体上看起来比较简单。

例如读取鼠标数据为例，应该怎样操作呢？



板子到之后，就开始研究HID通信。

客户发来一个工具读取参数的，可与设备正常通信。

不过自编写的代码读取不到参数。

重新研究HID协议，安装bus hound抓USB包，对照协议分析报文，对HID有一点认识。

深入跟踪hidapi库源码，发现打开USB设备时出错，具体来说，枚举阶段，以读的方式打开，其后使用读写方式，但失败，返回ERROR_ACCESS_DENIED（错误码为5L），于是再使用读方式打开，成功。

于是怀疑是因为读写方式打开失败的原因。

网上说windows10系统不让以读写方式打开HID，切换win7虚拟机，测试，效果一样。

在Linux系统用root权限跑同样代码，却正常。一度陷入困境。





Windows使用HID通信相对比较简单，HID都是通过PID、VID信息来查找连接的，相比于串口，几乎无变化，连接无需人工选择，十分方便，也不需要驱动。

本实例将HID接口分成3层，支持自动连接、断开状态通知，异步收发数据，单个数据包大小为64bytes（因为从设备的数据包设定为64bytes，保持一致）。



feature report 收发：
1、hid_get_feature_report：获取 Feature report。
2、hid_send_feature_report：发送 Feature report。

读写：
1、hid_read：读取数据 Input report。
2、hid_write：写数据 Output report。





这里是一个命令行工具。

https://github.com/OpenAcousticDevices/USB-HID-Tool

参数是vid、pid和64字节的数据。

Linux下默认不允许hid写入。



# hid数据格式

现在让我很困惑的，就是用工具下发是可以的。

我把工具下发的数据，填到代码里下发就不行。

工具应该是多封装了一些信息。那么是多封装了哪些信息呢？

还是在windows上用hidapi的官方例子编译测试看看。

如果可以，下发命令就用C语言来写。通过python里调用命令来发送。

找到问题所在了。是因为发送的长度不对。

应该发送61字节。最前面是report id。当前设备的report id是0x24 。

用下面的代码可以正常发送。

这个是问了设备端的人员才知道的。关键就是report的长度。

```
    write_data=bytearray(60)
    write_data[0] = 0xf0
    len = dev.send_feature_report(write_data,report_id=0x24)
```



# Linux下hid调试

现在在windows下找不到思路。

在Linux下看看。

我的笔记本，只接了一个usb鼠标。

在/sys/kernel/debug/hid下面都有暴露对应的调试接口，从这边我们可以结合hidrd工具来获取他们的HID报告描述符。

该目录下，有一个目录。

```
0003:046D:C077.0001
```

下面有2个只读文件。

```
events  rdesc
```

cat events，然后移动鼠标。就可以看到打印。

```
report (size 4) (unnumbered) =  00 fa 00 00
Button.0001 = 0
Button.0002 = 0
Button.0003 = 0
Button.0003 = 0
Button.0003 = 0
Button.0003 = 0
Button.0003 = 0
Button.0003 = 0
GenericDesktop.X = -6
GenericDesktop.Y = 0
GenericDesktop.Wheel = 0
```

rdesc的内容：后面的文本部分是对前面hex数据的解释。

```
root@thinkpad:/sys/kernel/debug/hid/0003:046D:C077.0001# cat rdesc 
05 01 09 02 a1 01 09 01 a1 00 05 09 19 01 29 03 15 00 25 01 95 08 75 01 81 02 05 01 09 30 09 31 09 38 15 81 25 7f 75 08 95 03 81 06 c0 c0 

  INPUT[INPUT]
    Field(0)
      Physical(GenericDesktop.Pointer)
      Application(GenericDesktop.Mouse)
      Usage(8)
        Button.0001
        Button.0002
        Button.0003
        Button.0003
        Button.0003
        Button.0003
        Button.0003
        Button.0003
      Logical Minimum(0)
      Logical Maximum(1)
      Report Size(1)
      Report Count(8)
      Report Offset(0)
      Flags( Variable Absolute )
    Field(1)
      Physical(GenericDesktop.Pointer)
      Application(GenericDesktop.Mouse)
      Usage(3)
        GenericDesktop.X
        GenericDesktop.Y
        GenericDesktop.Wheel
      Logical Minimum(-127)
      Logical Maximum(127)
      Report Size(8)
      Report Count(3)
      Report Offset(8)
      Flags( Variable Relative )

Button.0001 ---> Key.LeftBtn
Button.0002 ---> Key.RightBtn
Button.0003 ---> Key.MiddleBtn
Button.0003 ---> Key.SideBtn
Button.0003 ---> Key.ExtraBtn
Button.0003 ---> Key.ForwardBtn
Button.0003 ---> Key.BackBtn
Button.0003 ---> Key.TaskBtn
GenericDesktop.X ---> Relative.X
GenericDesktop.Y ---> Relative.Y
GenericDesktop.Wheel ---> Relative.Wheel
```



# 参考资料

1、

https://pypi.org/project/hid/

2、How to Determine where to install hidapi.dll?

https://stackoverflow.com/questions/62620247/how-to-determine-where-to-install-hidapi-dll

3、Using Python and the hidapi library with ADU USB Data Acquisition Products (Linux & OS X)

https://www.ontrak.net/pythonhidapi.htm

4、USB HID 设备类协议入门

https://blog.csdn.net/phenixyf/article/details/7580286

5、

https://my.oschina.net/micropython/blog/2996027

6、浅析几种HID硬件攻击

https://zhuanlan.zhihu.com/p/37659947

7、HID 简介

这个系列文章不错。

https://www.bytekits.com/hid/hid-intro.html

8、HID 应用程序编程接口 (API)

https://docs.microsoft.com/zh-cn/windows-hardware/drivers/hid/introduction-to-hid-concepts

9、Bus Hound使用步骤

https://jingyan.baidu.com/article/6525d4b194f5beac7c2e9467.html

10、如何查看BUSHOUND内容

https://blog.csdn.net/yu704645129/article/details/38819437

11、USB之HID类Set_Report Request[调试手记1]

http://www.cnblogs.com/libra13179/p/7365910.html

12、

https://eleccelerator.com/tutorial-about-usb-hid-report-descriptors/

13、

https://www.cnblogs.com/libra13179/p/6840049.html

14、STM32 USB HID的GET_REPORT 与 SET_REPORT请求

https://blog.csdn.net/xqhrs232/article/details/79525793

15、Python device Examples

https://python.hotexamples.com/examples/hid/-/device/python-device-function-examples.html

16、USB HID学习：一点开发记录

https://www.latelee.org/programming-under-windows/usb-note-develop-record.html

17、

https://blog.csdn.net/encourage2011/article/details/43603889

18、

https://www.cnblogs.com/xiaowuyi/p/5677827.html

19、【C#】HID API

https://www.cnblogs.com/beatfan/p/13624778.html

20、Python PyUSB HID Feature Report

https://stackoverflow.com/questions/35162889/python-pyusb-hid-feature-report

21、

https://my.oschina.net/u/3846209/blog/1805792