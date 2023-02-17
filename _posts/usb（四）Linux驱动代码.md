---
title: usb（四）Linux驱动代码
date: 2018-04-05 11:35:27
tags:
	- usb
typora-root-url: ../
---



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

# 配置描述符

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

**USB****可以热插拔的硬件原理**

　　 在USB集线器(hub)的每个下游端口的D+和D-上，分别接了一个15K欧姆的下拉电阻到地。这样，在集线器的端口悬空时，就被这两个下拉电阻拉到了低电平。

而在USB设备端，在D+或者D-上接了1.5K欧姆上拉电阻。对于全速和高速设备，上拉电阻是接在D+上；而低速设备则是上拉电阻接在D-上。这样，当设备插入到集线器时，由1.5K的上拉电阻和15K的下拉电阻分压，结果就将差分数据线中的一条拉高了。集线器检测到这个状态后，它就报告给USB主控制器（或者通过它上一层的集线器报告给USB主控制器），这样就检测到设备的插入了。USB高速设备先是被识别为全速设备，然后通过HOST和DEVICE两者之间的确认，再切换到高速模式的。**在高速模式下，是电流传输模式，这时将D+上的上拉电阻断开。**



# dwc2是什么

 dwc2就是usb2.0的一个控制器，dw是DesignWare是一个IP核设计公司。



参考资料

1、

https://blog.csdn.net/huohongpeng/article/details/116267891

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