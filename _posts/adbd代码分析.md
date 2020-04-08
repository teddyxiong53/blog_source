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

靠这个来使能的。

```
/etc/init.d # cat .usb_config     
usb_adb_en                        
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



参考资料

1、

