---
title: usb（四）Linux驱动代码
date: 2018-04-05 11:35:27
tags:
	- usb
typora-root-url: ../
---

--

# 高质量的系列文章

这个作者的linux usb系列文章，值得反复看，写得很全面了。

https://www.cnblogs.com/zyly/category/2340692.html

# 摸索

代码在linux/drivers/usb目录下。这里有一个README文件，我们看看。

这个README给了我们一些提示：

```
要理解linux里的usb框架，你需要这些资源：
1、源代码。make pdfdocs，然后阅读usb.pdf文件，这个是host的，gadget.pdf是外设端的。Documentation下的usb目录下有更多信息。
2、usb2.0规范。
3、芯片手册的usb控制器部分。
```



usb子系统的入口函数是在 core/usb.c里。

这个是subsys_init调用的。

usb_init函数内容：

```
1、usb_debugfs_init。
2、bus_register(&usb_bus_type)
3、bus_register_notifier(&usb_bus_type, &usb_bus_nb);
4、usb_major_init(); usb的major是180 ，是字符设备。
5、usb_register(&usbfs_driver);
6、usb_devio_init();
7、usbfs_init();
8、usb_hub_init();
9、usb_register_device_driver(&usb_generic_driver, THIS_MODULE);
```

我们还是以mini2440的，4.4版本的内核来进行分析。

在bsp文件里。

```
static struct platform_device *mini2440_devices[] __initdata = {
	&s3c_device_ohci,
	&s3c_device_wdt,
	&s3c_device_i2c0,
	&s3c_device_rtc,
	&s3c_device_usbgadget,//usb相关的就是这。
```

```
static struct resource s3c_usbgadget_resource[] = {
	[0] = DEFINE_RES_MEM(S3C24XX_PA_USBDEV, S3C24XX_SZ_USBDEV),
	[1] = DEFINE_RES_IRQ(IRQ_USBD),
};
```

寄存器在0x5200 0000处，范围是1M。中断号是S3C2410_IRQ(25) 。

otg设备也看到有定义，但是默认是不选配的。不管。



在用户看来，usb设备为主机提供了多种多样的附加功能。

但是对于usb主机来说，它跟usb设备的接口都是一样的。

一个usb设备由3个功能模块组成：

1、usb总线接口。

2、usb逻辑设备。

3、功能单元。

为了更好地描述usb设备的特征，usb协议里提出了一个设备架构的概念。

从这个概念出发，可以认为usb设备是由一些配置、接口、端点构成。

也就是说，一个usb设备可以含有一个或者多个配置，每个配置对应一个或者多个接口，一个接口对应多个端点。

配置和接口都是抽象概念，实际的数据传输由端点完成。

在使用usb设备之前，必须指明使用的配置和接口，这个一般在枚举的时候，就完成了。

层次关系是这样的。

![usb（四）-图1](/images/usb（四）-图1.png)

我们看这些概念在内核里的结构体分别是怎么样的。

# Linux usb驱动的框架描述

Linux USB驱动的框架是由多个组件构成的，其中包括核心USB驱动、USB设备驱动以及USB主机控制器驱动。这些组件共同协作，使得Linux系统能够管理和控制USB设备。

1. **USB核心驱动**：USB核心驱动提供了与USB总线通信的基本功能。它管理USB设备的探测、配置和数据传输等任务。该核心驱动提供了访问USB设备的接口，使得设备驱动程序能够注册自己并与USB总线进行通信。

2. **USB设备驱动**：每个连接到系统的USB设备都需要相应的设备驱动程序来进行控制和通信。这些设备驱动程序负责处理特定类型的USB设备，例如存储设备、键盘、鼠标等。它们与USB核心驱动交互以实现对设备的操作。

3. **USB主机控制器驱动**：USB主机控制器驱动管理物理USB总线控制器，负责和USB设备进行通信。这些驱动程序针对特定类型的硬件控制器，例如EHCI、OHCI、xHCI等，并提供统一的接口供USB核心驱动使用。

4. **USB层次结构**：USB驱动的层次结构允许系统与USB设备进行通信，并提供了一系列抽象层次，从物理硬件层到逻辑设备驱动层的管理。

在Linux系统中，这些驱动程序通常以模块的形式存在，可以在需要时加载和卸载。此外，Linux内核提供了丰富的API和工具，帮助开发人员编写和调试USB驱动程序，使其能够与系统正常交互并正确控制USB设备。

# Linux usb驱动的发展历史

Linux USB驱动的发展历史可以追溯到Linux内核的早期阶段。USB驱动的发展经历了多个阶段和改进：

1. **早期支持（1990年代末 - 2000年代初）**：在Linux内核较早的版本中，USB支持还比较有限。仅支持一些基本的USB设备，例如键盘、鼠标等。这个阶段的驱动开发主要关注于实现对基本USB设备的支持。

2. **USB 2.0时代（2000年代初 - 中期）**：随着USB 2.0标准的普及，Linux开始加强对高速USB 2.0设备的支持。内核中新增了更多的USB驱动程序，以支持更多种类的设备，例如存储设备、摄像头、打印机等。

3. **功能扩展和改进（2010年代）**：随着技术的发展，USB标准不断演进，引入了新的功能和性能提升，例如USB 3.0和USB 3.1。Linux内核持续改进USB驱动，以支持新的USB标准和更高的传输速率，同时增加对更多USB设备类型的支持。

4. **持续改进和增强（目前）**：到了当前，Linux内核持续不断地改进USB子系统，以适应不断变化的USB标准和新型设备的出现。这包括对USB Type-C、USB 4.0等新标准的支持，同时也在增强USB驱动的稳定性、性能和兼容性。

USB驱动的发展是一个持续不断的过程，Linux社区与硬件制造商合作，共同努力以确保Linux系统能够良好地支持各种USB设备，并不断推动USB技术在Linux平台上的发展。

# 设备描述符

struct usb_device_descriptor

```
1. u8 bLength //描述符长度。
2. u8 bDescriptorType  //描述符类型。
3. u16 bcdUSB //usb版本
4. u8 bDeviceClass //设备类。
5. u8 bDeviceSubClass //设备子类。
6. u8 bDeviceProtocol //协议。
7. u8 bMaxPacketSize0 //endpoint0的最大包的大小。
8. u16 idVendor //厂商
9. u16 idProduct //产品编号。
10. u16 bcdDevice //设备出厂编号。
11. u8 iManufacturer //厂商字符串索引。
12. u8 iProduct //产品字符串索引。
13. u8 iSerialNumber //序列化索引。
14. u8 bNumConfigurations //可能的配置数量。
```

设备描述符（Device Descriptor）是USB设备中最基本的描述符之一，

它包含了关于设备本身的重要信息，并在USB通信中起着关键的作用：

1. **唯一识别设备**：设备描述符包含厂商ID（Vendor ID）和产品ID（Product ID），==这些信息可以唯一地识别一个USB设备。==当设备连接到计算机时，计算机会使用这些ID来确定设备的身份，以便加载适当的驱动程序。

2. **确定设备类别和协议**：设备描述符中包含设备的类别信息，比如设备是存储设备、音频设备还是人机接口设备等。这有助于操作系统识别设备的功能和所需的驱动程序。

3. **设备配置和管理**：设备描述符指明了设备支持的USB规范版本，最大包大小（Max Packet Size）等参数，这些信息对于操作系统配置和管理USB设备非常重要。

4. **与USB架构交互**：设备描述符是USB架构中的基本组成部分，它与其他描述符（如配置描述符、接口描述符等）共同构成了USB设备的信息框架。==操作系统通过读取设备描述符来理解设备的能力和特性==，以便正确地配置和管理设备。

总的来说，设备描述符提供了关键的元数据，帮助操作系统正确识别、配置和与USB设备进行通信。它是设备和主机之间进行协商、建立通信的重要桥梁之一。

# 配置描述符

一个设备对应多个配置。

相当于蓝牙里的profile的意思。

struct usb_config_descriptor

```
1. u8 bLength //描述符长度。
2. bDescriptorType //描述符类型。
3. u16 wTotoalLenght //配置返回的所有数据的大小。
4. u8 bNumInterface //配置所支持的接口数。
5. u8 bConfigurationValue //参数值。
6. u8 iConfiguration //描述该配置的字符串的索引值。
7. u8 bmAttributes //供电模式的选择。
8.78 bMaxPower //设备从总线提取的最大电流。
```

配置描述符（Configuration Descriptor）是USB设备描述符中的一个部分，它承载了关于设备配置信息的重要内容。其作用包括以下几点：

1. **描述设备的不同配置**：USB设备可以支持多种不同的工作配置。配置描述符允许设备定义其可用的不同工作状态。每个配置可以有不同的属性、接口和端点设置。

2. **指定设备的功率需求**：配置描述符包含有关配置的最大功率需求信息。这对于USB总线的管理和功率分配是至关重要的，以确保设备在连接时能够获得足够的电力供应。

3. **配置设备的接口和端点**：每个配置描述符可以包含一个或多个接口描述符，从而定义了设备支持的接口数量和类型。它们描述了设备上的不同功能、接口的类别、子类别和协议信息，以及端点的数目和类型。

4. **确定设备支持的功能和特性**：通过配置描述符，操作系统可以了解设备所支持的不同功能和特性，以便正确地为设备配置驱动程序和资源。

5. **管理设备状态转换**：配置描述符使得设备可以切换不同的工作状态，例如在不同的工作模式下运行。主机可以请求设备切换到特定的配置，以满足不同的需求或实现不同的功能。

配置描述符是设备描述符中的重要部分，它提供了有关设备不同工作状态和属性的信息，帮助主机正确配置和管理USB设备。

# 接口描述符

struct usb_interface_descriptor

```
1. u8 bLength // 描述符的长度。
2. u8 bDescriptorType //描述符类型。
3. u8 bInterfaceNumber //接口的编号。
4. u8 bAlternateSetting //备用的接口描述符编号。
5. u8 bNumEndpoints // 该接口使用的端点数，不包括端点0 。
6. u8 bInterfaceClass //接口类型
7. u8 bInterfaceSubClass //接口子类型。
8. u8 bInterfaceProtocol //接口协议。
9. u8 iInterface // 描述该接口的字符串的索引值。
```

接口描述符（Interface Descriptor）是USB设备描述符中的一部分，它提供了关于设备上单个接口的详细信息。每个USB设备可以包含一个或多个接口，每个接口可以代表设备上的一个功能单元。

以下是接口描述符的主要作用和内容：

1. **描述设备功能**：接口描述符定义了设备上的一个功能单元，它可以表示设备的一个特定功能，比如音频输入、打印服务等。一个USB设备可能包含多个接口，每个接口对应不同的功能。

2. **指定接口的类别和协议**：描述了接口的类别、子类别和协议信息，帮助主机操作系统正确地识别和管理接口，以便加载适当的驱动程序。

3. **定义端点及传输方式**：接口描述符中包含了关于该接口所使用的端点的信息，包括端点的数量、端点类型（控制、批量、中断、等等）、最大包大小等。这些信息对于数据传输方式的定义非常重要。

4. **唯一标识接口**：接口描述符中包含了接口的编号，这有助于主机操作系统识别和区分设备上不同的功能单元。

接口描述符是USB设备描述符中的重要组成部分，它提供了有关设备上单个功能的详细信息，帮助主机正确地配置和管理USB设备，以实现对设备功能的控制和数据交换。

# 端点描述符

struct usb_endpoint_descriptor

```
1. u8 bLength //
2. u8 bDescriptorType //
3. u8 bEndpointAddress //端点地址，0到3位是端点好，bit7是方向（0：out，1：in）。
4. u8 bmAttributes // 端点属性。
5. u16 wMaxPacketSize //本端点的最大信息包的大小。
6. u8 bInterval //轮询数据传送端点的时间间隔。
7. u8 bRefresh //
8. u8 bSynchAddress //
```

**USB**端点:

USB设备与主机会有若干个通信的”端点”,

每个端点都有个端点号,

除了端点0外，

每一个端点只能工作在一种传输类型(控制传输、中断传输、批量传输、实时传输)下,一个传输方向下

**传输方向都是基于USB主机的立场说的,**

比如:鼠标的数据是从鼠标传到PC机, 对应的端点称为"中断输入端点"

其中端点0是设备的默认控制端点, 既能输出也能输入,用于USB设备的识别过程



# 字符串描述符

struct usb_string_descriptor

```
1. u8 bLength //
2. u8 bDescriptorType //
3. u16 wData[1]
```

上面这些描述符都在include/uapi/linux/usb/ch9.h里。

**之所以叫ch9.h，是因为这些内容是根据usb协议文档第9章写的。**

上面这些描述符都要声明为pack的，不能被编译器对齐。

**还定义了一个描述符头部的结构体。因为所有描述符的最前面都是这2个成员。**

```
struct usb_descriptor_header {
	__u8  bLength;
	__u8  bDescriptorType;
} __attribute__ ((packed));
```

这些描述符都是内部的，外部不会用到的。



# 怎样编写一个usb驱动？

跟i2c这些总线的驱动类型。

我们以usb/host/ohci-s3c2410.c的为例来看。

usb默认提供了一个drivers/usb/usb-skeleton.c 的文件，来给大家做参考。

核心就是定义实现这个结构体。

```
static struct usb_driver skel_driver = {
	.name =		"skeleton",
	.probe =	skel_probe,
	.disconnect =	skel_disconnect,
	.suspend =	skel_suspend,
	.resume =	skel_resume,
	.pre_reset =	skel_pre_reset,
	.post_reset =	skel_post_reset,
	.id_table =	skel_table,
	.supports_autosuspend = 1,
};
```



# urb结构体

这个是usb通信过程中的包。

usb request block。



# OHCI等概念辨析

linux的usb驱动有ohci、ehci、uhci、fhci、xhci这5个东西，名字看起来差不多，具体代表了什么含义，有什么区别，我们怎么选择。

ehci：为usb2.0提供支持。也是Intel主导的。

ohci：一个不仅仅是usb用的host控制器标准。嵌入式上用。

uhci：Intel在pc上的。与ohci不兼容。

xhci：usb3.0用的。



ochi、uhci都是usb1.1的接口。

ehci是usb2.0的接口。

xhci是usb3.0的接口。



要想成为一个USB主机,硬件上就必须要有USB主机控制器才行,USB主机控制器又分为4种接口:

**OHCI（Open Host Controller Interface）:** 微软主导的低速USB1.0(1.5Mbps)和全速USB1.1(12Mbps),OHCI接口的软件简单,硬件复杂  

**UHCI（Universal Host Controller Interface）:** Intel主导的低速USB1.0(1.5Mbps)和全速USB1.1(12Mbps), 而UHCI接口的软件复杂,硬件简单  

**EHCI（Enhanced Host Controller Interface）：**高速USB2.0(480Mbps),

**xHCI（eXtensible Host Controller Interface）：**USB3.0(5.0Gbps),采用了9针脚设计,同时也支持USB2.0、1.1等



2440用的就是ohci的。

```
#define CONFIG_USB_OHCI_HCD 1
```

开机打印是这样的：

```
ohci_hcd: USB 1.1 'Open' Host Controller (OHCI) Driver
ohci-s3c2410: OHCI S3C2410 driver
s3c2410-ohci s3c2410-ohci: OHCI Host Controller
s3c2410-ohci s3c2410-ohci: new USB bus registered, assigned bus number 1
s3c2410-ohci s3c2410-ohci: irq 42, io mem 0x49000000
s3c2410-ohci s3c2410-ohci: init err (00000000 0000)
```

对应的文件是usb/host/ohci-hcd.c。



# 代码阅读

ohcu_hcd是usb_hcd的一个实例。

需要重点看的文件是ohci-hcd.c和ohci-s3c2410.c。

ohcd-hcd.c里include了不少的c文件。

```
#include "ohci-hub.c"
#include "ohci-dbg.c"
#include "ohci-mem.c"
#include "ohci-q.c"
```



# 看usbled.c文件

这个因为功能很简单。所以适合作为分析的对象。在usb/misc目录下。

1、首先要看的就是usb_device_id。

```
#define VENDOR_ID	0x0fc5
#define PRODUCT_ID	0x1223

/* table of devices that work with this driver */
static const struct usb_device_id id_table[] = {
	{ USB_DEVICE(VENDOR_ID, PRODUCT_ID) },
	{ },
};
```

2、probe函数。

这个是在枚举之后，根据usb_deivce_id来调用的。

3、断开disconnect函数。

4、数据传输。这里的输出传输很简单，就是控制led灯的颜色。

用的函数是usb_control_msg。

在usb/core/message.c里。这里就是usb协议相关的东西了。



对外头文件：

linux/usb.h。

对外结构体：

```
struct usb_device_id
```







主要接口函数
usb_register



# 什么是udc驱动

udc驱动跟Function驱动对应。



USB设备控制器（UDC）驱动

指的是作为其他USB主机控制器外设的USB硬件设备上底层硬件控制器的驱动，

该硬件和驱动负责将一个USB设备依附于一个USB主机控制器上。

```
usb device --attach-> usb host 
```



例如，当某运行Linux系统的手机作为PC的U盘时，

手机中的底层USB控制器行使USB设备控制器的功能，

这时运行在底层的是UDC驱动，

手机要成为U盘，在UDC驱动之上需要另外一个驱动，

对于USB大容量存储器而言，这个驱动为File Storage驱动，称为**Function驱动**。

https://codeantenna.com/a/yBnF5eY6DJ



1、usb_gadget表示一个从机设备(UDC + 端点)，它包含一些端点(包括端点0和其他端点)。所以它有一个端点列表成员ep_list， 初始化过程中会将所有需要的端点放到该链表中。

2、 usb_gadget_ops主要用来操作UDC。

3、 usb_ep表示一个端点，每个端点都有自己的操作函数usb_ep_ops。

4、 usb_ep_ops主要用来操作端点。



udc驱动，就是操作soc的芯片的寄存器的实现。





https://www.cnblogs.com/lifexy/p/7631900.html

# **USB可以热插拔的硬件原理**

在USB集线器(hub)的每个下游端口的D+和D-上，分别接了一个15K欧姆的下拉电阻到地。这样，在集线器的端口悬空时，就被这两个下拉电阻拉到了低电平。

而在USB设备端，在D+或者D-上接了1.5K欧姆上拉电阻。对于全速和高速设备，上拉电阻是接在D+上；而低速设备则是上拉电阻接在D-上。这样，当设备插入到集线器时，由1.5K的上拉电阻和15K的下拉电阻分压，结果就将差分数据线中的一条拉高了。集线器检测到这个状态后，它就报告给USB主控制器（或者通过它上一层的集线器报告给USB主控制器），这样就检测到设备的插入了。USB高速设备先是被识别为全速设备，然后通过HOST和DEVICE两者之间的确认，再切换到高速模式的。**在高速模式下，是电流传输模式，这时将D+上的上拉电阻断开。**



# dwc2是什么

 dwc2就是usb2.0的一个控制器，dw是DesignWare是一个IP核设计公司。

DWC代表的确实是DesignWare USB IP Core的缩写，它来自Synopsys公司。

DesignWare是Synopsys提供的一系列IP核的品牌，

而DWC是其中专门用于USB功能的IP核。

这些IP核可以用于在芯片设计中集成USB控制器、PHY和其他与USB通信相关的功能。

参考资料

1、

https://blog.csdn.net/huohongpeng/article/details/116267891

# crg是什么

crg是芯源的代号。也是一家USB IP核厂家。跟dwc是对等的。



# kernel里重要的usb相关配置

```
CONFIG_USB_HID=y
CONFIG_USB_HIDDEV=y
CONFIG_USB_OHCI_LITTLE_ENDIAN=y
CONFIG_USB_SUPPORT=y
CONFIG_USB_COMMON=y
CONFIG_USB_ARCH_HAS_HCD=y
CONFIG_USB=y
CONFIG_USB_PCI=y
CONFIG_USB_ANNOUNCE_NEW_DEVICES=y

CONFIG_USB_STORAGE=y
CONFIG_USB_DWC3=y
CONFIG_USB_DWC3_DUAL_ROLE=y

CONFIG_USB_PHY=y

CONFIG_USB_LIBCOMPOSITE=y
CONFIG_USB_U_ETHER=y
CONFIG_USB_F_RNDIS=y
CONFIG_USB_F_FS=y
CONFIG_USB_F_ACC=y
CONFIG_USB_CONFIGFS=y
CONFIG_USB_CONFIGFS_UEVENT=y
CONFIG_USB_CONFIGFS_F_FS=y
CONFIG_USB_CONFIGFS_F_ACC=y

CONFIG_AMLOGIC_USB=y
CONFIG_AMLOGIC_USB_DWC_OTG_HCD=y
CONFIG_AMLOGIC_CRG=y
```

# linux内核代码里的usb相关代码分布

Linux内核中的USB相关代码通常位于以下几个主要位置：

1. **drivers/usb/** 目录：这是最主要的USB驱动代码目录，其中包含了许多子目录，每个子目录对应不同类型的USB设备或功能。
- **drivers/usb/core/**：这个目录包含USB核心驱动代码，处理USB总线的基本功能，包括USB设备的探测、管理、驱动模型等。
    
    - **drivers/usb/host/**：这里包含了USB主机控制器驱动程序，用于管理USB总线上的主机控制器（例如EHCI、OHCI、xHCI等）。
    
    - **drivers/usb/storage/**：包含了USB存储设备的驱动程序，用于支持USB存储设备（如闪存驱动器、外置硬盘等）。
    
    - **drivers/usb/input/**：包含了USB输入设备的驱动程序，用于支持USB键盘、鼠标等输入设备。
    
    - **drivers/usb/misc/**：包含了一些其他类型的USB设备的驱动程序，例如USB摄像头、USB网卡等。
    
2. **include/linux/usb/** 目录：这个目录包含了USB子系统的头文件，定义了USB设备描述符、请求类型、USB控制请求等数据结构和宏定义。

3. **drivers/usb/gadget/** 目录：这个目录包含了USB gadget驱动程序，用于实现Linux作为USB设备的功能，允许Linux设备模拟为USB设备（如USB存储设备、网络适配器等）。

4. **Documentation/usb/** 目录：这里包含了关于Linux内核中USB子系统的文档，提供了对USB驱动程序开发的一些指导和说明。

这些目录包含了Linux内核中与USB相关的核心驱动、设备驱动、USB设备功能模拟以及与USB通信相关的头文件和文档。在这些目录中，你可以找到许多不同类型的USB设备驱动程序的源代码，可以根据需要阅读、学习或修改。

# usb的configfs主要作用是什么？

`configfs` 是一个用于配置USB gadget的内核配置文件系统，它允许用户空间动态创建和配置USB gadget，并且可以与USB设备进行通信。主要作用包括：

1. **USB Gadget 配置**：configfs允许用户动态创建和配置USB Gadget，这些Gadget可以模拟各种USB设备类型（如存储设备、网络适配器等）。用户可以通过修改配置文件来定义Gadget的属性和行为，例如描述符、端点、接口等。

2. **无需重新编译内核**：传统上，配置和使用USB gadget需要在内核配置中静态定义。而使用configfs，可以在运行时动态创建和配置Gadget，无需重新编译内核。这使得USB gadget的开发和测试更加灵活和方便。

3. **与用户空间通信**：configfs通过文件系统接口与用户空间进行通信。用户可以通过在configfs中读写配置文件，来配置USB gadget的参数和属性。这种方式提供了一种简单而直观的接口，便于用户与USB gadget进行交互。

4. **支持虚拟文件系统**：configfs创建了一个虚拟文件系统，以文件和目录的方式来表示USB gadget的不同配置和属性。用户可以通过文件系统的方式轻松地浏览和修改配置。

5. **灵活性和扩展性**：configfs提供了一种灵活和可扩展的方式来配置和管理USB gadget，使得对于需要频繁更改或动态配置的场景非常有用。

总的来说，configfs允许动态创建、配置和管理USB Gadget，为用户提供了一种灵活、可扩展的方式来模拟和控制USB设备，而无需重新编译内核。

# USB gadget是什么

USB Gadget 是一种允许 Linux 设备模拟 USB 设备功能的框架。

它允许 Linux 设备作为 USB 设备工作，而不是传统的 USB 主机。

==通过 USB Gadget 框架，Linux 设备可以模拟各种 USB 设备类型，==

比如 USB 存储设备、键盘、鼠标、网络适配器等。

USB Gadget 框架的关键部分包括：

1. **Gadget 驱动**：这些是 Linux 内核中的模块，允许设备实现特定类型的 USB 功能。例如，g_mass_storage 可以让 Linux 设备模拟 USB 存储设备。

2. **FunctionFS（Function Filesystem）**：这是一种用户空间工具，允许用户配置 Gadget 功能。FunctionFS 允许用户空间程序像操作文件一样与 USB Gadget 进行通信。

USB Gadget 使得 Linux 设备能够以不同的方式与其他 USB 设备进行通信。这对于模拟特定类型的 USB 设备、测试 USB 驱动程序、进行嵌入式开发以及设备连接等方面非常有用。例如，一个嵌入式系统可以使用 USB Gadget 框架模拟 USB 存储设备来与计算机进行文件传输，或者模拟 USB 网络适配器来进行网络连接。

# Linux usb一次通信过程描述

USB在Linux中的一次通信过程涉及多个步骤，主要分为设备探测、配置和数据传输阶段。以下是典型的USB通信过程的主要步骤：

### 1. 设备探测和初始化

1. **设备连接**：当USB设备插入到主机上时，USB总线会检测到新的设备连接事件。
2. **设备探测**：内核识别并探测新连接的设备，尝试匹配已加载的驱动程序或加载适当的驱动来管理该设备。
3. **分配资源**：内核分配资源给设备，为设备的操作分配内存空间、分配中断等。

### 2. 配置和描述符获取

1. **获取描述符**：==内核通过控制传输请求，从设备中获取设备描述符、配置描述符和其他相关描述符，以了解设备的能力和特性。==
2. **配置设备**：根据设备描述符和配置描述符的信息，内核配置设备，准备好与设备进行通信。

### 3. 数据传输

1. **数据交换**：根据设备的类型和应用需求，进行数据传输。
    - **控制传输**：用于配置和管理设备，例如读取设备描述符、设置设备属性等。
    - **批量传输**：大块数据的传输，通常用于存储设备等。
    - **中断传输**：周期性、低延迟的小数据传输，例如鼠标、键盘等。
    - ==**等时传输**：实时性要求较高的传输，如音频、视频等。==

2. **USB数据包处理**：内核处理USB传输过程中的数据包，包括将数据打包成USB数据包、错误检测和纠正等。

3. **数据传输完成**：数据传输完成后，内核可能会释放相应的资源，如断开与设备的连接、释放分配的内存等。

在整个USB通信过程中，内核负责管理USB设备的配置、数据传输和资源分配。这些步骤可以根据特定的设备类型和应用需求略有不同，但这个过程展示了在Linux中典型的USB通信流程。

# linux内核里usb相关的重要结构体有哪些

在 Linux 内核中，USB 子系统涉及许多重要的结构体，用于表示和管理 USB 设备、端点、请求等。以下是其中一些重要的结构体：

1. **usb_device**：表示一个 USB 设备，包含设备的基本信息，如设备描述符、配置、接口等。该结构体定义在 `include/linux/usb.h` 中。

2. **usb_interface**：表示 USB 设备上的一个接口，包含接口描述符和相关的端点信息。该结构体定义在 `include/linux/usb.h` 中。

3. **usb_endpoint_descriptor**：表示 USB 端点的描述符，包含有关端点的属性，如端点地址、传输类型、最大包大小等信息。该结构体定义在 `include/uapi/linux/usb/ch9.h` 中。

4. **usb_host_endpoint**：表示 USB 主机端点，用于管理和操作 USB 主机端点相关的数据结构。该结构体定义在 `include/linux/usb.h` 中。

5. **usb_request**：表示 USB 传输请求，用于向 USB 设备发送或接收数据。该结构体定义在 `include/linux/usb.h` 中。

6. **usb_driver**：表示 USB 设备驱动程序，包含设备驱动的注册和初始化函数等。该结构体定义在 `include/linux/usb.h` 中。

7. **usb_device_id**：用于匹配 USB 设备和设备驱动程序之间的映射关系，用于设备驱动程序的识别和绑定。该结构体定义在 `include/linux/usb.h` 中。

这些结构体在 Linux 内核中扮演着重要角色，用于描述和管理 USB 设备的各个方面。它们提供了对 USB 设备、接口、端点等不同层面的抽象和管理，为 USB 子系统的操作和驱动提供了必要的数据结构和接口。

# linux内核里usb相关的api函数有哪些

| 函数                                                         | 说明                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| usb_control_msg                                              |                                                              |
| usb_sndctrlpipe                                              |                                                              |
| usb_autopm_put_interface                                     |                                                              |
| usb_autopm_get_interface                                     |                                                              |
| to_usb_interface                                             |                                                              |
| usb_get_intfdata<br />usb_set_intfdata                       |                                                              |
| usb_get_dev                                                  |                                                              |
| usb_find_common_endpoints                                    |                                                              |
| usb_endpoint_maxp                                            |                                                              |
| usb_register_dev                                             |                                                              |
| usb_register_driver<br />usb_register<br />usb_deregister    | 这2个register的是一样的，都是注册驱动。<br />usb_register是对usb_register_driver的宏定义简单版本。 |
| usb_register_device_driver<br />usb_deregister_device_driver | 参数是usb_device_driver                                      |
| usb_register_dev<br />usb_deregister_dev                     | 参数是usb_interface                                          |

urb相关的函数

| 函数                                 | 说明 |
| ------------------------------------ | ---- |
| usb_fill_control_urb                 |      |
| usb_fill_bulk_urb                    |      |
| usb_fill_int_urb                     |      |
| usb_init_urb                         |      |
| usb_alloc_urb<br />usb_free_urb      |      |
| usb_put_urb<br />usb_get_urb         |      |
| usb_submit_urb                       |      |
| usb_unlink_urb                       |      |
| usb_kill_urb                         |      |
| usb_poison_urb<br />usb_unpoison_urb |      |
| usb_block_urb                        |      |
| usb_urb_dir_in<br />usb_urb_dir_out  |      |
|                                      |      |



# usb/misc下面的设备分析

| 文件名     | 说明                       |
| ---------- | -------------------------- |
| usb251xb.c | usb hub                    |
| usb3503.c  | usb hub                    |
| usb4604    | usb hub                    |
| usblcd     | usb接口的显示屏            |
| usbsevseg  | usb接口的七段数码管        |
| usbtest    | 一个测试设备？用来demo的？ |

# struct usb_device_id 作用

`struct usb_device_id` 是 Linux 内核中==用于 USB 设备驱动匹配==的数据结构。

它在 USB 驱动程序中扮演着重要的角色，用于标识和匹配特定的 USB 设备与相应的驱动程序。

这个结构体定义了一组用于描述 USB 设备的标识符，

包括 USB 设备的厂商ID、产品ID、设备类别、子类别、协议等信息。

这些信息可以帮助内核确定特定的 USB 设备类型，并将其与适当的驱动程序进行匹配。



在编写 USB 设备驱动程序时，开发者会创建一个或多个`struct usb_device_id` 实例，并在其中填入要匹配的 USB 设备的信息。

然后，这些信息将被注册到 USB 设备驱动程序中，内核会使用这些信息来确定与其相匹配的驱动程序。

当新的 USB 设备连接到系统时，内核会检查设备的信息，并尝试将其与已注册的驱动程序进行匹配。如果设备的描述符与某个`usb_device_id` 结构中的信息匹配，内核会加载相应的驱动程序来管理和控制这个设备。

因此，`struct usb_device_id` 在 USB 驱动开发中用于设备与驱动的匹配，是 Linux 内核中实现 USB 设备驱动匹配机制的重要数据结构之一。

# usb插入时，设备驱动加载的过程分析

当一个USB设备被插入到计算机的USB端口中时，系统会触发一系列事件，导致设备驱动程序的加载和设备的配置。以下是USB设备插入时设备驱动加载的基本过程：

1. **设备插入检测**：
   - USB总线控制器检测到新的设备插入。
   - 操作系统的USB子系统收到插入事件的通知。

2. **设备识别**：
   - USB子系统开始尝试识别插入的设备。
   - 系统读取设备的描述符信息，包括设备的厂商ID、产品ID等。
  
3. **匹配设备驱动**：
   - 内核遍历已加载的设备驱动程序列表或设备ID表。
   - 内核尝试将插入设备的描述符信息与驱动程序的匹配项进行比对。

4. **加载适当的设备驱动**：
   - 如果存在匹配的驱动程序，内核会加载相应的驱动程序。
   - 加载过程可能包括分配资源、初始化设备、注册驱动等操作。

5. **配置设备**：
   - 加载成功的设备驱动可能会对设备进行配置和初始化。
   - 设备可能会被设置为可用状态，以便与系统进行交互。

6. **系统通知**：
   - 系统可能向用户空间发送相应的通知，例如通过udev系统或其他机制发送设备插入通知。

总的来说，当USB设备插入时，操作系统会尝试识别该设备，并通过设备的描述符信息匹配适当的设备驱动程序。如果存在匹配的驱动程序，系统会加载该驱动程序并配置设备，使其能够与系统进行通信和交互。这个过程是由USB子系统和设备驱动程序协同完成的。

# USB总线控制器检测插入是怎么实现的？

USB总线控制器检测设备插入通常==依赖于硬件层面的电气特性和信号传输的变化==。

当一个USB设备被插入到计算机的USB端口时，这些变化会触发USB总线控制器检测到新设备的插入。

具体来说，USB总线控制器会监测USB端口的电压变化和信号线的状态。

当一个设备被插入时，这些状态会发生变化，

触发USB总线控制器发送插入事件的通知给操作系统的USB子系统。

这些状态变化可能包括：

1. **电源状态改变**：USB总线控制器可能会检测到端口电源线上的电压变化，表示有设备被接入或断开。

2. **数据线状态**：USB总线控制器也会检测数据线的状态变化。在USB连接中，数据线的状态变化也是一种指示设备插入或拔出的信号。

3. **信号线上的插入/拔出通知**：有些USB接口设计中，会有专门的信号线用于传输插入/拔出的通知，USB总线控制器会通过这些信号线接收到插入事件的通知。

总的来说，USB总线控制器通过监测USB端口的物理状态变化来检测设备的插入。一旦检测到这些变化，USB控制器会向操作系统的USB子系统发送相应的信号，触发系统对新设备的处理和识别。这个过程在硬件层面和驱动层面共同作用，以便在系统中正确处理新插入的USB设备。

# i2c和usb对比

| 对比项     | i2c                                                          | usb                                                          |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 设备       | i2c_client<br />继承struct device                            | usb_device<br />继承struct device                            |
| 驱动       | i2c_driver<br />继承struct device_driver                     | usb_driver<br />没有继承struct device_driver                 |
| 总线       | i2c_bus_type<br />没有结构体，struct bus_type类型的全局变量。 | usb_bus<br />结构体struct usb_bus。                          |
| 传输结构体 | i2c_msg                                                      | urb                                                          |
| host侧     | i2c_adapter<br />继承struct device                           | usb_hcd<br />include\linux\usb\hcd.h<br />usb_host_endpoint<br />usb_host_interface<br />usb_interface：包含了多个usb_host_interface<br />usb_host_config |
| host编程   | module_platform_driver(i2c_slave_driver);<br />是platform_driver编程。<br />做master的是这个：<br />module_platform_driver(meson_i2c_driver); |                                                              |
| device编程 | module_i2c_driver(ad82128_i2c_driver);<br />实现这个driver   | module_usb_driver(lcd_driver);<br />实现这个driver。         |
|            |                                                              |                                                              |

# usb_class_driver、usb_device_driver、usb_driver



# 内核usb文档分析

## Linux 上的 USB 简介

通用串行总线 (USB) 用于将主机（例如 PC 或工作站）连接到许多外围设备。 

> USB采用树形结构，
>
> 主机为根（系统的主设备），
>
> 集线器为内部节点，
>
> 外设为叶（和从设备）。

现代 PC 支持多个此类 USB 设备树，

通常是一些 USB 3.0 (5 GBit/s) 或 USB 3.1 (10 GBit/s) 以及一些传统的 USB 2.0 (480 MBit/s) 总线，以防万一。

主/从不对称的设计有多种原因，其中之一是易于使用。

物理上不可能弄错上游和下游，或者使用 C 型插头（或者它们内置于外设中）并不重要。

此外，主机软件不需要处理分布式自动配置，因为预先指定的主节点管理所有这些。

内核开发人员在 2.2 内核系列的早期就为 Linux 添加了 USB 支持，并从那时起一直在进一步开发它。

除了对每一代 USB 的支持之外，还获得了对各种主机控制器的支持，添加了新的外设驱动程序，并引入了延迟测量和改进的电源管理的高级功能。

Linux 可以在 USB 设备内部以及控制设备的主机上运行。

但是，在这些外设内部运行的 USB 设备驱动程序与在主机内部运行的 USB 设备驱动程序执行的操作不同，因此它们被赋予了不同的名称：小工具驱动程序。

本文档不涵盖小工具驱动程序。（就是gadget driver）

## USB Host-Side API Model

USB 设备的主机端驱动程序与“usbcore”API 进行通信。

有两个。

一种用于通用驱动程序（通过驱动程序框架公开），

另一种用于作为核心一部分的驱动程序。

此类核心驱动程序包括集线器驱动程序（管理 USB 设备树）和几种不同类型的主机控制器驱动程序（控制各个总线）。

USB驱动程序看到的设备模型相对复杂。

- USB 支持四种数据传输（控制、批量、中断和同步）。其中两个（控制和批量）使用可用带宽，而另外两个（中断和同步）则计划提供有保证的带宽。
- 设备描述模型包括每个设备的一个或多个“配置”，一次只有其中之一是活动的。设备应该能够以低于其最高速度的速度运行，并且可以提供 BOS 描述符，显示它们保持完全运行的最低速度。
- 从 USB 3.0 开始，配置具有一个或多个“功能”，这些“功能”提供通用功能并出于电源管理的目的而组合在一起。
- 配置或功能具有一个或多个“接口”，每个接口都可以具有“备用设置”。接口可以通过 USB“类”规范进行标准化，也可以特定于供应商或设备。
- ==USB 设备驱动程序实际上绑定到接口，而不是设备。==将它们视为“接口驱动程序”，尽管您可能不会看到很多设备的区别很重要。==大多数 USB 设备都很简单，只有一种功能、一种配置、一种接口和一种备用设置。==
- 接口具有一个或多个“端点”，每个端点都支持一种类型和方向的数据传输，例如“批量输出”或“中断输入”。整个配置在每个方向上最多可以有 16 个端点，根据需要在所有接口之间分配。
- USB 上的数据传输是打包的；每个端点都有最大数据包大小。驱动程序必须经常了解约定，例如使用“短”（包括零长度）数据包标记批量传输的结束。
- Linux USB API 支持控制和批量消息的同步调用。它还使用称为“URB”（USB 请求块）的请求结构支持各种数据传输的异步调用。

因此，暴露给设备驱动程序的 USB Core API 涵盖了相当多的领域。

您可能需要查阅 USB 3.0 规范（可从 www.usb.org 在线免费获取）以及类别或设备规范。

唯一真正接触硬件（读/写寄存器、处理 IRQ 等）的主机端驱动程序是 HCD。

理论上，所有 HCD 通过相同的 API 提供相同的功能。

在实践中，这变得更加正确，但仍然存在差异，

特别是在不太常见的控制器上的故障处理方面。

不同的控制器不一定会报告相同方面的故障，并且从故障中恢复（包括软件引起的故障，例如取消链接 URB）尚不完全一致。

设备驱动程序作者应该注意对每个不同的主机控制器驱动程序进行断开连接测试（当设备处于活动状态时），以确保驱动程序没有自己的错误，并确保它们不依赖于某些HCD 特定行为。



## USB-Standard Types

在 include/uapi/linux/usb/ch9.h 中，

您将找到 USB 规范第 9 章中定义的 USB 数据类型。

这些数据类型在整个 USB 和 API 中使用，

包括主机端 API、小工具 API、USB 字符设备和 debugfs 接口。

该文件本身包含在 include/linux/usb/ch9.h 中，

其中还包含一些用于操作这些数据类型的实用程序例程的声明；

实现位于 drivers/usb/common/common.c 中。

| 函数                                 | 说明                               |
| ------------------------------------ | ---------------------------------- |
| **usb_ep_type_string**               | 返回endpointer的类型的名字字符串。 |
| **usb_speed_string**                 | 返回速度字符串。                   |
| **usb_get_maximum_speed**            |                                    |
| **usb_get_maximum_ssp_rate**         | SuperSpeed Plus                    |
| **usb_state_string**                 |                                    |
| **usb_get_role_switch_default_mode** |                                    |
|                                      |                                    |

## Host-Side Data Types and Macros

| 数据结构              | 说明                                                         |
| --------------------- | ------------------------------------------------------------ |
| **usb_host_endpoint** |                                                              |
| **usb_interface**     | USB 设备驱动程序连接到物理设备上的接口。<br />每个接口都封装了一个高级功能，例如将音频流馈送到扬声器或报告音量控制的变化。<br />许多 USB 设备只有一个接口。<br />用于与接口端点通信的协议可以在 USB“类”规范中定义，也可以由产品供应商定义。 <br />（默认）控制端点是每个接口的一部分，但从未在接口的描述符中列出。 |
| **usb_host_config**   | USB 设备可能有多种配置，但任何时候只能有一种配置处于活动状态。<br />每个封装了不同的操作环境；例如，双速设备将具有用于全速和高速操作的单独配置。<br />可用配置的数量作为 bNumConfigurations 存储在设备描述符中。<br />一个配置可以包含多个接口。<br />每个都对应 USB 设备的不同功能，并且只要配置处于活动状态，所有功能都可用。 USB 标准规定接口应该从 0 到 desc.bNumInterfaces-1 进行编号，但很多设备都犯了这个错误。此外，不保证接口数组按数字顺序排序。使用 usb_ifnum_to_if() 根据接口编号查找接口条目。 |
| **usb_device**        | USB 设备的内核表示                                           |
| **usbdrv_wrap**       | wrapper for driver-model structure                           |
| **usb_driver**        | USB 接口驱动程序必须提供名称、probe() 和disconnect() 方法以及id_table。其他驱动程序字段是可选的。<br />id_table 用于热插拔。它保存一组描述符，并且专用数据可以与每个条目相关联。该表由用户模式和内核模式热插拔支持使用。<br />probe()和disconnect()方法在它们可以休眠的上下文中调用，但它们应该避免滥用特权。<br />连接到设备的大多数工作应在设备打开时完成，并在最后一次关闭时撤消。断开连接代码需要解决与 open() 和 close() 方法相关的并发问题，以及强制所有挂起的 I/O 请求完成（通过根据需要取消链接它们，并阻塞直到取消链接完成）。 |
| **usb_device_driver** | identifies USB device driver to usbcore                      |
| **usb_class_driver**  | identifies a USB driver that wants to use the USB major number<br />该结构用于 usb_register_dev() 和 usb_deregister_dev() 函数，以合并用于它们的许多参数。 |
| **urb**               | 该结构标识 USB 传输请求。 <br />URB 必须通过调用 usb_alloc_urb() 进行分配，并通过调用 usb_free_urb() 进行释放。<br />可以使用各种 usb_fill_*_urb() 函数来完成初始化。 <br />URB 使用 usb_submit_urb() 提交，挂起的请求可以使用 usb_unlink_urb() 或 usb_kill_urb() 取消。<br /><br />buffer的行为：<br />通常驱动程序提供用 kmalloc() 分配的 I/O 缓冲区或从通用页池中获取的 I/O 缓冲区。<br />这是由transfer_buffer 提供的（控制请求也使用setup_packet），主机控制器驱动程序为每个传输的缓冲区执行dma 映射（和取消映射）。<br />或者，驱动程序可以传递 URB_NO_TRANSFER_DMA_MAP 传输标志，该标志告诉主机控制器驱动程序，transfer_buffer 不需要此类映射，因为设备驱动程序是 DMA 感知的。<br />例如，设备驱动程序可能使用 usb_alloc_coherent() 或调用 usb_buffer_map() 分配 DMA 缓冲区。<br />当提供此传输标志时，主机控制器驱动程序将尝试使用在transfer_dma字段中找到的dma地址，而不是自己确定dma地址。 |
|                       |                                                              |



## USB Core APIs

USB API 中有两种基本的 I/O 模型。

==最基本的一个是异步的：==

驱动程序以 URB 的形式提交请求，URB 的完成回调处理下一步。

所有 USB 传输类型都支持该模型，

尽管控制 URB（始终具有设置和状态阶段，但可能没有数据阶段）和等时 URB（允许大数据包并包括每个数据包的故障报告）有特殊情况。

在此之上构建的是同步 API 支持，其中驱动程序调用分配一个或多个 URB 的例程、提交它们并等待它们完成。

有用于单缓冲区控制和批量传输（在某些驱动程序断开连接场景中使用起来很尴尬）以及基于分散列表的流 I/O（批量或中断）的同步包装器。



USB 驱动程序需要提供可用于 DMA 的缓冲区，尽管它们本身不一定需要提供 DMA 映射。

分配 DMA 缓冲区时可以使用一些 API，

这可以防止在某些系统上使用反弹缓冲区。

在某些情况下，驱动程序可能能够依靠 64 位 DMA 来消除另一种反弹缓冲区。

## The USB character device nodes

本章介绍 Linux 字符设备节点。

您可能更愿意避免为 USB 驱动程序编写新的内核代码。

用户模式设备驱动程序通常打包为应用程序或库，并且可以通过包装它的某些编程库来使用字符设备。

此类库包括：

用于 C/C++ 的 libusb，以及用于 Java 的 jUSB。

有关它的一些旧信息可以在 USB 指南的“USB 设备文件系统”部分中看到。



“devtmpfs”中有哪些文件？

usbfs 通常安装在 /dev/bus/usb/，其功能包括：

/dev/bus/usb/BBB/DDD ... 魔术文件公开每个设备的配置描述符，并支持一系列用于发出设备请求的 ioctl，包括设备的 I/O。 （纯粹供程序访问。）

根据枚举时间，每条总线都会被赋予一个编号 (BBB)；

在每条总线中，每个设备都被赋予一个相似的编号（DDD）。

这些 BBB/DDD 路径不是“稳定”的标识符；

即使您始终将设备插入同一集线器端口，也期望它们会发生变化。

甚至不要考虑将它们保存在应用程序配置文件中。

对于想要使用它们的用户模式应用程序来说，可以使用稳定的标识符。 

HID 和网络设备公开这些稳定的 ID，因此您可以确保您告诉正确的 UPS 关闭其第二个服务器的电源。请注意，它（尚未）公开这些 ID。

### /dev/bus/usb/BBB/DDD

通过以下基本方式之一使用这些文件：

- 可以读取它们，首先生成设备描述符（18 字节），然后生成当前配置的描述符。有关这些二进制数据格式的详细信息，请参阅 USB 2.0 规范。您需要将大多数多字节值从小端格式转换为本机主机字节顺序，尽管设备描述符中的一些字段（BCD 编码字段以及供应商和产品 ID）将被字节交换你。请注意，配置描述符包括接口描述符、altsettings、端点，可能还包括其他类描述符。
- 使用 ioctl() 请求执行 USB 操作，以发出端点 I/O 请求（同步或异步）或管理设备。这些请求需要 CAP_SYS_RAWIO 功能以及文件系统访问权限。一次只能对这些设备文件之一发出一个 ioctl 请求。这意味着，如果您从一个线程同步读取端点，则在读取完成之前，您将无法从另一线程写入不同的端点。这适用于半双工协议，但否则您将使用异步 I/O 请求。

每个连接的 USB 设备都有一个文件。 

BBB 表示总线编号。 

DDD 指示该总线上的设备地址。

这两个号码都是按顺序分配的，并且可以重复使用，

因此您不能依赖它们来稳定地访问设备。

例如，设备在仍处于连接状态时重新枚举是相对常见的情况（可能有人推挤了电源、集线器或 USB 电缆），因此设备在首次连接时可能为 002/027，有时可能为 002/048之后。

这些文件可以作为二进制数据读取。

二进制数据首先包含设备描述符，然后包含设备每个配置的描述符。

设备描述符中的多字节字段由内核转换为主机字节序。

配置描述符采用总线字节序格式！

配置描述符相隔 wTotalLength 字节。

如果设备返回的配置描述符数据少于 wTotalLength 指示的数据，则文件中将出现缺失字节的漏洞。此信息还通过 /sys/kernel/debug/usb/devices 文件以文本形式显示，稍后将进行描述。



这些文件还可用于为 USB 设备编写用户级驱动程序。

您将打开 /dev/bus/usb/BBB/DDD 文件读/写，读取其描述符以确保它是您期望的设备，然后使用 ioctl 调用绑定到一个接口（或可能多个）。

您可以向设备发出更多 ioctl，以便使用控制、批量或其他类型的 USB 传输与其进行通信。 

IOCTL 列在 linux/usbdevice_fs.h 文件中，在撰写本文时，源代码 (linux/drivers/usb/core/devio.c) 是如何通过这些文件访问设备的主要参考。

请注意，由于默认情况下这些 BBB/DDD 文件只能由 root 写入，因此只有 root 可以写入此类用户模式驱动程序。您可以使用 chmod 有选择地向其他用户授予读/写权限。此外，usbfs 挂载选项（例如 devmode=0666）可能会有所帮助。

### Life Cycle of User Mode Drivers

这样的驱动程序首先需要找到它知道如何处理的设备的设备文件。

也许是因为 /sbin/hotplug 事件处理代理选择了该驱动程序来处理新设备，所以被告知了这一点。

或者它可能是一个扫描所有 /dev/bus/usb 设备文件并忽略大多数设备的应用程序。无论哪种情况，它都应该从设备文件中 read() 所有描述符，并根据它知道如何处理的内容检查它们。它可能会拒绝除特定供应商和产品 ID 之外的所有内容，或者需要更复杂的策略。



https://docs.kernel.org/driver-api/usb/usb.html



# 怎样使用libusb来编写usb设备驱动？

使用 libusb 来编写 USB 设备驱动并不是直接编写内核级的驱动程序，而是通过用户空间的库函数与 USB 设备进行交互和控制。这种方法适用于一些需要在用户空间进行USB设备通信的情况，而不涉及对内核进行修改或驱动程序开发。

以下是使用 libusb 编写 USB 设备控制程序的一般步骤：

### 步骤：

1. **安装 libusb 库**：
   - 安装 libusb 库到你的开发环境中。可以通过包管理器获取或者从源码编译安装。

2. **连接和检测设备**：
   - 使用 libusb 扫描系统上的 USB 总线，找到要控制的 USB 设备。可以使用 libusb 提供的函数进行设备的枚举和检测。

3. **打开设备**：
   - 使用 libusb 函数打开你想要控制的 USB 设备，获取设备的句柄（handle）用于后续的通信和操作。

4. **数据传输和控制**：
   - 使用 libusb 提供的函数进行数据的传输，如发送命令、接收数据等操作。这包括控制传输（control transfer）、批量传输（bulk transfer）、中断传输（interrupt transfer）等。

5. **关闭设备**：
   - 在完成操作后，使用 libusb 函数关闭设备的句柄。

6. **清理和释放资源**：
   - 在程序结束时释放 libusb 所分配的资源，确保资源的正确释放和清理。

### 注意事项：
- 需要以足够的权限运行程序，通常需要 root 权限或者通过配置 udev 规则进行设备访问权限的设置。
- 了解 USB 设备的通信协议和数据格式是非常重要的，以便正确地使用 libusb 函数进行数据的发送和接收。

总的来说，使用 libusb 来编写 USB 设备控制程序能够在用户空间进行 USB 设备的通信和控制，但需要开发者对 USB 设备的通信协议和 libusb 库的使用有一定的了解和掌握。

## 有哪些驱动是使用libusb来实现的

许多USB设备的驱动程序都使用了libusb库来进行实现，特别是那些并非由操作系统原生支持的设备或是需要在用户空间进行控制和通信的设备。

一些常见的使用libusb实现的USB设备驱动包括：

1. **USB设备测试程序**：用于测试USB设备功能和性能的工具，比如USB传输分析工具等。

2. **USB设备模拟器**：模拟特定类型的USB设备，用于测试和开发。

3. **自定义USB设备的用户空间驱动程序**：对于一些特殊的、非标准的或自定义的USB设备，开发者可能需要编写自定义的用户空间驱动程序来进行通信和控制。

4. **USB设备访问工具**：用于与USB设备进行交互的工具或库，例如USB摄像头控制程序、USB存储设备的文件传输工具等。

这些驱动程序或工具通常需要直接与USB设备进行通信，并且可能使用libusb提供的API来发送控制命令、读取设备描述符、进行数据传输等操作。这些应用通常不需要在内核层面进行编程，而是在用户空间利用libusb库进行USB设备的控制和管理。

## libusb设备模拟器实现

使用 libusb 来实现 USB 设备模拟器通常涉及以下步骤和方法：

### 步骤：

1. **确定模拟器的功能**：
   - 确定你想要模拟的USB设备的类型和功能，包括设备描述符、端点、协议等信息。

2. **使用 libusb 准备模拟器**：
   - 利用 libusb 提供的函数创建虚拟的 USB 设备句柄。
   - 设置设备描述符、端点配置等设备信息，以模拟特定类型的USB设备。

3. **实现设备功能**：
   - 根据模拟设备的类型和功能，编写模拟设备的行为和响应，例如对请求的应答、数据的发送等。

4. **与主机进行通信**：
   - 模拟器需要与主机进行通信，可以通过 libusb 提供的接口模拟设备和主机之间的数据交换。
   - 实现数据的收发、命令的响应等模拟USB设备与主机之间的通信。

5. **模拟器的运行**：
   - 在模拟器中运行模拟的USB设备，监听来自主机的请求，并模拟相应的设备行为和数据交换。

### 注意事项：
- 了解和遵循USB规范以及对应设备的通信协议是非常重要的。
- 确保模拟器的行为与实际设备一致，以便与主机正确地进行通信和交互。
- 了解 libusb 提供的函数和接口，以便正确地使用其进行设备模拟和与主机的通信。

实现 USB 设备模拟器需要对 USB 协议和 libusb 库有一定的了解，并且需要根据具体的设备类型和功能进行相应的模拟。这样的模拟器通常用于测试、开发和调试，以便在没有实际硬件设备的情况下模拟特定类型的USB设备。

# BOS是什么

在 USB 规范中，BOS（Binary Object Store）是一种用于描述 USB 设备所支持的其他容器和功能的数据结构。

BOS 通常包含了设备提供的各种容器和功能描述符的集合，用于提供额外的信息，例如各种容器的标识、设备支持的USB版本等。

这些描述符可以包括 SuperSpeed USB、USB Power Delivery、USB Type-C 等描述符，以及其他额外的描述符来说明设备的能力和特性。

BOS 结构提供了一种扩展机制，使得设备能够提供一些不属于其他标准描述符（如设备描述符、配置描述符等）的附加信息。这有助于操作系统和驱动程序了解设备的更多特性和能力，以便进行适当的配置和管理。

在 Linux 中，USB核心层（USB Core）会解析和处理设备的 BOS 数据结构，并提供相应的接口供驱动程序访问设备的附加信息和能力。 BOS 结构对于了解设备的高级功能和兼容性是非常有用的，尤其是对于一些具备高级特性或新型USB功能的设备。



# RK3399的usb驱动

这篇文章分析很好。

https://www.cnblogs.com/zyly/p/17701211.html

这个作者的linux usb系列文章

https://www.cnblogs.com/zyly/category/2340692.html

https://www.cnblogs.com/zyly/p/17705814.html

# 参考资料

1、Linux USB 驱动开发（一）—— USB设备基础概念

https://blog.csdn.net/zqixiao_09/article/details/50984074

2、

https://www.ibm.com/developerworks/cn/linux/l-usb/index1.html

3、几种USB控制器类型：OHCI,UHCI,EHCI,xHCI

https://wenku.baidu.com/view/5d7a7eb0102de2bd960588ae.html

4、Linux USB 驱动开发实例（一） —— USB摄像头驱动实现源码分析

知秋一叶的博客可以看看。

https://blog.csdn.net/zqixiao_09/article/details/50984412

5、 linux内核驱动--usbled.c学习分析

https://blog.csdn.net/wang__rongwei/article/details/70991748

6、QEMU调试Linux系统的USB协议栈

这个思路很好。但是不方便操作。

https://blog.csdn.net/zoomdy/article/details/50954190

7、

https://blog.csdn.net/u011037593/article/details/123467147