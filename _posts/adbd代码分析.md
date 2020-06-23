---
title: adbd代码分析
date: 2020-04-08 13:09:51
tags:
	- Linux

---

1

rk3308的Linux开发包支持adb的方式进行调试。

板端运行了adbd。

启动脚本是/etc/init.d/S50usbdevice。这个脚本放在buildroot/package/rockchip/usbdevice/S50usbdevice。

usbdevice目录下的文件有：

```
├── 61-usbdevice.rules 这个会被安装到/lib/udev/rules.d目录下。
├── Config.in
├── NOTICE
├── S50usbdevice 这个安装到/etc/init.d目录。
├── usbdevice  这个是一个脚本，被安装到/usr/bin目录。
└── usbdevice.mk
```

靠这个来使能的。可能使能不同的功能。现在使能的是adb功能。也可以使能mtp功能。

```
/etc/init.d # cat .usb_config     
usb_adb_en                        
```

61-usbdevice.rules内容：

```
SUBSYSTEM=="udc",ACTION=="change",DRIVER=="configfs-gadget",RUN+="/usr/bin/usbdevice %E{DEVPATH}"
```



涉及的系统目录有：

```
/sys/kernel/config/usb_gadget
/sys/class/android_usb
```



在系统里的选配是：BR2_PACKAGE_ANDROID_TOOLS_ADBD [=y] 

这个包是在

```
 Target packages
 	System tools  ---> 
 		[*] android-tools
 		-*-   adbd
 		[ ]   fastboot 
		[ ]   adb      
```

看看fastboot的package怎么写的。

并不存在一个package的名字叫fastboot。

是在android-tools这个目录下。

到这个目录下看看代码。

```
├── bootimg.c
├── engine.c
├── fastboot.c
├── fastboot.h
├── protocol.c
├── usb.h
├── usb_linux.c
├── usb_osx.c
├── usbtest.c
├── usb_windows.c
├── util_linux.c
├── util_osx.c
└── util_windows.c
```



Ubuntu下安装：

```
sudo apt-get install android-tools-adb  android-tools-adbd android-tools-fastboot
```



use the USB Gadget ConfigFS to configure the USB peripheral port.

操作是靠fd，ioctl来做的 。

io是基于epoll来做的。



adbd也是使用了libusb来跟usb进行通信的。不是，是有多种实现，但是编译的是usb_linux.c。

```
SRCS+= transport_usb.c
SRCS+= usb_linux.c
SRCS+= usb_vendors.c
```

实际上是用usb_linux_client.c。

```
void usb_init()
{
    if (access(USB_FFS_ADB_EP0, F_OK) == 0)
        usb_ffs_init();//这个分支。
    else
        usb_adb_init();
}
```

靠打开/dev/usb-ffs/adb目录下的这3个ep节点来操作。

```
# ls /dev/usb-ffs/adb/
ep0  ep1  ep2
```

ep0是控制信息。

ep2是输入数据。

ep1是输出数据。

```
#define USB_FFS_ADB_EP0   USB_FFS_ADB_EP(ep0)
#define USB_FFS_ADB_OUT   USB_FFS_ADB_EP(ep1)
#define USB_FFS_ADB_IN    USB_FFS_ADB_EP(ep2)
```

ffs的functionfs的缩写。







参考资料

1、

https://developer.toradex.com/knowledge-base/usb-device-mode-(linux)