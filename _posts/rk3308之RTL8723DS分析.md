---
title: rockchip之RTL8723DS分析
date: 2020-03-24 18:01:11
tags:
	- rockchip

---

1

看rockchip对wifi驱动处理有些不一样。看看具体做了些什么。

有这么几个目录：

```
1、external/rkwifibt
	这个目录放了博通和瑞昱的东西。
	bin目录是二进制工具的，不用管。
	brcm_tools 放的是博通的工具。不管。
	firmware 放的也是博通的固件，不管。
	Realtek
		这个目录是重点。
		bluetooth_uart_driver
			蓝牙串口驱动。
		demo
			放了avrcp和hfp的例子。
		docs
			文档。
		rtk_hciattach
			为什么要自己另外写hciattach，标准的为什么不能？
		RTL8723DS
			放的都是二进制文件。
	src
		只有一个c文件，叫rk_wifi_init.c。
	脚本文件。
		S66load_wifi_modules
			rk_wifi_init BT_TTY_DEV //这个就是rk_wifi_init.c得到的程序。
			就启动这个进程。本质就是insmod。
		bt_realtek_start
			insmod /usr/lib/modules/hci_uart.ko
			rtk_hciattach -n -s 115200 /dev/ttyS4 rtk_h5 &
			hciconfig hci0 up
			
```



rk_wifi_init.c

```
module_list
	这个就是罗列了各种模块的描述。名字，对应的so文件路径。
	
通过/sys/bus/sdio/devices下的东西，拿到wifi的类型。

sprintf(temp, "insmod %s %s", wifi_ko_path, wifi_ko_arg);
这样insmod来调用wifi驱动
通过查询/proc/net/dev，看wifi是否就绪。
就是做了这一个事情。
```

hci_uart.ko 

这个文件哪里编译出来的？是external/rkwifibt/realtck/bluetooth_uart_driver目录里编译出来的。

rtk_hciattach

这个是从bluez/tools/hciattch.c的基础上改的。



# avrcp

代码在rkwifibt\realtek\demo\avrcp目录下。就一个c文件和一个头文件。

对外提供的接口很简单，直接，就是播放、暂停这些控制函数。

要让手机连接音箱进行播放操作，需要执行下面的操作：

```
# 启动bluez的daemon程序。这个是一切的基础。
/usr/libexec/bluetooth/bluetoothd --compat -n  &
# 添加A2SNK，作为sink端。
sdptool add A2SNK
# 这个是扫描。
hciconfig hci0 piscan
# 给自己改名，这个不是必须的，只是明白改名是这样操作。
hciconfig hci0 name 'XXX'
# 启动bluealsa进程。
bluealsa --profile=a2dp-sink & 
```

板端进行这些操作后，手机就可以连上板端的蓝牙，然后进行播放操作了。





参考资料

1、

